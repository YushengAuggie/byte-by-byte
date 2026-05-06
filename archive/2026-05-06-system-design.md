# 🏗️ 系统设计 / System Design — Day 30
## Design an E-Commerce Platform (Advanced · Mastery Phase)

---

### 场景 / Scenario

想象你在设计一个像 Amazon 一样的电商平台。每天有数百万用户浏览商品、下订单、支付、等待发货。你的系统需要处理秒杀活动（100万人同时抢同一件商品）、保证库存准确性、同时支持搜索、推荐、履约（fulfillment）全流程。

*Imagine you're designing an e-commerce platform like Amazon. Millions of users daily browse products, place orders, pay, and wait for delivery. Your system must handle flash sales (1M concurrent users on one product), guarantee inventory accuracy, and support search, recommendations, and fulfillment end-to-end.*

---

### 架构图 / Architecture Diagram

```
                        ┌─────────────────────────────┐
  Users ──────▶ CDN ──▶ │      API Gateway / BFF      │
                        └──────────┬──────────────────┘
                                   │
         ┌─────────────────────────┼───────────────────────────┐
         ▼                         ▼                           ▼
  ┌─────────────┐       ┌─────────────────┐        ┌────────────────────┐
  │ Product     │       │  Order Service  │        │  Inventory Service │
  │ Service     │       │                 │        │  (Redis + DB)      │
  │ (Elastic    │       │  ┌───────────┐  │        │                    │
  │  Search +   │       │  │ Payment   │  │        │  Pessimistic Lock  │
  │  PostgreSQL)│       │  │ Service   │  │        │  for Flash Sales   │
  └─────────────┘       │  └───────────┘  │        └────────────────────┘
                        │  ┌───────────┐  │
  ┌─────────────┐       │  │ Fulfillmt │  │        ┌────────────────────┐
  │ Search &    │       │  │ Service   │  │        │  Notification      │
  │ Recommend   │       │  └───────────┘  │        │  Service (Kafka)   │
  │ (Kafka      │       └────────┬────────┘        └────────────────────┘
  │  + ML)      │                │
  └─────────────┘        ┌───────▼────────┐
                         │  Message Queue │
                         │  (Kafka / SQS) │
                         └────────────────┘
```

---

### 关键设计决策 / Key Design Decisions

#### 1. 库存扣减 (Inventory Deduction)
这是电商最难的问题。两种策略：

**悲观锁（秒杀场景）：** `SELECT ... FOR UPDATE` + Redis atomic decrement  
**乐观锁（普通场景）：** `UPDATE SET stock=stock-1 WHERE stock > 0 AND version=N`

*Inventory deduction is the hardest e-commerce problem. Use pessimistic locking (SELECT FOR UPDATE + Redis) for flash sales, optimistic locking (version-based) for normal traffic.*

#### 2. 订单状态机 (Order State Machine)
```
PENDING → PAID → PROCESSING → SHIPPED → DELIVERED
       ↘ CANCELLED ↗
```
使用 Kafka 驱动状态转换，保证最终一致性，避免分布式事务。

*Use Kafka to drive state transitions. Avoid distributed transactions — embrace eventual consistency.*

#### 3. 搜索 vs 查询 (Search vs Query)
- 产品查询 → PostgreSQL (精确，ACID)
- 商品搜索 → Elasticsearch (全文，相关性)
- 推荐 → Feature store + ML model

---

### 为什么这样设计？/ Tradeoffs

| 选择 | 优点 | 缺点 |
|------|------|------|
| Redis 库存 | 原子操作，毫秒级 | 需要异步同步到DB |
| Kafka 异步解耦 | 峰值削平，容错 | 最终一致性，更复杂 |
| Elasticsearch | 全文搜索快 | 数据同步延迟，运维复杂 |
| 微服务拆分 | 独立扩展，隔离故障 | 分布式一致性难，延迟高 |

---

### ⚠️ 别踩这个坑 / Common Mistakes

1. **超卖（oversell）**：不加锁直接 `stock -= 1` → 用 Redis `DECR` + Lua 脚本做原子操作
2. **支付超时**：用户支付中，库存一直占用 → 订单设 TTL（如15分钟），超时自动释放库存
3. **价格竞态**：促销时价格变化，但已在购物车里的旧价格 → 下单时重新验证价格
4. **履约幂等**：重复发货通知 → 每个消息带幂等键，消费者做去重

*Oversell prevention, payment timeout TTL (15min hold), price re-validation at checkout, and idempotent fulfillment are the four most commonly missed details.*

---

### 📚 References
- [System Design: E-Commerce — ByteByteGo Newsletter](https://blog.bytebytego.com/p/design-an-e-commerce-website)
- [Amazon's Approach to Inventory Management](https://aws.amazon.com/solutions/case-studies/amazon-inventory/)
- [Distributed Transactions in Microservices — Martin Fowler](https://martinfowler.com/articles/microservices.html)

### 🧒 ELI5
电商就像一个超级大超市。搜索是导购员（Elasticsearch），库存是收银机（Redis原子操作），支付是结账台，发货是后仓。秒杀就像限量版球鞋发售，要排队领号，不然大家都抢同一双。

*An e-commerce system is like a giant supermarket. Search is the directory board, inventory is the checkout counter, payment is the cashier, and fulfillment is the warehouse. A flash sale is like limited sneaker drops — you need a queue system or everyone fights for the same pair.*
