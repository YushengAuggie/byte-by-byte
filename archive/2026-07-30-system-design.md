# 🏗️ 系统设计 / System Design — Day 104 (Synthesis)
**Date:** 2026-07-30 | **Phase:** Expert

---

## 综合对比：分布式系统的四大核心权衡
## Synthesis: The Four Core Trade-offs of Distributed Systems

经过前60个系统设计主题，我们反复看到同样的权衡模式。今天把它们系统化。  
After 60 system design topics, the same trade-off patterns keep recurring. Let's systematize them.

---

### 权衡一：一致性 vs 可用性 (CAP Theorem in Practice)
### Trade-off 1: Consistency vs Availability

```
强一致性 (Strong Consistency)          最终一致性 (Eventual Consistency)
─────────────────────────────────────────────────────────
银行转账 ✅                              社交媒体点赞 ✅
库存扣减 ✅                              DNS 缓存 ✅
订单状态 ✅                              推荐系统 ✅

代价：高延迟，单点协调                   代价：脏读窗口，冲突解决复杂
Cost: Higher latency, coord overhead    Cost: Stale reads, conflict resolution
```

**实战教训 / Lessons from the field:**
- Stripe 支付：写入用 2PC → 读取走 replica（最终一致 for 报表）
- Twitter 时间线：fanout 是最终一致的，但用户自己的推文立即可见（read-your-own-writes）
- 设计时先问："这个操作如果丢了/重复了，代价是什么？"

---

### 权衡二：推模式 vs 拉模式 (Push vs Pull)
### Trade-off 2: Push vs Pull

```
Push (Server → Client)          Pull (Client → Server)
────────────────────────────────────────────────────────
WebSocket, SSE, WebHooks        Polling, REST GET

低延迟，实时推送                  简单，客户端控制频率
适合：聊天、股票行情               适合：邮件检查、分页加载

问题：N 个订阅者 = N 个连接        问题：空轮询浪费资源
Fan-out 大时崩溃（Twitter 名人）  Long polling 折中方案
```

**混合策略 / Hybrid Strategy:** Slack 用 WebSocket for real-time + REST for history fetch。设计聊天/通知系统时几乎总是混用。

---

### 权衡三：计算在哪里 (Where to Compute)
### Trade-off 3: Where to Put the Compute

```
客户端 → 边缘/CDN → 应用层 → 数据库
Client   Edge       App       DB
```

| 决策 | 对应场景 |
|------|----------|
| 数据库计算 (SQL aggregation) | 简单统计，数据不出库 |
| 应用层计算 | 业务逻辑复杂，DB 是瓶颈 |
| 边缘计算 (Edge Functions) | 个性化、A/B 测试、地理路由 |
| 客户端计算 | 表单验证、本地搜索 |

**经验法则 / Rule of thumb:** 数据量大 → 把计算推向数据。用户多 → 把计算推向边缘。

---

### 权衡四：同步 vs 异步 (Sync vs Async)
### Trade-off 4: Synchronous vs Asynchronous

```
同步调用链                    消息队列异步
A → B → C → D               A → Queue → B, C, D (并行)
                                         ↓
延迟叠加 (latency chain)      解耦，可重试，背压控制
单点失败导致全链失败           消费者可独立扩容
```

**何时必须同步 / When sync is required:**
- 用户等待结果（支付确认）
- 顺序依赖（步骤2依赖步骤1的输出）

**何时应该异步 / When to go async:**
- 发邮件、发通知
- 数据分析、报告生成
- 图片/视频处理

---

### 综合架构模式 / The Meta-Pattern

```
                    ┌─────────────────────────────────┐
                    │   系统设计决策树 / Decision Tree   │
                    └─────────────────────────────────┘
                              ↓
                    规模有多大？(Scale?)
                   /                    \
              < 10M DAU               > 10M DAU
                  ↓                       ↓
           单体 + Postgres         拆服务 + 专用存储
           Monolith + RDS          Microservices + Specialized DBs
                                          ↓
                                   写多 or 读多？
                                  /            \
                               写多            读多
                            CQRS/Event         读副本 +
                            Sourcing           缓存层
```

---

### 🧒 ELI5
系统设计其实就是在问：数据存在哪？谁先知道？谁来算？出错了怎么办？把这四个问题想清楚，大部分设计就出来了。  
System design is really just asking: Where does data live? Who knows first? Who does the math? What happens when things break? Answer those four and most designs follow.

---

### 📚 References
- [Designing Data-Intensive Applications (Kleppmann)](https://dataintensive.net/)
- [CAP Theorem Explained — Brewer's original talk](https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf)
- [Martin Fowler on Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
