# 🏗️ 系统设计 / System Design — Day 28
## Design a Chat System (WhatsApp/Slack)

> **难度 / Difficulty:** Advanced | **阶段 / Phase:** Growth | **预计阅读 / Read time:** 3 min

---

### 🧠 真实场景 / Real-World Scenario

想象你在设计一个即时通讯系统，目标是支持 **5亿用户**，每天发送 **500亿条消息**（就像WhatsApp）。你的系统需要支持：一对一私聊、群组聊天（最多500人）、消息状态（已发送/已送达/已读）、在线状态显示、文件/图片传输。

Imagine you're designing a real-time messaging system to support **500M users** with **50B messages/day** (think WhatsApp). Requirements: 1:1 chat, group chat (up to 500 members), message status (sent/delivered/read), online presence, and file/media sharing.

---

### 📐 Architecture Overview

```
                        ┌─────────────────────────────────────┐
                        │          Client (Mobile/Web)         │
                        └──────────────┬──────────────────────┘
                                       │ WebSocket (persistent)
                        ┌──────────────▼──────────────────────┐
                        │          API Gateway / LB            │
                        └──────┬──────────────┬───────────────┘
                               │              │
              ┌────────────────▼──┐    ┌──────▼──────────────┐
              │  Chat Service     │    │  Presence Service    │
              │  (WebSocket Mgr)  │    │  (Redis Pub/Sub)     │
              └────────┬──────────┘    └──────┬───────────────┘
                       │                      │
         ┌─────────────▼──────────┐    ┌──────▼───────────────┐
         │  Message Queue (Kafka) │    │  Redis (Online State)│
         └─────────────┬──────────┘    └──────────────────────┘
                       │
         ┌─────────────▼──────────────────────────────┐
         │  Message Processor                          │
         │  - fan-out to recipients                    │
         │  - push notification if offline             │
         └───┬────────────────────────┬───────────────┘
             │                        │
    ┌────────▼──────────┐    ┌────────▼───────────────┐
    │  Message DB        │    │  Push Notification      │
    │  (Cassandra)       │    │  Service (APNs/FCM)     │
    └───────────────────┘    └────────────────────────┘

    ┌──────────────────────────────────────────────────┐
    │  Media Service                                   │
    │  - S3 for storage, CDN for delivery             │
    │  - Pre-signed URLs for upload/download          │
    └──────────────────────────────────────────────────┘
```

---

### ⚡ Key Design Decisions / 关键设计决策

#### 1. WebSocket vs HTTP Polling
**用WebSocket，不用轮询。**  
WebSocket keeps a persistent bidirectional connection — ideal for real-time messaging. HTTP long-polling (Comet) works but wastes resources. Server-Sent Events (SSE) is one-way only.

**选WebSocket的原因:** 延迟低（< 100ms），服务器可主动推送，连接复用减少握手开销。

#### 2. Message Storage: Cassandra (not MySQL)
- 写入极重 (write-heavy): 每秒数百万条消息
- 按 `(chat_id, message_id)` 分区，天然支持时间范围查询
- 高可用，无单点故障
- **Schema:**
  ```sql
  CREATE TABLE messages (
    chat_id     UUID,
    message_id  TIMEUUID,   -- sortable by time
    sender_id   UUID,
    content     TEXT,
    type        TEXT,       -- 'text', 'image', 'file'
    status      TEXT,       -- 'sent', 'delivered', 'read'
    PRIMARY KEY (chat_id, message_id)
  ) WITH CLUSTERING ORDER BY (message_id DESC);
  ```

#### 3. Message Fan-Out Strategy
For 1:1 chat: simple — push to recipient's WebSocket connection.  
For group chat (up to 500 members): **fan-out on write** via Kafka.
- Message lands in Kafka topic
- Consumer service fans out to each member's inbox
- Why Kafka? Durability, replay, and decouples producers from consumers

**群组消息扇出 (fan-out on write) vs 扇出读取 (fan-out on read):**  
Fan-out on write = 写入时复制到每人收件箱（适合中小群组）  
Fan-out on read = 读取时聚合（适合超大群组/Twitter模式）  
**500人以内：写时扇出** — 读取延迟更低，体验更好。

#### 4. Online Presence
- Use **Redis pub/sub** per user channel
- Client sends heartbeat every 5s; server marks user online in Redis with TTL=10s
- Subscribe to friend's channel to receive presence updates
- **问题:** 5亿用户在线状态 → Redis Cluster，按用户ID分片

---

### ❌ 别踩这些坑 / Common Mistakes

| ❌ 误区 | ✅ 正确做法 |
|---------|------------|
| 用MySQL存消息 | 用Cassandra/HBase — 写入QPS太高 |
| HTTP轮询实现"实时" | WebSocket长连接 |
| 同步fan-out到群成员 | 异步Kafka消费 |
| 不做消息去重 | 每条消息UUID + 客户端幂等性 |
| 媒体文件存数据库 | S3 + CDN + pre-signed URL |
| 忘记离线消息 | 推送通知 (APNs/FCM) + 消息持久化 |

---

### 🔢 Back-of-Envelope / 估算

```
DAU: 500M users
Messages per user per day: 40
Total messages/day: 20B
Peak QPS: 20B / 86400 * 2 (peak factor) ≈ 460K msg/s

Storage per message: ~100 bytes
Daily storage: 20B * 100 = 2TB/day
5-year retention: ~3.6PB (need compression + tiering)

WebSocket connections (peak): ~100M concurrent
→ Need ~10,000 chat servers (each handles ~10K connections)
```

---

### 📚 References

- [System Design Interview – WhatsApp](https://www.youtube.com/watch?v=vvhC64hQZMk) — Alex Xu walkthrough
- [How Discord Stores Billions of Messages](https://discord.com/blog/how-discord-stores-billions-of-messages) — Real Cassandra story
- [WhatsApp Architecture](https://highscalability.com/blog/2014/2/26/the-whatsapp-architecture-facebook-bought-for-19-billion.html) — HighScalability

---

### 🧒 ELI5

把聊天系统想成邮局：你发信（消息）→ 邮局（服务器）分拣 → 立刻送到收件人信箱（WebSocket）。如果收件人不在家（离线），就留张纸条（推送通知）让他回来取。Cassandra就像超大容量的信件档案室，永不丢信。

Think of it like a postal service: you drop a letter → post office (server) sorts it → delivers to recipient's mailbox instantly (WebSocket). If they're offline, leave a note (push notification). Cassandra is the giant mail archive that never loses a letter.
