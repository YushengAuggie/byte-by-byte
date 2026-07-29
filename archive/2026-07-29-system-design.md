# 系统设计综合 / System Design Synthesis — Day 103

## 🏗️ 系统设计 / System Design (Expert Synthesis)

### 跨系统权衡综合：一致性 vs 可用性 vs 分区容错 — 真实场景决策指南
### Cross-System Synthesis: Consistency vs Availability vs Partition Tolerance — Real-World Decision Guide

---

你已经学过 60 个系统设计主题。今天我们退一步，从更高的视角来看：**在真实的生产系统中，你如何在设计时做出那些最关键的取舍决策？**

You've studied 60 system design topics. Today we step back and look from higher ground: **how do you make the most critical trade-off decisions when designing real production systems?**

---

### 🗺️ 大图景：所有系统的共同压力
### The Big Picture: Forces Acting on Every System

```
所有分布式系统都处于三个张力之间：
All distributed systems sit under three tensions:

      ┌─────────────────────────────────────────┐
      │           PARTITION TOLERANCE            │
      │           分区容错（必须接受）              │
      │         (you must accept this)            │
      └──────────────┬──────────────────┬────────┘
                     │                  │
         ┌───────────▼───┐        ┌─────▼──────────┐
         │  CONSISTENCY  │        │  AVAILABILITY  │
         │    一致性      │   VS   │    可用性       │
         │  (all nodes   │        │ (always respond│
         │  see same data│        │  even if stale)│
         └───────────────┘        └────────────────┘
```

**CAP 定理说**：网络分区时，你只能二选一。  
**CAP theorem says**: during a network partition, you pick one.

---

### 🔍 案例对比：你见过的六个真实系统
### Case Study Matrix: Six Systems You've Already Seen

| 系统 System | 选择 Choice | 为什么 Why |
|-------------|------------|-----------|
| 银行支付 (Stripe) | CP — 强一致性 | 不能丢钱，宁可返回错误 |
| 购物车 (Amazon) | AP — 最终一致性 | 加购失败比超卖更影响转化 |
| DNS | AP | 全球可用性 > 立即一致 |
| Google Docs (OT) | AP + CRDT | 离线编辑，自动合并冲突 |
| 库存系统 (Ticketmaster) | CP | 超卖比停服损失更大 |
| 社交 Feed (Twitter) | AP | 看到旧推文没关系 |

---

### 🧩 决策框架：三个问题定方向
### Decision Framework: Three Questions That Determine Architecture

**1. 数据不一致的代价是什么？**  
**1. What's the cost of stale data?**
- 金钱损失 / money lost → 选 CP
- 用户体验略差 / minor UX degradation → 选 AP

**2. 停服的代价是什么？**  
**2. What's the cost of being unavailable?**
- 无法关键操作 → 选 AP（能降级服务）
- 错误比停服更可接受 → 选 CP

**3. 数据更新频率和冲突概率？**  
**3. How often is data updated, and by how many writers?**
- 高写入冲突 → 需要乐观锁或 CRDT
- 低冲突 / append-only → 最终一致性很安全

---

### 🔗 关键模式回顾：真实系统如何实现"两全其美"
### How Real Systems Achieve Both (Almost)

**Multi-region active-active（你学过第 54 天）**：
- 每个区域优先读本地（高可用）
- 写入通过 CRDTs 或 last-write-wins 跨区域同步
- 关键操作（支付）路由到单一 leader

**读写分离 + 异步复制（缓存课 Day 6）**：
- 读从 replica（AP），写到 primary（CP）
- 接受副本延迟，用 cache-aside + TTL 兜底

**Saga 模式（支付系统 Day 38）**：
- 长事务拆成多步，每步有补偿操作
- 用最终一致性代替分布式锁

---

### ❌ 常见错误 / Common Mistakes

**错误 1**：面试时说"我要强一致性"，却没说清楚成本  
→ 强一致性 = 更高延迟 + 更复杂的协调 + 更差的可用性

**错误 2**：把"最终一致性"当做"不用设计"  
→ 最终一致 = 你必须设计 **何时一致、冲突如何解决、用户看到旧数据的 UX**

**错误 3**：忘记 CAP 只在分区时才需要二选一  
→ 平时可以两全，只有网络断了才 forced trade-off

---

### 📚 References
- https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html
- https://jepsen.io/consistency

### 🧒 ELI5
想象你和室友合用一个购物清单。如果你们必须每次都确认对方看到了更新（强一致性），那出门前要等很久。如果你们各自记各自的再回来合并（最终一致性），效率高但可能买了两份牛奶。系统设计就是决定你们家买牛奶的策略。

Imagine you and a roommate share a shopping list. If you always wait for each other to confirm every update (strong consistency), you spend forever before leaving. If you each keep notes and merge later (eventual consistency), you're faster but might buy two milks. System design is deciding your household's milk-buying strategy.
