# 🏗️ 系统设计 / System Design — Day 153 (Synthesis)
**分布式事务模式全比较：SAGA vs 2PC vs Outbox Pattern**

---

## 想象你在设计…

你在构建一个电商平台（像我们 Day 38 设计的 Stripe 支付系统 + Day 36 的 E-Commerce Platform）。用户下单时需要同时：
1. 扣减库存
2. 创建订单
3. 扣款
4. 发送确认邮件

这四步分布在四个不同的微服务上。任何一步失败都需要回滚。**如何保证分布式事务的一致性？**

---

## ASCII 架构对比

```
         ┌─────────────────────────────────────────────────────┐
         │              分布式事务三大模式                        │
         └─────────────────────────────────────────────────────┘

2PC (Two-Phase Commit):
  Coordinator ──→ Phase 1: "准备好了吗?" ──→ [ServiceA, ServiceB, ServiceC]
  Coordinator ←── Phase 1 Response: "YES" ←── [all vote]
  Coordinator ──→ Phase 2: "提交!" ──→ [ServiceA, ServiceB, ServiceC]
  ⚠️ 协调者宕机 = 所有参与者阻塞

SAGA (Choreography):
  OrderService ──→ [event: OrderCreated]
       ↓
  InventoryService ──→ [event: InventoryReserved]
       ↓
  PaymentService ──→ [event: PaymentFailed]
       ↓
  InventoryService ←── [compensate: ReleaseInventory]  ← 补偿事务
  OrderService ←── [compensate: CancelOrder]

Transactional Outbox:
  ┌──────────────┐    ┌────────────────┐    ┌──────────────┐
  │   Service DB  │    │  Outbox Table  │    │  Message Bus │
  │ order: saved  │ ── │ event: pending │ ──→│  Kafka/SQS   │
  │ (same TX)     │    │ (atomic write) │    │              │
  └──────────────┘    └────────────────┘    └──────────────┘
  CDC (Debezium) or polling pulls outbox → publishes events
```

---

## 为什么这样设计？关键权衡

| 模式 | 一致性 | 可用性 | 复杂度 | 适用场景 |
|------|--------|--------|--------|----------|
| **2PC** | 强一致性 | ❌ 低（协调者是单点） | 中等 | 金融核心账本、跨库同一数据中心 |
| **SAGA** | 最终一致性 | ✅ 高 | 高（需补偿逻辑） | 微服务、跨服务工作流 |
| **Outbox** | 至少一次 | ✅ 高 | 中等 | 保证"事件一定发出去" |

**核心原则**：CAP 定理（Day 12）告诉我们，分布式系统无法同时保证 C + A + P。SAGA 选择 AP，2PC 选择 CP。

---

## 常见错误 / 别踩这个坑

❌ **误用 2PC 于跨数据中心场景**：网络延迟 + 协调者宕机 = 全系统阻塞。2PC 只适合同一数据中心的强一致需求。

❌ **SAGA 忘记幂等补偿**：补偿事务可能执行多次（网络重试）。每个补偿操作必须是幂等的。

❌ **Outbox 不清理**：Outbox 表会无限增长。���要在事件确认发出后及时删除或归档记录。

✅ **现实选择**：Stripe 用 Outbox + Idempotency Keys；Uber 用 SAGA + Cadence/Temporal workflow engine（我们 Day 41 讨论过 Distributed Task Queue）。

---

## 深度连接：与之前内容的联系

- **Day 13 消息队列**：SAGA 的编排依赖 Kafka/SQS 可靠传递
- **Day 38 支付系统**：Stripe 使用幂等 Key + Outbox 保证支付事件不丢失
- **Day 47 Raft/Paxos**：2PC 的协调者可以用 Raft 实现 HA
- **Day 63 分布式锁**：SAGA 补偿期间需要锁防止并发冲突

---

## 📚 References
- https://microservices.io/patterns/data/saga.html
- https://microservices.io/patterns/data/transactional-outbox.html
- https://martin.kleppmann.com/2015/09/26/transactions-at-various-levels-of-consistency.html

## 🧒 ELI5
想象你和朋友合伙买礼物。**2PC** 是：你问所有人"有钱吗？"等大家都说有才付款，但如果你（协调人）突然失联，大家都傻等着。**SAGA** 是：每人先付自己那份，如果中途有人没钱，之前付了的人各自退款。**Outbox** 是：先把"我要给你发钱"这个承诺写在纸上压在枕头下，确保即使中途断网，这个承诺也不会丢。
