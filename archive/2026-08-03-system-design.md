# 🏗️ 系统设计合成 / System Design Synthesis — Day 107

> 📊 NeetCode: 83/150 · SysDesign: 60/60 · Behavioral: 60/60 · Frontend: 37/50 · AI: 30/30
> 🔥 6-day streak!

---

## 一致性 vs 可用性：跨系统决策框架
## Consistency vs Availability: A Cross-System Decision Framework

所有60个系统设计专题都覆盖完毕。今天做一次高阶合成——当你真正坐在白板前设计系统时，**如何在一致性、可用性和延迟之间做出正确的工程决策**？

All 60 system design topics are complete. Today's synthesis: **how do you actually choose** between consistency, availability, and latency when facing a real design interview or production decision?

---

### 📊 我们设计过的系统：CAP 分类一览

| 系统 | CAP 选择 | 一致性模型 | 核心原因 |
|------|---------|-----------|---------|
| Redis Cluster | AP | 最终一致 | 速度优先；允许短暂脏读 |
| etcd / ZooKeeper | CP | 线性一致 | 分布式锁不容出错 |
| Cassandra | AP | 可调一致（quorum） | 写高可用；读可配置 |
| Kafka | CP | 顺序一致 | 消息不能乱序或丢失 |
| Spanner | CP* | 外部一致（外部时钟） | 原子钟；真正的全球强一致 |
| DynamoDB | AP | 最终一致（可选强读） | 互联网规模；低延迟优先 |
| Raft-based (TiKV, etcd) | CP | 强一致 | Leader选举保证唯一写入 |

*Spanner 用 TrueTime 在实践中接近 CA，但理论上仍是 CP

---

### 🔑 决策框架：三问法 / Three-Question Framework

```
Q1: 用户可见吗？
  → 购物车、评论、点赞 → 最终一致 OK
  → 库存、余额、订单状态 → 强一致必须

Q2: 写冲突怎么办？
  → Last-Write-Wins → 适合 AP（允许少量覆盖）
  → CRDT / 乐观锁 → 协作编辑（Google Docs）
  → 悲观锁 → 票务系统（Ticketmaster）

Q3: 网络分区时优先哪个？
  → 必须响应（哪怕数据稍旧） → AP
  → 宁愿拒绝请求（保证数据准确） → CP
```

---

### 🔄 跨系统模式复用

设计过的这些系统里，有几个决策会反复出现：

1. **写扩散 vs 读扩散** — 社交 feed (Twitter/Instagram) 选写扩散；搜索引擎选读时聚合
2. **同步 vs 异步** — 支付系统用同步（Stripe）；通知系统用异步 Kafka
3. **单主 vs 多主** — MySQL 主从用于读扩展；Cassandra 多主用于写高可用
4. **本地缓存 vs 分布式缓存** — Redis 处理热点；CDN 处理静态资源；本地 LRU 处理用户 session

---

### ⚠️ 面试常见误区 / Common Mistakes in Interviews

- **"我用 Postgres 就没有分布式问题"** — 单节点没问题，但一旦分库分表，CAP 立刻出现
- **混淆两个 C** — ACID 的 C = 约束一致性（外键、唯一键）；CAP 的 C = 线性一致性（读到最新写）
- **忽略 Partition Tolerance** — 互联网环境下 P 几乎不可避免，实际只有 **AP vs CP** 的选择
- **过度设计一致性** — 头像图片不需要强一致；但账户余额必须

---

### 🧒 ELI5

想象你和朋友在两个城市用同一块白板：
- **CP** = 你改了之后，朋友必须等传真到达才能看到；中途白板"锁住"不让写
- **AP** = 你们都能随时写；偶尔版本会打架，系统自动合并（可能丢掉一条笔记）

选哪个取决于——**丢一条笔记** vs **等传真** 哪个更能接受？

---

### 📚 References
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html
- https://jepsen.io/consistency
- https://aws.amazon.com/blogs/database/amazon-dynamodb-under-the-hood-how-we-built-a-hyper-scale-database/
