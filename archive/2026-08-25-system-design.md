# 🏗️ 系统设计 / System Design — Day 119 (Synthesis)
## 分布式一致性全景：强一致性 vs 最终一致性的取舍哲学
## Distributed Consistency Landscape: When to Choose Strong vs. Eventual Consistency

---

### 核心问题 / The Core Question

你之前学过 CAP 定理、Raft 共识、分布式锁、多区域活跃等系统设计。但真实世界的问题是：**你在什么情况下选强一致性，什么时候接受最终一致性？**

You've studied CAP theorem, Raft consensus, distributed locks, multi-region active-active. The real-world question is: **when do you pay the cost of strong consistency, and when do you accept eventual consistency?**

---

### 一致性光谱 / The Consistency Spectrum

```
Linearizability       Sequential          Causal          Eventual
(最强/Strongest)  →  Consistency  →  Consistency  →  Consistency (最弱)
       ↑                                                      ↑
  高延迟/Low throughput                         低延迟/High throughput
 (Zookeeper, etcd)                           (DynamoDB, Cassandra, DNS)
```

---

### 三大类系统对比 / Three System Categories

#### 1. 强一致性 (Strong / Linearizable Consistency)
**用途 / When to use:** 金融交易、分布式锁、配置管理

**代表系统 / Examples:**
- **Raft** (etcd, TiKV): 写入 Leader → 多数节点复制 → commit
- **Google Spanner**: TrueTime API 提供全球 external consistency
- **Zookeeper ZAB**: 类 Paxos，ZooKeeper Atomic Broadcast

**代价 / Cost:** P50 latency 提升 2-10x；跨数据中心时，round-trip 导致写延迟不可避免

#### 2. 有界陈旧 (Bounded Staleness / Read-Your-Writes)
**用途 / When to use:** 社交 feed、商品库存近似值、用户 profile

- Cassandra QUORUM reads: R + W > N 保证 read-your-writes
- Redis Sentinel: 主从异步复制 + 可配置的 replica lag 上限

#### 3. 最终一致性 (Eventual Consistency)
**用途 / When to use:** DNS、CDN 缓存、推荐系统、购物车

- DynamoDB 默认模式: last-writer-wins (LWW)
- CRDTs (Conflict-free Replicated Data Types): 天然可合并，无需协调

---

### 真实系统选型对照 / Real Systems Compared

| 系统 / System       | 一致性模型                        | 典型场景                  |
|---------------------|----------------------------------|---------------------------|
| Google Spanner      | External Consistency (TrueTime)  | 全球银行交易               |
| Amazon DynamoDB     | Eventual (default) / Strong (opt)| 购物车、用户会话           |
| Apache Kafka        | Log ordering within partition    | 事件流，exactly-once       |
| PostgreSQL + Citus  | Read-your-writes                 | 多租户 SaaS               |
| Redis Cluster       | Eventual (async replication)     | 缓存、限流计数器           |
| Zookeeper / etcd    | Linearizable                     | 选主、分布式锁、配置中心   |

---

### 别踩这个坑 / Common Mistakes

❌ **全用强一致性** — 分布式系统下 latency 不可接受，吞吐量受限
❌ **全用最终一致性** — 支付余额和库存扣减不能用 LWW（超卖、双花）
❌ **忽视 read repair** — Cassandra 没有 read repair 时 QUORUM 读可能返回旧值
❌ **混淆 CP vs CA** — CAP 定理描述的是网络分区时的取舍，不是日常操作

✅ **按数据类型决策:**
- User profile → eventual (陈旧 1 分钟没问题)
- Bank balance → strong (0 容忍不一致)
- Inventory display → eventual (显示近似库存)
- Inventory deduction → pessimistic lock (防止超卖)

---

### 面试答题框架 / Interview Decision Framework

面试官问一致性时，用这 5 步回答：

1. **数据是什么?** — 什么实体，读写频率如何？
2. **出错代价?** — 不一致会导致什么业务问题？
3. **容忍多久的陈旧?** — 100ms? 1s? 5 分钟？
4. **跨区域还是单区域?** — 跨区域强一致需要 Paxos/Raft，代价巨大
5. **冲突如何解决?** — LWW? CRDT? Saga + compensating transaction?

---

### 深度连接：你学过的系统 / Connecting the Dots

- **Day 12 CAP Theorem** → 理论基础：为什么不能同时有 C + A + P
- **Day 47 Raft/Paxos** → 实现强一致性的机制：Leader Election + Log Replication
- **Day 63 Distributed Lock** → 应用强一致性：etcd 的 lease-based lock
- **Day 54 Multi-Region Active-Active** → 最终一致性的挑战：conflict resolution at scale
- **Day 21 Key-Value Store** → 如何暴露一致性级别给用户（DynamoDB-style API）

---

### 📚 References
- https://jepsen.io/consistency — Kyle Kingsbury 的权威一致性模型分析
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html — Kleppmann 论 CAP 误解
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html — Werner Vogels (Amazon CTO) 论最终一致性

### 🧒 ELI5
想象一个家庭共享购物清单。爸妈在不同超市，清单可能暂时不同步（最终一致性）——这对购物没问题，顶多买了两瓶牛奶。但家庭账户余额必须实时同步，不然会出现"双花"（强一致性）。选哪种取决于出错的代价有多大。

Like a shared family shopping list: mom and dad at different stores might briefly see different versions (eventual) — worst case: two cartons of milk. But the family bank account must always be perfectly in sync (strong) or someone overdrafts. The choice depends entirely on the cost of being wrong.
