# 🏗️ 系统设计 / System Design — 数据库选型框架

*综合第7天（SQL vs NoSQL）、第21天（KV Store）、第39天（分布式缓存）、第52天（时序数据库）*

---

## 核心问题：该用哪种数据库？

Senior 级别面试必考：给你一个业务场景，你如何选型？没有万能答案，只有合适的权衡。

---

## 五类数据库对比

```
┌─────────────────┬──────────────┬─────────────┬──────────────┬─────────────┐
│                 │ Relational   │ Document    │ Key-Value    │ Time-Series │
│                 │ (Postgres)   │ (MongoDB)   │ (Redis)      │ (InfluxDB)  │
├─────────────────┼──────────────┼─────────────┼──────────────┼─────────────┤
│ 数据结构         │ 表/行/列      │ JSON 文档    │ hash/set/    │ 时间戳+标签  │
│                 │             │             │ sorted set   │             │
├─────────────────┼──────────────┼─────────────┼──────────────┼─────────────┤
│ 强项            │ ACID 事务     │ 灵活 schema  │ 极低延迟     │ 高写入吞吐   │
│                 │ 复杂 JOIN    │ 嵌套数据     │ 原子操作     │ 时间范围查询  │
├─────────────────┼──────────────┼─────────────┼──────────────┼─────────────┤
│ 弱项            │ 水平扩展难    │ 事务弱       │ 数据量受内存  │ 不支持 JOIN  │
│                 │ schema 变更  │ 一致性弱     │ 限制         │             │
├─────────────────┼──────────────┼─────────────┼──────────────┼─────────────┤
│ 典型场景        │ 电商、金融    │ 用户档案     │ Session、缓存 │ 监控指标     │
│                 │ ERP          │ CMS、目录   │ 排行榜       │ IoT、APM     │
└─────────────────┴──────────────┴─────────────┴──────────────┴─────────────┘
```

---

## 决策框架 (Decision Tree)

```
需要 ACID 多表事务？
  YES → 关系型数据库 (Postgres / MySQL)
  NO
    ↓
数据结构高度嵌套 / schema 变化快？
  YES → 文档型 (MongoDB / DynamoDB)
  NO
    ↓
需要极低延迟 / 读多写少 / 数据能放内存？
  YES → KV Store (Redis / Memcached)
  NO
    ↓
数据带时间戳 / 高频写入 / 范围聚合？
  YES → 时序数据库 (InfluxDB / TimescaleDB)
  NO → 列式存储 (Cassandra / BigTable) for large-scale analytics
```

---

## 实战举例：设计一个电商系统

| 业务模块 | 数据库 | 原因 |
|---------|--------|------|
| 用户账户 & 订单 | Postgres | 需要 ACID，ORDER JOIN USER |
| 产品目录 | MongoDB | schema 变化多，嵌套属性 |
| 购物车 / Session | Redis | 临时状态，毫秒响应 |
| 价格历史 / 埋点 | InfluxDB | 时序，高写入 |

---

## 别踩这个坑

❌ 用 MongoDB 存财务流水 → 缺乏 ACID，对账困难  
❌ 用 Redis 作为唯一存储 → 内存爆炸，持久化策略复杂  
❌ 用 Postgres 存 IoT 指标（每秒万条）→ 表膨胀，查询慢  
✅ 多数系统用混合存储：Postgres 主库 + Redis 缓存 + 时序补充

---

## 面试话术模板

> "I'd start with a relational DB for strong consistency. As we scale, I'd introduce Redis for hot-path caching and consider sharding the main DB or migrating read-heavy tables to a document store — but only when we hit a concrete pain point."

---

## 📚 References
- https://www.postgresql.org/docs/current/
- https://redis.io/docs/data-types/
- https://docs.influxdata.com/influxdb/v2/

## 🧒 ELI5
数据库就像不同的收纳工具。Postgres 是文件柜（有序、分类严谨）；MongoDB 是大箱子（什么都能扔）；Redis 是桌面（最近用的东西，随手就拿到）；InfluxDB 是日记本（按时间记录每件事）。装衣服不要用日记本，写日记不要用衣柜。
