# 🏗️ 系统设计 Day 11 / System Design Day 11
## CAP 定理与最终一致性 / CAP Theorem & Eventual Consistency

> **难度 / Difficulty:** Intermediate | **阶段 / Phase:** Growth | **预计阅读时间 / Read time:** 3 min

---

## 🌍 真实场景 / Real-World Scenario

想象你在设计 Twitter（现 X）的点赞系统。用户遍布全球，分布在北美、欧洲、亚洲的数据中心。当网络故障发生时，你必须做一个选择：

**要么**继续接受点赞写入（可能导致各地数据不一致）；
**要么**拒绝所有写入（保证数据一致，但系统不可用）。

这就是 CAP 定理的核心困境。

Imagine you're designing Twitter's like system, with users spread across data centers in North America, Europe, and Asia. When a network partition occurs, you face a hard choice:

**Either** keep accepting like writes (risking inconsistent counts across regions),
**or** reject all writes (keeping data consistent, but making the system unavailable).

This is the core dilemma of the CAP theorem.

---

## 📐 CAP 定理解释 / CAP Theorem Explained

CAP 定理由 Eric Brewer 在 2000 年提出，它说：**分布式系统最多只能同时满足以下三项中的两项：**

CAP theorem (Brewer, 2000) states: **a distributed system can guarantee at most 2 of these 3 properties simultaneously:**

| 属性 | 英文 | 解释 |
|------|------|------|
| **C** | Consistency | 所有节点在同一时刻看到相同数据 / All nodes see same data at same time |
| **A** | Availability | 每个请求都收到响应（非错误）/ Every request gets a response (non-error) |
| **P** | Partition Tolerance | 网络分区时系统仍继续运行 / System works despite network partitions |

> ⚠️ **关键洞察：** 在真实分布式系统中，网络分区（P）是不可避免的。所以你实际上是在 **CA（一致性 vs 可用性）** 之间做取舍。

---

## 🏛️ ASCII 架构图 / Architecture Diagram

```
正常状态 / Normal State:
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Node A  │◄───────►│  Node B  │◄───────►│  Node C  │
│ likes=42 │         │ likes=42 │         │ likes=42 │
└──────────┘         └──────────┘         └──────────┘
      ▲
  user writes

网络分区 / Network Partition:
┌──────────┐    ✗    ┌──────────┐         ┌──────────┐
│  Node A  │ BROKEN  │  Node B  │◄───────►│  Node C  │
│ likes=45 │         │ likes=42 │         │ likes=42 │
└──────────┘         └──────────┘         └──────────┘
(user wrote 3 more)   (partition: can't sync)

CP 选择 (e.g. HBase, Zookeeper):   AP 选择 (e.g. Cassandra, DynamoDB):
→ 拒绝 Node B/C 的写入               → 允许各自独立写入
→ 数据一致，但不可用                  → 可用，但数据暂时不一致
```

---

## ⚖️ 关键权衡 / Key Tradeoffs

### CP 系统（一致性 + 分区容错）

**为什么这样设计？** 需要强一致性的场景，例如金融交易、库存系统。

- ✅ 数据永远一致，不会有脏读
- ❌ 网络分区时部分节点不可用
- 📦 代表：HBase, MongoDB (default), ZooKeeper, etcd

### AP 系统（可用性 + 分区容错）

**为什么这样设计？** 高可用性更重要，短暂不一致可接受，例如社交 feed、购物车。

- ✅ 系统始终响应，用户体验好
- ❌ 不同节点可能返回不同结果（**最终一致性**）
- 📦 代表：Cassandra, DynamoDB, CouchDB, DNS

### 最终一致性 / Eventual Consistency

```
时间线 Timeline:

t=0  User writes likes=45 to Node A
t=1  Node A is isolated (partition)
t=2  User reads from Node B → gets 42 (stale!)
t=5  Partition heals, nodes sync
t=6  User reads from Node B → gets 45 ✅ (eventually consistent)
```

**最终一致性** 并非"随机错误"，而是"在网络恢复后，所有副本最终达到相同状态"。

---

## 🚫 常见错误 / Common Mistakes

**别踩这个坑：**

1. **误解 CAP 是固定选择** — 现代系统（如 DynamoDB）允许你按操作级别调整一致性（`ConsistencyLevel: QUORUM` vs `ONE`），而不是全局二选一。

2. **把 CA 作为选项** — 不存在真正的"CA 系统"，因为没有网络分区容错的系统根本不是分布式系统。

3. **忽视 PACELC 扩展** — CAP 只描述分区时的行为，[PACELC 模型](https://en.wikipedia.org/wiki/PACELC_theorem)还考虑了**正常运行时**的延迟 vs 一致性权衡，更全面。

4. **混淆最终一致性和弱一致性** — 最终一致性保证"最终会对齐"；弱一致性不做任何保证。

---

## 🔍 面试重点 / Interview Focus

当面试官问"你会如何设计 X 系统"时，主动提出 CAP：

> "这取决于一致性需求。如果是金融交易，我会选 CP；如果是社交 feed，AP + 最终一致性更合适，因为用户短暂看到旧数据不是大问题。"

---

## 📚 参考资料 / References

- 🔗 [CAP Theorem Explained — IBM](https://www.ibm.com/topics/cap-theorem)
- 🔗 [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services](https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf)
- 🔗 [PACELC theorem — Wikipedia](https://en.wikipedia.org/wiki/PACELC_theorem)
- 🔗 [Cassandra vs MongoDB — Consistency Model Comparison](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)

---

## 🧒 ELI5（像我5岁一样解释）

想象你和好朋友各有一本记事本，记录班里同学的生日。你们约定互相抄写更新。

- **CP**：如果你们之间的电话断了，就不写新内容，直到联系上为止（一致，但暂停工作）
- **AP**：各自继续记录，电话修好后再对比合并（继续工作，但暂时可能不一样）

大多数社交网站选择 AP：你的点赞数可能偶尔显示"旧数据"，但网站从不宕机。
