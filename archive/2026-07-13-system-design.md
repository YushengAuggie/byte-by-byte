# System Design Synthesis — Day 89: Read Path vs. Write Path Optimization

## 🏗️ 系统设计综合 / System Design Synthesis
**专题: 读路径 vs 写路径优化 — 如何为不同访问模式设计不同的架构**
**Topic: Read Path vs. Write Path Optimization — Designing Different Architectures for Different Access Patterns**

---

### 想象你在 Meta 担任系统设计面试官 / Imagine You're a System Design Interviewer at Meta

被面试者给出一个看似合理的设计：一个数据库，所有读写都走同一路径。你会问什么？

*A candidate gives you a seemingly reasonable design: one database, all reads and writes go through the same path. What do you ask?*

**"你的读写比是多少？为什么读和写要用同一个代码路径？"**

*"What's your read-to-write ratio? Why do reads and writes share the same code path?"*

---

### 核心洞察：读写路径天生就不同 / Core Insight: Read & Write Paths Are Fundamentally Different

| 维度 / Dimension | 读路径 Read Path | 写路径 Write Path |
|---|---|---|
| 一致性要求 | 可以稍微过时 (stale OK) | 必须持久化、原子性 |
| 延迟要求 | 极低 P99 | 可接受稍高延迟 |
| 扩展方式 | 水平扩展 Read Replicas | 分片 / WAL / Append-only |
| 失败影响 | 降级展示旧数据 | 数据丢失，不可接受 |
| 缓存友好性 | 极高 | 低（需要失效） |

---

### 真实架构对比 / Real Architecture Comparison

**案例 1: Twitter/X 的 Fanout 演化**
- 早期: 写入时 fanout (写路径重)，每条 tweet 写入所有 follower 的 timeline
- 问题: 名人用户 (Lady Gaga) 写一条推文 → 1亿次写入
- 解法: 混合模式 — 普通用户写入 fanout，名人用户读取时 merge
- **教训**: 写路径优化 ≠ 读路径简单，需要针对访问模式拆分

**案例 2: Facebook TAO (The Associations and Objects)**
- 读路径: 多层缓存 (L1 local + L2 regional) → 99%+ hit rate
- 写路径: 单 leader 写入 MySQL → 异步复制到 cache
- 关键: 读写完全解耦，读路径不感知底层存储

**案例 3: Kafka 作为写路径的 Buffer**
- 写路径: Producer → Kafka → Consumer (异步，append-only)
- 读路径: 预计算结果存入 Redis/Elasticsearch 供查询
- **CQRS (Command Query Responsibility Segregation)** 的极致体现

---

### 架构图 / Architecture

```
Write Path (写路径):
Client → API Gateway → Write Service
           ↓
        Kafka (Buffer)
           ↓
   [Consumer Workers] → Primary DB (MySQL/Postgres)
           ↓
   Async Replication → Read Replicas
           ↓
   Cache Invalidation → Redis

Read Path (读路径):
Client → API Gateway → Read Service
           ↓
        Redis Cache (L1) ←─── 99% hits
           ↓ (miss)
     Read Replicas (L2)
           ↓ (miss)
     Primary DB (L3, rare)
```

---

### 什么时候分离读写路径？/ When to Separate Read/Write Paths?

✅ **必须分离 / Must separate:**
- 读写比 > 10:1 (大多数 CRUD 应用)
- 读延迟 SLA < 10ms 但写可以接受 100ms
- 需要不同的一致性保证 (最终一致 vs 强一致)

⚠️ **可以不分离 / Can skip:**
- 小型服务 (<1K QPS)
- 强一致性是硬需求 (金融交易)
- 团队规模小，复杂度成本高过收益

---

### 常见的坑 / Common Mistakes

❌ **对所有查询都用主库** → 浪费 read replica 资源，主库成瓶颈
❌ **缓存失效逻辑在写路径** → 难以维护，容易造成不一致
❌ **忽略复制延迟** → 读到过时数据导致用户困惑 (刚刚发的帖子看不到)
✅ **最佳实践**: 写后读 (read-after-write consistency) 用 session token 或 version 号

---

### 📚 References
- [Facebook TAO: The Power of the Graph](https://www.usenix.org/conference/atc13/technical-sessions/presentation/bronson) — USENIX ATC 2013
- [Twitter's Fanout Service Evolution](https://blog.twitter.com/engineering/en_us/topics/infrastructure/2021/processing-billions-of-events-in-real-time-at-twitter) — Twitter Engineering Blog
- [CQRS Pattern — Martin Fowler](https://martinfowler.com/bliki/CQRS.html)
- [Designing Data-Intensive Applications, Chapter 5](https://dataintensive.net/) — Martin Kleppmann

### 🧒 ELI5
想象餐厅里有两条通道：一条是厨房的"出菜口"（读），另一条是"点餐台"（写）。如果每次有人点单，厨师都要停下来处理，出菜就慢了。把两条通道分开，厨师专心做菜，收银员专心收单，效率翻倍。

*Imagine a restaurant with two lanes: one for food pickup (read), one for order taking (write). If the chef had to stop cooking every time someone placed an order, meals would be slow. Separate the lanes — chef cooks, cashier takes orders — double the throughput.*
