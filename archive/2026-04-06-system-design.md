🏗️ **系统设计 Day 16 / System Design Day 16**

### 场景 / Scenario
想象你在设计一个公共 API（比如 Twitter API 或 OpenAI API）。如果某个用户或恶意脚本在一秒内发送了 10,000 个请求，你的服务器可能会崩溃，其他正常用户也会受到影响。你需要一个“限流器”（Rate Limiter）来控制每个用户在特定时间内的请求数量。
*Imagine you are designing a public API (like Twitter API or OpenAI API). If a user or malicious script sends 10,000 requests in one second, your server might crash, affecting other legitimate users. You need a "Rate Limiter" to control the number of requests each user can make within a specific time window.*

### 架构图 / Architecture Diagram
```text
[ Client ] 
    │ (1) Request
    ▼
[ API Gateway / Load Balancer ]
    │ (2) Check Rate Limit
    ├──► [ Rate Limiter Cache (Redis) ]
    │      ◄── (3) Allow / Deny
    ▼
(4) If Allow: [ Backend API Servers ]
(4) If Deny:  Return 429 Too Many Requests
```

### 核心权衡 / Key Tradeoffs
**为什么这样设计？ / Why design it this way?**
1. **Where to put it? (放在哪里？)**: 通常放在 API Gateway（网关），而不是后端应用服务器。这样可以在流量到达核心业务逻辑之前将其拦截，节省资源。
2. **Storage (存储)**: 使用像 Redis 这样的内存缓存（In-memory Cache），而不是关系型数据库。因为限流需要极低的延迟（Low Latency），并且 Redis 支持原子操作（如 `INCR` 和 `EXPIRE`）。
3. **Algorithms (算法选择)**:
   - **Token Bucket (令牌桶)**: 最常用（Stripe, Amazon 使用）。允许一定程度的突发流量（Burst traffic）。
   - **Sliding Window (滑动窗口)**: 更精确，但内存占用稍高（Cloudflare 使用）。

### 常见误区 / Common Mistakes
- ❌ **使用单机内存 (Using local memory in a distributed system)**: 如果你有 5 台网关服务器，每台自己记录限流，那么用户总共可以发送 5 倍的请求。必须使用集中式缓存（如 Redis）。
- ❌ **同步阻塞请求 (Synchronous blocking)**: 检查限流的过程必须极快，否则限流器本身会成为性能瓶颈。

### 📚 延伸阅读 / References
- [Stripe: Rate Limiters and how they work](https://stripe.com/blog/rate-limiters)
- [Cloudflare: How we built rate limiting](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
- [ByteByteGo: Rate Limiting Fundamentals](https://blog.bytebytego.com/p/rate-limiting-fundamentals)

### 🧒 ELI5 (Explain Like I'm 5)
限流器就像游乐园的检票员。如果你买的是“每小时只能玩 3 次”的票，检票员会记录你玩的次数。如果你这小时已经玩了 3 次还想玩，检票员会让你在旁边等（返回 429 错误），直到下一个小时重新开始。
*A rate limiter is like a ticket checker at an amusement park. If your ticket says "3 rides per hour", the checker tallies your rides. If you try to ride a 4th time in that hour, they tell you to wait (returning a 429 error) until the next hour starts.*