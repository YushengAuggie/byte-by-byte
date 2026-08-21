# 📊 Day 116 — System Design Synthesis
> 🔥 Expert Level | Synthesis: Distributed Transactions

---

# 🏗️ 系统设计 / System Design — 分布式事务大比拼

## 分布式事务的真相 / Distributed Transactions: 2PC vs SAGA vs 最终一致性

---

### 场景引入 / The Problem

想象你在设计一个电商支付系统。用户点击"购买"时，需要同时：
1. 扣减库存（Inventory Service）
2. 扣款（Payment Service）
3. 创建订单（Order Service）

三个独立服务，如果支付成功但库存扣减失败怎么办？

*Imagine: user clicks "Buy" — inventory, payment, and order creation must all succeed or all fail. Three different databases, three different services.*

---

### 方案一：两阶段提交 / 2PC (Two-Phase Commit)

```
协调者 Coordinator
    │
    ├─── Phase 1: PREPARE ──► Service A: "Can you commit?"
    │                    ──► Service B: "Can you commit?"
    │                    ──► Service C: "Can you commit?"
    │
    └─── Phase 2: COMMIT ───► All: "Commit!" (or ROLLBACK if any said no)
```

**优点：** 强一致性，ACID 保证
**缺点：**
- 协调者宕机 → 所有参与者卡住（锁住资源）
- 网络分区 → 脑裂 (split-brain)
- 延迟高（两轮网络往返）

**何时用：** 数据库内部（MySQL InnoDB Cluster），不推荐跨微服务

---

### 方案二：Saga 模式 / Saga Pattern

每步操作 + 对应的**补偿事务 (compensating transaction)**：

```
Order Created
    → Payment Charged ✅
        → Inventory Reserved ❌ FAIL
            → COMPENSATE: Refund Payment
                → COMPENSATE: Cancel Order
```

两种实现：
- **Choreography（编舞）**：每个服务发事件触发下一步，去中心化
- **Orchestration（编排）**：中央 Saga Orchestrator 控制流程

**优点：** 高可用，无分布式锁，适合微服务
**缺点：** 补偿逻辑复杂，无法保证隔离性（中间状态可见）

---

### 方案三：最终一致性 / Eventual Consistency + Idempotency

```
Write to local DB + Outbox table (same transaction)
    → Outbox Poller reads and publishes to Kafka
        → Consumers process with idempotency key
```

**Outbox Pattern** 是关键：先写本地，再异步传播。

**幂等性 (Idempotency)** 是保障：同一请求重试多次结果相同。

---

### 选型决策树 / Decision Framework

```
需要强一致性？
    ├── 是 → 单数据库能搞定吗？
    │         ├── 是 → 用单DB事务 ✅
    │         └── 否 → 考虑 2PC（仅内部系统，短事务）
    └── 否 → 业务允许补偿？
              ├── 是 → SAGA（推荐跨微服务）
              └── 否 → 最终一致性 + Outbox Pattern
```

---

### 常见陷阱 / Common Mistakes

| 错误 | 正确做法 |
|------|---------|
| 用 2PC 跨公网服务 | 用 SAGA + 幂等补偿 |
| Saga 没有幂等保证 | 每步加 idempotency key |
| 补偿逻辑写得不完整 | 画出所有失败路径，逐一实现 |
| 忽略中间状态的可见性 | 用"待确认/pending"状态隐藏中间态 |

---

### 📚 References

- [Saga Pattern — microservices.io](https://microservices.io/patterns/data/saga.html)
- [Transactional Outbox — microservices.io](https://microservices.io/patterns/data/transactional-outbox.html)
- [Distributed Transactions, Not Microservices — InfoQ](https://www.infoq.com/articles/saga-orchestration-outbox/)

### 🧒 ELI5

你和朋友一起去餐厅，各自点菜。如果你的菜来了但朋友的没来，你们有三种选择：等大家都到了再吃（2PC）、先吃先到的、没到的退款（SAGA）、或者大家异步到了再吃不管顺序（最终一致性）。
