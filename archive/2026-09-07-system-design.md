# 🏗️ 系统设计 / System Design — Day 128 (Synthesis: Expert)

> **合成模式** — 60个精选主题已全部覆盖。今天深度对比：分布式系统一致性权衡全景。

---

## 一致性不是布尔值 — 从 CAP 到产品的真实权衡

**Consistency Isn't Binary — Real Tradeoffs from CAP to Production**

---

### 🎭 想象你是一家大型电商的首席架构师

Black Friday 即将来临。你的系统横跨 3 个大洲、12 个数据中心。老板问："库存数据必须准确吗？"

你需要在 **一致性**、**可用性**、**分区容忍性** 中做选择。但真实世界比 CAP 定理复杂得多。

**Imagine you're the lead architect at a major e-commerce company.**  
Black Friday is approaching. Your system spans 3 continents, 12 datacenters. The CEO asks: "Does inventory data need to be exact?" The answer reveals your entire consistency strategy.

---

### 📊 我们学过的所有系统，一张图看懂一致性光谱

```
强一致性 ←————————————————→ 最终一致性
Strong                         Eventual

  PostgreSQL    etcd/ZK    Redis     DynamoDB   Cassandra
  (ACID)        (Raft)     (AOF)     (tunable)  (tunable)
     |             |          |           |          |
  单机强一致    分布式强   主从复制    可调一致性  可调一致性
  Multi-row     Consensus  Async rep  R+W>N opt  QUORUM opt
  transactions  Lineariz.  ~ms lag   strong opt  ~100ms lag

  ← CP (一致性+分区)      AP (可用性+分区) →
```

---

### 🔍 5类系统的真实一致性策略

**1. 强一致性系统 (CP) — PostgreSQL + etcd**

PostgreSQL 通过 WAL + MVCC 保证单机 ACID。  
etcd/Zookeeper 通过 Raft/Paxos 保证分布式线性一致性 (Linearizability)。

适合：**金融账户、分布式锁、配置中心、Leader 选举**

代价：写延迟高 (跨节点需 2-phase commit 或 Raft round-trip)

**Strong consistency (CP): PostgreSQL + etcd**  
Best for: financial ledgers, distributed locks, config, leader election.  
Cost: Higher write latency — every write needs consensus.

---

**2. 可调一致性 (Tunable) — DynamoDB + Cassandra**

```
Cassandra 写: W=QUORUM (写超过半数节点成功才返回)
Cassandra 读: R=QUORUM (读超过半数节点比较返回最新)
条件: R + W > N → 强一致; R + W <= N → 最终一致
```

DynamoDB 默认最终一致，强一致性读额外收费 2x。

适合：**购物车 (最终一致)、订单状态 (强一致)**

**Tunable consistency — DynamoDB + Cassandra**  
R + W > N guarantees strong consistency. Most apps use eventual (cheaper, faster).

---

**3. 主从异步复制 — Redis Cluster + MySQL replication**

主节点写 → 异步复制到从节点 → 网络延迟期间从节点数据可能落后。

```
Primary:  [W1] → [W2] → [W3]   ← 写入成功
Replica:  [W1] → [W2]          ← 还没收到 W3
读从库:   可能读到旧数据 (stale read)
```

适合：**读多写少 (只读副本)、缓存层**

---

**4. Kafka 的"一致性" — 有序 + 持久，但非线性一致**

Kafka 保证：分区内消息有序、持久化到磁盘、at-least-once 投递。  
不保证：跨分区全局顺序、exactly-once (需额外配置)。

适合：**事件溯源、审计日志、异步解耦**

---

**5. CDN 边缘节点 — 极端最终一致性**

```
Origin → Edge PoP (全球200+节点)
         TTL=3600s 内: 可能看到旧内容
         更新传播: 分钟级
```

适合：**静态资源、不敏感数据**  
不适合：**用户权限、价格 (要 TTL=0 或 bypass cache)**

---

### ⚠️ 面试常见误区 / Common Interview Mistakes

| 误区 | 真相 |
|------|------|
| "用 Redis 就可以保证数据不丢" | Redis 默认 fsync=everysec，最多丢 1s 数据 |
| "Cassandra 是 AP，不能做强一致" | QUORUM 读写可以实现强一致，只是慢 |
| "微服务用分布式事务就行" | 2PC 在高并发下是性能杀手，优先考虑 Saga |
| "读从库没问题，反正差不多" | 主从延迟期间读到旧数据是真实 bug 来源 |

---

### 🎯 架构决策框架 / Decision Framework

```
问题: 这个数据，读到旧值会有多严重？

严重 (钱/权限/库存) → 强一致 → etcd/PostgreSQL/QUORUM
中等 (帖子/计数)    → 最终一致 → Cassandra/DynamoDB eventually
轻微 (推荐/排行)    → 缓存 + 定期更新 → Redis TTL
静态 (图片/CSS)     → CDN，TTL尽量长
```

---

### 📚 深入阅读 / References

- https://jepsen.io/analyses — 真实系统的一致性测试报告
- https://www.allthingsdistributed.com/2007/12/eventually_consistent.html — Werner Vogels (Amazon CTO) 经典文章
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html — CAP 定理的局限性

### 🧒 ELI5

想象一家连锁超市。**强一致性** 就像所有门店共享一个实时库存系统，买了就减，但系统慢。**最终一致性** 就像每个门店有自己的库存本，每晚同步一次 — 快但中途可能卖出重复。你卖的是什么决定用哪种：卖飞机票要强一致，卖书可以最终一致。
