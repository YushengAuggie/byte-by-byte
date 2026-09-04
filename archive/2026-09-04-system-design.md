# 系统设计合成 / System Design Synthesis — Day 126

🏗️ **系统设计合成 / System Design Synthesis**
**第 126 天 · Expert 阶段 · 合成主题**

---

## 一致性模型全谱——从强一致到最终一致的工程决策指南
## Consistency Models: A Field Guide from Linearizability to Eventual Consistency

想象你负责一个全球电商平台，横跨三个数据中心。用户在纽约下单，库存在上海。问题来了：库存数量需要强一致吗？购物车呢？用户评论呢？不同答案，代价天差地别。

*Imagine a global e-commerce platform across three data centers. User orders from New York, warehouse is in Shanghai. Does inventory need strong consistency? What about the cart? User reviews? Wrong choices cost you either money or users.*

---

### 一致性模型谱系 / The Consistency Spectrum

```
强一致 (Linearizability) ──── 最安全，最慢，写入阻塞直到所有副本确认
    │
顺序一致 (Sequential)   ──── 全局顺序保证，但允许滞后
    │
因果一致 (Causal)       ──── 有因果关系的操作有序，无关操作可乱序
    │
读己所写 (Read-your-writes) ── 你写了立刻能读到，别人可能还没看到
    │
最终一致 (Eventual)     ──── 最终收敛，中间可能读到旧值
    │
弱一致 (Weak)           ──── 完全不保证，看心情
```

---

### 60 个系统设计题的一致性选择总结

| 系统 | 选择 | 理由 |
|------|------|------|
| 分布式锁 (etcd/Zookeeper) | 强一致 (Raft) | 防止双重持有，锁不能脏读 |
| 股票撮合引擎 | 线性一致 | 订单状态必须全局有序 |
| 分布式缓存 (Redis Cluster) | 最终一致 | 性能优先，短暂脏读可接受 |
| 聊天系统 (WhatsApp) | 因果一致 | A→B 消息有序，全局顺序不必要 |
| 协同编辑 (Google Docs) | CRDT / OT | 离线编辑合并，无需中央协调 |
| URL 缩短 (TinyURL) | 读己所写 | 创建后立即可读即可 |
| 推荐系统 | 弱一致 | 旧推荐影响极小，staleness 可接受 |
| 支付系统 (Stripe) | 可串行化 | 幂等 + 唯一约束防重复扣款 |

---

### 工程决策三问 / Decision Framework

**1. 两个节点看到不同值，最坏后果是什么？**
- 用户多扣款 / 库存超卖 → 强一致
- 点赞数暂时差 1 → 最终一致

**2. 读多写少 or 写高吞吐？**
- 读多：leader + sync follower 读，主从延迟 < 1ms 可接受
- 写高吞吐：最终一致 + 客户端 read-repair / 向量时钟解冲突

**3. CAP 中你实际放弃了哪个？**
- 放 P：单机 MySQL（但云时代你躲不了网络分区）
- 放 A：Raft/Paxos，分区时拒绝写入（银行选这个）
- 放 C：Dynamo/Cassandra，分区时接受脏读（购物车选这个）

---

### 别踩这些坑 / Common Mistakes

**❌** "用了 Redis 就是最终一致" → **✅** Redis Cluster 主从是异步复制，主节点宕机会丢数据。需要强一致请用 etcd 或 Redis + `WAIT` 命令。

**❌** "分布式事务解决一致性" → **✅** 2PC 解决原子性，不解决分区可用性。Saga 模式（补偿事务）+ 事件驱动才是微服务正解。

**❌** "微服务同步调用链保证一致" → **✅** 同步链 A→B→C 级联故障。Outbox Pattern + Kafka 才能在保证最终一致的同时解耦故障域。

---

### Staff 级洞察 / Staff-Level Insight

> 最优答案不是"用最强的一致性"，而是**针对每个数据域，选择满足业务不变量所需的最弱一致性模型**。

实战分层：
- **库存超卖允许补单** → Redis 最终一致 + MySQL 异步核账
- **金融转账** → CockroachDB Serializable 隔离（强一致）
- **社交 Feed** → Cassandra eventual + 前端容忍乱序展示

*The best system designers don't pick one consistency model for the whole system — they mix models per data domain.*

---

📚 **References:**
- https://jepsen.io/consistency — 一致性模型权威可视化图谱
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html — Kleppmann: CAP 的误解
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html — Werner Vogels (Amazon CTO) on eventual consistency

🧒 **ELI5:** 三个朋友共用一块黑板。强一致 = 每次擦写所有人都必须看到并点头才能继续；最终一致 = 各自先抄，事后对一遍，中间可能有差异。前者慢但准，后者快但会短暂不同。选哪个取决于"暂时不同"有多危险。
