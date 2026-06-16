# 🏗️ 系统设计 / System Design — Day 67
**主题 / Topic:** Design a Rate Limiter as a Service
**难度 / Difficulty:** Advanced | **阶段 / Phase:** Expert
**预计阅读 / Read time:** ~3 min

---

## 🏗️ 系统设计 / System Design

**设计一个限流服务 / Design a Rate Limiter as a Service**

---

### 场景 / Scenario

想象你在 Stripe 基础设施团队。每秒有数百万个 API 请求打到你们的系统，客户的代码 bug、恶意爬虫、或者流量突增随时可能压垮下游服务。你需要设计一个分布式限流服务，支持多种算法、多级限流（按用户、按 IP、按 API key），且延迟必须在 1ms 以内。

*Imagine you're on Stripe's infrastructure team. Millions of API requests hit your system every second — buggy client code, malicious scrapers, and traffic spikes can take down downstream services at any moment. Design a distributed rate limiter service with multiple algorithms, multi-level limiting (by user, IP, API key), and sub-1ms latency.*

---

### 🏛️ 架构图 / Architecture Diagram

```
                    ┌─────────────────────────────────┐
                    │          API Gateway              │
                    │   (Nginx / Envoy / Kong)          │
                    └──────────────┬──────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │  Rate Limiter      │
                         │  Sidecar / SDK     │
                         │                   │
                         │  1. Check limit    │
                         │  2. Increment ctr  │
                         │  3. Return allow/  │
                         │     deny + headers │
                         └────────┬──────────┘
                      ┌───────────┼───────────┐
                      │           │           │
              ┌───────▼──┐  ┌─────▼────┐ ┌───▼──────┐
              │  Redis   │  │  Redis   │ │  Redis   │
              │ Cluster  │  │ Cluster  │ │ Cluster  │
              │ (Shard1) │  │ (Shard2) │ │ (Shard3) │
              └──────────┘  └──────────┘ └──────────┘
                      │           │           │
              ┌───────▼───────────▼───────────▼───────┐
              │         Config Service                  │
              │  (limits per API key / IP / user)       │
              │  Stored in DB, cached in Redis          │
              └─────────────────────────────────────────┘
```

---

### ⚙️ 核心算法对比 / Algorithm Comparison

**四种主流限流算法 / Four main algorithms:**

| 算法 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Token Bucket** 令牌桶 | 允许突发流量 | 实现稍复杂 | API 限流（最常用）|
| **Leaky Bucket** 漏桶 | 平滑输出 | 不允许突发 | 流媒体、网络 |
| **Fixed Window** 固定窗口 | 简单，O(1) | 边界突发问题 | 简单场景 |
| **Sliding Window Log** 滑动日志 | 精确 | 内存占用大 | 精确计费 |
| **Sliding Window Counter** 滑动计数 | 近似精确+高效 | 有误差 | 生产推荐 ✅ |

**Redis 实现 — 滑动窗口计数 / Redis Sliding Window Counter:**

```python
import redis
import time

r = redis.Redis()

def is_allowed(key: str, limit: int, window_seconds: int) -> bool:
    now = time.time()
    window_start = now - window_seconds
    
    pipe = r.pipeline()
    # Remove old entries outside the window
    pipe.zremrangebyscore(key, 0, window_start)
    # Add current request
    pipe.zadd(key, {str(now): now})
    # Count requests in window
    pipe.zcard(key)
    # Set expiry to avoid memory leak
    pipe.expire(key, window_seconds + 1)
    results = pipe.execute()
    
    count = results[2]
    return count <= limit

# Usage
key = f"rate_limit:user:{user_id}:api_key:{api_key}"
if not is_allowed(key, limit=100, window_seconds=60):
    return 429, {"Retry-After": 60}
```

---

### ⚖️ 关键权衡 / Key Tradeoffs

**1. 本地缓存 vs 完全依赖 Redis**
- 方案A：每次请求都查 Redis → 精确，但 +0.5-1ms 延迟
- 方案B：本地缓存 + Redis 异步同步 → 快，但允许小幅超限（~1-5%）
- **生产选择：** 方案B，通过软限制 + 硬限制双层实现（本地 soft limit 95%，Redis hard limit 100%）

**2. 分布式 Race Condition**
- 问题：多个节点同时读写同一个计数器可能超限
- 解决：Redis Lua 脚本原子操作（EVAL），或用 Redis INCR + EXPIRE 组合

**3. 多维度限流优先级**
```
API Key Level  → 10,000 req/min
└── User Level → 1,000 req/min
    └── IP Level → 100 req/min
```
按最严格的维度拒绝，返回对应的 `X-RateLimit-*` headers。

---

### ❌ 常见坑 / Common Mistakes

1. **固定窗口的边界突发**：如果窗口 0:59 来 100 次，1:01 再来 100 次，两秒内实际 200 次但都算合法。用滑动窗口解决。
2. **没有降级机制**：Redis 挂了怎么办？应该有 fail-open（放行）vs fail-closed（拒绝）的配置，通常选 fail-open 避免影响业务。
3. **忘记返回标准 headers**：`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`

---

### 📚 深入阅读 / References

1. [System Design: Rate Limiter — Alex Xu DDIA-style](https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter)
2. [Redis Rate Limiting Patterns](https://redis.io/learn/develop/dotnet/aspnetcore/rate-limiting/sliding-window)
3. [Stripe's Rate Limiting Approach](https://stripe.com/blog/rate-limiters)

---

### 🧒 ELI5

*限流就像超市收银台排队：每分钟只能结 100 个人，超了就让你等一会儿，不是不让你来，只是让你稍等。*

*Rate limiting is like a checkout line: only 100 people per minute, extras just wait — you're not banned, just slowed down.*
