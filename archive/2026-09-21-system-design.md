# 🏗️ 系统设计综合 / System Design Synthesis — Day 134

**数据存储选型决策矩阵：Staff 工程师的完整框架**
**Data Storage Selection Matrix: A Staff Engineer's Complete Framework**

> 想象你是一家中型电商公司的 Staff 工程师。产品经理带来了 7 个新需求，你来选型。
> You're a Staff engineer at a mid-size e-commerce. PM brings 7 new requirements. You pick the storage.

---

## 场景 → 选型 / Scenario → Choice

| 需求 Need | 方案 Solution | 理由 Why |
|-----------|---------------|----------|
| 用户会话 Sessions | Redis | TTL 自动过期，O(1) 读写，横向扩展 |
| 商品目录 Product catalog | PostgreSQL + Elasticsearch | 结构化 ACID + 全文搜索 |
| 订单历史 Order history | PostgreSQL | 强一致性，事务，审计日志 |
| 实时点击流 Clickstream | Kafka + ClickHouse | 高吞吐写入，列存聚合 |
| 通知推送 Notifications | Kafka | 持久化，扇出，消费者解耦 |
| 限流计数器 Rate limiting | Redis INCR + EXPIRE | 原子操作，毫秒级 |
| 附近商家 Nearby merchants | PostgreSQL + PostGIS | 地理空间索引 |

---

## 系统架构 / Architecture

```
[Client]
   ↓
[API Gateway] ──→ [Rate Limiter (Redis INCR)]
   ↓
[Service Layer]
  ├──→ [PostgreSQL]     # orders, users, catalog (ACID)
  ├──→ [Redis Cluster]  # sessions, cache, rate limit (O(1))
  ├──→ [Elasticsearch]  # full-text product search
  ├──→ [Kafka]          # events, notifications (durable fan-out)
  └──→ [ClickHouse]     # analytics, dashboards (columnar)
           ↑
      consumed from Kafka
```

---

## 核心决策维度 / Key Decision Dimensions

**一致性需求 / Consistency**
- 金融/订单 → PostgreSQL (ACID, serializable isolation)
- 用户行为日志 → Kafka + eventually-consistent store
- 会话缓存 → Redis (丢了重新登录即可)

**读写比例 / Read/Write ratio**
- 读多写少 → 加 Redis 缓存 + CDN
- 写多读少 → Kafka 写入 + 批量读取
- 读写均衡 → Read Replicas (主从分离)

**查询模式 / Query patterns**
- 点查询 → Redis / KV store (O(1))
- 范围查询 → PostgreSQL B-tree index
- 全文搜索 → Elasticsearch (倒排索引)
- 时间序列聚合 → ClickHouse / TimescaleDB
- 地理空间 → PostGIS (GiST index)

---

## 为什么这样设计？/ Why This Design?

**多数据库共存不是过度设计，是专业化。** 每种存储都为特定访问模式优化：

- Redis 几乎所有操作 O(1)，但不支持复杂查询，持久化弱
- PostgreSQL MVCC 保证并发安全，但横向扩展有天花板
- ClickHouse 列式存储让聚合查询快 100x，但写入延迟高、不支持事务
- Kafka 保证消息持久化和顺序，但不是实时查询的工具

Using multiple databases isn't over-engineering — it's matching the engine to the access pattern. Each store does one thing extremely well.

---

## 别踩这个坑 / Common Mistakes

❌ **Redis 当主库** — 断电丢数据，没有 JOIN，运维复杂度暴增
❌ **什么都塞 PostgreSQL** — 全文搜索性能差，时序聚合慢，高并发写入锁竞争
❌ **过早引入 Kafka** — 简单场景用 PostgreSQL LISTEN/NOTIFY 或数据库轮询够了
❌ **忘记 Connection Pool** — 1 万用户并发但 DB max_connections=100，直接崩溃
❌ **缓存与数据库不一致** — 写数据库成功但缓存更新失败，导致脏读

✅ **原则**: Start with PostgreSQL + Redis. Add Elasticsearch/Kafka/ClickHouse only when you have a **measured bottleneck**, not a theoretical one.

---

## 选型速查表 / Quick Reference

```
需要 ACID 事务?          → PostgreSQL
需要 <1ms 读取?          → Redis
需要全文搜索?            → Elasticsearch
需要时序聚合分析?        → ClickHouse / TimescaleDB
需要异步解耦/扇出?       → Kafka
需要图关系查询?          → Neo4j
需要地理空间?            → PostGIS (PostgreSQL extension)
需要 schema-less?        → MongoDB (小心事务!)
```

---

## 📚 References
- https://aws.amazon.com/products/databases/ — AWS database selection guide
- https://www.postgresql.org/docs/current/indexes.html — PostgreSQL indexing
- https://kafka.apache.org/documentation/#gettingStarted — Kafka fundamentals
- https://clickhouse.com/docs/en/intro — ClickHouse intro

## 🧒 ELI5
厨房里有不同工具：冰箱放新鲜食物（Redis）、档案柜存重要文件（PostgreSQL）、公告板贴消息（Kafka）、统计日历（ClickHouse）、搜索引擎（Elasticsearch）。用对工具才能做好饭！

Different tools for different jobs: fridge for fresh stuff (Redis), filing cabinet for records (PostgreSQL), bulletin board for messages (Kafka), stats calendar (ClickHouse). Right tool = right outcome.
