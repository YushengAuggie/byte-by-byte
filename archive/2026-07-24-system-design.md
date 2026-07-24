# Day 99 — System Design Synthesis: 分布式系统一致性模型全景 / Consistency Models in Distributed Systems

## 🏗️ 系统设计综合 / System Design Synthesis

**主题：分布式一致性模型 — 从最终到线性化**
**Topic: Distributed Consistency Models — From Eventual to Linearizability**

---

### 为什么这很重要 / Why This Matters

过去99天里你学了几十个系统：缓存、数据库、消息队列、分布式锁、共识协议。它们全都在解决同一个核心问题：**多个节点如何就数据状态达成一致？**

Over 99 days you've seen dozens of systems: caches, databases, message queues, distributed locks, consensus protocols. They all solve the same core problem: **how do multiple nodes agree on data state?**

---

### 一致性模型谱系 / The Consistency Spectrum

```
强 (Strong) ←————————————————————→ 弱 (Weak)

Linearizability → Sequential → Causal → Eventual
     ↑                ↑           ↑          ↑
  Zookeeper        Raft/Paxos   Dynamo    Cassandra
  etcd             consensus    DynamoDB  Redis (async)
  Single-node DB               Kafka*
```

**线性化 Linearizability**
- Every op appears instantaneous at some point between start and end
- Example: Google Spanner (TrueTime), Zookeeper
- Cost: high latency (cross-region coordination)

**顺序一致性 Sequential Consistency**
- All nodes see same order of ops, but may lag real time
- Example: Raft-based systems (etcd, CockroachDB)
- Cost: requires leader election, leader becomes bottleneck

**因果一致性 Causal Consistency**
- Ops that are causally related appear in order; concurrent ops may differ
- Example: DynamoDB (with vector clocks), MongoDB (sessions)
- Good balance for social media, collaborative editing

**最终一致性 Eventual Consistency**
- Given no new writes, all replicas converge eventually
- Example: Cassandra, S3, DNS
- Cost: application must handle stale reads, conflicts

---

### 你见过这些在哪里 / Where You've Seen These

| System (你学过的) | Consistency Model | Why They Chose It |
|---|---|---|
| Redis (primary) | Linearizable | Single-threaded, sync writes |
| Redis Cluster | Eventual | Async replication, prefer availability |
| Kafka | Sequential (per-partition) | Ordered log, partition = unit of ordering |
| Cassandra | Tunable (ONE → QUORUM → ALL) | Tradeoff at query time |
| Zookeeper / etcd | Linearizable | Coordination requires strong guarantees |
| DynamoDB | Eventual (default) / Strong (option) | Cost: strong reads 2x price |
| Google Spanner | External consistency (beyond linearizable!) | TrueTime atomic clocks |
| PostgreSQL | Serializable (strongest SQL level) | MVCC + snapshot isolation |

---

### 关键权衡 / Key Tradeoffs (Expert Level)

**CAP ≠ 简单的三选二 CAP is not a simple pick-2**

Modern nuance: You don't choose between C and A globally. You choose **per operation**. Cassandra lets you choose consistency level per read/write.

**PACELC 模型更准确 PACELC is more accurate:**
```
If Partition: choose Availability vs Consistency
Else (normal): choose Latency vs Consistency
```
DynamoDB = PA/EL (available + low latency by default)
Spanner = PC/EC (consistent always, higher latency)

**向量时钟 vs 最后写入赢 Vector Clocks vs Last-Write-Wins**
- Vector clocks track causality but add metadata overhead
- LWW is simpler but can silently discard data
- CRDTs (Conflict-free Replicated Data Types) are the modern solution — design data structures that merge deterministically

---

### 面试中如何使用这个知识 / How to Use in Interviews

面试官问"你怎么保证数据一致性？"时，别说"用数据库"。说：

When an interviewer asks "how do you ensure data consistency?", don't say "use a database." Say:

> "First I'd clarify the consistency requirement. For inventory counts (双十一 flash sale), I need strong consistency at checkout — use Redis with single leader or SQL with serializable isolation. For user feed ranking, eventual consistency is fine and I'd use Cassandra with QUORUM reads for a balance."

**✅ Framing:** Consistency is a spectrum. State the tradeoff explicitly, then justify your choice.

---

### 📚 References
- https://jepsen.io/consistency — Kyle Kingsbury's definitive consistency model map
- https://lamport.azurewebsites.net/pubs/time-clocks.pdf — Lamport's original paper on logical clocks
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html — Werner Vogels (Amazon CTO) on eventual consistency
- https://cloud.google.com/spanner/docs/true-time-external-consistency — Google Spanner TrueTime

### 🧒 ELI5
想象你和朋友在不同城市更新同一个共享购物清单。强一致性：每次更新前都打电话确认，慢但准确。最终一致性：各自记笔记，隔天同步，可能有冲突。大多数系统选择中间路线。

Imagine you and friends in different cities update a shared grocery list. Strong consistency: call each other before every edit — slow but accurate. Eventual consistency: each person keeps notes, sync tomorrow — might have conflicts. Most systems pick something in between.
