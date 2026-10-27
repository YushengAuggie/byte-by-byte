# 🏗️ 系统设计 / System Design — Expert Synthesis Day 143

**高可用三角：限流 + 缓存 + 一致性 — 综合实战**
**The HA Triangle: Rate Limiting + Caching + Consistency — Expert Synthesis**

---

## 想象你是首席架构师 / Imagine You're the Principal Architect

你的 VP 说："我们 Black Friday 要扛 50x 流量，不能挂。"

你脑海里立刻出现三个武器：**限流、缓存、一致性策略**。但真正的挑战不是每个独立用，而是**三者如何协同，又如何相互冲突**。

Your VP says: "We can't go down on Black Friday — expect 50x traffic." Your three weapons: rate limiting, caching, and consistency. The real challenge is how they interact — and when they fight each other.

---

## ASCII 架构图

```
Client
  │
  ▼
[CDN / Edge Cache]  ← 静态资源 + HTML Shell
  │
  ▼
[API Gateway]
  ├─ Rate Limiter (Token Bucket / Sliding Window)
  └─ Auth / JWT verify
       │
       ▼
  [Application Layer]
       ├─ Redis Cache (read-through)  ← 热点数据，TTL 5-60s
       └─ DB (PostgreSQL / DynamoDB)
            ├─ Read Replica ← 分流读流量
            └─ Write Primary ← 强一致写
```

---

## 三者协同：理想与现实 / The Ideal vs Reality

**限流（Rate Limiting）→ 保护后端**
- Token Bucket：允许短时 burst，适合 API
- Sliding Window：更公平，适合 per-user 限流
- ⚠️ 陷阱：分布式限流需要用 Redis Lua 脚本做原子操作，否则多实例会超限

**缓存（Caching）→ 降低延迟和 DB 压力**
- Cache-aside（Lazy Load）：cache miss 才查 DB，简单但首次慢
- Write-through：写 DB 同时更新缓存，一致性好但写慢
- ⚠️ 陷阱：Cache stampede — 热点 key 过期时几千请求同时穿透 → 用 mutex lock + 概率过期（jitter TTL）

**一致性（Consistency）→ 正确性保证**
- 读己所写（Read Your Writes）：90% 业务只需要这个，不需要全局强一致
- 最终一致（Eventual）：评论、点赞、浏览量 — 脏读无所谓
- 线性一致（Linearizable）：库存扣减、支付 — 必须用分布式锁或 CAS

---

## 真实冲突案例 / Real Conflicts

**案例：商品秒杀**
```
问题：10万人同时抢 1 个商品
❌ 方案1：读缓存判断 → 超卖（缓存不一致）
❌ 方案2：每次查 DB → DB 崩溃
✅ 方案3：
  - 限流：前端 + 网关削峰，只放 1000 QPS 进来
  - Redis DECR 原子操作：库存 > 0 才进入 DB
  - DB 最终写入：用乐观锁 (version) 防止并发超卖
```

---

## 常见错误 / Common Mistakes

❌ 只做单层缓存，没有多级降级（CDN → Redis → DB）
❌ 缓存 key 粒度太粗，一个 key 更新就让所有用户缓存失效（惊群）
❌ 限流在 LB 上做，而不是在每个服务实例上做，导致实例间不均衡

✅ **Senior 答法**：先问"这个数据的一致性要求是什么？"再决定缓存策略

---

## 关键洞察 / Key Insight

> **限流 = 系统的免疫系统；缓存 = 系统的记忆；一致性 = 系统的诚信。三者失衡，系统必出问题。**
> Rate limiting is your immune system; caching is your memory; consistency is your integrity. Imbalance any one of them and the system breaks.

---

## 📚 References
- [AWS Architecture: Cache Strategies](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
- [Cloudflare: How we handle Black Friday traffic](https://blog.cloudflare.com/traffic-spikes-and-ddos-protection/)
- [Martin Fowler: Patterns of Distributed Systems — Two-Phase Locking](https://martinfowler.com/articles/patterns-of-distributed-systems/two-phase-locking.html)

## 🧒 ELI5
超市收银台（限流）控制人流，仓库有备货（缓存）不用每次去总仓拿，账本（一致性）确保每笔买卖都记对。三件事都做好，超市才不会在促销日崩掉。
