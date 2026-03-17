# 🏗️ 系统设计 Day 4 / System Design Day 4 — 负载均衡 / Load Balancing

> **基础阶段 Foundation Phase** | 预计阅读时间 ~3-4 分钟

---

## 场景引入 / Scenario

想象你开了一家超级火爆的奶茶店 🧋。第一天只有一个收银台，没问题。但第二天去大众点评上了热搜，突然排队排到门外一百米。怎么办？你开了第二个、第三个收银台，还派了一个引导员在门口，告诉每个客人该去哪个收银台排队。

这个"引导员"就是**负载均衡器（Load Balancer）**。

Imagine you open a super-popular boba tea shop. Day one: one cashier, no problem. Day two: you go viral, and there's a 100-meter queue outside. Solution? You open more cashier lanes and station someone at the entrance directing each customer to the shortest line.

That person at the entrance is your **Load Balancer**.

---

## 架构图 / Architecture Diagram

```
                        ┌─────────────────────────────┐
                        │         用户请求             │
                        │     Incoming Requests        │
                        └──────────────┬──────────────┘
                                       │
                                       ▼
                        ┌─────────────────────────────┐
                        │       Load Balancer          │
                        │     负载均衡器               │
                        │  (Nginx / AWS ALB / HAProxy) │
                        └───────┬──────┬──────┬───────┘
                                │      │      │
                     ┌──────────┘      │      └──────────┐
                     ▼                 ▼                  ▼
              ┌────────────┐  ┌────────────┐  ┌────────────┐
              │  Server 1  │  │  Server 2  │  │  Server 3  │
              │  服务器 1  │  │  服务器 2  │  │  服务器 3  │
              │  ████████  │  │  ████      │  │  ██        │
              │ (80% load) │  │ (40% load) │  │ (20% load) │
              └────────────┘  └────────────┘  └────────────┘
                                       │
                        ┌──────────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │   Shared Database   │
              │    共享数据库        │
              └─────────────────────┘
```

---

## 核心概念 / Key Concepts

### 负载均衡算法 / Load Balancing Algorithms

**1. Round Robin（轮询）**
- 依次把请求分给每台服务器，循环往复
- 类比：收银台依次叫号
- 适用：服务器性能相同、请求处理时间相近的场景

**2. Weighted Round Robin（加权轮询）**
- 性能强的服务器分配更多请求（权重更高）
- 类比：有个收银员超快，就多给她排队
- 适用：服务器配置不均匀的场景

**3. Least Connections（最少连接）**
- 把新请求分给当前连接数最少的服务器
- 类比：去排队最短的那个收银台
- 适用：请求处理时长差异大的场景（如文件上传 vs 简单查询）

**4. IP Hash（IP 哈希）**
- 根据客户端 IP 地址决定路由到哪台服务器
- 同一个用户总是被路由到同一台服务器
- 适用：需要会话粘性（Session Stickiness）的场景

### 为什么这样设计？/ Why This Design?

| 目标 Goal | 解决方案 Solution |
|----------|-----------------|
| 高可用 High Availability | 一台服务器挂了，流量自动转移 |
| 水平扩展 Horizontal Scaling | 加新服务器，不改代码 |
| 性能 Performance | 避免单点瓶颈，减少响应时间 |
| 健康检查 Health Checks | LB 自动剔除故障节点 |

### 两种类型 / Two Types

**Layer 4 (Transport Layer) LB**
- 基于 IP + TCP/UDP 端口路由
- 速度快，但"看不懂"请求内容
- 类比：只看信封地址，不看信的内容

**Layer 7 (Application Layer) LB**
- 基于 HTTP 头、URL、Cookie 等路由
- 更智能（可以把 `/api` 路由到 API 服务器，把 `/static` 路由到 CDN）
- 类比：根据信的内容决定投递给哪个部门
- 性能稍低，但灵活得多

---

## 别踩这个坑 / Don't Fall Into This Trap

### 坑 1：有状态的服务器（Stateful Servers）

❌ **错误做法：** 把用户 Session 存在单台服务器的内存里
```
用户第1次请求 → Server 1 (Session 存在这里)
用户第2次请求 → Server 2 (找不到 Session！用户被登出)
```

✅ **正确做法：** Session 外置到共享存储
```
用户第1次请求 → Server 1 → 把 Session 写入 Redis
用户第2次请求 → Server 2 → 从 Redis 读 Session ✓
```

**关键原则：服务器要做到"无状态"(Stateless)，所有状态都存外部！**

### 坑 2：负载均衡器自身成为单点故障

如果 LB 本身挂了怎么办？

✅ **解决方案：** 部署主备 LB（Active-Passive）或使用 DNS 轮询 + 多 LB

### 坑 3：健康检查不够频繁

LB 依赖健康检查（Health Check）来知道哪台服务器挂了。如果检查间隔太长（比如 60s），可能有 1 分钟的流量打到死服务器上。

✅ 生产环境通常设置：每 5-10 秒一次健康检查。

---

## 延伸阅读 / Going Deeper

- 昨天（Day 3）我们聊了 HTTP/REST，现在你知道 LB 就工作在 HTTP 这一层之上
- 下周我们会聊**数据库扩展**，届时 LB 的概念还会出现（读写分离 + 连接池）
- 如果你听说过 **Nginx、HAProxy、AWS ALB/NLB**，它们都是负载均衡器的具体实现

---

*Day 4 / 100 — 系统设计基础系列 System Design Foundations*
