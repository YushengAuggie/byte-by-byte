# 🏗️ 系统设计 / System Design — Day 34
## 设计分布式任务队列 / Design a Distributed Task Queue (Celery)
> Mastery Phase · ~3 min read

---

### 🎯 场景 / Real-World Scenario

想象你在设计 **Instagram 的后处理流水线** — 用户上传一张照片，系统需要：
- 生成多个分辨率的缩略图（异步，不阻塞上传响应）
- 运行内容审核 AI
- 更新搜索索引
- 发送通知给关注者

这些操作不能在 HTTP 请求里完成，需要一个任务队列系统。

Imagine you're designing **Instagram's post-processing pipeline** — when a user uploads a photo, the system needs to generate thumbnails, run content moderation AI, update search indexes, and send follower notifications — all without blocking the upload response.

---

### 🏛️ 架构图 / Architecture Diagram

```
Producers (Web Servers)
    |
    v
[Message Broker]  ← Redis / RabbitMQ / SQS
    |         |
    v         v
[Worker Pool 1]  [Worker Pool 2]   ← Celery workers
(image resize)   (send email)
    |
    v
[Result Backend]  ← Redis / DB (optional)
    |
    v
[Monitoring]  ← Flower / Prometheus
```

**核心组件：**
- **Producer（生产者）**：Web 服务器把任务序列化后推入队列
- **Broker（消息代理）**：Redis 或 RabbitMQ，存储待处理任务
- **Workers（工作进程）**：多个进程消费任务，可独立扩容
- **Result Backend（结果后端）**：可选，存储任务执行结果

---

### ⚖️ 关键权衡 / Key Tradeoffs

**为什么用 Redis 而不是 RabbitMQ？**

| | Redis | RabbitMQ |
|---|---|---|
| 优点 | 简单、快、同时做缓存 | 消息持久化更可靠 |
| 缺点 | 内存受限，消息可能丢失 | 运维复杂度高 |
| 适用 | 任务可重试，丢失可接受 | 金融/计费等不容丢失 |

**任务幂等性（Idempotency）**：Worker 崩溃后任务会重试，所以任务必须是幂等的 — 执行两次和执行一次效果相同。

**优先级队列**：重要任务（如付费用户）用高优先级队列，避免被低优先级任务堵塞。

---

### 🔥 常见错误 / Common Mistakes

**别踩这个坑 ⚠️**

1. **把大对象放进任务参数** — 任务只传 ID，不传整个 object：
   ```python
   # ❌ Wrong
   process_image.delay(full_image_bytes)
   
   # ✅ Right
   process_image.delay(image_id=123)  # worker fetches from S3
   ```

2. **忘记设置 task_acks_late** — 默认任务在开始执行时就从队列删除，崩溃后丢失：
   ```python
   app.conf.task_acks_late = True  # ack only after success
   ```

3. **没有死信队列（Dead Letter Queue）** — 持续失败的任务应移入 DLQ 而不是无限重试

4. **在任务里做同步 HTTP 请求** — Worker 被阻塞，吞吐量暴降。用异步或专用 I/O worker

---

### 📊 扩容策略 / Scaling

- **水平扩展**：加 Worker 节点（无状态，k8s 一行搞定）
- **队列隔离**：不同任务类型用不同队列，避免慢任务阻塞快任务
- **Autoscaling**：根据队列深度（queue depth）自动增减 Worker 数量

---

### 📚 References
- https://docs.celeryq.dev/en/stable/userguide/tasks.html
- https://redis.io/docs/manual/pubsub/
- https://aws.amazon.com/sqs/

### 🧒 ELI5
任务队列就像餐厅的点菜单 — 顾客（服务器）把订单（任务）贴到厨房（队列），厨师（Worker）按顺序做菜，做完告诉服务员。顾客不用等厨师做完，下一单继续。

A task queue is like a restaurant order system — the waiter (server) puts orders on a board (queue), chefs (workers) cook them in order. The waiter doesn't wait for each dish before taking the next order.
