🏗️ **系统设计 / System Design** — Synthesis: Designing a Multi-Tenant SaaS Control Plane

想象你在 Snowflake / Databricks / Vercel 这类公司做架构师。你需要设计一个 **多租户控制平面 (control plane)**：成千上万的客户共享底层基础设施，但每个客户的数据、配额、密钥都严格隔离。这个设计综合了我们之前覆盖过的 **API Gateway、Rate Limiting、Secrets Vault、Feature Flags、Multi-Region Active-Active、Distributed Tracing**。

Imagine you're an architect at Snowflake / Databricks / Vercel. You need to design a **multi-tenant control plane**: thousands of customers share underlying infrastructure, but each tenant's data, quotas, and secrets are strictly isolated. This synthesizes previously covered topics: **API Gateway, Rate Limiting, Secrets Vault, Feature Flags, Multi-Region Active-Active, Distributed Tracing**.

---

### 架构图 / ASCII Architecture

```
                 ┌───────────────────────────────────────────┐
   Customer ────▶│  Global API Gateway (CloudFront/Cloudflare)│
   (tenant_id)   │  - JWT auth, mTLS, WAF, DDoS              │
                 └──────────────┬────────────────────────────┘
                                │ x-tenant-id header
                 ┌──────────────▼────────────────────────────┐
                 │ Tenant Router (sharded by hash(tenant_id)) │
                 │  - Rate limit (token bucket per tenant)    │
                 │  - Feature flag lookup (LaunchDarkly)      │
                 │  - OpenTelemetry trace id injection        │
                 └─────┬──────────────────────────┬──────────┘
                       │                          │
             ┌─────────▼─────────┐      ┌────────▼─────────┐
             │ Cell US-WEST-2    │      │ Cell EU-WEST-1   │
             │ (Shard 0..499)    │      │ (Shard 500..999) │
             │                   │      │                  │
             │ ┌─ control svc ─┐ │      │ ┌─ control svc ─┐│
             │ │ ┌─ Postgres ─┐│ │      │ │ ┌─ Postgres ─┐││
             │ │ │tenant_db_N ││ │      │ │ │tenant_db_M │││
             │ │ └────────────┘│ │      │ │ └────────────┘││
             │ └───────────────┘ │      │ └───────────────┘│
             │  ┌─ Vault (KMS) ─┐│      │  ┌─ Vault (KMS)─┐│
             │  │ per-tenant key││      │  │ per-tenant key││
             │  └───────────────┘│      │  └───────────────┘│
             └───────────────────┘      └──────────────────┘
                       │                          │
                       └────── Global Metadata ───┘
                              (CockroachDB / Spanner, strong consistency
                               for tenant → cell mapping)
```

---

### 关键权衡 / Key Tradeoffs

| 决策 Decision | 为什么 Why |
|---|---|
| **Cell-based (shuffle sharding)** | Blast radius 隔离：一个 cell 挂掉只影响部分租户。AWS、Slack 都用。参考 Shuffle Sharding 论文。|
| **Pool model + Silo for enterprise** | 小客户共享 Postgres schema (cheap)，大客户独立数据库 (security/compliance)。|
| **Global metadata ≠ Global data** | tenant→cell mapping 用强一致存储；业务数据永远留在 cell 内，不跨区同步。|
| **Per-tenant KMS data key** | Envelope encryption：主密钥在 Vault，每个 tenant 自己的 DEK。关键 compliance 诉求。|
| **Rate limit at edge, not DB** | 恶意租户的 abusive traffic 不能挤占共享的 DB 连接池。|

---

### 别踩这个坑 / Common Mistakes

1. **"noisy neighbor" via connection pool** — 一个租户的慢查询吃光共享 pgbouncer 连接。解法：per-tenant pool quotas + pg_stat_activity 监控 + 自动 kill 长查询。
2. **Tenant ID 只在 app 层 enforce** — SQL injection 或代码 bug 一旦漏 `WHERE tenant_id=?`，所有租户数据暴露。必须用 **Postgres Row-Level Security (RLS)** 做兜底。
3. **跨 cell 的 "backfill" 作业变成单点** — ETL 一旦全局运行就违背了 cell 隔离。每个 cell 独立跑。
4. **Feature flag per-tenant 爆炸** — 10k 租户 × 100 flags = 1M flag evaluations/s。要本地缓存 + bulk evaluation API。
5. **Trace sampling 全局 1%** — 大租户看不到自己的问题。改成 **per-tenant sampling rate**，关键租户 100% 采样。

---

### 📚 References
- AWS Shuffle Sharding: https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/
- Multi-tenant SaaS data isolation (AWS): https://aws.amazon.com/blogs/apn/multi-tenant-saas-storage-strategies/
- Postgres Row-Level Security: https://www.postgresql.org/docs/current/ddl-rowsecurity.html

### 🧒 ELI5
想象一座大楼有 1000 个租户。你不能让他们共用一个大门（会堵），也不给每人盖一栋楼（太贵）。所以把楼分成"单元"——每个单元 50 户，有自己的电梯、水表、保险箱。一个单元出事（停电）只影响那 50 户。门口有保安（gateway）看证件（tenant_id），决定你走哪部电梯。这就是 cell-based multi-tenancy。
