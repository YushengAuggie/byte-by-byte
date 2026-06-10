# Day 62 — 系统设计 / System Design

🏗️ **系统设计 / System Design** · Day 62 · Expert Phase

---

## 设计股票交易所 / Design a Stock Exchange & Order Matching Engine

---

### 真实场景 / Real-World Scenario

想象你在设计纳斯达克的核心撮合引擎。每天处理数十亿笔订单，延迟要在**微秒级别**，任何一个 bug 都可能造成百万美元损失，还要绝对公平（谁先来谁先成交）。

*Imagine you're building the core matching engine for NASDAQ. Billions of orders per day, sub-microsecond latency, catastrophic bug cost, and strict fairness: first-come, first-served.*

---

### 核心需求 / Core Requirements

**功能需求 / Functional:**
- 下单（市价单/限价单/止损单）/ Place orders (market/limit/stop)
- 撮合引擎 / Order matching engine (FIFO per price level)
- 订单簿 / Order book (real-time bid/ask)
- 成交回报 / Trade execution & confirmations
- 行情推送 / Market data feed (level 1 & 2)

**非功能需求 / Non-Functional:**
- 吞吐量：1M+ orders/sec / Throughput: 1M+ orders/sec
- 延迟：< 1ms end-to-end / Latency: sub-millisecond
- 强一致性（不允许丢单）/ Strong consistency, no lost orders
- 审计日志 / Full audit trail

---

### 架构图 / Architecture

```
                         ┌─────────────────────────────────┐
                         │           Client Layer           │
                         │  Trading Apps / Market Makers    │
                         └──────────────┬──────────────────┘
                                        │ FIX protocol / WebSocket
                         ┌──────────────▼──────────────────┐
                         │         Gateway Cluster          │
                         │  - Auth & Rate Limiting          │
                         │  - Order validation              │
                         │  - Sequence numbering            │
                         └──────────────┬──────────────────┘
                                        │
              ┌─────────────────────────▼──────────────────────────┐
              │              Order Router (by symbol)               │
              │   AAPL → Engine-1  |  GOOG → Engine-2  | ...       │
              └─────────┬──────────────────────────┬───────────────┘
                        │                          │
         ┌──────────────▼──────┐      ┌────────────▼────────────┐
         │  Matching Engine 1   │      │  Matching Engine 2      │
         │  (single-threaded)   │      │  (single-threaded)      │
         │  Order Book (AAPL)   │      │  Order Book (GOOG)      │
         │  - Bid: MaxHeap      │      │  - Bid: MaxHeap         │
         │  - Ask: MinHeap      │      │  - Ask: MinHeap         │
         └──────────┬──────────┘      └─────────────────────────┘
                    │ Trades
         ┌──────────▼──────────────────────────────────────────┐
         │              Event Bus (Kafka / Chronicle)           │
         └───┬────────────────────────┬────────────────────────┘
             │                        │
    ┌─────────▼─────────┐    ┌────────▼──────────────┐
    │  Trade Settlement  │    │   Market Data Feed     │
    │  (clearing house)  │    │   (WebSocket / UDP     │
    │  DB: PostgreSQL    │    │    multicast)           │
    └───────────────────┘    └───────────────────────┘
                    ┌──────────────────────────────────┐
                    │     Audit Log (append-only)      │
                    │     WAL / immutable store        │
                    └──────────────────────────────────┘
```

---

### 撮合引擎核心 / Matching Engine Core

**订单簿数据结构 / Order Book Data Structure:**

```python
import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Order:
    order_id: str
    symbol: str
    side: str        # "BUY" or "SELL"
    price: float     # 0 for market orders
    quantity: int
    timestamp: int   # sequence number for FIFO

@dataclass
class PriceLevel:
    price: float
    orders: deque = field(default_factory=deque)  # FIFO queue at each price

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        # Bids: max-heap (negate price for Python's min-heap)
        self.bids: list[tuple] = []  # (-price, timestamp, PriceLevel)
        # Asks: min-heap
        self.asks: list[tuple] = []  # (price, timestamp, PriceLevel)
        self.price_levels: dict[float, PriceLevel] = {}

    def add_limit_order(self, order: Order) -> list[dict]:
        """Add order, attempt immediate match, return trades."""
        trades = []
        remaining = order.quantity

        if order.side == "BUY":
            # Try to match against asks (lowest ask first)
            while remaining > 0 and self.asks:
                best_ask_price = self.asks[0][0]
                if best_ask_price > order.price:
                    break  # No match possible
                # Match!
                level = self.asks[0][2]
                remaining, new_trades = self._fill_from_level(
                    level, order, remaining
                )
                trades.extend(new_trades)
                if not level.orders:
                    heapq.heappop(self.asks)

        # If unfilled quantity remains, add to book
        if remaining > 0:
            order.quantity = remaining
            self._insert_order(order)

        return trades

    def _fill_from_level(self, level, incoming, remaining):
        trades = []
        while level.orders and remaining > 0:
            resting = level.orders[0]
            fill_qty = min(remaining, resting.quantity)
            trades.append({
                "buyer": incoming.order_id if incoming.side == "BUY" else resting.order_id,
                "seller": resting.order_id if incoming.side == "BUY" else incoming.order_id,
                "price": level.price,
                "quantity": fill_qty,
            })
            resting.quantity -= fill_qty
            remaining -= fill_qty
            if resting.quantity == 0:
                level.orders.popleft()
        return remaining, trades
```

**撮合规则 / Matching Rules:**
- **Price-Time Priority (FIFO):** 同价格下，先到先得
- **市价单立即撮合** / Market orders match immediately at best available price
- **限价单可能部分成交** / Limit orders may partially fill

---

### 关键设计决策 / Key Design Decisions

| 决策 / Decision | 选择 / Choice | 原因 / Reason |
|---|---|---|
| 每股票一个引擎 | Shard by symbol | 避免锁竞争；单线程无需同步 |
| 单线程匹配 | Single-threaded per engine | 无锁 = 最低延迟 |
| 传输协议 | FIX protocol / UDP multicast | 行业标准；低延迟行情推送 |
| 持久化 | WAL + event sourcing | 可回放；完整审计 |
| 队列 | LMAX Disruptor / Chronicle | 避免 GC，ring buffer |

**为什么单线程？/ Why single-threaded?**
> 多线程需要锁，锁带来上下文切换，延迟飙升。交易所宁愿用更多机器（按股票分片），也不要锁竞争。NYSE 和 NASDAQ 的核心引擎都是单线程的。

---

### 别踩这个坑 / Common Mistakes

❌ **用关系数据库存订单簿** — 太慢了！订单簿必须在内存里，持久化靠 WAL。

❌ **忽视时钟同步** — 全球分布式系统里，序列号必须是逻辑时钟（单调递增），不能靠 wall clock。

❌ **市价单不设熔断** — 市场剧烈波动时市价单会以极端价格成交，需要熔断机制（circuit breaker）。

❌ **撮合结果异步确认** — 成交回报必须是同步的，否则客户端可能重复下单。

---

### 📚 References

- [LMAX Disruptor — High-performance inter-thread messaging](https://lmax-exchange.github.io/disruptor/)
- [Martin Fowler — Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [FIX Protocol Specification](https://www.fixtrading.org/standards/)
- [Designing a Matching Engine — Murat Demirbas](https://muratbuffalo.blogspot.com/2024/01/design-of-order-matching-engine.html)

---

### 🧒 ELI5

想象一个菜市场，买土豆的人说"我出5块钱一斤"，卖土豆的人说"我要6块钱一斤"——没有成交。等卖家说"5.5块也行"，买家的5.5块挂单就立刻成交了。股票交易所就是这个菜市场，只是每秒钟有几百万笔这样的对话。

*Imagine a marketplace: buyers shout their max price, sellers shout their min price. When they overlap, a trade happens. A stock exchange is just this market running at millions of matches per second, with strict rules about who gets matched first.*
