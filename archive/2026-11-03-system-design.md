# 🏗️ 系统设计 / System Design — Day 146 (Synthesis)
**可观测性三支柱大综合：Metrics、Logs、Traces 的架构边界**
**Observability Three Pillars Deep Synthesis: When to Use Metrics vs Logs vs Traces**

---

## 🔥 想象一下... / Real-World Scenario

凌晨 2 点，告警触发：**checkout 服务 p99 延迟 > 5s**。你是值班工程师，面对 200 个微服务。你的第一反应是什么？

It's 2 AM. Alert fires: **checkout service p99 latency > 5s**. You're on-call across 200 microservices. What do you reach for first?

这不是单一工具能回答的问题。可观测性的核心在于三支柱的**协同**，而不是各自为战。

---

## 🏗️ 架构图 / Architecture

```
用户请求 / User Request
         │
         ▼
┌─────────────────────────────────────────┐
│          API Gateway / Load Balancer     │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 Checkout   Payment    Inventory
 Service    Service    Service
    │          │          │
    └──────────┴──────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 METRICS     LOGS       TRACES
(Prometheus)(ELK Stack)(Jaeger/Zipkin)
    │          │          │
    └──────────┴──────────┘
               │
               ▼
    Observability Platform
    (Datadog / Grafana / etc.)
```

---

## 🎯 三支柱的边界 / When to Use Each

### 📊 Metrics — WHEN something is wrong
**特征 / Characteristics:** 聚合数值、时间序列、低基数
**用来 / Use for:**
- `checkout_latency_p99 > 5s` → 触发告警
- CPU/内存利用率趋势
- 请求速率、错误率（RED 方法：Rate, Error, Duration）
- SLO/SLA 合规监控

**不适合 / NOT for:**
- 高基数数据（每用户 ID、每订单 ID）→ 内存爆炸
- 调试具体的一次失败请求

```
# ✅ Good: 低基数 / Low cardinality
http_requests_total{method="POST", status="500"} 42

# ❌ Bad: 高基数 / High cardinality  
http_requests_total{user_id="u-82736", order_id="ord-99182"} 1
# → Prometheus 内存会爆 / This will OOM Prometheus
```

---

### 📋 Logs — WHAT happened
**特征 / Characteristics:** 结构化事件、任意上下文、可搜索
**用来 / Use for:**
- `"payment failed: card_declined, user_id=u-123, amount=99.99"` → 具体根因
- 审计日志（谁做了什么）
- 错误堆栈信息
- 业务事件流水

**不适合 / NOT for:**
- 跨服务调用链路分析（你能看到 A 和 B 各自的日志，但不知道 A→B→C 这条链上哪里慢了）
- 实时聚合计算（成本太高）

```python
# ✅ 结构化日志 / Structured logging
logger.error("payment_failed", extra={
    "user_id": user.id,
    "amount": order.total,
    "reason": "card_declined",
    "trace_id": request.trace_id,  # ← 关键：关联 trace
})
```

---

### 🔍 Traces — WHERE in the distributed call chain
**特征 / Characteristics:** 分布式请求链路、跨服务 span、时序瀑布图
**用来 / Use for:**
- 哪个服务最慢？(checkout → payment → bank API 哪段耗时最多)
- 服务依赖关系可视化
- 找出 fan-out 问题（1 个请求触发 50 个下游调用）

**不适合 / NOT for:**
- 统计聚合告警（用 metrics 更高效）
- 长期存储（trace 数据量大，通常采样 1%~10%）

```
Trace: order-checkout-82736
├── [0ms]   API Gateway              2ms
├── [2ms]   checkout-service        450ms  ← 瓶颈！
│   ├── [3ms]  inventory-check        5ms
│   ├── [8ms]  payment-service       440ms ← 再查这里
│   │   ├── [9ms]   fraud-check       2ms
│   │   └── [11ms]  bank-api         430ms ← 根因：外部 API 超时
│   └── [452ms] db-write              3ms
└── [455ms] response                  1ms
```

---

## 🔗 综合对比 / Synthesis Comparison

| 维度 | Metrics | Logs | Traces |
|------|---------|------|--------|
| **告警** | ✅ 最佳 | ⚠️ 可以 | ❌ 不适合 |
| **根因分析** | ⚠️ 粗粒度 | ✅ 最佳 | ✅ 跨服务最佳 |
| **调用链分析** | ❌ | ❌ | ✅ 最佳 |
| **存储成本** | 低 | 中~高 | 高（需采样） |
| **基数限制** | 严格低基数 | 无限制 | span 数量限制 |

**告警触发时的调查顺序 / Investigation order:**
1. **Metrics** → "哪个服务的哪个指标异常？"
2. **Traces** → "这条请求链路哪一段最慢？"
3. **Logs** → "那个具体的 span 里发生了什么？"

---

## 🚫 常见陷阱 / Common Mistakes

**别踩这些坑 / Don't do this:**

1. **生产环境 DEBUG 日志全开** → 日志量×10，成本爆炸，降级到 WARN/ERROR
2. **不传播 trace_id** → 日志和 Trace 无法关联，根因分析断链
3. **Metrics 用高基数标签** → `{user_id=xxx}` 会让 Prometheus 内存 OOM
4. **100% 采样 Trace** → 每个请求都记录完整 Trace，存储成本不可接受
5. **三者各自独立，不打通** → 看 metrics 发现问题，但日志里没有 trace_id，无法关联

---

## 🛠️ 黄金标准实践 / Golden Standard

```
告警规则 (Metrics)  →  SLO Dashboard
                         ↓
                    触发调查
                    (Trace ID from log)
                         ↓
                    Trace 瀑布图定位慢 span
                         ↓
                    跳到该 span 的 Logs
                         ↓
                    根因：外部 API 超时
```

**工具链推荐 / Toolchain:**
- Open source: **Prometheus + Loki + Tempo** (Grafana 三件套, 同一 trace_id 互通)
- SaaS: **Datadog** (三合一, 最贵) / **New Relic** / **Honeycomb** (trace-first)

---

## 📚 参考资料 / References

1. [Grafana Observability — Metrics, Logs, Traces](https://grafana.com/blog/2020/09/23/the-three-pillars-of-observability-metrics-logs-and-traces/)
2. [OpenTelemetry — The Standard](https://opentelemetry.io/docs/concepts/observability-primer/)
3. [Honeycomb: Observability vs Monitoring](https://www.honeycomb.io/blog/observability-vs-monitoring)

---

## 🧒 ELI5

想象你家的电力系统：
- **Metrics** = 电表（告诉你用了多少度电，啥时候用电量突然飙升）
- **Logs** = 用电记录本（"晚上8点，微波炉用了600W，空调用了1200W"）
- **Traces** = 电路图（帮你找到哪根线路跳闸了导致厨房停电）

三个都要，缺一不可。
