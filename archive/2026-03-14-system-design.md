# System Design Day 1 — Client-Server Model & How the Internet Works
*Date: 2026-03-14 | Category: Fundamentals | Difficulty: Beginner*

---

🏗️ **系统设计 Day 1 / System Design Day 1**
**客户端-服务器模型 & 互联网是怎么运转的**
**Client-Server Model & How the Internet Works**

---

想象你在一家餐厅点餐。你（客户端）告诉服务员（网络）你想要什么，厨房（服务器）接到订单后准备好食物，再通过服务员把食物送到你面前。互联网的每一次请求，都是这个流程的数字版本。

*Imagine you're ordering food at a restaurant. You (the client) tell the waiter (the network) what you want, the kitchen (the server) prepares it, and the waiter brings it back. Every internet request follows this exact same flow — digitally.*

---

**架构图 / Architecture Diagram**

```
你的浏览器 / Your Browser
        |
        | HTTP Request (GET /index.html)
        v
+-------+--------+
|   DNS Resolver  |   "把 google.com 翻译成 IP 地址"
|  (Phone book)   |   "Translates domain → IP address"
+-------+--------+
        |
        | IP: 142.250.80.46
        v
+-------+--------+
|    Internet     |   路由器、交换机、光缆
|  (The pipes)    |   Routers, switches, fiber cables
+-------+--------+
        |
        v
+-------+--------+
|  Web Server     |   nginx / Apache
|  (The waiter)   |   Receives your request
+-------+--------+
        |
        v
+-------+--------+
| App Server      |   Node.js / Django / Spring
| (The kitchen)   |   Runs your business logic
+-------+--------+
        |
        v
+-------+--------+
|   Database      |   PostgreSQL / MySQL / MongoDB
|  (The pantry)   |   Stores & retrieves data
+-------+--------+
        |
        | HTTP Response (200 OK + HTML)
        v
你的浏览器渲染页面 / Browser renders the page
```

---

**关键概念 / Key Concepts**

**1. IP 地址 — 互联网的门牌号**
每台联网设备都有一个 IP 地址，就像你家的门牌号。
`IPv4: 192.168.1.1` (4组数字，已快耗尽)
`IPv6: 2001:0db8:85a3::8a2e:0370:7334` (新标准，几乎无限)

*Every device on the internet has an IP address — like a postal address for packets.*

**2. DNS — 互联网的电话簿**
你记 `google.com`，但计算机需要 `142.250.80.46`。DNS 负责翻译。
解析顺序：浏览器缓存 → 系统缓存 → 本地 DNS 服务器 → 根域名服务器

*You type `google.com`, DNS translates it to an IP. Without DNS, you'd memorize numbers for every website.*

**3. HTTP/HTTPS — 请求的语言**
```
GET  /api/users        → 获取资源 / Fetch resource
POST /api/users        → 创建资源 / Create resource
PUT  /api/users/1      → 更新资源 / Update resource
DELETE /api/users/1    → 删除资源 / Delete resource
```
HTTPS = HTTP + TLS 加密。没有 HTTPS，你的数据在网络上是明文。

**4. TCP/IP — 可靠传输的保障**
TCP 保证数据包完整到达，就像注册邮件（有回执）。
UDP 不保证，但更快，适合视频流、游戏（偶尔丢帧没关系）。

---

**为什么这样设计？/ Why This Design?**

客户端-服务器分离的核心好处：

- **可扩展性**：可以独立扩展服务器（加机器），不影响客户端
- **安全性**：数据库不暴露给互联网，只有应用服务器能访问
- **可维护性**：前端、后端、数据库各自独立部署

*Separation of concerns: clients handle presentation, servers handle logic and data. This lets you scale, secure, and maintain each layer independently.*

---

**别踩这个坑 / Don't Fall Into This Trap**

❌ **面试时说「用户点击按钮，数据就存到数据库了」**
这跳过了太多层。面试官想听到：
DNS解析 → TCP握手 → HTTP请求 → 负载均衡 → 应用服务器 → 数据库

✅ **学会分层描述系统**
每次系统设计，先画出这张图的骨架，再逐层深入。

*In interviews, never skip layers. "The user clicks a button and data gets saved" misses: DNS, TCP handshake, load balancers, app servers, caching, and database transactions. Walk through every hop.*

---

**明日预告 / Tomorrow**
Day 2 将深入 **负载均衡** — 当一台服务器不够用时，如何优雅地横向扩展。
*Day 2 covers Load Balancing — what happens when one server isn't enough.*
