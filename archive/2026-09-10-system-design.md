# 🏗️ 系统设计 / System Design — Day 131 (Synthesis)
**主题：可观测性三支柱 — 日志、指标、追踪的取舍 / Observability Trinity: Logs, Metrics, Traces**

---

## 场景 / Scenario

想象你管理着一个横跨 20 个微服务的支付平台。凌晨 3 点，P99 延迟突然从 50ms 飙升到 3s。你会怎么排查？

You manage a payment platform across 20 microservices. At 3 AM, P99 latency spikes from 50ms to 3s. Where do you even start?

答案在于你是否建立了完整的**可观测性（Observability）**体系，而不仅仅是监控告警。

---

## 三支柱全景 / The Three Pillars

```
┌─────────────────────────────────────────────────────────┐
│                    OBSERVABILITY STACK                  │
│                                                         │
│  📋 LOGS           📊 METRICS          🔍 TRACES        │
│  ─────────         ──────────          ────────         │
│  "What happened"   "How much/often"    "Why it's slow"  │
│                                                         │
│  Elasticsearch     Prometheus          Jaeger / Zipkin  │
│  Loki              InfluxDB            AWS X-Ray        │
│  CloudWatch        Datadog             OpenTelemetry    │
│                                                         │
│  Cost: HIGH        Cost: LOW           Cost: MEDIUM     │
│  Query: SLOW       Query: FAST         Query: MEDIUM    │
│  Cardinality: ∞    Cardinality: LOW    Cardinality: MED │
└─────────────────────────────────────────────────────────┘
```

---

## 深度对比 / Deep Comparison

### 📋 日志 (Logs)
**优点：** 信息最完整，可以记录任意字段，排查 bug 无可替代
**缺点：** 存储成本最高（TB级），查询慢，高基数字段会压垮 Elasticsearch

**最佳实践：**
- 用结构化日志（JSON），不要用字符串拼接
- 区分 DEBUG/INFO/WARN/ERROR — 生产只保留 INFO+
- 必须包含 `trace_id`，把日志和追踪打通

```python
# ❌ 字符串日志
logger.info(f"User {user_id} paid {amount}")

# ✅ 结构化日志
logger.info("payment.processed", extra={
    "user_id": user_id,
    "amount": amount,
    "trace_id": current_trace_id(),
    "service": "payment-service"
})
```

### 📊 指标 (Metrics)
**优点：** 查询极快（预聚合），存储成本低，适合告警和大盘
**缺点：** 无法存储高基数字段（每个 user_id 都是一个时间序列 → 炸库）

**核心指标类型：**
- **Counter**: 只增不减（请求数、错误数）
- **Gauge**: 任意变化（内存使用、连接数）
- **Histogram**: 分布（延迟百分位 P50/P95/P99）

```python
# Prometheus 指标示例
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency')

@REQUEST_LATENCY.time()
def handle_request(method):
    # ... business logic
    REQUEST_COUNT.labels(method=method, status='200').inc()
```

### 🔍 分布式追踪 (Distributed Traces)
**优点：** 唯一能展示**跨服务调用链**的工具，找到慢在哪个服务
**缺点：** 采样带来的信息丢失，存储成本介于二者之间

```
Trace: checkout-flow (total: 2.8s)
├── auth-service.verify (50ms)
├── inventory-service.check (200ms)
├── payment-service.charge (2.4s) ← 🔴 bottleneck!
│   ├── fraud-check (100ms)
│   ├── stripe-api.charge (2.1s) ← 🔴 external call!
│   └── db.write (200ms)
└── notification-service.send (150ms)
```

---

## 决策框架 / When to Use What

| 场景 | 优先用 | 原因 |
|------|--------|------|
| 告警 + SLO 监控 | Metrics | 快、便宜 |
| 找 bug / 定位错误 | Logs | 信息完整 |
| 找跨服务慢点 | Traces | 调用链可见 |
| 安全审计 | Logs | 不可变记录 |
| 容量规划 | Metrics | 趋势分析 |
| 新服务上线排查 | Traces + Logs | 双保险 |

---

## 综合建议 / Senior Engineer Perspective

**别踩这个坑：**

1. **Logs 中记录高基数字段当指标用** → 用 Prometheus 记 P99，不要在 ES 里 avg() 查延迟
2. **100% 追踪采样** → 流量大时会自杀；用头部采样 (head-based) 1-5%，或尾部采样 (tail-based) 保留慢请求
3. **忘记关联三者** → `trace_id` 必须同时出现在 log、metric label 和 span 里，否则排查时就是三个孤岛

**OpenTelemetry 是终局：**
2026年工业界已基本收敛到 OpenTelemetry (OTel) 作为统一采集标准，后端可以自由切换 Jaeger/Datadog/Honeycomb，不被供应商锁定。

---

## 📚 References
- https://opentelemetry.io/docs/concepts/observability-primer/
- https://grafana.com/blog/2022/03/21/how-labels-in-prometheus-can-affect-performance/
- https://www.jaegertracing.io/docs/1.50/architecture/

## 🧒 ELI5
你的身体出问题了，医生要诊断：
- **日志** = 日记（"今天早上头疼，午饭后好了"）
- **指标** = 体检报告数字（血压 130/85，体温 37.2°）
- **追踪** = 看你一天的行程轨迹（几点去哪里做了什么）

三样都有，才能找到病根。
