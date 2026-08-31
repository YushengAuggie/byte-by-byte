# 🏗️ 系统设计 / System Design — Day 122 (Synthesis)
**一致性模型大对比：从缓存到数据库到共识算法**
**Consistency Models Compared: From Cache to DB to Consensus**

---

## 想象你是 Staff Engineer，需要在这三个方案中选择

你们的系统需要在多个节点间保证数据正确性。你面前有三类工具：
- **Redis Cluster**（你在 Day 6 设计的缓存）
- **Cassandra**（Day 9 的分布式数据库方案之一）
- **Raft 共识**（Day 47 深入讲过）

它们的一致性保证**根本不同**。选错了，生产事故就等着你。

---

## 一致性模型速查表

```
强一致性 (Strong Consistency)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
读总能看到最新写 → 用户看到的数据永远正确
代价：高延迟，可用性↓

最终一致性 (Eventual Consistency)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
写入最终会同步，但读可能暂时落后
代价：业务逻辑复杂，需要幂等处理

可调一致性 (Tunable Consistency)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
按请求指定强度：R + W > N → 强一致
代价：需要理解 quorum 数学
```

---

## 三个系统的对比

| 系统 | 默认一致性 | 强一致怎么实现 | 适合场景 |
|------|-----------|--------------|---------|
| Redis (单主) | 强一致 | 默认就是 | 计数、Session、排行榜 |
| Redis Cluster | 最终一致 | WAIT 命令（代价高） | 分布式 KV，允许短暂脏读 |
| Cassandra | 最终一致 | QUORUM 读写 | 写多读少，地理分布 |
| PostgreSQL 主从 | 最终（异步复制） | synchronous_commit=on | 金融数据，不能丢 |
| etcd / Raft | 强一致 | 内置，无法关闭 | 配置、分布式锁、服务发现 |

---

## 为什么这样设计？— CAP 定理的实际应用

Day 12 讲过 CAP：**P（分区容忍）在分布式系统中是必选项**。
所以真正的选择是 **CP vs AP**：

```
CP（一致性 > 可用性）：Raft/etcd, Zookeeper, PostgreSQL 同步复制
→ 用于：支付、库存、选主、配置中心

AP（可用性 > 一致性）：Cassandra(ONE), Redis Cluster, DynamoDB(最终)
→ 用于：社交 Feed、日志收集、购物车、DNS
```

---

## 别踩这个坑 ⚠️

**坑 1：以为 Redis 都是强一致**
Redis Sentinel / Cluster 有异步复制 → 主故障时最多丢几毫秒的写入。
银行扣款不能用 Redis 做最终来源，只能做缓存层。

**坑 2：Cassandra QUORUM 不等于强一致**
如果你的集群是 N=3，R=2，W=2，看起来满足 R+W>N。
但如果有节点在 hinted handoff 状态，读可能绕过 quorum。
**必须配合 read repair 和 nodetool repair。**

**坑 3：用 Raft 存大数据**
Raft 的 log 需要所有节点同步 → 吞吐量被 leader 限制。
etcd 官方建议数据 < 8GB。别把它当数据库用。

---

## 实际架构：把三者组合起来

```
[Client]
    │
    ├─► Redis (Cache, CP per key) ──► hit: return
    │         │ miss
    ▼
[PostgreSQL Primary] ──sync replica──► [PG Replica] (read)
    │
    └─► [etcd] (分布式锁，防止并发超卖)
```

这是 Day 37 Ticketmaster 和 Day 38 Payment System 里用到的真实模式：
- **etcd** 做选主和分布式锁（强一致，CP）
- **PostgreSQL** 同步复制做持久化（CP）
- **Redis** 做缓存加速（可接受最终一致）

---

## 📚 References
- [Consistency Models — Jepsen](https://jepsen.io/consistency)
- [Cassandra Consistency Levels](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html)
- [etcd v3 Linearizability](https://etcd.io/docs/v3.5/learning/api_guarantees/)

## 🧒 ELI5
把数据库想成黑板。强一致 = 所有人看同一块黑板；最终一致 = 每人有自己的小本子，但每隔一段时间对一次答案。选哪个取决于你是在做考试题（必须精确）还是记购物清单（差一点没关系）。
