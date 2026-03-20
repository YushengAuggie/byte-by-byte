# 🏗️ 系统设计 Day 7 (3 min read) / System Design Day 7
## Database Types: SQL vs NoSQL — 数据库类型：关系型 vs 非关系型

---

想象你在设计一个新的社交媒体平台…

你的用户数据整齐划一：每人都有 ID、用户名、邮箱、注册时间。这很适合用 **SQL 数据库** — 就像一张结构清晰的 Excel 表格，行和列整整齐齐。

但是，用户发的帖子呢？有人只写文字，有人附图片，有人嵌入视频，有人加了位置标签… 每条帖子的结构都不同。这时候 **NoSQL** 就大放异彩 — 像一个灵活的 JSON 文档，想放什么字段就放什么。

---

### 架构对比 / Architecture Comparison

```
         SQL Database                    NoSQL Database
    ┌─────────────────────┐         ┌─────────────────────────┐
    │      USERS TABLE    │         │    users collection     │
    ├──────┬──────┬───────┤         │                         │
    │  id  │ name │ email │         │ { id: 1,                │
    ├──────┼──────┼───────┤         │   name: "Alice",        │
    │  1   │Alice │a@x.com│         │   email: "a@x.com",     │
    │  2   │ Bob  │b@y.com│         │   preferences: {...},   │
    └──────┴──────┴───────┘         │   badges: ["🏆","⭐"] } │
                                    └─────────────────────────┘
    Schema enforced upfront          Schema flexible / per doc
    JOIN across tables               Embed related data
    ACID transactions                Eventual consistency (often)
    Scale: vertical (bigger server)  Scale: horizontal (more servers)
```

---

### 核心概念 / Key Concepts

**SQL (关系型数据库) — MySQL, PostgreSQL, SQLite**
- **结构化数据**: 表、行、列，schema 固定
- **ACID 事务**: Atomicity（原子性）, Consistency（一致性）, Isolation（隔离性）, Durability（持久性）— 银行转账不能丢数据！
- **JOIN 操作**: 多表关联查询，数据不冗余
- **强一致性**: 写入后立即可读

**NoSQL — MongoDB (文档), Redis (键值), Cassandra (列族), Neo4j (图)**
- **灵活 schema**: 每条记录结构可以不同
- **水平扩展**: 分片（sharding）轻松加机器
- **最终一致性**: 写入后可能有短暂延迟才全局可见
- **高吞吐量**: 读写速度极快（尤其键值存储）

---

### 为什么这样设计？How to Choose?

| 场景 | 推荐 | 原因 |
|------|------|------|
| 用户账户、订单、财务 | SQL | 需要 ACID，数据关系明确 |
| 用户会话、缓存、排行榜 | Redis (NoSQL) | 极速读写，TTL 支持 |
| 产品目录、内容管理 | MongoDB (NoSQL) | 结构多变，嵌套文档 |
| 社交图谱、推荐系统 | Neo4j (Graph) | 关系查询是核心需求 |
| 日志、时序数据 | Cassandra (NoSQL) | 海量写入，时间范围查询 |

**经验法则**: 先问"我的数据关系是否复杂？事务是否关键？" → 是则 SQL。"数据量是否巨大？结构是否多变？" → 是则 NoSQL。

**现实中：两者共存！**
- Instagram: PostgreSQL（用户/帖子关系） + Cassandra（活动 feed） + Redis（缓存）
- 单一数据库解决所有问题是反模式

---

### 别踩这个坑 / Common Mistakes

❌ **"NoSQL 比 SQL 更快"** — 错！取决于使用场景。复杂 JOIN 查询 SQL 更高效；简单键值查找 Redis 秒杀一切。

❌ **"NoSQL 不支持事务"** — MongoDB 4.0+ 已支持多文档 ACID 事务，只是使用场景不同。

❌ **"选了就不能换"** — 实践中，随着业务演进经常需要引入第二种数据库。提前规划数据访问层（DAL）让切换更容易。

❌ **过早优化** — 99% 的创业公司用 PostgreSQL 就够了。等真正有 scale 问题再引入 NoSQL。

---

📚 **深入学习 / Learn More:**
- [Uber Engineering: Postgres to MySQL Migration](https://www.uber.com/blog/postgres-to-mysql-migration/) — 真实案例：为什么 Uber 从 PostgreSQL 迁移到 MySQL
- [ByteByteGo: SQL vs NoSQL](https://www.youtube.com/watch?v=_Ss42Vb1SU4) — 可视化对比讲解（YouTube）
- [Designing Data-Intensive Applications, Ch. 2](https://dataintensive.net/) — Martin Kleppmann 的权威参考书

🧒 **ELI5:** A SQL database is like a super organized binder with divider tabs where everything goes in exactly the right slot; a NoSQL database is like a big backpack where you can throw in anything — a book, a lunchbox, a basketball — whatever shape it is.
