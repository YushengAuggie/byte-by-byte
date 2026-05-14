# 🏗️ 系统设计 / System Design — Day 43
**Topic:** Design a Logging System (ELK Stack)
**Difficulty:** Advanced | **Phase:** Mastery

---

## 想象你在设计...
你是 Netflix 的基础设施工程师。每秒有数百万用户在播放视频，服务跨越数百个微服务，每秒产生数 GB 的日志。当出现生产事故时，你如何在几秒内找到根因？答案：ELK Stack — Elasticsearch + Logstash + Kibana。

*You're an infrastructure engineer at Netflix. Millions of users stream every second, hundreds of microservices emit gigabytes of logs per second. When a production incident hits, how do you find the root cause in seconds? The answer: ELK Stack.*

---

## Architecture

```
[Services / Apps]
  Service A ──→ Filebeat/Fluentd ──┐
  Service B ──→ Filebeat/Fluentd ──┤──→ [Kafka] ──→ [Logstash] ──→ [Elasticsearch Cluster]
  Service C ──→ Filebeat/Fluentd ──┘                                    │
                                                                         ▼
                                                                   [Kibana]
                                                                 (Search & Viz)
                                                                         │
                                                                         ▼
                                                               [Alerting: PagerDuty]

Elasticsearch Cluster:
┌─────────────────────────────────────┐
│  Master Node (cluster management)   │
│  Data Node 1 — hot (recent logs)    │
│  Data Node 2 — warm (7-30 days)     │
│  Data Node 3 — cold (30+ days → S3) │
└─────────────────────────────────────┘
```

**数据流 / Data Flow:**
1. **Filebeat/Fluentd** — lightweight shippers on each service host, tail log files, ship to Kafka
2. **Kafka** — buffers bursts, decouples producers from consumers, survives Logstash restarts
3. **Logstash** — parse, enrich (add geo, service metadata), filter, route
4. **Elasticsearch** — distributed inverted index; stores JSON documents, enables full-text search
5. **Kibana** — visualization, dashboards, alerts

---

## Key Tradeoffs — 为什么这样设计？

**为什么用 Kafka 做缓冲？**
日志高峰（发布时）流量是平时 10x，Logstash 处理不过来。Kafka 作为缓冲层解耦生产/消费速率，宁可 Logstash 慢，也不丢日志。

*Kafka buffers log spikes (10x at deploys), decouples ingestion speed from processing speed. Never drop logs.*

**为什么不直接存原始字符串？**
结构化日志（JSON）才能做聚合、过滤、指标提取。`{"level":"ERROR","service":"auth","userId":"u123","latency_ms":2341}` vs `[ERROR] auth service user u123 2341ms`

**冷热数据分层 / Tiered Storage:**
- Hot (SSD, 0-7d): fast queries for recent debugging
- Warm (HDD, 7-30d): slower, for compliance
- Cold (S3, 30d+): near-zero cost, retrieve if needed

---

## Common Mistakes — 别踩这个坑

❌ **每个服务直接连 Elasticsearch** — 高峰时 ES 过载崩溃
✅ Filebeat → Kafka → Logstash → ES，中间有缓冲

❌ **无结构日志** — `print(f"Error: {e}")` 没有上下文
✅ 结构化日志: `logger.error("payment_failed", extra={"user_id": uid, "amount": amt, "error": str(e)})`

❌ **保留所有日志** — 成本爆炸
✅ 采样：DEBUG 日志 1%，INFO 10%，ERROR/WARN 100%

❌ **单个 ES index 放所有日志** — 索引太大，查询慢
✅ 按天分 index：`logs-2026-05-14`，用 ILM (Index Lifecycle Management) 自动滚动和删除

---

## 📚 References
- [Elastic: ELK Stack Overview](https://www.elastic.co/what-is/elk-stack)
- [Kafka as Log Buffer](https://kafka.apache.org/uses)
- [Index Lifecycle Management](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)

## 🧒 ELI5
想象你是餐厅老板，每桌服务员都在说话（日志）。你请了一个助手（Filebeat）把所有人说的话记下来，交给翻译（Logstash）整理，然后存进一个超级大索引（Elasticsearch），任何时候你都能搜 "桌7报怨了什么"。Kibana 就是你的大屏幕仪表盘。

*Imagine each microservice is a waiter talking non-stop. Filebeat writes everything down, Kafka holds the notepad, Logstash organizes notes, Elasticsearch indexes them, and Kibana shows you a searchable dashboard.*
