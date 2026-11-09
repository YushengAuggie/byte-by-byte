# 🏗️ 系统设计 / System Design — Day 151 (Synthesis)

> **综合深化 / Expert Synthesis:** 60个系统设计话题全部完成。今天深入对比——分布式一致性模型全景图。

---

## 分布式系统一致性模型深度对比 — From Redis to Spanner

### 想象你在设计...

你是技术负责人，面对三个不同的存储选型问题：
1. 用户 session — 丢数据无所谓，速度第一
2. 库存扣减 — 超卖一次损失巨大
3. 全球用户档案 — 需要跨区域读写、强一致

这三个场景需要完全不同的一致性模型。

---

### 一致性模型谱系 (Consistency Spectrum)

```
Weak          Eventual         Strong         Linearizable
  |               |               |                |
Redis Cache   Cassandra      DynamoDB          Spanner
(no sync)    (tunable)      (single-key)     (global txn)

← 延迟低、可用高                      延迟高、可用受限 →
```

**四种核心模型:**

**1. Weak Consistency (弱一致)**
- 写完不保证立刻可读
- 典型: CPU Cache, Redis (默认)
- 场景: 限流计数器、view count，错一点无所谓

**2. Eventual Consistency (最终一致)**
- 最终收敛，不保证何时
- 典型: Cassandra, DynamoDB (eventually consistent reads), DNS
- 场景: 社交 feed、用户 profile、购物车

**3. Strong Consistency (强一致)**
- 读到最新写入
- 典型: DynamoDB (strongly consistent reads), RDBMS (single node)
- 场景: 账户余额、读-改-写需要串行化

**4. Linearizability / External Consistency**
- 所有操作有全局时间顺序，像单机一样
- 典型: Google Spanner (TrueTime API), etcd, ZooKeeper
- 场景: 分布式锁、金融转账跨行、分布式 CAS

---

### 为什么这样设计？关键权衡

**CAP vs PACELC:**
- CAP 只描述分区时的选择 (CP or AP)
- PACELC 补充了正常运行时的选择: 延迟 vs 一致性
- 真实系统更多是 PACELC 问题，网络分区是小概率事件

**Cassandra 的 Quorum 魔法:**
```
W + R > N → 保证至少一个节点重叠 → 读到最新写

N=3, W=2, R=2 → 强一致 (but slower)
N=3, W=1, R=1 → 弱一致 (but fast)
N=3, W=1, R=3 → read-heavy strong (rarely used)
```

**Spanner 的 TrueTime:**
Google 用 GPS + 原子钟，把时间不确定性压到 <7ms，然后等待这个窗口再提交事务 → 全球 linearizable 但有延迟代价。

---

### 别踩这个坑 (Common Mistakes)

❌ **误区1:** "我们用 Cassandra，所以要强一致就全设 W=N, R=N"
→ 性能断崖。真正需要强一致的数据应该换 DB，不要强拧 Cassandra。

❌ **误区2:** "微服务间用最终一致性，加个重试就好了"
→ 没有幂等性设计的重试 = 数据翻倍。Outbox Pattern + idempotency key 是标配。

❌ **误区3:** 分布式锁用 Redis SETNX 就够了
→ Redis 故障转移窗口内锁会失效。高风险场景用 Redlock 或直接 etcd。

---

### 选型决策框架

| 需求 | 推荐 | 原因 |
|------|------|------|
| 高吞吐写、跨区读 | Cassandra | Tunable consistency |
| 低延迟 K-V + 强一致单 key | DynamoDB | Per-key atomic ops |
| 分布式事务、全球一致 | Spanner/CockroachDB | TrueTime / HLC |
| 分布式锁/选主 | etcd/ZooKeeper | Raft-based linearizable |
| 缓存/速率限制 | Redis | Who cares about consistency here |

---

### 📚 References
- https://jepsen.io/consistency — Consistency models interactive guide
- https://cloud.google.com/spanner/docs/true-time-external-consistency — Spanner TrueTime
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html — Werner Vogels on eventual consistency
- https://martinfowler.com/articles/patterns-of-distributed-systems/two-phase-commit.html — 2PC patterns

### 🧒 ELI5
想象你家有三个人共用同一个银行账户：妈妈、爸爸、你。
- **弱一致** = 各自记小本子，偶尔对一下，可能有人多花了钱
- **最终一致** = 每晚同步一次，白天可能有出入，但第二天一定对齐
- **强一致** = 每次花钱都要打电话给全家人确认，慢但不会超支
- **Linearizable** = 全家人都在同一个房间，一个人买东西所有人立刻知道
