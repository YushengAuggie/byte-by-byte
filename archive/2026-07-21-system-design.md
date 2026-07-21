# 系统设计综合 / System Design Synthesis — Day 96

**Day 96 | Expert Phase | Synthesis Mode**

---

## 🏗️ 系统设计 / System Design
### 综合：缓存 vs 队列 vs 数据库 — 三角决策框架
**Synthesis: Cache vs Queue vs Database — The Triad Decision Framework**

---

当你设计一个系统，最常犯的错误是 **用错了数据存储**：把需要持久化的东西放进了 Cache，把实时的东西塞进了 Queue，把临时状态存进了 DB。今天我们综合前面所有系统设计话题，建立一个决策框架。

The most common system design mistake: **choosing the wrong storage primitive**. Let's build a mental model across all the systems we've covered.

---

### 🔺 决策三角 / The Decision Triangle

```
                    ┌─────────────────────┐
                    │     你的数据需求      │
                    │   Your Data Need     │
                    └────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  CACHE   │  │  QUEUE   │  │    DB    │
        │  (Redis) │  │(Kafka/SQS│  │(Postgres)│
        └──────────┘  └──────────┘  └──────────┘
        快/临时/读多   异步/解耦/顺序   持久/查询/ACID
        Fast/Temp/R   Async/Decouple  Persist/Query
```

---

### 📐 选哪个？/ Which One?

| 问题 / Question | 选 / Choose |
|---|---|
| 同一数据被读100次以上? | Cache |
| 生产者比消费者快？ | Queue |
| 需要事务/回滚？ | DB |
| 数据可以过期/丢失？ | Cache |
| 下游服务可能宕机？ | Queue |
| 需要跨表 JOIN 查询？ | DB |
| 分布式锁/互斥？ | Cache (SETNX) |
| 事件溯源/回放？ | Queue (Kafka) |
| 用户配置/账单/订单？ | DB |

---

### 🏛️ 真实案例：电商下单流程 / Real Case: E-Commerce Order Flow

```
用户下单
User places order
     │
     ▼
[API Gateway]
     │
     ├──► Redis Cache ──► 检查库存快照 (< 1ms)
     │                    Check inventory snapshot
     │
     ├──► Postgres ──────► 写订单记录 (ACID)
     │                    Write order record
     │
     └──► Kafka ─────────► 触发下游: 支付/邮件/库存扣减
                           Trigger downstream: payment/email/inventory
```

**关键设计决策 / Key Design Decisions:**
1. **先查 Cache** — 库存查询 QPS 可达 100K+，不能每次打 DB
2. **写 DB 用事务** — 订单必须原子写入，支持回滚
3. **Kafka 解耦** — 支付服务宕机不影响订单写入

---

### ⚠️ 常见陷阱 / Common Pitfalls

**❌ Cache Stampede (缓存雪崩)**
```
大量 Key 同时过期 → 所有请求打到 DB → DB 崩溃
```
**✅ Fix:** 随机 TTL + 互斥锁 + 后台预热

**❌ Queue Backpressure (队列积压)**
```
消费者处理速度 < 生产者发送速度 → 队列无限增长
```
**✅ Fix:** 监控 lag、动态扩容消费者、设置 max queue size

**❌ DB Hot Spot (数据库热点)**
```
所有写请求打到同一个 partition/shard
```
**✅ Fix:** 分散 partition key、写操作异步化

---

### 🎯 Expert-Level Insight

**真正的系统设计不是"用哪个"，而是"如何组合"。**

The best systems use all three in concert:
- **Cache** absorbs read traffic — Redis for session, inventory, rate limiting
- **Queue** absorbs write spikes — Kafka for events, SQS for tasks  
- **DB** is the source of truth — Postgres/MySQL for transactional data

**面试中如何展示这个框架 / How to show this in interviews:**
> "首先我会分析读写比例和一致性要求。读多写少 + 可容忍短暂不一致 → Cache 层；写入有峰值 + 下游解耦 → Queue；需要强一致性 + 复杂查询 → 关系型 DB。"

---

### 📚 References
- [Redis Architecture](https://redis.io/docs/get-started/faq/)
- [Kafka Design](https://kafka.apache.org/documentation/#design)
- [PostgreSQL MVCC](https://www.postgresql.org/docs/current/mvcc-intro.html)

### 🧒 ELI5
- **Cache** = 桌面上的笔记本（快，但可能丢）
- **Queue** = 邮箱收件箱（顺序处理，不丢）
- **DB** = 文件柜（慢，但永久保存）
