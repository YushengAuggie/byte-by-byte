# 🏗️ 系统设计 / System Design — Day 159 (Synthesis)
**主题 / Topic:** Event Sourcing + CQRS：把分布式系统所有经验串起来

---

## 想象你在设计一个金融交易系统...

传统做法：用户下单 → UPDATE orders SET status='paid' WHERE id=X。

问题是：**你永远不知道"发生过什么"，只知道"现在是什么"**。

这就是为什么 Stripe、Shopify、Uber 都用 Event Sourcing。

---

## 核心思想 / Core Concepts

**Event Sourcing（事件溯源）**：不存储当前状态，存储每一个**事件**（发生了什么）。

```
❌ 传统：orders table { id, status="paid", amount=100 }
✅ ES：events table { order_created, payment_initiated, payment_confirmed }
         → 当前状态 = replay(所有事件)
```

**CQRS（命令查询职责分离）**：写操作（Command）和读操作（Query）走不同的路径。

---

## ASCII 架构图

```
Client
  │
  ▼
┌─────────────────────────────────────────────────────┐
│  API Gateway                                        │
└──────┬───────────────────────────┬──────────────────┘
       │ Commands                  │ Queries
       ▼                           ▼
┌────────────┐              ┌─────────────────┐
│  Command   │              │  Query Service  │
│  Handler   │              │  (Read Model)   │
└─────┬──────┘              └────────┬────────┘
      │ Publish Events               │ Read from
      ▼                              ▼
┌─────────────┐  Project    ┌────────────────┐
│  Event      │ ──────────▶ │  Read DB       │
│  Store      │             │  (Postgres,    │
│  (Kafka /   │             │   Elasticsearch│
│   EventDB)  │             │   Redis)       │
└─────┬───────┘             └────────────────┘
      │ Replay
      ▼
┌────────────┐
│ Snapshot   │  ← 每隔N个事件存一次快照，避免replay太慢
│ Store      │
└────────────┘
```

---

## 为什么这样设计？/ Key Tradeoffs

| 优势 Pros | 劣势 Cons |
|-----------|-----------|
| 完整审计日志（金融合规必备） | 读取需要 replay，要维护 Read Model |
| 时间旅行：可以回放到任意时间点 | 最终一致性，读写有延迟 |
| 解耦：事件驱动，微服务天然解耦 | Event schema 变更很难（不可变事件） |
| 读写独立扩展 | 学习曲线陡，调试复杂 |

**这正好串联了我们学过的所有主题：**
- Kafka（消息队列 Day 13）→ 事件总线
- Redis（分布式缓存 Day 39）→ Read Model 加速
- Elasticsearch（搜索引擎 Day 29）→ 复杂查询 Read Model
- 最终一致性（CAP 定理 Day 12）→ 命令/查询延迟
- Snapshot → 类似数据库检查点

---

## 别踩这个坑 / Common Mistakes

**坑 1：事件太粗粒度**
```
❌ UserUpdated { all_fields... }  # 什么都改了？
✅ UserEmailChanged { old, new }
   UserAddressUpdated { address }
```

**坑 2：在事件里存业务逻辑**
```
❌ event: { discount_applied: true, final_price: 90 }  # 价格逻辑变了就麻烦
✅ event: { coupon_code: "SAVE10" }  # 在 replay 时重新计算
```

**坑 3：忘记 Idempotency**
事件可能被消费多次（Kafka at-least-once），处理器必须幂等。

---

## 什么时候用 / When to Use

✅ 金融/支付系统（Stripe）
✅ 电商订单（Shopify）
✅ 协作编辑（Google Docs — Operational Transform 是变种）
✅ 游戏状态（每帧 = 一个事件）

❌ 简单 CRUD 应用（杀鸡用牛刀）
❌ 读多写少且不需要历史（用普通缓存更简单）

---

## 📚 References
- [Martin Fowler — Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Microsoft CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Greg Young — CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)

## 🧒 ELI5
想象你的银行不存"余额=1000元"，而是存"存了500、花了200、存了700..."的流水账。要知道余额，就把所有账单加起来。这样你永远能查到**任何一天的余额**，也能知道**每笔钱怎么来的**。Event Sourcing 就是这个思路。
