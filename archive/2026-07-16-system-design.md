# 系统设计综合 — 分布式系统权衡的终极对比 / System Design Synthesis — Ultimate Distributed Tradeoffs

> Day 92 · Expert · Synthesis Mode

---

## 🏗️ 系统设计 / System Design — 综合深化：一致性 vs 可用性 vs 分区容错

### 真实场景 / Real Scenario

想象你是一个大厂的 Principal Engineer，架构委员会问你：
"我们有 5 个核心系统——缓存、消息队列、数据库、分布式锁、推荐系统。每个在 CAP 上该怎么选？为什么？"

Imagine you're a Principal Engineer at a big tech company. The architecture committee asks: "We have 5 core systems — cache, message queue, database, distributed lock, recommendation system. How should each be positioned on the CAP theorem and why?"

---

### 综合架构图 / Synthesis Architecture

```
                    CAP Triangle
                    
                    Consistency
                        /\
                       /  \
                      /    \
           Zookeeper /      \ HBase
           (CP)      /        \ (CP)
                    /          \
                   /   NO CA    \
                  /  in dist.   \
    CA(local) ----               ---- CA(local)
              \                    /
   PostgreSQL  \  PARTITION       / DynamoDB
   (CA local)   \  TOLERANCE     / (AP)
                 \              /
                  \            /
          Cassandra \          / Redis
             (AP)    \        / (AP/CP configurable)
                      --------
                   Availability

System Choices:
┌─────────────────┬─────┬─────────────────────────────────┐
│ System          │ CAP │ Why                             │
├─────────────────┼─────┼─────────────────────────────────┤
│ Redis Cache     │ AP  │ Stale cache OK; availability > │
│                 │     │ consistency                     │
├─────────────────┼─────┼─────────────────────────────────┤
│ Kafka MQ        │ AP  │ Messages can be slightly stale  │
│                 │     │ but queue must stay available   │
├─────────────────┼─────┼─────────────────────────────────┤
│ PostgreSQL      │ CP  │ Financial data: consistency non-│
│                 │     │ negotiable, sacrifice avail.    │
├─────────────────┼─────┼─────────────────────────────────┤
│ Zookeeper/etcd  │ CP  │ Distributed locks MUST be       │
│ (Dist. Lock)    │     │ consistent or you get 2 leaders │
├─────────────────┼─────┼─────────────────────────────────┤
│ Recommendation  │ AP  │ Slightly stale recs = fine;     │
│ System          │     │ downtime = lost revenue         │
└─────────────────┴─────┴─────────────────────────────────┘
```

---

### 深层权衡 / Deep Tradeoffs

#### 1. 强一致性的代价 (CP systems)
- **2PC (Two-Phase Commit)**: 协调者故障 → 系统卡住。适合金融事务，不适合高并发写。
- **Raft/Paxos**: 需要多数派 (quorum)。5节点集群，2节点故障 → 仍可用。但延迟增加（需要 round-trip 到多数节点）。
- **实际代价**: LinkedIn 研究显示，CP 系统在网络抖动时 P99 延迟高 3-5x。

#### 2. 最终一致性的工程技巧 (AP systems)
- **版本向量 (Vector Clocks)**: DynamoDB 用于冲突检测
- **CRDT**: Conflict-free Replicated Data Types，用于协作编辑（如 Figma）
- **Read Repair**: 读时修复过时副本（Cassandra）
- **Hinted Handoff**: 临时节点代为存储，节点恢复后补发（Cassandra）

#### 3. 真实面试陷阱 / Interview Traps

```
面试官: "设计一个银行转账系统"

❌ 初级答案: "用 Cassandra，AP，高可用！"
❌ 原因: 转账需要 ACID，Cassandra 不支持跨分区事务

✅ 正确思路:
1. PostgreSQL for accounts (CP, ACID transactions)
2. Outbox pattern + Kafka for async events
3. Idempotency keys for safe retries
4. Saga pattern for distributed transactions
   - Compensating transactions for rollback
```

---

### 六大系统综合选型框架 / 6-System Selection Framework

```
问自己这 3 个问题:

Q1: 数据过时 1 分钟，用户会受到什么影响？
  - 没影响 → AP (cache, feed, recommendations)
  - 钱少了/多了 → CP (payments, inventory)
  - 两个节点同时成为 leader → CP (distributed lock)

Q2: 宁可报错还是返回旧数据？
  - 返回旧数据 (degraded mode) → AP
  - 宁可报错也不给错数据 → CP

Q3: 写冲突发生时谁来解决？
  - 业务逻辑可以合并 (last-write-wins, CRDT) → AP
  - 需要严格串行化 → CP
```

---

### 高频考点：PACELC 比 CAP 更准确

CAP 只讨论分区时的选择，但实际上**无分区时的延迟(L)也是关键**：

```
PACELC: 
  If Partition: choose Availability or Consistency
  Else: choose Latency or Consistency

系统     | Partition | Else
---------|-----------|----------
DynamoDB | A         | L (eventual consistency)
HBase    | C         | C (strong consistency)
Cassandra| A         | L (tunable)
MongoDB  | C (default)| C
```

---

### 别踩这个坑 / Common Mistakes

1. **"我用 Cassandra 做分布式锁"** → ❌ Cassandra 是 AP，锁要求 CP
2. **"主从复制 = 强一致性"** → ❌ 默认异步复制有复制延迟，需要同步复制 (`synchronous_commit`)
3. **"微服务 = 每个服务独立数据库 = 跨库事务用 2PC"** → ❌ 用 Saga 模式代替 2PC

---

### 📚 References
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html (Werner Vogels' seminal post)
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html
- https://www.cs.cornell.edu/projects/ladis2012/papers/li-ladis2012.pdf (PACELC paper)
- https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/

### 🧒 ELI5
CAP theorem is like choosing between 3 restaurant rules during a storm (network partition): Consistency = everyone gets the same menu. Availability = everyone gets SOME food. Partition Tolerance = restaurant stays open even if kitchen is cut off. You can only pick 2. Banks pick CP (same menu, might close). Netflix picks AP (maybe old content, but always open).
