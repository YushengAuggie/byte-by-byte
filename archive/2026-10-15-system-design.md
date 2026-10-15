# 🏗️ 系统设计 / System Design — Day 139 (Synthesis)
## 从单机到亿级：系统扩展的三阶段演进框架
## Three-Phase Scale-Out Playbook: From Single Server to Billions

> **综合回顾 / Synthesis:** 我们已覆盖 60 个系统设计主题。今天做一次大整合——把所有内容串成一个实战框架。
> We've covered 60 system design topics. Today we stitch them into one cohesive decision framework.

---

### 想象你在设计一家创业公司的后端...

你的产品从 0 到 1 再到 1 亿用户。每个阶段的"正确答案"截然不同。
Your product goes from 0 to 100M users. The "right answer" changes completely at each stage.

---

### 📐 三阶段架构演进

```
阶段 1: 0 → 10K 用户              阶段 2: 10K → 1M 用户
─────────────────────────          ────────────────────────────────────────
  [Client]                           [Client]
     │                                  │
  [Single Server]                    [Load Balancer]
     │                                /           \
  [DB (Postgres)]                [Server 1]   [Server 2]
                                    │                │
                              [Redis Cache]     [Read Replica]
                                    │
                              [Message Queue]
                                    │
                              [Worker Processes]

阶段 3: 1M → 100M+ 用户
──────────────────────────────────────────────────────
  [Client]
     │
  [CDN] ── static assets
     │
  [API Gateway + Rate Limiter]
     │
  [Load Balancer]
  /   |   \
[Service A] [Service B] [Service C]  ← Microservices (selective!)
     │           │           │
  [Cache]    [Cache]      [Cache]    ← per-service Redis
     │           │           │
  [DB Primary] [DB Shard 0..N] [NoSQL]
     │
  [Message Queue (Kafka)]
     │
  [Multi-Region Replica]
```

---

### 🔑 每阶段的关键决策 / Key Decisions Per Stage

**阶段 1 — 单体优先 (Monolith First)**
- 部署一个进程，Postgres 够用。Move fast. 不要过度设计。
- **何时引入缓存？** 数据库 CPU > 70% 或 P99 延迟 > 100ms。
- 教训：URL Shortener (Day 19)、Key-Value Store (Day 21) 都从这里开始。

**阶段 2 — 第一次分布式 (First Distribution)**
引入顺序：**缓存 → 读副本 → 消息队列 → CDN**（按 ROI 排序）

| 问题 | 解法 | 我们学过 |
|------|------|----------|
| DB 读压力 | Read Replica + Redis Cache | Day 6, Day 8 |
| 请求高峰 | Message Queue (async) | Day 13 |
| 静态资源 | CDN | Day 64 |
| 单点故障 | Load Balancer | Day 4 |

**阶段 3 — 真正分布式 (Full Distribution)**
- **Microservices：只拆分真正需要独立扩展的服务**（别为了拆而拆）
- 数据库：先分库分表（Sharding, Day 9），NoSQL 用于高写吞吐
- 全局：Consistent Hashing (Day 11) + CAP 理论 (Day 12) 是核心武器
- 跨区域：Multi-Region Active-Active (Day 54) 需要最终一致性设计

---

### ⚡ 为什么这样设计？核心权衡

**过早微服务化是最常见的错误：**
- ✅ 微服务优势：独立部署、独立扩展、技术多样性
- ❌ 微服务代价：网络延迟、分布式事务、运维复杂度 (Day 14)
- 🎯 规则：**单体 → 服务化，当团队 > 10 人或流量差异 > 10x**

**一致性 vs 可用性（CAP）的实战选择：**
- 支付系统 (Day 38) → CP（宁可拒绝也不能双扣款）
- 推荐系统 (Day 46) → AP（短暂的数据不一致无所谓）
- 聊天系统 (Day 28) → AP + 最终一致（消息送达比绝对顺序重要）

---

### 🚫 别踩这个坑

| 坑 | 后果 | 正确做法 |
|----|------|----------|
| 过早引入 Kafka | 运维地狱，延迟上升 | 先用 Postgres + worker 表 |
| 缓存没有失效策略 | 数据脏了用户投诉 | Write-through 或 TTL |
| 全局唯一 ID 用自增 | 分布式下冲突 | Snowflake / ULID (Day 22) |
| 微服务共用 DB | 逻辑耦合没减少 | 每个服务独立 DB |

---

### 📚 References
- [System Design Primer — Scale from Zero to Millions](https://github.com/donnemartin/system-design-primer#how-to-scale-a-system)
- [Google SRE Book — Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Martin Fowler — Strangler Fig Pattern](https://martinfowler.com/bliki/StranglerFigApplication.html)

### 🧒 ELI5
就像搬家：你先住一间屋（单体）→ 装修加一个储物间（加缓存）→ 买了个套房（微服务）。但别刚入职第一天就买豪华别墅。
Like moving house: start in one room (monolith) → add a storage closet (cache) → get a bigger apartment (microservices). Don't buy a mansion on day one.
