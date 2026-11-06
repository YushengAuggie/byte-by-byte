# 🏗️ 系统设计 / System Design — Day 149 (Synthesis)
**一致性层级的工程权衡 — 从 Redis 到 Raft 的完整路线图**
**Consistency Spectrum in Distributed Systems — From Cache to Consensus**

---

## 场景 / Scenario

想象你在设计一个金融平台，需要 3 个子系统：用户会话缓存、交易事件流、账户余额存储。三个系统对"一致性"的要求完全不同。这不是选一个数据库的问题 — 而是理解不同一致性层级，然后匹配需求。

You're designing a fintech platform with 3 subsystems: user session cache, transaction event stream, and account balance storage. Each has radically different consistency requirements.

---

## 一致性层级全谱 / The Consistency Spectrum

```
弱一致性 ──────────────────────────────────────── 强一致性
Weak                                              Strong

[Redis Cache]   [Kafka]   [Postgres Replica]   [etcd/Raft]
  最终一致性    至少一次/    读自己的写           线性一致性
 Eventual      Exactly-once  Read-your-writes   Linearizable
   ~1ms          ~10ms           ~5ms              ~50ms+
```

---

## 系统对比 / System Comparison

| 系统 | 一致性模型 | CAP 选择 | 适用场景 |
|------|----------|---------|---------|
| Redis | 最终一致 | AP | 会话、缓存、限流 |
| Kafka | 顺序+持久化 | AP (acks=all) | 事件流、审计日志 |
| Postgres (single) | 可序列化 | CP | OLTP 交易 |
| Postgres (replica) | 读自己的写 | — | 读扩展 |
| etcd/Raft | 线性一致 | CP | 分布式锁、选主、配置 |

---

## 关键洞察：一致性不是免费的 / Consistency Is Not Free

**Redis 缓存雪崩场景**：
- 缓存失效 → 所有请求打到 DB → DB 过载
- 解法：互斥锁 + 缓存预热 (Day 6 + Day 47)

**Kafka exactly-once 的代价**：
- Exactly-once = idempotent producer + transactional consumer
- 吞吐量下降约 20-30%，延迟上升
- 金融场景必须接受这个代价 (Day 13)

**Raft 的性能天花板**：
- 每次写操作需要多数节点确认 (quorum)
- 3 节点集群最多容忍 1 个节点故障
- etcd 不适合高写入 TPS（用于配置/锁，不用于主数据库）(Day 47)

---

## 实战选型框架 / Decision Framework

```
需要强一致性吗？
├── YES: 写操作涉及钱/权限/状态 → Postgres + WAL / etcd
└── NO: 能接受短暂不一致？
    ├── YES: 读多写少 → Redis (TTL) + 异步更新
    └── 事件驱动: 需要有序+持久化 → Kafka (acks=all)

失败处理：
- Redis miss → fallback to DB (cache-aside pattern)
- Kafka consumer lag → backpressure + dead letter queue
- Raft leader 故障 → 自动选主，~150-300ms 不可用
```

---

## 别踩这个坑 / Common Mistakes

❌ **缓存+数据库双写没有原子性** — 永远先写 DB，再删缓存（而非更新缓存）

❌ **Kafka 当数据库用** — Kafka 是日志，不是查询引擎；join 和过滤在消费侧

❌ **etcd 存大数据** — etcd 默认 value 限制 1.5MB，整个数据库建议 < 8GB

✅ **分层一致性**：账户余额用 Postgres（强一致），余额展示用 Redis（最终一致），操作日志用 Kafka（有序持久）

---

## 📚 References

- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html
- https://raft.github.io/
- https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying

## 🧒 ELI5

三种系统就像三种记笔记的方式：便利贴（Redis）贴在桌上，快但可能掉；录音机（Kafka）全程录下来，回放有序但不能改；公证人（Raft）每次写都让所有人签字，最慢但最可信。
