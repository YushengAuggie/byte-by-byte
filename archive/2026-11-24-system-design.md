# 🏗️ 系统设计 / System Design — Day 156 (Synthesis)
## 一致性模型全景图 — 从 Eventual 到 Linearizable 的工程决策
## Consistency Model Panorama — Engineering Choices from Eventual to Linearizable

> 综合回顾: Day 12 (CAP), Day 9 (Replication), Day 39 (Cache), Day 47 (Consensus), Day 54 (Multi-Region)

---

### 🔍 为什么这很重要 / Why This Matters

过去60天，我们设计了YouTube、Google Maps、支付系统、分布式缓存……每次都会面临同一个问题：**这个数据需要多强的一致性？** 今天把这些散落的知识串成一张决策地图。

Over 60 designs, one question kept recurring: **how consistent does this data need to be?** Today we unify the scattered lessons into a single decision framework.

---

### 📊 一致性层级 / The Consistency Spectrum

```
弱 Weak ◄─────────────────────────────────► 强 Strong

Eventual       Read-your-writes    Monotonic Read    Sequential    Linearizable
最终一致          读自己写              单调读              顺序一致性         线性一致性

DNS, S3       User profile        Social feed       Kafka order    Redis INCR
Shopping cart  Auth session       Notification      Zookeeper      Bank balance
```

---

### 🏗️ 过去设计的一致性选择 / Consistency Choices Across Our Designs

| 系统 System | 选择 Choice | 原因 Why |
|---|---|---|
| URL Shortener (Day 19) | Eventual | 重定向不需要强一致；CDN 缓存可以短暂脏读 |
| 支付系统 Payment (Day 38) | Linearizable | 钱不能多扣；必须用分布式事务/2PC |
| 聊天系统 Chat (Day 28) | Causal | 消息要有因果序，但不需要全局线性 |
| 分布式缓存 Cache (Day 39) | Tunable | Redis 默认异步复制；关键场景用 WAIT 命令 |
| 多地 Active-Active (Day 54) | Eventual + CRDT | 跨 region 延迟太高，用 conflict-free structures |

---

### ⚡ 决策框架 / Decision Framework

```
问题1: 写后必须立即读到自己写的数据？
  YES → Read-your-writes (session affinity / read-after-write)
  NO  → 继续

问题2: 多用户并发写同一条记录？(如库存、余额)
  YES → Linearizable (单 leader + MVCC / distributed lock)
  NO  → 继续

问题3: 数据有因果依赖？(评论早于回复)
  YES → Causal consistency (vector clocks / Lamport timestamps)
  NO  → Eventual consistency is fine
```

---

### 🔴 别踩这个坑 / Common Mistakes

**坑1: 把"高可用"和"强一致"当成对立面**
> 实际上只是 latency vs consistency 的权衡。Redis Cluster 可以用 `WAIT` 实现 read-after-write，代价是 p99 延迟上升。

**坑2: 对所有数据用同一策略**
> 电商系统：商品价格用 Eventual（CDN 缓存），下单用 Linearizable（库存扣减），订单历史用 Read-your-writes（刚付完款要立刻看到）。

**坑3: 忽略 clock skew**
> 多 region 写时绝对不能用本地时间戳排序。用 Hybrid Logical Clocks (HLC) 或 Google TrueTime。

---

### 🧒 ELI5

就像餐厅记账：
- **Eventual**：服务员先用便利贴记，晚点再录入电脑。可能短暂不同步，但最终一致。
- **Linearizable**：收银机直接记，所有人看到的账都一样，但收银机坏了就完了。
- **Read-your-writes**：你点的菜服务员一定记住了，哪怕其他人还不知道。

---

### 📚 References
- https://jepsen.io/consistency — 最权威的一致性模型分类
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html
- https://aws.amazon.com/blogs/database/choosing-the-right-dynamodb-consistency-model/
