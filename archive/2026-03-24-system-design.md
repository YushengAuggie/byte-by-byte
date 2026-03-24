# 🏗️ 系统设计 Day 9 / System Design Day 9

**主题 / Topic:** 数据库复制与分片 / Database Replication & Sharding

---

## 🌏 真实场景 / Real-World Scenario

想象你在设计一个像微信读书或 Goodreads 的阅读应用——用户突破 5000 万，每天产生几亿条阅读记录、笔记和评论。单一数据库服务器已经撑不住了：写操作堵住读操作，单点故障导致整个 App 不可用，数据量超出单机磁盘上限。

你需要两把利器：**复制（Replication）**解决可用性和读性能，**分片（Sharding）**解决写性能和存储规模。

Imagine you're designing a reading app like Goodreads at 50M users, with hundreds of millions of reading records daily. A single database server buckles under load. You need **Replication** for availability & read scale, and **Sharding** for write scale & storage capacity.

---

## 🏛️ 架构图 / Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    应用服务层 / App Layer                │
│         [API Server 1] [API Server 2] [API Server 3]    │
└─────────┬──────────────────────────┬────────────────────┘
          │ Writes                    │ Reads
          ▼                           ▼
┌─────────────────┐        ┌────────────────────────┐
│   Primary DB    │──────► │  Read Replica 1        │
│ (Leader/Master) │──────► │  Read Replica 2        │
│                 │──────► │  Read Replica 3        │
└────────┬────────┘        └────────────────────────┘
         │ Replication Log (WAL / Binlog)
         │
         ▼  [After Replication → Add Sharding]
┌────────────────────────────────────────────────────┐
│                  Shard Router / Proxy              │
│           (e.g. Vitess, ProxySQL, PgBouncer)       │
└────┬──────────────────┬───────────────────┬────────┘
     │                  │                   │
     ▼                  ▼                   ▼
┌─────────┐       ┌─────────┐        ┌─────────┐
│ Shard 0 │       │ Shard 1 │        │ Shard 2 │
│user 0-33M│      │user33-66M│       │user66M+ │
│+Replicas│       │+Replicas│        │+Replicas│
└─────────┘       └─────────┘        └─────────┘
```

---

## ⚖️ 关键权衡 / Key Tradeoffs

### 复制 / Replication

| 方案 | 优点 | 缺点 |
|------|------|------|
| **同步复制** | 强一致性，不丢数据 | 写延迟高（等所有副本确认） |
| **异步复制** | 写延迟低，吞吐高 | 副本可能有延迟（replication lag） |
| **半同步** | 折中：至少 1 个副本确认 | 稍高写延迟，部分一致性 |

**为什么这样设计？**
- 读多写少的业务（如阅读记录）：异步复制 + 多读副本，读吞吐可水平扩展
- 金融、支付场景：同步复制或 Raft/Paxos 保证强一致

### 分片 / Sharding

| 策略 | 原理 | 适合场景 |
|------|------|------|
| **Range Sharding** | 按 user_id 范围切分 | 范围查询友好，但热点风险高 |
| **Hash Sharding** | `shard = hash(user_id) % N` | 均匀分布，但范围查询跨 shard |
| **Directory Sharding** | 查表确定归属 shard | 灵活，但查表本身是瓶颈 |

---

## 🚫 常见坑 / Common Mistakes

**坑 1：过早分片**
> 分片大幅增加系统复杂度。复制 + 读副本能抗住大多数流量，先用它，真正撑不住再分片。

**坑 2：选错 Shard Key**
> 按时间分片会导致最新 shard 永远是热点（写都打到最新月份）。按用户 ID hash 分片更均匀。

**坑 3：跨 Shard 事务**
> 分布式事务极复杂。设计 schema 时尽量让同一用户的数据在同一 shard，避免跨 shard join。

**坑 4：忽略 Replication Lag**
> 用户刚发评论，立刻刷新却看不到——因为读副本还没同步。对强一致性操作，读 Primary 或使用 read-your-writes 路由。

---

## 📚 参考资料 / References

1. [AWS Database Replication — RDS Read Replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
2. [Vitess — MySQL Sharding at YouTube Scale](https://vitess.io/docs/concepts/sharding/)
3. [Designing Data-Intensive Applications — Chapter 5 & 6 (Kleppmann)](https://dataintensive.net/)

---

## 🧒 ELI5 / 用小孩能理解的话说

**复制**就像把书抄写多份，放在不同图书馆。每个图书馆都能借给你看（读副本），但只有总馆能修改（Primary）。

**分片**就像把全班同学的作业按学号分给 3 个老师批改——不再一个老师批所有作业，每个老师只负责一段。

**Replication** = Make copies of the book so more people can read at once.
**Sharding** = Split the library into sections so no single librarian is overwhelmed.
