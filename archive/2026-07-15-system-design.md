# 系统设计 / System Design — Day 91 (Synthesis)
**Date:** 2026-07-15 | **Phase:** Expert | **Mode:** Synthesis

---

## 🏗️ 系统设计 / System Design
**综合对比: 分布式系统一致性模型全景 / Consistency Models Landscape**

---

### 想象这个场景 / Imagine This

你已经覆盖了 60 个系统设计主题。现在面试官问："给我讲讲各种一致性模型，以及在真实系统中如何选择。"

You've covered 60 system design topics. Now the interviewer asks: "Walk me through consistency models and how you choose between them in real systems."

---

### 一致性模型谱 / The Consistency Spectrum

```
强一致性                                          最终一致性
Strong ◄────────────────────────────────────► Eventual

Linearizability  Sequential  Causal  Read-Your-  Eventual
(线性化)          (顺序化)    (因果)  Writes      (最终)
     │               │          │        │          │
  最慢/最贵        较慢       适中    较快/廉价    最快
  Slowest          Slower   Moderate  Faster     Fastest
     │               │          │        │          │
  ZooKeeper       RDBMS     DynamoDB  DynamoDB   Cassandra
  etcd            Spanner   (option)  (eventual) (W+R<N)
  Redis w/AOF     CockroachDB         Cosmos DB
```

---

### 你学过的系统 → 一致性选择 / Systems You've Covered → Choices

| 系统 | 一致性级别 | 为什么？|
|------|-----------|---------|
| Redis (Caching) | Eventual (replica lag) | 性能 > 一致性，cache miss 可重建 |
| Distributed Cache | Strong (via locking) | 防止 thundering herd |
| URL Shortener | Eventual is OK | 短链"刚创建后读不到"可接受 |
| Payment System | Linearizable | 钱不能双花，必须强一致 |
| Chat (WhatsApp) | Causal | 消息顺序必须因果一致（A→B→C） |
| Rate Limiter | Approximate OK | 偶尔多放一个请求没关系 |
| Stock Exchange | Linearizable | 撮合引擎必须全局有序 |
| Distributed Lock | Linearizable | 锁语义要求线性化 |
| Search Autocomplete | Eventual | 稍旧的索引完全可接受 |
| Recommendation | Eventual | 推荐延迟更新无所谓 |

---

### CAP 回顾 + PACELC 升级 / CAP Revisited + PACELC Upgrade

你在 Day 12 学了 CAP。真实工程师用 **PACELC**：

You covered CAP on Day 12. Real engineers use **PACELC**:

```
CAP:    分区时选 C 或 A
PACELC: 分区时选 C 或 A，无分区时选 Latency 或 Consistency

CAP:    During partition, choose C or A
PACELC: During Partition → C or A; Else → Latency or Consistency
```

例子：DynamoDB = PA/EL（分区时选可用，正常时选低延迟）  
Spanner = PC/EC（两者都选一致性，靠原子钟）

---

### 关键设计选择 / Key Design Choices

**Write path 决定一致性：**
```python
# Strong consistency: sync replication
def write(data):
    primary.write(data)
    for replica in replicas:
        replica.write(data)  # 同步等待
    return "ok"  # 所有副本确认后返回

# Eventual consistency: async replication  
def write(data):
    primary.write(data)
    async_replicate_to(replicas, data)  # 异步，不等待
    return "ok"  # 立即返回
```

**Quorum 中间路线：**
- N=3 副本，W=2 写，R=2 读 → W+R > N → 强一致
- W=1，R=1 → 最终一致
- DynamoDB 让你**在请求级别**选择！

---

### 常见陷阱 / Common Mistakes

**别踩这个坑 — 一致性误区：**

1. ❌ "加了缓存，数据库和缓存怎么保持一致？" → 答案：**不能完全保持**，只能减少窗口
2. ❌ 为所有系统选强一致性 → 支付 OK，推荐系统杀鸡用牛刀
3. ❌ 混淆"一致性"（CAP）和"持久性"（ACID D）→ 两个不同维度
4. ✅ 告诉面试官：**"我选最终一致性，因为 X；用 [技术] 来缓解 Y 风险"**

---

### 面试答题框架 / Interview Framework

```
问自己 3 个问题 / Ask yourself 3 questions:

1. 数据错误的代价是什么？
   Cost of incorrect data?
   高（支付/锁）→ 强一致  低（推荐/feed）→ 最终

2. 读写比例是多少？
   Read/write ratio?
   读多 → 异步复制副本  写多 → 考虑分片

3. 用户能接受多少延迟？
   User latency tolerance?
   低延迟需求 → 最终一致 + 补偿机制
```

---

### 综合回顾图 / Big Picture

```
             你设计的系统分布:
                You've designed:

Financial Layer    ████████  Linearizable
(Payment, Exchange)          (ZooKeeper, Spanner)

Infrastructure     ██████    Strong-to-Causal
(Cache, Lock, ID gen)        (Redis, etcd, Snowflake)

Communication      █████     Causal
(Chat, Collab Docs)          (vector clocks, CRDTs)

Content/Discovery  ████████  Eventual
(Search, CDN, Rec)           (Cassandra, DynamoDB)
```

---

### 📚 深度参考 / References

- [Consistency Models — Jepsen.io](https://jepsen.io/consistency)
- [PACELC: Beyond CAP — Daniel Abadi](https://dbmsmusings.blogspot.com/2010/04/problems-with-cap-and-yahoos-little.html)
- [Designing Data-Intensive Applications — Ch.9](https://dataintensive.net/)

### 🧒 ELI5

一致性就像多个账本记同一笔钱：  
**强一致** = 每个账本同时更新，写完才能读  
**最终一致** = 先更新主账本，其他账本"最终"会跟上  
**选哪个** = 取决于"读到旧数据有多糟糕"

Consistency is like multiple ledgers tracking the same money:  
**Strong** = all ledgers update simultaneously before anyone can read  
**Eventual** = update the main ledger, others catch up "eventually"  
**Which to choose** = depends on "how bad is it to read stale data"
