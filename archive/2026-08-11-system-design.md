# 🏗️ 系统设计综合 / System Design Synthesis — Day 112

**主题 / Topic:** 构建高可用系统的决策矩阵 — 把60个设计题融成一张图
**The Architecture Decision Map — Synthesizing 60 System Design Patterns**

---

## 想象你是新任 Staff Engineer…

你刚加入一家快速增长的公司。系统开始出现裂缝：数据库超载、接口超时、部署困难。CTO 问你："我们应该怎么架构？"

You just joined a fast-growing company. The system is showing cracks: database overload, API timeouts, hard deployments. The CTO asks: "How should we architect this?"

**这是一个需要你综合所有知识的问题。/ This is the question that requires synthesizing everything.**

---

## 全栈请求路径 / Full Request Flow

```
用户 → CDN → Load Balancer → API Gateway → Services
       (静态)   (健康检查)    (Auth/Rate)   (微服务群)
                                                ↓
                               ┌─────────────────────────┐
                               │  同步 / Synchronous      │
                               │  REST / gRPC             │
                               └──────────┬──────────────┘
                                          ↓
                               ┌─────────────────────────┐
                               │  异步 / Async            │
                               │  Kafka / SQS / RabbitMQ  │
                               └──────────┬──────────────┘
                                          ↓
                               ┌─────────────────────────┐
                               │  存储层 / Storage        │
                               │  Cache → DB → Search     │
                               │  Redis → MySQL → ES      │
                               └─────────────────────────┘
```

---

## 四大核心权衡 / The 4 Core Trade-offs

### 1. 一致性 vs 可用性 (CAP Theorem)
- **强一致性** (Paxos/Raft): 金融交易、库存扣减 → 选 ZooKeeper, etcd, PostgreSQL
- **最终一致性**: 社交 feed、通知、点赞计数 → 选 Cassandra, DynamoDB, Redis

### 2. 同步 vs 异步通信
- **同步 (REST/gRPC)**: 需要立即响应 → 查余额、登录验证、实时搜索
- **异步 (Kafka/SQS)**: 可以延迟处理 → 发邮件、生成报告、推送通知
- 原则: **任何超过 200ms 的操作都考虑异步化**

### 3. 读多写少 vs 写多读少
- **读多 (100:1)** → Cache + Read Replicas (Redis + MySQL Replica)
- **写多 (1:1+)** → 分片 + 异步写 (Cassandra + Kafka)
- **时序数据** → InfluxDB / TimescaleDB (不要用关系型!)
- **全文搜索** → Elasticsearch (不要让 MySQL 做 LIKE '%query%')

### 4. 单体 vs 微服务
- **< 10人团队**: 先做单体，模块化设计，别过早分裂
- **团队按服务边界分**: 才考虑微服务 (Conway's Law)
- **微服务代价**: 网络延迟、分布式事务、运维复杂度
- 原则: **先单体，再根据团队/性能瓶颈拆分**

---

## 面试用"万能框架" / The Universal Interview Framework

```
Step 1 — Clarify (5 min)
  - 读写比是多少？DAU/QPS 估算？
  - 延迟要求：< 100ms? 或可接受秒级？
  - 一致性要求：强一致 or 最终一致？

Step 2 — Capacity Estimate (3 min)
  - QPS = DAU × 操作次数 / 86400
  - 存储 = 每条数据大小 × 数量 × 时间

Step 3 — High-level Design (10 min)
  - 画出主干架构图
  - 明确每个组件的职责

Step 4 — Deep Dive (15 min)
  - 挑最复杂/最有趣的组件展开

Step 5 — Bottlenecks (5 min)
  - 单点故障在哪？如何解决？
  - 如果流量翻10倍，哪里会崩？
```

---

## 别踩这个坑 / Common Mistakes

❌ **过早微服务化**: 10人团队不需要 Kubernetes 和 Service Mesh
❌ **忽略网络分区**: 假设服务间调用永远不会失败（它会的）
❌ **没有降级策略**: 下游挂了，上游也跟着挂（用 Circuit Breaker）
❌ **数据库做了不该做的事**: MySQL 全文搜索、MySQL 时序存储
✅ **先问需求**: 延迟 < 100ms? 99.99% SLA? 每天多少写入? 数据能丢吗?

---

## 快速选型速查 / Quick Selection Guide

| 需求 | 选择 |
|------|------|
| 强一致性 KV | Redis (单机) / etcd (分布式) |
| 海量写入 | Cassandra / DynamoDB |
| 关系型 + ACID | PostgreSQL / MySQL |
| 全文搜索 | Elasticsearch |
| 消息队列 | Kafka (高吞吐) / RabbitMQ (复杂路由) |
| CDN | Cloudflare / AWS CloudFront |
| 对象存储 | S3 / GCS |
| 实时通信 | WebSocket / SSE |

---

## 📚 References
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [The Architecture of Open Source Applications](https://aosabook.org/)

## 🧒 ELI5
搭乐高先想好要盖什么，再决定用哪种积木。每种积木都有优缺点，没有完美的答案，只有"在这个场景最合适"的答案。

Building with LEGO: plan what you're building before choosing pieces. Every piece has trade-offs — there's no perfect answer, only the right answer for your specific constraints.
