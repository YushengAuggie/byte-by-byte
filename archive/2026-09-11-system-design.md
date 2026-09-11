# 🏗️ 系统设计 / System Design — Day 132 (Synthesis)
**一致性模型全景对比：从 Linearizability 到 Eventual Consistency**
**Consistency Models: The Full Spectrum in Production**

---

## 为什么这个话题重要 / Why This Matters

过去几个月你学了 CAP 定理、Raft/Paxos、分布式锁、多区域 Active-Active、分布式缓存……但这些系统到底提供什么级别的一致性保障？面试官最爱问："你的设计能提供什么一致性？"很多人答不出来。

You've covered CAP theorem, Raft/Paxos, distributed locks, multi-region active-active, distributed caches — but what consistency level does each actually provide? This synthesis ties them all together.

---

## 一致性光谱 / The Consistency Spectrum

```
Strong ←————————————————————→ Weak
  │                               │
Linearizability  Sequential  Causal  Eventual
  │                               │
 etcd/Zookeeper   Spanner    Cassandra  DNS/CDN
 (single-leader)  (TrueTime)  (CRDT)   (async repl)
```

### 1. Linearizability（线性一致性）— "最强"
- 每次读都能看到最新写，好像只有一个节点
- 实现：Raft/Paxos，单 leader + 同步复制
- 代价：高延迟（需要 quorum 确认），不能分区
- **你学过的系统**：etcd (Day 63)、ZooKeeper 分布式锁

### 2. Sequential Consistency（顺序一致性）
- 所有操作有全序，但不要求实时。客户端看到的顺序一致
- Spanner 用 TrueTime 实现近似线性一致性
- 比 Linearizability 稍宽松，性能更好

### 3. Causal Consistency（因果一致性）
- "你写了一条消息，你朋友一定能读到" — 因果相关的操作有序
- 实现：Vector clocks、CRDT
- **你学过的系统**：Cassandra 的 LWW（Last Write Wins）是因果一致性的近似

### 4. Eventual Consistency（最终一致性）
- 最终会收敛，但过程中可能读到旧数据
- 代价最低，可用性最高
- **你学过的系统**：CDN (Day 64)、DNS、S3 replication

---

## 你的设计对应哪个级别？

| 系统 | 一致性级别 | 原因 |
|------|-----------|------|
| 分布式锁 (etcd) | Linearizable | Raft quorum writes |
| 分布式缓存 (Redis Cluster) | Eventual | async replication |
| 多区域 Active-Active | Eventual / Causal | cross-region lag |
| Chat 系统消息顺序 | Causal | per-user ordering |
| 支付系统 | Linearizable | 不能丢钱 |
| 推荐系统计数器 | Eventual | 丢几个点击无所谓 |

---

## 常见错误 / Common Mistakes

❌ "我用 Redis，所以是强一致" — Redis Cluster 是最终一致的！  
❌ 混淆 "CP" 和 "Linearizable" — CAP 的 C 是 Sequential，不是 Linearizability  
✅ 面试时先问：这个系统对一致性的要求是什么？钱 > 帖子点赞数

---

## 决策框架 / Decision Framework

```
需要"读你的写"(read-your-writes)?
  → YES: 至少 Causal Consistency (sticky sessions 或 Raft)
  
允许短暂读到旧数据?
  → YES: Eventual (DNS, CDN, 社交 feed)
  
涉及金钱/库存/锁?
  → YES: Linearizable (etcd/Zookeeper, single-region RDBMS + sync repl)
```

---

## 📚 References
- https://jepsen.io/consistency — Kyle Kingsbury 的一致性模型权威指南
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html (Werner Vogels / Amazon CTO)

## 🧒 ELI5
想象你和同学共享一份笔记。Linearizable = 有一本原版，每次改都先锁住给大家看；Eventual = 每人先记自己的，最后汇总——可能有一段时间不同步，但最终一样。
Linearizability = one shared notebook, everyone waits their turn. Eventual consistency = everyone has their own copy that syncs up... eventually.
