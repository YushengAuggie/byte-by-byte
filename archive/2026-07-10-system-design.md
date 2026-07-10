# System Design Synthesis: Event-Driven vs. Request-Response Architectures
*Day 87 — Expert Synthesis | 2026-07-10*

---

## 🏗️ 系统设计综合 / System Design Synthesis

### 事件驱动 vs 请求-响应架构深度对比
### Event-Driven vs. Request-Response Architecture Deep Dive

---

想象你已经覆盖了 60 个系统设计主题。从 URL Shortener 到 LLM 推理服务，你脑海中有大量架构蓝图。但面试官真正想考察的，是你能不能跨主题做出有依据的**架构决策**。
*Imagine you've covered 60 system design topics — from TinyURL to LLM inference. Interviewers want to see you make **principled architectural decisions** across topics, not just recall patterns.*

---

### 核心问题 / The Core Question

> 什么时候选择**请求-响应**？什么时候选择**事件驱动**？
> *When do you choose request-response? When do you choose event-driven?*

---

### 架构对比 / Side-by-Side

```
请求-响应 (Request-Response)
──────────────────────────────────────────────────
  Client ──── HTTP/gRPC ──▶ Service ──▶ DB
              ◀────────────── (sync reply)

典型系统: URL Shortener, Rate Limiter, Auth

事件驱动 (Event-Driven)
──────────────────────────────────────────────────
  Producer ──▶ [Message Queue] ──▶ Consumer A
                    │                Consumer B
                    └──────────────▶ Consumer C

典型系统: Notification System, Web Crawler,
          Payment System, Content Moderation
```

---

### 关键权衡 / Key Tradeoffs

| 维度 | 请求-响应 | 事件驱动 |
|------|-----------|----------|
| **延迟** | 低 (ms级) | 更高 (秒级) |
| **耦合** | 紧耦合 | 松耦合 |
| **一致性** | 强一致性容易实现 | 最终一致性 |
| **调试** | 简单，有栈追踪 | 复杂，需分布式追踪 |
| **扩展** | 水平扩展有上限 | 消费者独立扩展 |
| **错误处理** | 即时反馈 | 需要 DLQ + 重试逻辑 |

---

### 跨系统模式识别 / Cross-System Pattern Recognition

从你学过的系统中提炼规律：

**必须同步（请求-响应）的场景：**
- 认证/授权（用户等待登录结果）
- Rate Limiter（每个请求都需要实时决策）
- 搜索/查询（用户期待即时结果）

**应该异步（事件驱动）的场景：**
- 通知发送（Email/SMS 不需要用户等）
- 内容审核（批量处理，人工复审）
- 支付后处理（对账、报表生成）
- 日志/监控（高吞吐，非关键路径）

---

### 典型陷阱 / Common Mistakes

**❌ 错误：把事件驱动用于强一致性场景**
```
用户下单 → Kafka → 扣库存 (异步)
问题: 如果消费者宕机，库存未扣但订单已确认
```

**✅ 正确：Saga Pattern 保证分布式一致性**
```
用户下单 → 同步创建 Order (PENDING)
         → 发送事件到 Kafka
         → 库存服务消费、扣减、回调确认
         → Order 状态 → CONFIRMED
```

**❌ 错误：事件驱动系统忽略消息顺序**
```
用户账户: 创建 → 充值 → 消费
若乱序处理 "消费" 先到 → 余额为负
解决: Kafka partition key = user_id (保证同用户有序)
```

---

### Staff 工程师视角 / Staff Engineer Lens

在实际系统中，两种架构**共存**才是常态：

```
前端请求 ──▶ API Gateway (同步，低延迟)
                │
                ├── Auth Service (同步，必须)
                ├── Core Business Logic (同步)
                └── Side Effects ──▶ Kafka (异步)
                                      ├── Audit Log Service
                                      ├── Analytics Pipeline
                                      ├── Email Notification
                                      └── Cache Invalidation
```

**决策框架（面试时说这个）：**
1. 用户需要**立即知道结果**吗？→ 同步
2. 操作是**核心业务**还是**副作用**？→ 副作用用异步
3. 需要**扇出**给多个下游？→ 事件驱动
4. 需要**峰值削峰**？→ 消息队列

---

### 📚 深度资料 / References

- [Martin Fowler: Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [AWS: Choosing between messaging services](https://aws.amazon.com/compare/the-difference-between-sqs-sns-and-eventbridge/)
- [Confluent: Event-Driven Microservices](https://www.confluent.io/blog/event-driven-microservices-with-kafka/)

### 🧒 ELI5

你去餐厅吃饭：
- **请求-响应** = 服务员站你旁边等你点餐，你说什么，他马上记下来（同步）
- **事件驱动** = 你把菜单投进一个槽里，厨房各部门各自看到自己该做什么（异步，松耦合）

大餐厅（高流量系统）两种都要用！
