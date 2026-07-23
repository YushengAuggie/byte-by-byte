# 🏗️ 系统设计 / System Design — Day 98 (Synthesis)
**Expert Phase — Cross-Topic Synthesis**

---

## 综合对比 / Synthesis: 数据库选型决策框架
### When to Choose What — 8 DB Types Compared

你是系统设计面试中的候选人，面试官说："为我们设计一个需要存储用户配置、会话数据、内容推荐、时间序列指标、全文搜索和地理位置查询的平台。"这道题的核心不是某一个数据库——而是**多个数据库协同工作**。

---

## 决策矩阵 / Decision Matrix

```
需求 / Need              | 选型 / Choice          | 原因 / Why
-------------------------|------------------------|-------------------------------
用户配置、关系数据        | PostgreSQL (SQL)       | ACID, joins, structured
会话 / 缓存              | Redis                  | In-memory, TTL, O(1)
内容推荐、社交图谱        | Neo4j / DGraph         | Graph traversal, relationships
时间序列指标              | InfluxDB / TimescaleDB | Optimized for time-range scans
全文搜索                  | Elasticsearch          | Inverted index, ranking
地理位置                  | PostGIS / MongoDB Geo  | Geospatial indexes
非结构化文档              | MongoDB                | Flexible schema, JSON-native
大规模分析                | Redshift / BigQuery    | Columnar, OLAP
```

---

## 架构图 / Architecture

```
                    ┌────────────────────────────────────────────┐
                    │            API Gateway / BFF               │
                    └────────┬───────┬───────┬────────┬──────────┘
                             │       │       │        │
                    ┌────────▼──┐  ┌─▼────┐ │   ┌───▼──────────┐
                    │PostgreSQL │  │Redis │ │   │Elasticsearch  │
                    │(users,    │  │(cache│ │   │(search, logs) │
                    │ orders)   │  │ sess)│ │   └──────────────┘
                    └───────────┘  └──────┘ │
                                            │
                    ┌───────────────────┐   ▼
                    │   InfluxDB        │  Neo4j
                    │(metrics, timeseries│  (social graph,
                    │ monitoring)        │   recommendations)
                    └───────────────────┘
```

---

## 核心权衡 / Key Tradeoffs

**1. 一致性 vs 可用性**
- PostgreSQL: Strong consistency (ACID) → 适合金融、订单
- Redis: Eventual consistency (optional) → 适合缓存、会话
- Cassandra: Eventual by default → 适合写密集、全球分布

**2. 读 vs 写优化**
- Elasticsearch: 写入慢（index建立），读极快
- InfluxDB: 追加写极快，随机写差
- PostgreSQL: 均衡，靠索引调优

**3. Schema 灵活性 vs 查询能力**
- MongoDB: 无 schema，但 JOIN 痛苦
- PostgreSQL: Rigid schema，强查询
- 组合策略：核心关系 → SQL，扩展属性 → JSON column

---

## 面试中常被考的组合 / Classic Interview Combos

```
系统              | 主DB           | 辅助
-----------------|----------------|------------------
Twitter/X        | MySQL/Postgres  | Redis (timeline), Elasticsearch (search)
Uber             | MySQL           | Redis (location cache), PostGIS
Netflix          | Cassandra       | Elasticsearch (search), Redis (session)
Airbnb           | MySQL           | Elasticsearch (search), Redis (cache)
WhatsApp         | HBase/Cassandra | Redis (presence), MySQL (metadata)
```

**面试技巧 / Interview Tip:**
当面试官问"你会用什么数据库？"正确答案几乎永远是：
> "这取决于读/写比例、数据结构、一致性需求和查询模式。让我分析一下……"

然后用上面的框架逐一分析。

---

## 别踩这个坑 / Common Mistakes

- ❌ 默认所有东西用 PostgreSQL（"RDBMS first"思维）
- ❌ 把 Redis 当主数据库（内存有限，非持久化）
- ❌ 忘记考虑 data locality（地理分布 → 多区域复制）
- ✅ 先问清楚 QPS、数据量、一致性要求，再选型

---

## 📚 References
- https://www.postgresql.org/docs/current/index.html
- https://redis.io/docs/latest/
- https://www.elastic.co/guide/index.html
- https://docs.influxdata.com/influxdb/v2/

## 🧒 ELI5
就像家里的收纳：衣服放衣柜（结构化），零食随便堆一个箱子（非结构化），常用钥匙放门口（缓存），账单按日期归档（时间序列）。不同的东西放不同的地方，效率最高。
