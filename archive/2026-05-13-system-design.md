# 🏗️ 系统设计 / System Design — Design a Monitoring & Alerting System (Datadog)

> Day 42 · Mastery Phase · ~3 min read

---

## 想象你在设计... / Imagine You're Designing...

你在 Stripe 担任平台工程师，负责为数千个微服务搭建监控系统。每天处理数十亿个指标数据点，当支付服务延迟超过 200ms 时必须在 30 秒内触发报警。

You're a platform engineer at Stripe, building monitoring infrastructure for thousands of microservices. The system processes billions of metric data points daily and must trigger alerts within 30 seconds when payment service latency exceeds 200ms.

---

## 架构图 / Architecture Diagram

```
Services / Hosts
     │
     ▼
[Metrics Agent]  ──────────────────────────────────────────
[Log Shipper ]                                             │
[Trace Sidecar]                                            │
     │                                                     │
     ▼                                                     ▼
[Ingestion Gateway]  ←── Load Balancer              [Config Service]
  /metrics  /logs  /traces                          (alert rules,
     │                                               dashboards)
     ▼
[Kafka Topics]
  metrics-raw │ logs-raw │ traces-raw
     │
     ├──────────────────────────────────┐
     ▼                                  ▼
[Stream Processor]              [Cold Storage Writer]
 (Flink/Spark Streaming)         (S3/GCS Parquet)
 - Aggregation (1min/5min)
 - Anomaly detection
 - Alert evaluation
     │                    │
     ▼                    ▼
[TSDB]               [Alert Engine]
(Prometheus/         - Rule evaluation
 InfluxDB)           - Dedup & grouping
 Hot: 7 days         - Escalation policy
 Cold: S3            │
                     ▼
              [Notification Service]
              PagerDuty │ Slack │ Email │ Webhook
                     │
                     ▼
              [Alert Store] ← ACK / Silence / History
```

---

## 核心组件设计 / Core Component Design

### 指标摄入 / Metrics Ingestion
- **Pull model**: Prometheus 主动拉取 endpoints（适合内部服务）
- **Push model**: StatsD / OpenTelemetry SDK 主动推送（适合短生命周期任务）
- **Hybrid**: Agent (push to gateway) → Kafka → TSDB
- 数据格式：`metric_name{label=value} value timestamp`

### 时序数据库 / Time-Series Database
- **存储层次化（Tiered Storage）**:
  - Hot: 1-7 天，SSD，高压缩率（Gorilla 压缩）
  - Warm: 7-90 天，HDD，降采样（5min 粒度）
  - Cold: 90天+，S3 Parquet，1h 粒度
- **Gorilla 压缩**: Facebook 开源，时序数据压缩率高达 12x
- **Cardinality 爆炸问题**: 高基数标签（user_id）会导致数百万个时间序列

### 报警引擎 / Alert Engine
```
Alert Rule: avg(latency{service="payment"}[5m]) > 200ms for 3m

Evaluation loop:
  every 30s → query TSDB → evaluate condition
            → PENDING (condition met but not for 3m yet)
            → FIRING (condition met for 3m)
            → RESOLVED (condition no longer met)
```

### 去重与静默 / Dedup & Silencing
- **Alert grouping**: 同一服务 50 个 pod 全挂 → 合并成 1 个告警
- **Inhibition rules**: DB 挂了 → 抑制所有依赖该 DB 的服务告警
- **Maintenance windows**: 计划维护期间自动静默

---

## 关键权衡 / Key Tradeoffs

| 决策 | 选项 A | 选项 B | 我的选择 |
|------|--------|--------|----------|
| 拉 vs 推 | Pull (Prometheus) | Push (StatsD) | Hybrid |
| 存储 | 专用 TSDB | 通用数据库 | TSDB (Gorilla 压缩) |
| 处理 | 批处理 | 流处理 | 流处理 (低延迟) |
| 告警评估 | 客户端 | 服务端 | 服务端 (统一规则) |

**为什么用 Kafka 做缓冲？/ Why Kafka as buffer?**
- 削峰填谷：流量突刺时 TSDB 不被打垮
- 多消费者：流处理、存储、审计可并行消费
- 回放能力：出 bug 时可重新处理历史数据

---

## 别踩这个坑 / Common Mistakes

1. **Cardinality 爆炸** — 不要把 user_id 这类高基数字段作为 label，会创建数百万时间序列
2. **告警疲劳** — 告警太多导致 on-call 忽略。解决：分级（P0/P1/P2）+ 合并 + 抑制
3. **单点 TSDB** — 时序数据库本身要高可用，用集群模式（Cortex/Thanos for Prometheus）
4. **不测试告警** — 要定期"演练"：确认告警真的能触发，不是 dead link

---

## 📚 References

- [Prometheus Data Model](https://prometheus.io/docs/concepts/data_model/)
- [Facebook Gorilla: Fast, Scalable, In-Memory Time Series Database](https://vldb.org/pvldb/vol8/p1816-teller.pdf)
- [How Datadog Scales with Kafka](https://www.datadoghq.com/blog/engineering/datastores-at-datadog/)

## 🧒 ELI5

监控系统就像医院的体检仪器。传感器（agent）不停量你的心跳（CPU）、血压（内存）、体温（延迟）。数据存进病历（TSDB）。医生提前写好"如果体温超过 38.5 度就打电话给我"（告警规则）。一旦触发，护士（通知服务）就打电话、发短信（PagerDuty/Slack）。

A monitoring system is like a hospital's diagnostic equipment. Sensors (agents) constantly measure your heart rate (CPU), blood pressure (memory), and temperature (latency). Data is stored in medical records (TSDB). Doctors pre-define "call me if temperature exceeds 38.5°C" (alert rules). When triggered, nurses (notification service) call and text (PagerDuty/Slack).
