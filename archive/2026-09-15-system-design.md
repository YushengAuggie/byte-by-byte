# 系统设计综合 / System Design Synthesis — Day 133
**日期 / Date:** 2026-09-15 | **阶段 / Phase:** Expert | **模式 / Mode:** Synthesis

---

## 🏗️ 系统设计 / System Design — 事件驱动 vs 请求驱动架构的终极对比
### Event-Driven vs Request-Driven Architecture: When to Use What at Scale

---

### 🌏 综合背景 / Synthesis Background

在过去 132 天里，我们深入研究了：
- 消息队列与事件驱动架构（Day 13）
- 限流与节流（Day 17）
- 通知系统（Day 24）
- 聊天系统（Day 28）
- 支付系统（Day 38）
- 股票交易所（Day 62）
- 实时流媒体（Day 61）

今天将这些系统背后的**架构选型**做一次系统性对比。

Over 132 days, we've designed systems that span both paradigms. Today: the meta-question — **when does event-driven win, and when does it hurt you?**

---

### 🏛️ 两种范式对比 / Two Paradigms Compared

```
REQUEST-DRIVEN (同步 / Synchronous)
┌──────────┐    HTTP/gRPC    ┌──────────────┐
│  Client  │ ─────────────► │   Service B  │
│          │ ◄───────────── │              │
└──────────┘   response      └──────────────┘
特点: 即时反馈、强耦合、调用链清晰

EVENT-DRIVEN (异步 / Asynchronous)
┌──────────┐   publish    ┌─────────────┐   subscribe  ┌──────────┐
│ Producer │ ───────────► │  Message    │ ────────────► │Consumer A│
│          │              │  Broker     │               ├──────────┤
└──────────┘              │ (Kafka/SQS) │ ────────────► │Consumer B│
                          └─────────────┘               └──────────┘
特点: 解耦、异步、最终一致性
```

---

### ⚡ 实战系统分析 / Real-World System Analysis

| 系统 / System | 核心通信方式 | 为什么这样选？|
|---|---|---|
| 支付系统 (Day 38) | **请求驱动** (同步 HTTP + 2PC) | 需要即时确认、幂等性保证、强一致性 |
| 通知系统 (Day 24) | **事件驱动** (Kafka + 扇出) | 低优先级、可延迟、需要广播给多个消费者 |
| 聊天系统 (Day 28) | **混合**: WebSocket (实时) + MQ (离线) | 在线用户走 push，离线用户走 queue |
| 股票交易所 (Day 62) | **事件溯源** (Event Sourcing) | 不可变审计日志、时间回溯、订单簿重建 |
| 推荐系统 (Day 46) | **事件驱动** (行为流 → Flink) | 用户行为是天然的事件流，批/流混合 |

---

### 🧩 架构决策框架 / Decision Framework

**选择请求驱动 (同步) 当：**
```
✅ 需要即时响应 (用户等待结果)
✅ 强一致性是硬需求 (支付、库存扣减)
✅ 调用链简单、团队小
✅ 需要向调用方传播错误
```

**选择事件驱动 (异步) 当：**
```
✅ 解耦多个独立消费者 (1对多)
✅ 流量削峰填谷 (promotions, flash sales)
✅ 操作可以最终一致 (邮件、推送、审计日志)
✅ 需要时间旅行 / 事件回放 (Event Sourcing)
✅ 跨服务边界的 saga 编排
```

---

### 💥 别踩的坑 / Common Mistakes at Scale

**事件驱动最常见错误：**

1. **消息不幂等** — 消费者 crash 后重消费导致副作用
   - ✅ 解法：事件携带唯一 ID，消费前检查是否已处理

2. **顺序假设** — Kafka 分区内有序，但不同分区间无序
   - ✅ 解法：同一实体（如 user_id）路由到同一分区

3. **事件 schema 演进** — 生产者改字段，旧消费者崩溃
   - ✅ 解法：Avro/Protobuf + Schema Registry，向后兼容

4. **没有 dead letter queue (DLQ)** — 毒消息让消费者永久卡住
   - ✅ 解法：maxDeliveryAttempts + DLQ + 告警

**请求驱动最常见错误：**
1. **同步链路过深** — A→B→C→D→E，任何一环超时整个链路挂
   - ✅ 解法：超过 2 跳的非关键操作异步化

---

### 🎯 高级模式：Saga Pattern / Advanced: Saga for Distributed Transactions

```
# 支付流程 Saga (编排模式 / Orchestrator Pattern)
class PaymentSaga:
    def execute(self, order):
        steps = [
            (self.reserve_inventory, self.release_inventory),
            (self.charge_payment,    self.refund_payment),
            (self.ship_order,        self.cancel_shipment),
        ]
        completed = []
        for forward, compensate in steps:
            try:
                forward(order)
                completed.append(compensate)
            except Exception:
                # 补偿事务回滚 / Run compensating transactions
                for comp in reversed(completed):
                    comp(order)
                raise
```

> **核心洞察：** Saga 用一系列本地事务 + 补偿事务替代分布式两阶段提交（2PC），牺牲强一致性换取可用性，是微服务时代的标准解法。
>
> **Key Insight:** Saga replaces distributed 2PC with local transactions + compensating actions. Trade strong consistency for availability — the standard microservices pattern.

---

### 📚 References
- https://martinfowler.com/articles/201701-event-driven.html — Martin Fowler on event-driven architectures
- https://microservices.io/patterns/data/saga.html — Saga pattern documentation
- https://www.confluent.io/blog/event-sourcing-cqrs-stream-processing-apache-kafka-whats-connection/ — Confluent on Event Sourcing + Kafka

### 🧒 ELI5
请求驱动就像打电话：你说话，等对方回应，再继续。事件驱动就像发短信到群里：你发出去就不管了，想看的人自己去看。购物付款要打电话（同步），发优惠券推送发短信就够了（异步）。

Request-driven is like a phone call — you talk, wait for the reply, continue. Event-driven is like a group text — you send it and move on, subscribers read when they can. Use the phone for payments, group texts for notifications.
