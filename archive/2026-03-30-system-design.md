# 🏗️ 系统设计 Day 13 / System Design Day 13
## 微服务 vs 单体架构 / Microservices vs Monolith

**📊 Day 14/150 · NeetCode: 13/150 · SysDesign: 13/40 · Behavioral: 12/40 · Frontend: 13/50 · AI: 5/30**
**🔥 2-day streak!**

---

## 场景 / Scenario

想象你在一家快速成长的电商公司工作，最初你们用一个 Rails 单体应用处理所有逻辑——用户、商品、订单、支付、搜索。现在用户量增长了 100 倍，你们的 CEO 说"我们要做微服务！"。但真的值得吗？

*Imagine you're at a fast-growing e-commerce company. You started with a single Rails monolith handling everything — users, products, orders, payments, search. Now you're 100x bigger and the CEO says "we need microservices!" But is it really worth it?*

---

## 单体架构 / Monolith

```
┌─────────────────────────────────────────────────────┐
│                   Monolith App                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────────┐   │
│  │   Users   │  │ Products  │  │    Orders     │   │
│  │  Module   │  │  Module   │  │    Module     │   │
│  └─────┬─────┘  └─────┬─────┘  └──────┬────────┘   │
│        │               │               │             │
│  ┌─────▼───────────────▼───────────────▼────────┐   │
│  │              Shared Database                 │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
         ↑ 部署一次，所有功能都在一起
```

**优点 / Pros:**
- 开发简单，本地运行一个进程 / Simple to develop, one process locally
- 事务处理容易（ACID 保证）/ Easy transactions (ACID guarantees)
- 调试直接，日志集中 / Simple debugging, centralized logs
- 初期团队小时效率高 / High efficiency for small teams early on

**缺点 / Cons:**
- 扩展只能整体扩容 / Scaling requires scaling everything
- 一个 bug 可以拖垮整个系统 / One bug can take down the whole system
- 技术栈锁定 / Tech stack lock-in
- 大团队协作冲突多 / Large teams conflict on deployments

---

## 微服务架构 / Microservices

```
        ┌──────────┐
        │  Client  │
        └────┬─────┘
             ↓
     ┌───────────────┐
     │  API Gateway  │ ← 统一入口 / Single entry point
     └──┬────┬────┬──┘
        ↓    ↓    ↓
 ┌──────┐ ┌──────┐ ┌──────────┐ ┌──────────┐
 │ User │ │ Auth │ │ Product  │ │  Order   │
 │ Svc  │ │ Svc  │ │  Svc     │ │  Svc     │
 └──┬───┘ └──────┘ └────┬─────┘ └────┬─────┘
    ↓                    ↓            ↓
 ┌──────┐          ┌──────────┐ ┌──────────┐
 │Users │          │ Products │ │  Orders  │
 │  DB  │          │    DB    │ │    DB    │
 └──────┘          └──────────┘ └──────────┘
         ↑ 每个服务独立部署、独立数据库
```

**优点 / Pros:**
- 独立扩展，按需分配资源 / Independent scaling per service
- 技术异构，不同服务用不同语言 / Polyglot — different languages per service
- 故障隔离，一个服务挂不影响其他 / Fault isolation
- 团队独立部署，解耦 / Independent team deployments

**缺点 / Cons:**
- 分布式系统复杂性 / Distributed systems complexity
- 网络延迟、跨服务调用 / Network latency, cross-service calls
- 数据一致性难（没有跨服务事务）/ No cross-service ACID transactions
- 运维成本高（需要 K8s、Service Mesh 等）/ High ops overhead

---

## 关键权衡 / Key Tradeoffs

| 维度 / Dimension | 单体 / Monolith | 微服务 / Microservices |
|---|---|---|
| **复杂度 / Complexity** | 低 | 高 |
| **扩展性 / Scalability** | 整体扩展 | 按需扩展 |
| **部署速度 / Deploy speed** | 慢（整体重新部署）| 快（单服务部署）|
| **数据一致性 / Data consistency** | 强一致 | 最终一致 |
| **适合团队 / Team size** | < 20 工程师 | > 50 工程师 |
| **初期开发 / Early dev** | ✅ 快 | ❌ 慢（过早优化）|

**Martin Fowler 的建议：** 先做单体，等你真的遇到瓶颈了再拆。"Monolith First" 原则。

*Martin Fowler's advice: Start with a monolith, migrate to microservices only when you hit real bottlenecks. "Monolith First" principle.*

---

## 别踩这个坑 / Common Mistakes

❌ **坑 1: 过早微服务化**
Day 1 就搞微服务是「分布式单体」——一堆微服务共享同一个数据库，既有微服务的复杂性，又没有单体的简单性。

*Pitfall 1: Premature microservices. Day 1 microservices that share a database = "distributed monolith." You get all the complexity with none of the benefits.*

❌ **坑 2: 按技术分层而非业务能力分层**
不要按"前端服务/后端服务/DB服务"分，要按"用户服务/支付服务/搜索服务"分（领域驱动设计 DDD）。

*Pitfall 2: Splitting by tech layer instead of business capability. Don't split into "frontend/backend/DB" services — split by domain: users, payments, search (Domain-Driven Design).*

❌ **坑 3: 忽视分布式事务**
"用户下单 → 扣库存 → 扣余额"如果中间一步失败怎么办？需要 Saga 模式或两阶段提交，不是简单 DB transaction 能解决的。

*Pitfall 3: Ignoring distributed transactions. "Place order → deduct inventory → deduct balance" — what if one step fails? You need Saga pattern or 2PC, not a simple DB transaction.*

---

## 📚 References
- [Martin Fowler — Microservices Guide](https://martinfowler.com/articles/microservices.html)
- [Monolith First — Martin Fowler](https://martinfowler.com/bliki/MonolithFirst.html)
- [AWS — Microservices vs Monolithic](https://aws.amazon.com/compare/the-difference-between-monolithic-and-microservices-architecture/)

## 🧒 ELI5
单体架构就像一个全科医生诊所，一个医生搞定所有事，简单高效。微服务就像一家大医院，每个科室专注一件事，但你需要预约、挂号、各科室协调——更专业但也更复杂。

*Monolith = a solo doctor's clinic, one person handles everything — simple and efficient. Microservices = a big hospital with specialized departments — more powerful but you need appointments, referrals, and coordination between departments.*
