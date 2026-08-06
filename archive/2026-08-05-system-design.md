# 🏗️ 系统设计 / System Design — Day 108 (Synthesis)

## 一次请求的解剖 / Anatomy of a Production Request: 10 Systems in 100ms

> 综合回顾 / Synthesis Review — Expert Level

当用户在手机上点击"发送"，接下来 100ms 内发生了什么？这是一个把我们过去几个月学到的所有系统设计知识串联起来的机会。

When a user taps "Send" on their phone, what happens in the next 100ms? This is your chance to connect every system design concept we've learned.

---

## 📍 完整请求链路 / The Complete Request Journey

```
User Phone
    │
    ▼
[1] DNS Resolution (Anycast → nearest PoP)
    │  ~5ms (cached) or ~50ms (cold)
    ▼
[2] CDN / Edge (Cloudflare, Fastly)
    │  Static assets served here. Cache-hit = done in <10ms.
    │  Cache-miss → forward to origin
    ▼
[3] Load Balancer (L4/L7, e.g. AWS ALB)
    │  Health checks, sticky sessions, weighted routing
    ▼
[4] API Gateway (Kong, AWS APIGW)
    │  Auth (JWT verify), rate limiting, request validation
    ▼
[5] Rate Limiter (Token Bucket / Sliding Window)
    │  Redis-backed. 429 if exceeded.
    ▼
[6] App Server (Kubernetes Pod)
    │  Business logic. Check cache first!
    ▼
[7] Cache (Redis / Memcached)
    │  Cache hit → return immediately (~1ms)
    │  Cache miss → query DB
    ▼
[8] Database (Primary + Read Replica)
    │  Read from replica, write to primary
    │  Indexed queries: ~5-20ms
    ▼
[9] Distributed Tracing (Jaeger / OpenTelemetry)
    │  trace_id propagated through ALL hops
    ▼
[10] Monitoring / Alerting (Datadog / Prometheus)
     Metrics: latency p50/p95/p99, error rate, saturation
```

---

## 🔗 各层关键设计决策 / Key Design Decisions at Each Layer

### 1. DNS + CDN
- **Anycast routing** → 用户被路由到最近的 PoP (Point of Presence)
- CDN 缓存静态资源 (HTML, JS, images)；API calls 通常不缓存
- **TTL 设置很重要**：太长→部署慢，太短→DNS 压力大

### 2. Load Balancer
- L4 (TCP level) vs L7 (HTTP level) — L7 更智能但开销更高
- **算法**：Round Robin, Least Connections, IP Hash (sticky sessions)
- **健康检查**：每 10s 一次，3次失败则摘除节点

### 3. API Gateway + Rate Limiter
- 将横切关注点 (auth, rate limit, logging) 从业务代码剥离
- Rate limiter 需要用 Redis 实现分布式限流，单机限流没有意义
- **为什么不在 LB 层做 rate limit？** → LB 无法识别用户身份

### 4. Cache 策略
- **Read-through**: App 层透明，缓存代为查 DB
- **Write-through**: 写 DB 同时写缓存，一致性好但写慢
- **Write-behind (Write-back)**: 先写缓存，异步写 DB，快但有丢失风险
- 今天最常用：**Cache-aside (Lazy loading)**

### 5. Database
- **主从分离**：写主库，读从库
- **连接池**：不要每次请求新建连接 (pgbouncer, HikariCP)
- **慢查询日志** → 找到未加索引的查询

---

## ⚡ 延迟预算 / Latency Budget (Target: <100ms p99)

| Layer | Budget | Optimization |
|-------|---------|-------------|
| DNS | 0ms (cached) | Long TTL for stable services |
| CDN | 5ms | Edge cache, HTTP/3 |
| LB + Gateway | 2ms | Keep it lightweight |
| Rate Limiter | 1ms | Redis pipelining |
| App Logic | 10ms | Avoid N+1 queries |
| Cache Hit | 1ms | Redis in same VPC |
| Cache Miss + DB | 30-50ms | Indexes, read replicas |
| **Total** | **~70ms** | **30ms buffer for tail latency** |

---

## 🔴 常见陷阱 / Common Architectural Mistakes

1. **跳过 CDN** → 把静态资源请求打到 origin，浪费带宽和计算
2. **单点 Redis** → 缓存挂了整个系统崩溃，要用 Redis Cluster 或 Sentinel
3. **在 app server 做 auth** → 每个 service 都要重新实现，应该在 API Gateway 统一处理
4. **不传递 trace_id** → 出了问题无法跨服务追踪
5. **忘记熔断器** → 下游服务超时会让 app server 线程耗尽 (thread pool exhaustion)

---

## 💡 面试中如何讲这个 / How to Present This in Interviews

Senior/Staff 级别面试官最欣赏的不是"你知道所有组件"，而是：
- **你知道为什么每层存在**（职责分离）
- **你能讨论权衡**（CDN 带来复杂性，但值得）
- **你关心延迟预算**（100ms 是用户感知的临界点）
- **你考虑故障模式**（每层挂掉会发生什么）

The key signal for senior+ interviews: can you reason about **which layer owns which concern** and **what breaks when each layer fails**?

---

## 📚 References
- https://www.cloudflare.com/learning/cdn/what-is-a-cdn/
- https://www.nginx.com/blog/introduction-to-microservices/
- https://aws.amazon.com/architecture/well-architected/

## 🧒 ELI5
想象你去麦当劳点汉堡：收银员（LB）分配任务→厨师检查食材架（Cache）→如果没有去仓库取（DB）→包装员验证订单（API Gateway）→监控员确保质量（Monitoring）。每个人各司其职，整个流程才能在 2 分钟内完成。

Imagine ordering at McDonald's: cashier (LB) routes your order → cook checks the ingredient rack (Cache) → if empty, fetches from storage (DB) → wrapper validates the order (API Gateway) → quality monitor checks everything (Monitoring). Everyone has one job — that's why it works fast.
