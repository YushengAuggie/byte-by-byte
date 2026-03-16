# 🏗️ 系统设计 Day 3 / System Design Day 3
**HTTP/HTTPS & REST APIs**
*Category: Fundamentals | Difficulty: Beginner | Phase: Foundation*

---

## 想象你在设计... / Imagine You're Building...

想象你是一家餐厅的服务员。客人（浏览器）坐下来，告诉你他想要什么（HTTP请求），你去厨房（服务器）取回食物，然后送回来（HTTP响应）。这就是HTTP的本质——一种双方约定好的"点餐协议"。

Imagine you're a waiter at a restaurant. The customer (browser) tells you what they want (HTTP request), you go to the kitchen (server), and bring back the food (HTTP response). That's HTTP in a nutshell — a standardized "ordering protocol" both sides agree on.

---

## 架构图 / Architecture Diagram

```
  CLIENT (Browser/App)
        │
        │  HTTP Request
        │  GET /api/users/123
        │  Headers: {Authorization: "Bearer token..."}
        ▼
  ┌─────────────────────┐
  │    LOAD BALANCER     │
  │  (distributes load)  │
  └──────┬──────┬────────┘
         │      │
         ▼      ▼
  ┌──────────┐ ┌──────────┐
  │ Server 1 │ │ Server 2 │   ← Stateless REST servers
  └──────┬───┘ └──────┬───┘
         │             │
         └──────┬──────┘
                ▼
        ┌───────────────┐
        │   DATABASE    │
        │  (source of   │
        │    truth)     │
        └───────────────┘
                │
        HTTP Response
        200 OK
        {"id": 123, "name": "Alice"}
        │
        ▼
  CLIENT receives data
```

---

## HTTP vs HTTPS — 核心区别 / Core Difference

**HTTP** — HyperText Transfer Protocol
- 明文传输，数据可被中间人截获
- Plaintext transmission; data can be intercepted

**HTTPS** — HTTP + TLS/SSL 加密
- 所有数据加密传输，第三方无法读取内容
- All data encrypted; third parties can't read the content
- 通过证书验证服务器身份（你真的是在和 google.com 说话吗？）
- Certificate verifies server identity (are you really talking to google.com?)

```
HTTP:   你的密码 → [网络] → 服务器       ← 路由器能看到！
HTTPS:  你的密码 → [加密] → [网络] → [解密] → 服务器  ← 中间人只看到乱码
```

---

## REST API — 六个约束 / Six Constraints

REST (Representational State Transfer) 不是技术，是一套设计风格：

1. **Stateless（无状态）** — 服务器不记住你。每个请求自带所有信息。
   Server doesn't remember you. Each request carries all needed info.

2. **Client-Server（客户端-服务器分离）** — 前端和后端独立演化。
   Frontend and backend evolve independently.

3. **Cacheable（可缓存）** — 响应可以被缓存，减少重复请求。
   Responses can be cached to reduce redundant requests.

4. **Uniform Interface（统一接口）** — 用标准HTTP方法操作资源。
   Use standard HTTP verbs to manipulate resources.

5. **Layered System（分层系统）** — 客户端不关心中间有几层。
   Client doesn't care how many layers exist in between.

6. **Code on Demand (Optional)** — 服务器可返回可执行代码（如JS）。
   Server can return executable code (e.g., JavaScript).

---

## HTTP 方法 CRUD 对应关系 / HTTP Methods → CRUD

```
HTTP Method    CRUD Operation    Example
──────────────────────────────────────────────────
GET            Read              GET /users/123
POST           Create            POST /users  {body}
PUT            Replace (全量)    PUT /users/123  {full body}
PATCH          Update (部分)     PATCH /users/123 {partial}
DELETE         Delete            DELETE /users/123
```

**状态码速查 / Status Code Cheat Sheet:**
```
2xx  ✅  成功 / Success
  200 OK           — 请求成功
  201 Created      — 资源已创建
  204 No Content   — 成功但无返回体

3xx  ↩️  重定向 / Redirect
  301 Moved Permanently  — 永久跳转
  304 Not Modified       — 用缓存

4xx  ❌  客户端错误 / Client Error
  400 Bad Request    — 你的请求有问题
  401 Unauthorized   — 没登录
  403 Forbidden      — 登录了但没权限
  404 Not Found      — 资源不存在
  429 Too Many Reqs  — 限流了

5xx  💥  服务器错误 / Server Error
  500 Internal Server Error — 服务器崩了
  503 Service Unavailable   — 服务不可用
```

---

## 为什么这样设计？/ Why This Design?

**为什么REST选择无状态（Stateless）？**

如果服务器记住每个用户的状态，那扩展到100台服务器时，你必须确保每次请求都打到同一台机器（叫做"粘性会话"sticky session）。这非常麻烦。

无状态的好处：任何服务器都能处理任何请求，水平扩展极其简单。

If servers remembered user state, scaling to 100 servers would require routing each user to the same server every time ("sticky sessions") — a maintenance nightmare. Stateless = any server can handle any request = horizontal scaling is trivial.

---

## 别踩这个坑 / Don't Fall Into This Trap

**坑 1: 在GET请求中修改数据**
```
❌  GET /deleteUser?id=123    # 语义错误，GET应该是只读的
✅  DELETE /users/123
```

**坑 2: 用动词命名资源（URL应该是名词）**
```
❌  POST /createUser
❌  GET  /getUserById?id=123
✅  POST /users
✅  GET  /users/123
```

**坑 3: 忘记区分401和403**
```
401 Unauthorized → "你是谁？请先登录" (Who are you? Please log in)
403 Forbidden    → "我知道你是谁，但你没权限" (I know who you are, but you can't)
```

**坑 4: 滥用200 OK返回错误信息**
```
❌  200 OK  {"error": "User not found"}   # 前端要额外解析body判断成功失败
✅  404 Not Found  {"message": "User not found"}
```

---

## 与昨天的联系 / Connection to Day 2

昨天我们学了DNS和TCP/IP。现在你明白了完整链路：

1. 你在浏览器输入 `https://api.example.com/users`
2. **DNS** 解析域名 → IP地址
3. **TCP** 建立连接（三次握手）
4. **TLS** 握手，建立加密通道（HTTPS）
5. **HTTP** 发送请求，服务器返回响应
6. 浏览器渲染数据

Yesterday we covered DNS and TCP/IP. Now you see the full picture: DNS → TCP → TLS → HTTP → response. Each layer builds on the one before it.

---

*Day 3 | 系统设计基础系列 | 明天：数据库基础*
