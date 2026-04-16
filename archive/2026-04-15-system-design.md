# 🏗️ 系统设计 / System Design — Day 21: Design a Notification System

> 📊 Day 24 | Phase: Growth | Topic: System Design Problems

---

## 想象这个场景 / The Scenario

想象你在 Airbnb 工作。用户订了一个民宿，系统需要同时发送：
- 📱 Push notification（App 通知）
- 📧 Email（预订确认）
- 💬 SMS（支付成功短信）

You're at Airbnb. A user books a listing — the system needs to simultaneously send a push notification, confirmation email, and SMS payment receipt. How do you design this at scale?

---

## 架构图 / Architecture Diagram

```
Clients (iOS/Android/Web)
          │
          ▼
    [API Gateway]
          │
          ▼
  [Notification Service]
     /     |      \
    ▼      ▼       ▼
[Push]  [Email]  [SMS]
Worker  Worker   Worker
  │       │        │
  ▼       ▼        ▼
[APNS] [SendGrid] [Twilio]
[FCM]

          ▲
  [Message Queue]  ←── [Event Sources]
  (Kafka/SQS)          (Order Service,
                        Payment Service,
                        etc.)

  [Notification DB]  ←── stores delivery status
  [User Preference]  ←── opt-in/out per channel
  [Rate Limiter]     ←── prevent spam
```

---

## 核心设计决策 / Key Design Decisions

### 1. 为什么用消息队列？/ Why Message Queue?

**问题 / Problem:** 通知系统是下游依赖 — 如果 Email 服务挂了，不应该影响核心业务流程（下单、支付）。  
**解法 / Solution:** 用 Kafka/SQS 解耦生产者和消费者。生产者（订单服务）发消息就完事，消费者（通知工作进程）异步处理。

> **关键权衡 / Key Tradeoff:** 异步 = 高可用 + 高吞吐，但牺牲了实时性（最终一致）。对通知场景完全可接受。

### 2. 用户偏好表 / User Preference Table

```sql
CREATE TABLE user_notification_preferences (
  user_id       BIGINT,
  channel       ENUM('push', 'email', 'sms'),
  notification_type VARCHAR(50),  -- 'marketing', 'transactional'
  enabled       BOOLEAN DEFAULT true,
  PRIMARY KEY (user_id, channel, notification_type)
);
```

发送前先查这张表 — 用户关闭了营销邮件就别发。  
Check this table before sending — respect user opt-outs.

### 3. 幂等性 / Idempotency

Worker 崩溃重启后可能重复发送 → 每条通知有唯一 `notification_id`，发送成功后写入 DB。再次处理时先查 DB，已发送则跳过。

Worker restarts may cause duplicate sends → each notification has a unique `notification_id`. Mark as sent in DB; skip if already delivered.

### 4. 推送三方服务 / Third-Party Push Services

- **iOS:** Apple Push Notification Service (APNS)
- **Android:** Firebase Cloud Messaging (FCM)
- **Email:** SendGrid / AWS SES
- **SMS:** Twilio / AWS SNS

---

## 数据量估算 / Scale Estimation

- DAU: 10M users
- 每用户每天平均 3 条通知 → 30M notifications/day
- QPS: 30M / 86400 ≈ **350 notifications/sec** (peak 5x = ~1750/sec)
- 消息队列分区 / Kafka partitions: 按 `user_id % N` 分区确保顺序

---

## 别踩这个坑 / Common Mistakes

| ❌ 错误做法 | ✅ 正确做法 |
|-----------|-----------|
| 同步发送通知（阻塞主流程）| 异步队列解耦 |
| 不记录发送状态 | 写 DB + 幂等处理 |
| 忽略用户偏好 | 发送前查 preference 表 |
| 不限速 | Rate limiter 防骚扰 |
| 只有一个推送渠道 | 失败重试 + fallback（push → SMS）|

---

## 📚 References

- https://systemdesign.one/notification-system-design/
- https://aws.amazon.com/blogs/mobile/how-to-build-a-scalable-notification-system/
- https://engineering.fb.com/2015/12/03/ios/delivering-billions-of-messages-instantly/

---

## 🧒 ELI5

想象你开了一家餐厅。厨师做好菜了，不能亲自跑去告诉每桌客人——他只需要把菜放到传菜台（消息队列），服务员（Worker）去各桌通知。有人不吃辣就不发辣的（用户偏好），菜已经送到就不再送（幂等性）。

Think of it like a restaurant. The chef (core service) puts finished dishes on a conveyor (message queue). Waiters (workers) deliver them to the right tables (push/email/SMS). If a customer said "no spicy food" (user preference), skip it. If the dish was already delivered, don't deliver again (idempotency).
