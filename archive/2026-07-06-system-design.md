# 🏗️ 系统设计 / System Design — Day 83 · Expert Synthesis

**主题 / Topic:** 综合对比 — 当系统撞上系统：设计决策的跨系统矩阵
**Synthesis: When Systems Collide — Cross-Architecture Decision Matrix**

---

## 想象一下 / Real-World Scenario

你是一家独角兽公司的 Staff Engineer。CTO 问你："我们要同时支持实时聊天、视频流、支付处理，以及搜索自动补全。这四个能共用同一套基础设施吗？"

You're a Staff Engineer at a unicorn. CTO asks: "We need real-time chat, video streaming, payment processing, and search autocomplete simultaneously. Can they share infrastructure?"

**答案不是"能"或"不能"—— 而是"哪些层可以共享，哪些必须隔离"。**
The answer isn't yes or no — it's "which layers can share, which must isolate."

---

## 四大系统的核心约束对比 / Core Constraints Comparison

```
System         | Latency  | Throughput | Consistency | Storage     | Protocol
---------------|----------|------------|-------------|-------------|----------
Chat (Slack)   | <100ms   | Medium     | Eventual OK | Hot+Archive | WebSocket
Video (Netflix)| <200ms   | Very High  | Eventual OK | CDN-heavy   | HLS/DASH
Payment        | <500ms   | Low-Med    | STRONG ⚠️   | ACID DB     | HTTPS/REST
Autocomplete   | <50ms    | Very High  | Stale OK    | In-Memory   | HTTP/REST

                          ↑
              Payment is the odd one out:
              it CANNOT share eventual-consistency infra
```

---

## 架构决策矩阵 / What Can Be Shared

```
                     ┌────────────────────────────────────┐
                     │           Shared Layer              │
                     │  ┌──────────┐  ┌────────────────┐  │
                     │  │   API    │  │   Auth/AuthZ   │  │
                     │  │ Gateway  │  │  (JWT, OAuth)  │  │
                     │  └──────────┘  └────────────────┘  │
                     │  ┌──────────┐  ┌────────────────┐  │
                     │  │ CDN/Edge │  │  Observability │  │
                     │  │ (static) │  │  (logs/traces) │  │
                     │  └──────────┘  └────────────────┘  │
                     └────────────────────────────────────┘
                                      │
         ┌────────────────────────────┼──────────────────────────┐
         ▼                            ▼                          ▼
  ┌─────────────┐             ┌──────────────┐          ┌──────────────┐
  │  Chat + Video│             │   Payment    │          │ Autocomplete │
  │  (eventual)  │             │ (isolated!)  │          │  (read-only) │
  │  Kafka+Redis │             │ Postgres+2PC │          │ Redis/Trie   │
  └─────────────┘             └──────────────┘          └──────────────┘
```

### ✅ 可以共享 / Can Share:
- API Gateway (rate limiting, routing)
- CDN (static assets)
- Authentication service
- Distributed tracing (Jaeger/OpenTelemetry)
- Object storage (S3) for artifacts

### ❌ 不能混用 / Must Isolate:
- **Payment** ← MUST have its own ACID database, cannot share eventual-consistency Kafka pipeline
- **Autocomplete** ← Must be read-optimized; never co-locate with write-heavy workloads
- **Video transcoding** ← CPU-bound; isolate in separate worker pools

---

## 关键权衡 / Key Tradeoffs

### 1. 一致性隔离 / Consistency Isolation
**Chat** 可以接受"消息延迟几秒"(最终一致性)，但 **Payment** 必须保证"扣款只发生一次"(强一致性)。把它们放在同一个数据库里会让 Chat 的性能拖慢 Payment，或让 Payment 的锁机制拖慢 Chat。

Chat can tolerate "message delayed by seconds" (eventual consistency), but Payment demands "charge happens exactly once" (strong consistency). Mixing them either kills Chat performance via Payment's locking, or compromises Payment's correctness.

### 2. 流量模式 / Traffic Pattern Mismatch
- Autocomplete: 每秒百万次读取，极低写入 → Redis sorted sets, in-memory only
- Video: 大块字节流 → 不走应用服务器，直接 CDN-to-client
- Chat: 小包高频 → WebSocket long-lived connections

### 3. 故障域隔离 / Blast Radius
```
❌ Bad: Payment service shares DB connection pool with Chat
   → Chat traffic spike exhausts connections → Payment fails

✅ Good: Bulkhead pattern — each system has independent connection pools
   → Chat DB slow → only Chat degrades; Payment unaffected
```

---

## 综合架构原则 / Synthesis Principles (Staff-Level)

1. **按一致性需求划分数据边界** — 强一致性系统永远隔离
   Partition data boundaries by consistency requirement — strong-consistency systems always isolated

2. **共享无状态层，隔离有状态层** — API Gateway/Auth 可共享；数据库不行
   Share stateless layers, isolate stateful ones — API Gateway/Auth can share; databases cannot

3. **识别"写放大"风险** — 视频上传触发转码队列，转码队列不能与支付队列共用 worker
   Identify write amplification risks — video upload → transcode queue must not share workers with payment queue

4. **降级策略需匹配** — 聊天系统降级 = 消息缓冲几秒（可接受）；支付系统降级 = 拒绝请求（不能丢单）
   Degradation strategies must match business requirements — chat buffering is OK; payment must reject, never silently lose

---

## 别踩这个坑 / Common Mistakes

```
❌ 把 Kafka 当"万能总线"接入支付流程
   Using Kafka as universal bus for payment — at-least-once delivery ≠ exactly-once billing

❌ 让搜索索引和业务数据库共用同一个 Postgres
   Sharing Postgres between search index and business data — vacuum/autovacuum conflicts

❌ 跨系统共享缓存 key 空间 (Redis)
   Sharing Redis key namespace across systems — cache eviction policies conflict

✅ 正确做法: 每个系统独立的 Redis instance 或 cluster，通过 prefix + TTL policy 隔离
   Each system gets its own Redis cluster/namespace with independent eviction policy
```

---

## 📚 References

- [System Design Primer — Consistency Patterns](https://github.com/donnemartin/system-design-primer#consistency-patterns)
- [AWS Well-Architected Framework — Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- [Martin Kleppmann — Designing Data-Intensive Applications](https://dataintensive.net/) (Chapter 5, Replication)
- [Netflix TechBlog — Embracing the Differences: Inside the Netflix API Redesign](https://netflixtechblog.com/embracing-the-differences-inside-the-netflix-api-redesign-15fd8b3dc49d)

---

## 🧒 ELI5

想象四家餐厅共用一栋大楼：
- 快餐店（聊天）：效率第一，偶尔上错菜没关系
- 电影院小卖部（视频）：卖大爆米花桶，走量
- 银行柜台（支付）：每一笔账必须准确，绝不能错
- 糖果店（搜索）：只卖不进货，货架永远满着

快餐店和电影院可以共用仓库，但**银行柜台绝对不能跟快餐店共用收银机**。

Imagine four restaurants in one building. The cash register at the bank counter can NEVER be shared with the fast-food counter — even if it looks like the same hardware. Isolation is about trust and correctness, not just hardware cost.
