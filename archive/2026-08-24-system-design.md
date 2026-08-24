# 📊 Day 118 — System Design Synthesis
> 🔥 Expert Level | Synthesis: 存储选型决策框架

---

🏗️ **系统设计 / System Design**
**存储选型全景图 — 何时用哪种数据库？**
**Storage Selection Guide — Picking the Right Database for Every Job**

---

## 🎯 核心问题 / The Core Question

面试官最爱问：「你会用什么数据库？为什么？」  
Interviewers love asking: "What database would you use? Why?"

❌ 错误答案：「用 PostgreSQL，它很可靠。」  
❌ Wrong answer: "PostgreSQL, it's reliable."

✅ 正确答案：取决于数据模式、访问模式、一致性要求和规模。  
✅ Right answer: Depends on data shape, access pattern, consistency requirements, and scale.

---

## 📊 存储类型速查 / Storage Cheatsheet

```
场景 / Scenario              → 推荐存储 / Use This
──────────────────────────────────────────────────────────
ACID 事务 / ACID transact.   → PostgreSQL / MySQL
灵活 Schema / Flexible schema → MongoDB (document DB)
低延迟热数据 / Hot cache      → Redis / Memcached
时序数据 / Time-series        → InfluxDB / TimescaleDB
全文搜索 / Full-text search   → Elasticsearch / OpenSearch
文件/对象 / Blobs             → S3 / GCS
事件流 / Event stream         → Kafka / Kinesis
图关系 / Graph queries        → Neo4j / Amazon Neptune
全球低延迟 KV                 → DynamoDB / Cassandra
OLAP 分析 / Analytics         → BigQuery / Snowflake
```

---

## 🔑 关键决策轴 / Key Decision Axes

### 1. 一致性 vs 可用性 (CAP 回顾)
- **强一致性**：PostgreSQL, MySQL, etcd, Zookeeper — 用于金融、支付
- **最终一致性**：DynamoDB, Cassandra, Redis Cluster — 用于社交、推荐
- 口诀：钱要强一致，点赞可最终。

### 2. 读写比例
- **读多写少** (>10:1)：PostgreSQL + Read Replica + Redis 缓存层
- **写多读少**：Cassandra（LSM-Tree 写路径极快），ClickHouse（列存批写）
- **均等**：单 PostgreSQL + 合理索引往往撑到 10K QPS

### 3. 数据结构
- 结构化关系 → SQL（JOIN 是第一公民）
- 嵌套文档（用户配置、JSON） → MongoDB / DynamoDB
- 纯 Key-Value 点查 → Redis / DynamoDB
- 宽列（时序、日志行） → Cassandra / HBase

### 4. 规模边界（经验值）
```
< 1TB,  < 10K QPS    → 单 PostgreSQL 实例
< 10TB, < 100K QPS   → PostgreSQL + Read Replica + Redis
> 10TB  or 全球分布  → DynamoDB Global / Cassandra / Vitess
PB 级分析            → BigQuery / Snowflake (OLAP, 不是 OLTP!)
```

---

## 🏗️ 典型生产架构 / Typical Polyglot Stack

```
用户请求 / User Request
    │
    ├── CDN (S3 + CloudFront) ── 静态资源 / Static assets
    │
    └── API Server
            ├── Redis ────────────── 缓存、Session、分布式锁
            ├── PostgreSQL ──────── 用户/订单/核心业务 (ACID)
            ├── Elasticsearch ────── 搜索、日志分析
            ├── S3 ──────────────── 文件、图片、备份
            └── Kafka ──────────── 事件流、服务解耦
```

为什么这样设计？  
Why this design?
- 每个存储做它最擅长的事。PostgreSQL 不擅长 TB 级搜索，Elasticsearch 不擅长 ACID。
- Each storage does what it's best at. PostgreSQL is bad at TB-scale search; Elasticsearch is bad at ACID.

---

## ⚠️ 常见误区 / Common Mistakes

❌ **过早引入 NoSQL**  
很多初创公司数据量很小时就用 MongoDB，反而失去了 JOIN 和 ACID，后来痛苦迁回 PostgreSQL。  
Many startups adopt MongoDB prematurely, lose JOINs + ACID, then migrate back to Postgres in pain.

❌ **把 Redis 当主数据库**  
Redis 是缓存/会话存储，数据有丢失风险（AOF+RDB 需要配置，且 Redis 重启有延迟）。  
Redis is a cache/session store. Data loss risk unless persistence is carefully configured.

❌ **一库解决所有问题**（Mono-DB Fallacy）  
认为 PostgreSQL 或 MongoDB 能搞定一切。生产系统几乎都是多存储架构。  
Production systems are almost always polyglot. No single DB wins everything.

❌ **混淆 OLTP 和 OLAP**  
在 PostgreSQL 上跑大量分析查询会锁表、拖慢在线业务。复杂分析要走数仓（BigQuery/Snowflake）。  
Running heavy analytics on your OLTP database slows production traffic. Separate your data warehouse.

---

## 📚 References
- https://architecturenotes.co/things-you-should-know-about-databases/
- https://use-the-index-luke.com/
- https://www.postgresql.org/docs/current/indexes.html
- https://cassandra.apache.org/doc/latest/cassandra/architecture/overview.html

## 🧒 ELI5
不同存储就像厨房工具：冰箱存食材（PostgreSQL），微波炉快速加热（Redis），归档柜存食谱（S3），留言板传消息（Kafka），搜索引擎找食谱（Elasticsearch）。  
Different databases are like kitchen tools: fridge for ingredients (Postgres), microwave for quick reheating (Redis), filing cabinet for recipes (S3), message board for communication (Kafka), index for finding recipes (Elasticsearch). Use the right tool for the job.
