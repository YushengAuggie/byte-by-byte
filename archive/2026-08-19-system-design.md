# 系统设计综合 — 消息队列选型终极对比
# System Design Synthesis — Kafka vs Kinesis vs SQS vs RabbitMQ

> Day 114 · Synthesis Mode · Expert Phase

---

## 🏗️ 系统设计 / System Design

**消息队列选型：生产环境如何做决策？**
**Message Queue Selection: How to Decide in Production?**

---

### 🎯 核心场景 / Real-World Scenario

想象你在设计一个电商平台的事件总线。每天处理 5 亿次用户行为事件：下单、支付、库存变更、物流更新。
你的架构师问：*"我们用 Kafka 还是 SQS？"*

Imagine you're designing an event bus for an e-commerce platform handling 500M daily events: orders, payments, inventory changes, shipping updates. Your architect asks: *"Kafka or SQS?"*

---

### 🗺️ 架构对比图 / Architecture Comparison

```
消息队列全景 / Message Queue Landscape

┌──────────────────────────────────────────────────────┐
│                    USE CASE MATRIX                     │
├─────────────┬──────────┬──────────┬──────────┬────────┤
│             │  Kafka   │ Kinesis  │   SQS    │Rabbit  │
├─────────────┼──────────┼──────────┼──────────┼────────┤
│ Throughput  │ 极高/10M+│ 高/1M+   │ 中/3000  │ 中高   │
│ Retention   │ 永久     │ 7天默认  │ 14天     │ 无持久 │
│ Ordering    │ 分区内   │ 分片内   │ FIFO可选 │ 支持   │
│ Replay      │ ✅ 完全  │ ✅ 支持  │ ❌ 否    │ ❌ 否  │
│ Consumer    │ Pull     │ Pull     │ Pull     │ Push   │
│ Ops Cost    │ 高(自管) │ 低(托管) │ 最低     │ 中     │
│ Latency     │ 毫秒级   │ 毫秒级   │ 秒级     │ 微秒级 │
└─────────────┴──────────┴──────────┴──────────┴────────┘

E-Commerce Event Bus Decision:
                                                        
  Order Service ──→ ┌─────────┐ ──→ Inventory Service  
  Payment       ──→ │  KAFKA  │ ──→ Analytics Pipeline  
  Shipping      ──→ │(Log bus)│ ──→ Fraud Detection     
                    └────┬────┘ ──→ Email Service       
                         │                              
                    ┌────▼────┐                         
                    │   SQS   │ ──→ Email/SMS Workers   
                    │(tasks)  │     (at-most-once OK)   
                    └─────────┘                         
```

---

### ⚖️ 关键权衡 / Key Tradeoffs

**为什么用 Kafka？/ Why Kafka?**
- **重放能力** — 审计日志、机器学习训练、错误回放
- **高吞吐** — 分区并行，单集群支持 TB/天
- **多消费者组** — 同一消息被 analytics、fraud、email 独立消费
- 代价：需要运维 (ZooKeeper/KRaft)，或用 Confluent Cloud

**为什么用 Kinesis？/ Why Kinesis?**
- 你在 AWS 生态，不想运维 Kafka
- 需要与 Lambda、Firehose、S3 无缝集成
- 分片模型比 Kafka 简单，但扩容需手动 reshard

**为什么用 SQS？/ Why SQS?**
- 任务队列语义：每条消息只被处理一次
- 成本最低，无需维护
- 适合：发邮件、生成缩略图、异步 API 调用
- 不适合：流处理、需要重放的场景

**为什么用 RabbitMQ？/ Why RabbitMQ?**
- 复杂路由 (Exchange → Queue 映射)
- 低延迟 push 模型 (微秒级)
- 金融、游戏场景

---

### 🚩 别踩这个坑 / Common Mistakes

1. **把 SQS 当 Kafka 用** — SQS 消费后即删除，无法重放。如果 fraud 团队要分析历史数据，他们已经没有数据了
2. **Kafka topic 分区数设太少** — 后期增加分区会破坏 key-based ordering
3. **忽略 consumer lag 监控** — Kafka lag 积压是下游服务"悄悄挂掉"的第一信号
4. **Kinesis Hot Shard** — 所有 userId 模 10 全落到同一个 shard，吞吐打满

---

### 🏆 决策框架 / Decision Framework

```
需要重放？→ Kafka 或 Kinesis
需要复杂路由？→ RabbitMQ
只需任务队列？→ SQS
在 AWS 上不想运维？→ Kinesis (流) + SQS (任务)
极高吞吐 + 多消费者组？→ Kafka
```

---

### 📚 References
- https://kafka.apache.org/documentation/
- https://aws.amazon.com/kinesis/data-streams/
- https://aws.amazon.com/sqs/
- https://www.rabbitmq.com/tutorials/amqp-concepts.html
- https://www.conduktor.io/kafka/kafka-vs-rabbitmq/

### 🧒 ELI5
Kafka 是个大型录音机，人人都可以倒带重听。SQS 是个传令兵，送完就跑，不留副本。Kinesis 是 AWS 版录音机，省心但贵一点。RabbitMQ 是邮局，能精准分拣到不同信箱。
Kafka is a big recorder everyone can rewind. SQS is a courier who delivers once and leaves. Kinesis is the AWS recorder — easier but pricier. RabbitMQ is a post office with precise routing.
