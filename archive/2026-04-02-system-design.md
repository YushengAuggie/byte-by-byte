# 🏗️ 系统设计 Day 14 / System Design Day 14
## API Gateway & Service Mesh

---

### 🌍 真实场景 / Real-World Scenario

想象你在优步工作，系统里有 200 个微服务：乘客服务、司机服务、定价服务、路线服务、支付服务……

每个客户端（iOS App、Android App、Web 前端、第三方合作伙伴）直接调用每个服务？**噩梦开始了。**

这就是为什么优步、Netflix、Amazon 都在用 **API Gateway + Service Mesh** 这两层抽象。

---

Imagine you're at Uber with 200 microservices: rider, driver, pricing, routing, payments...

Every client (iOS, Android, web, partners) calling each service directly? **Nightmare begins.**

This is why Uber, Netflix, and Amazon all use **API Gateway + Service Mesh** — two layers of abstraction.

---

### 🏛️ ASCII 架构图

```
外部流量 / External Traffic
         │
         ▼
┌─────────────────────┐
│    API Gateway      │  ← 统一入口 / Single Entry Point
│  (Kong/AWS API GW)  │    认证、限流、路由、日志
│                     │    Auth, Rate Limit, Route, Log
└────────┬────────────┘
         │ 内部流量 / Internal Traffic
         ▼
┌─────────────────────────────────────────┐
│           Service Mesh (Istio/Envoy)    │
│                                         │
│  ┌──────────┐    ┌──────────┐          │
│  │Service A │◄──►│Service B │          │
│  │[sidecar] │    │[sidecar] │          │
│  └──────────┘    └──────────┘          │
│         ↕               ↕              │
│  ┌──────────┐    ┌──────────┐          │
│  │Service C │◄──►│Service D │          │
│  │[sidecar] │    │[sidecar] │          │
│  └──────────┘    └──────────┘          │
│                                         │
│  自动 mTLS、熔断、重试、可观测性        │
│  Auto mTLS, Circuit Break, Retry, Obs  │
└─────────────────────────────────────────┘
```

---

### 🔍 核心概念 / Core Concepts

#### API Gateway — 对外的门卫
**做什么 / What it does:**
- ✅ 认证鉴权 (JWT/OAuth2)
- ✅ 速率限制 (Rate Limiting) — 防刷
- ✅ 请求路由 — `/api/v1/users` → User Service
- ✅ 协议转换 — REST → gRPC
- ✅ 请求聚合 — 一次请求，内部调 3 个服务
- ✅ SSL 终止 (TLS Termination)

**常见产品 / Products:** Kong, AWS API Gateway, Nginx, Envoy, Traefik

#### Service Mesh — 对内的神经系统
**做什么 / What it does:**
- ✅ 服务间 mTLS 加密（零信任网络）
- ✅ 熔断器 (Circuit Breaker) — 防雪崩
- ✅ 自动重试 + 超时
- ✅ 流量管理 (Canary, A/B Test)
- ✅ 分布式追踪 (Tracing)
- ✅ 服务发现 (Service Discovery)

**实现方式:** Sidecar 代理（每个服务旁边注入一个 Envoy 代理）
**常见产品 / Products:** Istio, Linkerd, Consul Connect

---

### ⚖️ 关键权衡 / Key Tradeoffs

| 方案 | 优点 | 缺点 |
|------|------|------|
| API Gateway 独立 | 简单，运维成本低 | 服务间通信无管控 |
| Service Mesh 独立 | 内部流量全覆盖 | 复杂度高，sidecar 开销 |
| 两者结合 ✅ | 完整的流量控制 | 需要专门的平台团队维护 |

**为什么这样设计？/ Why this design?**

API Gateway 和 Service Mesh 解决**不同层面**的问题：
- Gateway = **南北流量**（外→内）
- Service Mesh = **东西流量**（内→内）

用一个工具同时管两种流量会导致职责不清、配置混乱。

---

### ⚠️ 常见踩坑 / Common Mistakes

```
❌ 把所有业务逻辑放在 API Gateway 里
   → Gateway 应该是"哑路由"，不应该懂业务

❌ 在没有可观测性的情况下上 Service Mesh
   → Mesh 的价值在于追踪和监控，没有这些等于白上

❌ 用 Service Mesh 替代 API Gateway
   → Mesh 不做外部认证和速率限制

❌ 每个团队各自搭 Gateway
   → 应该是全公司统一，否则安全策略碎片化
```

---

### 📚 References

- [Kong API Gateway Docs](https://docs.konghq.com/gateway/latest/) — 主流开源 API Gateway
- [Istio Architecture Overview](https://istio.io/latest/docs/ops/deployment/architecture/) — Service Mesh 权威文档
- [What is a Service Mesh? — CNCF](https://glossary.cncf.io/service-mesh/) — 清晰的概念解释

---

### 🧒 ELI5 (像我5岁一样解释)

**中文：**
想象一个大型游乐园。API Gateway 是大门口的保安，检查你的票、告诉你哪个游乐设施在哪里。Service Mesh 是园区内部的通信系统——每个游乐设施之间如何协调、出故障时怎么绕路。一个管进门，一个管园内。

**English:**
Imagine a big theme park. The API Gateway is the security guard at the main entrance — checks your ticket, tells you where things are. The Service Mesh is the internal walkie-talkie system between rides — how they coordinate, what happens when one breaks down. One manages getting IN, the other manages moving AROUND.
