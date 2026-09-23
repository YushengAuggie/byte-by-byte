# 🏗️ 系统设计 / System Design — 专家综合 Day 61

> **综合模式 / Synthesis Mode:** 所有60个专题已覆盖，今天深度对比多个核心概念。

---

## 分布式一致性终极对比：从理论到生产选型

**Distributed Consistency Deep Dive: From Theory to Production Decisions**

---

### 为什么今天讲这个？/ Why This Topic?

你已经学过 CAP 定理（Day 12）、Raft/Paxos（Day 47）、多区域 Active-Active（Day 54）、分布式缓存（Day 39）。但面试官最爱问的不是"什么是一致性"，而是："**你会为这个系统选什么一致性模型，为什么？**"

今天把所有知识点串联起来。

---

### 三种核心一致性模型

**1. Strong Consistency（强一致性）**
- 写入后，任意节点**立刻**读到最新值
- 实现机制：Raft（etcd、TiKV）、2PC、Spanner TrueTime
- 代价：写入延迟高（需等多数节点确认），可用性降低
- 适用场景：金融转账、库存系统、分布式锁

**2. Eventual Consistency（最终一致性）**
- 写入后"最终"会同步，短期内可能读到旧值
- 实现机制：多主异步复制（Day 9）、Gossip 协议、CRDT
- 代价：需处理读到旧值、写-写冲突
- 适用场景：社交 Feed、购物车、DNS、计数器

**3. Causal Consistency（因果一致性）**
- 有因果关系的操作保证顺序，无因果关系的允许乱序
- 实现机制：向量时钟（Vector Clock）、混合逻辑时钟（HLC）
- 代价：复杂度中等，比强一致性快
- 适用场景：协作编辑（Day 59 Google Docs）、消息排序

---

### ASCII 决策框架

```
问自己三个问题：
1. 数据不一致会导致财务/法律损失？    → Strong Consistency
2. 短暂不一致用户根本感知不到？        → Eventual Consistency  
3. 顺序语义重要但全局同步代价太高？    → Causal Consistency

                   High Consistency (CP)
                          ↑
               金融/库存/分布式锁
               (Raft, Spanner, 2PC)
                          |
  AP ←────────────────────┼────────────────────→ CP
  高可用                  |                  强一致
  (Dynamo/Cassandra)      |              (etcd/ZK)
                          |
               协作/消息/会话
               (Causal, CRDT)
                          ↓
                   Low Consistency (AP)
```

---

### 跨系统综合对比

| 系统（之前学过）| 一致性模型 | 实现方式 | 原因 |
|---|---|---|---|
| Redis Sentinel (Day 39) | 最终一致 | 异步复制 | 缓存允许短暂 stale，优先吞吐 |
| etcd / ZooKeeper (Day 63) | 强一致 | Raft | 分布式锁不容错 |
| Cassandra (Day 21 KV) | 可调节 | QUORUM 写/读 | 跨数据中心灵活配置 |
| Google Docs (Day 59) | 因果一致 | OT / CRDT | 协作顺序重要，但不需要全局同步 |
| 支付系统 (Day 38) | 强一致 | 2PC + 幂等 | 钱不能丢也不能重复扣 |
| 推特 Feed (Day 86) | 最终一致 | 异步 fanout | 晚几秒看到 tweet 没人在意 |

---

### 面试常见陷阱 / Common Mistakes

❌ **"我用强一致性，因为最安全"**
✅ 强一致性 = 牺牲可用性 + 高延迟。金融系统值得；社交 Feed 不值得。

❌ **"CAP 定理说只能二选一"**
✅ CAP 只在**网络分区期间**成立。正常情况下 CP 系统仍然可用，只是分区时会拒绝请求。

❌ **"最终一致性太弱，生产不用"**
✅ Amazon DynamoDB、Cassandra、DNS 都是最终一致性，支撑全球最大的系统。

---

### 一句话选型口诀

> **钱/锁/序号用强一致；内容/状态/计数用最终一致；协作/消息流用因果一致。**

---

### 📚 References
- https://jepsen.io/consistency — 一致性模型权威可视化（必看）
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html — Werner Vogels 经典 Eventual Consistency 论文
- https://research.google/pubs/pub39966/ — Google Spanner: Globally-Distributed Databases

### 🧒 ELI5
强一致 = 全班同学同时看同一块黑板；最终一致 = 各人有自己的小黑板，老师会同步，但有时候有点延迟；因果一致 = "你说了A，我才说B"这种顺序保证了，其他无关的消息随便。
