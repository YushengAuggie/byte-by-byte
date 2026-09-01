# 🏗️ 系统设计合成 / System Design Synthesis — Day 123 (Expert)

> **合成模式** — 所有 60 个系统设计主题已完成。今日深度合成：PACELC 定理。
> Building on: Day 12 (CAP Theorem) · Day 9 (Replication) · Day 11 (Consistent Hashing) · Day 47 (Raft/Paxos)

---

## PACELC 定理：CAP 之后的完整图景
## PACELC Theorem: The Full Picture Beyond CAP

---

### 为什么 CAP 不够用？ / Why CAP Falls Short

CAP 定理（Day 12）告诉你：**网络分区发生时**，选一致性还是可用性。

**它没回答：分区不发生的 99.99% 时间里，你还要做另一个权衡。**

2012 年，Daniel Abadi 提出 **PACELC**：

```
if (Partition happens):
    choose between Availability  vs  Consistency   ← CAP covers this
else (normal operation):
    choose between Latency       vs  Consistency   ← this is what CAP ignores
```

**关键洞察 / Key Insight:** Latency（延迟）和 Consistency（一致性）之间的权衡是**永久性的**，不只在故障时存在。

---

### ASCII: 真实系统在 PACELC 光谱上的位置

```
                CONSISTENCY ◄──────────────────► AVAILABILITY / LOW LATENCY
  (Partition):  [Zookeeper]   [CockroachDB]   [Cassandra]   [DynamoDB]
                    PC              PC              PA            PA
  (Normal):     [MySQL/PG]    [Spanner]       [DynamoDB]    [Cassandra]
                    EC              EC              EC            EL

  Legend:
    P = Partition event  A = Available  C = Consistent
    E = Else (normal)    L = Low Latency
```

---

### 主要数据库对照 / System Comparison

| System | Partition | Normal ops | Real Cost |
|---|---|---|---|
| **Cassandra** (default) | A | L | Eventual consistency; tunable with QUORUM |
| **DynamoDB** (default) | A | L | Eventually consistent reads, ~1ms |
| **DynamoDB** (strong) | C | C | 2× read CU cost, higher latency |
| **Zookeeper / etcd** | C | C | Leader election overhead; ~5-20ms writes |
| **CockroachDB** | C | C | Raft consensus; ~10ms cross-region |
| **Spanner** (Google) | C | C | TrueTime (atomic clocks) → ~14ms global |
| **Cosmos DB** | Tunable | Tunable | 5 explicit consistency levels |

---

### Cosmos DB 的 5 级一致性 — PACELC 的精确量化版

```
Strong ← ——————————————————— → Eventual
  |            |          |            |          |
Strong    Bounded       Session    Consistent  Eventual
          Staleness               Prefix
  ↑ 更高延迟/更低可用性            更低延迟/更高可用性 ↑
```

这不是模糊的"最终一致"，而是精确承诺：
- **Bounded Staleness**: 最多落后 K 次操作 或 T 秒
- **Session**: 单会话内读自己的写（大多数应用的最佳选择）

---

### 为什么这样设计？ / Design Rationale

**Spanner 的极端案例：** Google 用 GPS 原子钟硬件保证全球时间误差 < 7ms（TrueTime API）。通过把"时间不确定性"变成硬件常数，Spanner 实现了 PC/EC 而延迟不超过 ~14ms。这是用硬件换一致性保证的极端例子。

**Cassandra 的实用主义：** QUORUM 读 + QUORUM 写 = 强一致性（RF=3 时需 2/3 节点）。`LOCAL_QUORUM` 让你只在本 region 内保证一致性，跨 region 最终一致——这是多数全球应用的正确选择。

---

### 别踩这个坑 / Common Mistakes

❌ **"我们用了 CAP 分析"** — CAP 只描述分区时行为，忽略了正常运行时的延迟代价  
✅ 问：正常情况下，写一致性需要什么？Cassandra QUORUM 写需等待 2/3 节点，延迟是 1× LOCAL vs 3× MULTI-REGION

❌ **"Cassandra 不安全因为最终一致"** — 误解  
✅ 用 `QUORUM` 读写 + `LWT (Light Weight Transactions)` 可达强一致；代价是 ~3× 延迟

❌ **面试时只说"CAP 所以选 AP"** — 太浅  
✅ 说出 PACELC 分析："分区时我们接受 A；正常时我们需要 L 因为 P99 < 10ms 是 SLO 要求"

---

### 🧒 ELI5

CAP 是问：地震断路了，餐厅是关门（C）还是继续卖但菜单可能过时（A）？PACELC 还问：**没地震的时候**，顾客点菜是等厨师打电话问总部确认（C，慢）还是直接按本地菜单做（L，快）？大多数餐厅平时选快，所以大多数数据库默认最终一致。

---

### 📚 References
- https://en.wikipedia.org/wiki/PACELC_theorem
- https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf (Daniel Abadi, 2012 original paper)
- https://fauna.com/blog/demystifying-database-systems-introduction-to-pacelc
- https://docs.microsoft.com/en-us/azure/cosmos-db/consistency-levels (Cosmos DB 5 levels)
