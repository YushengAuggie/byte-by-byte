# 🏗️ 系统设计 / System Design — 分布式追踪系统 (Jaeger/Zipkin)

> **Day 68 · Expert Phase · ~3 min read**

---

## 场景 / The Scenario

想象你在 Uber 工程团队：一个打车请求失败了，用户报告"无法匹配司机"。这个请求经过了 **API Gateway → Ride Service → Matching Service → Driver Service → Notification Service**，跨越 5 个微服务、3 个数据库、2 个消息队列。你怎么找到哪一步慢了？

You're on the Uber engineering team: a ride request failed. It touched 5 microservices, 3 databases, 2 queues. How do you find the bottleneck?

**答案 / Answer:** 分布式追踪系统。Distributed tracing.

---

## 架构图 / Architecture

```
                    ┌─────────────────────────────────────────┐
                    │         Client App / API Gateway         │
                    │   generates TraceID: abc123, SpanID: 1   │
                    └──────────────────┬──────────────────────┘
                                       │ HTTP Header: X-Trace-ID: abc123
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                           ▼
    ┌──────────────┐          ┌──────────────┐           ┌──────────────┐
    │ Ride Service │          │  Auth Service│           │ Maps Service │
    │  SpanID: 2   │          │  SpanID: 3   │           │  SpanID: 4   │
    │  parent: 1   │          │  parent: 1   │           │  parent: 1   │
    └──────┬───────┘          └──────────────┘           └──────────────┘
           │
    ┌──────▼───────┐
    │  DB Query    │
    │  SpanID: 5   │
    │  parent: 2   │
    │  latency: 450ms ⚠️│
    └──────────────┘

Each service sends span data to:
    ┌─────────────────────────────────────────┐
    │           Collector (Jaeger Agent)       │
    │  Receives spans via UDP (fire-and-forget)│
    └──────────────────┬──────────────────────┘
                       │
            ┌──────────▼──────────┐
            │   Storage Backend   │
            │  Cassandra / ES /   │
            │  Badger (local dev) │
            └──────────┬──────────┘
                       │
            ┌──────────▼──────────┐
            │    Query Service    │  ◄── Jaeger UI / Grafana Tempo
            │  TraceID lookup     │
            │  Dependency graph   │
            └─────────────────────┘
```

---

## 核心概念 / Core Concepts

### Span 是什么？
一个 **span** = 一个操作单元，包含：
- `trace_id`: 整条请求链路的唯一 ID
- `span_id`: 本次操作的 ID
- `parent_span_id`: 谁调用了我
- `operation_name`, `start_time`, `duration`
- `tags` (key-value), `logs` (events), `status`

A **span** = one unit of work. A **trace** = a tree of spans sharing the same `trace_id`.

### Context Propagation（上下文传播）
TraceID 需要在**每次跨服务调用**时传递：
- **HTTP:** `X-B3-TraceId`, `X-B3-SpanId` headers (Zipkin B3 format)
- **gRPC:** Metadata headers
- **Async/Queue:** Message headers (Kafka, RabbitMQ)
- **OpenTelemetry:** W3C `traceparent` header (now the standard)

---

## 采样策略 / Sampling Strategies

**为什么需要采样？** 100% 采样会产生巨量数据，影响性能。
Why sample? 100% tracing = too much data, too much overhead.

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **Head-based** | 在入口处决定采样（随机 1%） | 低流量，简单 |
| **Tail-based** | 请求完成后，根据结果决定（保留错误/慢请求） | 生产首选 |
| **Adaptive** | 动态调整采样率（Jaeger 默认） | 高流量系统 |

**最佳实践:** Tail-based sampling — 总是保留 error traces 和 P99 以上的慢 trace。

---

## 关键权衡 / Key Tradeoffs

### 存储选择
- **Cassandra:** 高写入吞吐，水平扩展佳 → Jaeger 生产首选
- **Elasticsearch:** 全文搜索，适合日志 + 追踪融合
- **ClickHouse:** Grafana Tempo 后端，列存储，超快聚合

### Push vs Pull
- **Jaeger:** 服务推送 spans 到 Agent（UDP，低延迟，不阻塞）
- **OpenTelemetry Collector:** 可配置 pipeline，支持 fan-out 到多个后端

### 与日志/指标的关系 (三大支柱)
```
Logs    → What happened (事件记录)
Metrics → How much / how fast (聚合数字)
Traces  → Why it happened (因果链路)
```

---

## 别踩这个坑 / Common Mistakes

❌ **同步发送 spans** — 会增加服务延迟
✅ **异步 + UDP** — fire-and-forget，span 丢失可接受（比业务延迟更重要）

❌ **100% 采样上生产** — 数据量是请求量的 10-100x
✅ **1% 随机 + 100% 错误/慢请求**

❌ **只追踪 HTTP，忘了 DB/Queue**
✅ **插桩所有 I/O**：DB queries, external HTTP calls, queue publishes

❌ **TraceID 不传给异步 worker**
✅ 把 TraceID 放进消息体/headers，让下游能关联

---

## 📚 References

- [OpenTelemetry Docs](https://opentelemetry.io/docs/) — W3C standard, vendor-neutral
- [Jaeger Architecture](https://www.jaegertracing.io/docs/1.58/architecture/) — official deep dive
- [Grafana Tempo](https://grafana.com/docs/tempo/latest/) — cost-efficient tracing storage

---

## 🧒 ELI5

你和朋友去迷宫，每个人都有一根毛线球，进每个房间都撕一段贴上自己名字。如果有人迷路了，顺着毛线就能找回来，还能看出谁进了哪些房间、用了多长时间。

Imagine a maze where everyone carries a ball of yarn and tears off a piece in each room with their name on it. If someone gets lost, you follow the yarn trail — and you can see exactly who went where and how long they spent there. Distributed tracing is that yarn for microservice requests.
