# 🏗️ 系统设计 Day 15 / System Design Day 15

## Rate Limiting & Throttling — 保护你的 API / Protecting Your API

---

### 🌏 真实场景 / Real-World Scenario

想象你在 Twitter（X）做工程师。某个下午，一个爬虫脚本突然对你的搜索 API 发起每秒 10,000 次请求，导致数据库崩溃，所有用户无法刷推。

你需要一个**限流系统**——在不影响正常用户的前提下，拒绝滥用流量。

Imagine you're an engineer at Twitter (X). One afternoon, a scraper script hammers your search API at 10,000 requests/second, crashing the database for all users. You need a **rate limiting system** — one that blocks abuse without affecting normal users.

---

### 📐 架构图 / Architecture Diagram

```
                          ┌─────────────────────┐
   Client Request ───────►│   API Gateway /      │
                          │   Rate Limiter       │
                          │                      │
                          │  1. Identify client  │
                          │     (IP / User ID /  │
                          │      API Key)        │
                          │  2. Check counter    │
                          │     in Redis         │
                          │  3. Allow or Block   │
                          └──────────┬───────────┘
                                     │ Allowed
                          ┌──────────▼───────────┐
                          │   Backend Service     │
                          └──────────────────────┘

Redis Counter Example (Sliding Window):
  key: "ratelimit:user123:2026-04-03T08"
  value: 47  (requests this hour)
  TTL: 3600s
```

---

### ⚙️ 主要算法 / Key Algorithms

| 算法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| **Token Bucket** | 令牌以固定速率补充，请求消耗令牌 | 允许突发流量 | 实现稍复杂 |
| **Leaky Bucket** | 请求以固定速率流出（队列） | 输出极平滑 | 不允许突发 |
| **Fixed Window** | 每个时间窗重置计数器 | 最简单 | 边界突破问题 |
| **Sliding Window** | 精确追踪过去 N 秒 | 最精确 | 内存占用高 |

**推荐：Token Bucket（令牌桶）** — 生产中最常用，兼顾突发和平均速率。

---

### 🔑 关键权衡 / Key Tradeoffs

**为什么用 Redis 而不是本地内存？/ Why Redis, not local memory?**

- 多台服务器共享同一计数器 → 分布式限流
- 原子操作（INCR + EXPIRE）避免竞态条件
- Redis 单线程模型保证计数器一致性

**限流粒度选择 / Granularity choices:**
- **Per IP** — 防爬虫，但误伤 NAT 用户（办公室）
- **Per User ID** — 最精确，需要认证
- **Per API Key** — B2B 场景首选
- **Per Endpoint** — 写接口比读接口更严格

---

### ❌ 常见错误 / Common Mistakes

**坑 1：Fixed Window 边界问题**
```
Window 1 (0:00-1:00): 99 requests ← allowed
Window 2 (1:00-2:00): 99 requests ← allowed
But at 0:59 + 1:01 = 198 requests in 2 seconds! ← spike!
```
→ 用 Sliding Window Log 或 Sliding Window Counter 解决

**坑 2：忘记 HTTP 响应头**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1743685200
Retry-After: 3600  ← 429 时必须包含
```
客户端需要知道何时重试！

**坑 3：硬拒绝 vs 降级**
不要直接返回 `503`，试试 queue、degrade（返回缓存数据）或 soft-limit（超出后降速）。

---

### 📚 References

- [System Design Interview — Rate Limiting (ByteByteGo)](https://blog.bytebytego.com/p/rate-limiting-fundamentals)
- [Cloudflare Rate Limiting Docs](https://developers.cloudflare.com/waf/rate-limiting-rules/)
- [Redis INCR for Rate Limiting](https://redis.io/docs/manual/patterns/rate-limiting/)

---

### 🧒 ELI5

就像游乐场的入口检票员：每个小时只放 100 个人进去。人满了就让你在外面等，而不是把游乐场挤爆。

It's like a bouncer at a club: "100 people per hour max." When it's full, you wait outside — the club doesn't collapse.
