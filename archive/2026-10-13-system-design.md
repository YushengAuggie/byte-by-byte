🏗️ **系统设计 / System Design** — Synthesis: Multi-Tenancy 架构模式对比 / Multi-Tenancy Architecture Patterns

> 📊 NeetCode: 107/150 · SysDesign: 60/60 ✅ · Behavioral: 60/60 ✅ · Python Craft: 50/50 ✅ · AI: 30/30 ✅
> 🔥 Day 138 · Expert phase · 综合复盘模式 / Synthesis mode

---

### 场景 / Scenario

想象你在设计一个 B2B SaaS 产品（比如 Notion、Linear、Datadog）：你的用户是**公司**，每家公司有自己的员工、数据、配置。关键问题：**所有租户共享一套基础设施，还是各自隔离？**

Imagine you're building a B2B SaaS product (Notion, Linear, Datadog): each customer is a company with isolated users, data, and config. The question: **share infra across tenants, or isolate per tenant?**

这是一个**跨越数据库、缓存、队列、权限、合规**的综合决策，不是一个"选 A 或 B"的问题。

---

### 三种主流模式对比

```
Pattern A: Shared Everything (池化 / Pool)
┌──────────────────────────────────────────────┐
│  App Servers (shared)                        │
│         ↓   tenant_id in every query         │
│  ┌────────────────────────────────────────┐  │
│  │ Single DB:                             │  │
│  │   users (tenant_id, user_id, ...)      │  │
│  │   docs  (tenant_id, doc_id,  ...)      │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
  ✅ Cheapest · ❌ Noisy-neighbor · ❌ Hard compliance

Pattern B: Shared App, Isolated DB (桥接 / Bridge)
┌──────────────────────────────────────────────┐
│  App Servers (shared)                        │
│         ↓    Router: tenant → shard          │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐          │
│  │ DB1 │  │ DB2 │  │ DB3 │  │ DBn │          │
│  └─────┘  └─────┘  └─────┘  └─────┘          │
│  (tenant per DB, or sharded by tenant_id)    │
└──────────────────────────────────────────────┘
  ✅ Blast-radius bounded · ✅ Per-tenant backup
  ❌ Schema migrations fan out

Pattern C: Silo (独栋 / Dedicated)
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Tenant A    │  │ Tenant B    │  │ Tenant C    │
│  App + DB   │  │  App + DB   │  │  App + DB   │
│  + Cache    │  │  + Cache    │  │  + Cache    │
└─────────────┘  └─────────────┘  └─────────────┘
  ✅ Strongest isolation / compliance (HIPAA, SOC2 strict)
  ❌ Ops cost O(N tenants) · Deploys are chaos
```

---

### 关键权衡 / Key Tradeoffs

| 维度 | Pool | Bridge | Silo |
|---|---|---|---|
| **Cost / tenant** | 💰 lowest | 💰💰 medium | 💰💰💰 highest |
| **Noisy neighbor** | ⚠️ high | ⚠️ medium | ✅ none |
| **Blast radius** | 全部挂 | one shard | one tenant |
| **Compliance** | 难 | 中等 | 容易 |
| **Schema change** | 1 次 | N shards | N stacks |
| **典型客户** | SMB | Mid-market | Enterprise |

**现实架构往往是混合的：** 免费/小客户 → Pool；中型客户 → 共享 Bridge shard；大企业客户 → Silo。Snowflake、Databricks、Confluent Cloud 都是这个套路。

**Real stacks are hybrid:** free/SMB on Pool, mid-market on Bridge shards, enterprise on Silo. Snowflake, Databricks, Confluent Cloud all do this.

---

### 为什么这样设计？

1. **Row-Level Security 不够。** `WHERE tenant_id = ?` 一旦漏写就是数据泄露。生产系统应该在**连接池层或 ORM 中间件层**强制注入（如 Postgres RLS、SQLAlchemy session-level filter）。
2. **缓存键必须带 tenant_id。** `cache.get("user:123")` 会跨租户串数据，正确写法 `cache.get(f"t:{tenant_id}:user:123")`。
3. **队列任务要携带 tenant 上下文。** Celery/SQS 任务反序列化后要能恢复 tenant，否则后台任务串数据比前台更难查。
4. **Noisy neighbor 用 token bucket per tenant** 限流（见 Day 17/67 的 Rate Limiter）。
5. **可观测性要按 tenant 切片**：Datadog tags, Prometheus labels — 否则一个租户出问题你看不出。

---

### ❌ Common mistakes

1. **把 tenant_id 当"加一个列"的事情。** 它应该是**索引的最左前缀**，否则大租户的查询会扫全表。
2. **假设 Pool → Silo 迁移简单。** 实际上数据搬迁 + 外键 + 跨租户引用（分析、admin）会反咬。设计 day 1 就要想迁移路径。
3. **把 "tenant" 和 "organization" 和 "workspace" 混淆。** Slack 一个用户在多个 workspace。模型应该是 `User ↔ Membership ↔ Tenant`，不是 `User → tenant_id`。
4. **忽略"god mode"用户。** 内部 support/admin 需要跨租户访问 — 必须审计日志 + 强制理由字段。

---

### 📚 References

- AWS SaaS Factory — Multi-tenant SaaS architectures: https://aws.amazon.com/partners/programs/saas-factory/tenant-isolation/
- Microsoft — Multitenant architecture patterns: https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/overview
- PostgreSQL Row Level Security: https://www.postgresql.org/docs/current/ddl-rowsecurity.html

### 🧒 ELI5

想象一座公寓楼。**Pool** = 所有人睡一张大床（便宜但乱）。**Bridge** = 每人一间房共享厨房（平衡）。**Silo** = 每人一栋别墅（贵但安全）。SaaS 公司通常"小客户住宿舍、大客户住别墅"。
