# System Design — Day 93: 合成深度 / Synthesis Deep Dive
## 一致性模型全景：从 Redis 到 Spanner / Consistency Models: From Redis to Spanner

> **综合模式** — 跨越过去所涵盖的主题，进行 Expert 级别对比与深度分析

---

## 场景 / Scenario

想象你在设计一个全球金融平台，需要在三个地区运行（美国、欧洲、亚洲）。你的团队争论激烈：

- 工程师 A 说：「用 Redis + 异步复制，简单快！」
- 工程师 B 说：「不行，金钱数据必须强一致，用 Spanner！」
- 工程师 C 说：「Cassandra 最终一致足够了吧？」

谁是对的？取决于你的**一致性需求矩阵**。

*Imagine you're designing a global financial platform across 3 regions. Your team disagrees on consistency — who's right? It depends on your consistency requirements matrix.*

---

## 一致性模型对比 / Consistency Model Comparison

```
强一致性 (Strong)          ←→         最终一致性 (Eventual)
     │                                        │
  Spanner                   Cassandra       DynamoDB
  CockroachDB               Redis Cluster   S3
  Postgres (single)         MongoDB         Kafka Topics
     │                                        │
  💰 高延迟，高成本           💚 低延迟，低成本
  ✅ 适合：金融、库存          ✅ 适合：用户档案、分析
```

```
线性一致性 (Linearizable):
  Every operation appears atomic at a single point in time.
  Read always sees latest write.
  Example: Spanner uses TrueTime API.

顺序一致性 (Sequential):
  All ops appear in some global order.
  Less strict than linearizable.

因果一致性 (Causal):
  Causally related ops maintain order.
  Example: "Reply after post" ordering.

最终一致性 (Eventual):
  Given enough time, all replicas converge.
  Example: DNS propagation, S3.
```

---

## 架构对比 / Architecture Comparison

```
[ Redis Sentinel ]              [ Google Spanner ]
  Primary ──► Replica 1          Node 1 (US-East)
           └─► Replica 2    ◄──► Node 2 (EU-West)
                                 Node 3 (Asia-Pacific)
  Async replication               Paxos consensus
  Failover ~30s                   TrueTime (GPS + atomic clocks)
  Eventual consistency            External consistency (linearizable)
  Latency: <1ms local             Latency: ~10ms cross-region
  Cost: 💚 cheap                  Cost: 💰 expensive
```

---

## 关键权衡 / Key Tradeoffs

| 维度 | Redis (Async) | Postgres (Sync Replica) | Spanner | Cassandra |
|------|--------------|------------------------|---------|-----------|
| 一致性 | 最终 | 强（单区）| 线性（全球）| 最终/可调 |
| 可用性 | 高 | 中（主挂即降级）| 很高 | 极高 |
| 延迟 | 亚毫秒 | 1-5ms | 10-100ms | 1-10ms |
| 扩展性 | 垂直+集群 | 读扩展 | 水平全球 | 水平无限 |
| 成本 | 低 | 中 | 极高 | 中 |

**决策框架 / Decision Framework:**
```
if money_or_inventory:
    → Spanner / CockroachDB (global)
    → Postgres with synchronous replication (regional)
elif user_profiles_or_feeds:
    → Cassandra / DynamoDB (eventual ok)
elif session_cache:
    → Redis (speed > consistency)
elif audit_log:
    → Kafka → cold storage (append-only wins)
```

---

## 别踩这个坑 / Common Mistakes

❌ **坑 1: 认为"最终一致"就是"不一致"**  
最终一致在窗口期（通常 ms~s）内可能读到旧数据，但最终会收敛。设计时要处理"读己写"场景。

❌ **坑 2: 忽视时钟漂移**  
分布式系统的"先后"是个难题。Spanner 用 GPS + 原子钟解决；你自己实现时要用逻辑时钟（Lamport / Vector Clock）。

❌ **坑 3: 强一致 ≠ 无 bug**  
即便 Spanner 保证线性一致，应用层的事务逻辑（转账的原子性）仍需正确设计。

---

## 📚 References
- https://cloud.google.com/spanner/docs/true-time-external-consistency
- https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html
- https://jepsen.io/consistency — Jepsen consistency model hierarchy
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html

## 🧒 ELI5
把数据库想象成班级公告栏。强一致 = 老师每次改公告必须等全班同学都看到才算完成（慢但准）。最终一致 = 老师先改，等下课了大家陆续看到（快但有时滞后）。Spanner 是那种用原子钟确保全球每个黑板在同一秒更新的黑科技教室。

*Think of a database like a school bulletin board. Strong consistency = the teacher waits until every student acknowledges the update before moving on (slow but precise). Eventual = teacher posts it and students gradually see it (fast but lagging). Spanner is the sci-fi classroom with atomic clocks ensuring every board globally updates at the exact same moment.*
