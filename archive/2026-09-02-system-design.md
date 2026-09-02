# 🏗️ 系统设计 / System Design — Day 124 (Synthesis)
**数据一致性大比拼：从最终一致到强一致，如何在生产中选型**
*Consistency Models in Production: A Cross-System Synthesis*

---

## 🧠 想象你在这个场景... / Real Scenario

你同时负责三个系统：
- **购物车服务**（用 DynamoDB）
- **账户余额服务**（用 PostgreSQL）
- **用户偏好服务**（用 Cassandra）

产品经理问：为什么购物车有时会"失忆"？为什么扣钱必须同步等待但推荐不用？你怎么解释背后的一致性设计？

Three systems, three consistency strategies. But why?

---

## 📐 一致性模型全谱 / The Consistency Spectrum

```
Strong ←————————————————————————————→ Eventual

Linearizability  Serializability  Causal  Read-your-writes  Eventual
    (etcd)         (PostgreSQL)   (Dynamo)  (MongoDB sess)  (Cassandra)

      Slowest ←——————————— Fastest
      Safest  ←——————————— Most Available
```

### 强一致 (Strong Consistency)
- **代表系统**: etcd, Google Spanner, CockroachDB, PostgreSQL with SERIALIZABLE
- **实现原理**: Raft/Paxos consensus — majority quorum before commit
- **代价**: 额外一次 network round-trip; 写放大 3x (quorum)
- **什么时候用**: 分布式锁、账户余额、库存扣减、选举
- **踩坑**: Spanner 用 TrueTime + GPS atomic clocks 保证 external consistency — 不是"强一致就便宜"

### 因果一致 (Causal Consistency)
- **代表系统**: MongoDB (causal sessions), DynamoDB (conditional writes)
- **实现原理**: Vector clocks or hybrid logical clocks track "happened-before"
- **关键**: "我看到的永远不会回退" — reads your own writes + monotonic reads
- **什么时候用**: 评论系统、协作文档、Feed

### 最终一致 (Eventual Consistency)
- **代表系统**: Cassandra, DynamoDB (default), Redis Cluster, S3
- **实现原理**: Gossip protocol + read repair + anti-entropy
- **代价**: Stale reads 可能持续 ms~s
- **什么时候用**: 用户偏好、DNS、CDN 缓存、推荐

---

## ⚖️ 核心 Trade-off 框架 / Decision Framework

```
问自己 3 个问题 / Ask yourself 3 questions:

1. 数据损失代价？
   - 钱/库存/锁 → 强一致（宁慢勿错）
   - 点赞/偏好/缓存 → 最终一致（宁快勿卡）

2. 写频率？
   - 高写吞吐 → 避免 Paxos (too slow), prefer CRDT/eventual
   - 低写高读 → Strong OK

3. 跨地域？
   - Multi-region active-active → CAP 定理迫使你选 AP (eventual)
   - Single-region → CP (strong) 可行
```

---

## 🔥 生产级对比表 / Production Comparison

| 系统 | 默认一致性 | 可调吗? | 延迟影响 |
|------|-----------|---------|----------|
| PostgreSQL | Serializable (可降级) | ✅ READ COMMITTED etc | +0ms (local) |
| DynamoDB | Eventually Consistent | ✅ `ConsistentRead=True` | +~2ms |
| Cassandra | Eventual (ONE) | ✅ QUORUM/ALL | +5-20ms |
| etcd / ZooKeeper | Linearizable | ❌ always strong | +network RTT |
| Redis Cluster | Eventual | ❌ (use WAIT cmd) | ~1ms |

---

## ❌ 别踩这个坑 / Common Mistakes

**坑1: "用 Cassandra 存钱包余额"**
→ Cassandra 没有真正的事务，高并发下会产生 lost updates。余额必须用 ACID DB。

**坑2: "强一致 = 性能差，所以我都用最终一致"**
→ 现代 NVMe + in-region Raft (etcd, CockroachDB) 延迟已降至 1-5ms。不要过早优化。

**坑3: "Read-your-writes = 强一致"**
→ 不是！你看到自己的写，但不一定看到别人的最新写。理解层级差异很重要。

---

## 🏗️ ASCII 架构 / Cross-System Architecture

```
Client
  │
  ├──[Cart Service]──→ DynamoDB (Eventual, fast writes)
  │                        │ quorum reads for checkout
  │
  ├──[Balance Service]──→ PostgreSQL SERIALIZABLE
  │                          + distributed lock (etcd)
  │
  └──[Preference Service]──→ Cassandra ONE
                                 (stale ok, fast)
```

---

## 📚 深读 / References
- https://jepsen.io/consistency — Kyle Kingsbury 的一致性模型权威可视化
- https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html — 分布式锁的正确姿势
- https://www.allthingsdistributed.com/2007/12/eventually_consistent.html — Werner Vogels (Amazon CTO) 原文

## 🧒 ELI5
强一致就像同一时间所有人看同一块白板，改了大家立刻都看到新内容，但改的时候要等大家都准备好。最终一致就像朋友圈——你发了朋友圈，不同的人看到的时间不一样，但过一会儿大家都看到了。用哪种取决于：你能接受暂时的不一致吗？
