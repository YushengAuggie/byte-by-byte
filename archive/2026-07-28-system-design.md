# 🏗️ 系统设计综合 / System Design Synthesis — Day 102

> **Expert Synthesis:** 今天不介绍新题目，而是跨越我们学过的系统进行横向对比。

---

## 横向对比：数据一致性 vs 可用性的权衡 / Cross-System: Consistency vs Availability Trade-offs

你已经学了 60 个系统设计题。今天回答一个真正的专家问题：

**面试官问："你如何在系统设计中选择一致性策略？"**

This is the question that separates Staff engineers from senior engineers.

---

## 框架：按业务影响分级 / Tiered by Business Impact

```
                    一致性要求 (Consistency Requirement)
                    强 ◄───────────────────────► 最终

金融/支付系统          ✅ Strong Consistency
(Payment, Banking)    Stripe, Order Matching Engine
                      → 两阶段提交, XA, Saga (串行)

用户数据/配置          ✅ Read-your-writes
(Profile, Settings)   Chat System, Feature Flags
                      → Leader读, 粘性Session

社交/推荐              ✅ Eventual Consistency
(Feed, Likes, Views)  YouTube, Twitter, Recommendation
                      → 异步复制, CRDT, 读修复

缓存/统计              ✅ Best Effort
(Counters, Metrics)   CDN, Monitoring, Autocomplete
                      → TTL失效, 近似值
```

---

## 真实案例对比 / Real-World Pattern Comparison

### 🔴 强一致性：支付系统 vs 分布式锁

| 系统 | 一致性机制 | 代价 |
|------|-----------|------|
| Stripe (Payment) | Saga + Idempotency Keys | 延迟高，需幂等 |
| Zookeeper/etcd (Lock) | Raft 共识 | Leader 瓶颈 |
| Order Matching Engine | 单线程队列 | 水平扩展困难 |

**核心洞察 / Key Insight:**  
强一致性通常意味着**序列化**（单点或全局锁）。当你引入分布式时，要么接受延迟，要么接受复杂性。

---

### 🟡 因果一致性：聊天系统 vs 协作编辑器

| 系统 | 一致性机制 | 用户感知 |
|------|-----------|---------|
| WhatsApp (Chat) | 消息顺序 + 已读回执 | 消息不乱序 |
| Google Docs (Collab) | OT / CRDT | 合并冲突透明 |

**为什么 Chat 不需要 Strong Consistency？**  
因为消息送达的顺序在不同设备间可以有微小差异（1-2秒），用户不会注意到。但如果消息丢失，用户一定会发现。→ **高可用性优先，因果顺序次之。**

---

### 🟢 最终一致性：YouTube vs Recommendation Engine

```
YouTube 播放量计数:
User View → Kafka → Counter Service → Approximate Count
                                     (±0.1% is fine)

Recommendation:
User Action → Feature Store (async) → Model (stale is OK)
             (30min lag acceptable for personalization)
```

**为什么最终一致性够用？**  
推荐系统的"正确答案"本身就是模糊的。没人知道"正确"推荐是什么，所以数据滞后 30 分钟也不影响用户体验。

---

## 专家决策树 / Expert Decision Tree

```
面对一个新系统，问自己:

1. 数据不一致会导致金钱损失吗？
   → YES → Strong Consistency (Saga / 2PC / Single-leader)
   → NO  → 继续

2. 用户能察觉到数据过期吗（< 1 秒）？
   → YES → Read-your-writes / Session Consistency
   → NO  → 继续

3. 数据冲突可以自动合并吗？
   → YES → CRDT / Eventual Consistency
   → NO  → Last-Write-Wins + Conflict Resolution UI
```

---

## 常见面试陷阱 / Common Interview Traps

**❌ 错误回答：** "我会用强一致性保证正确性"  
→ 面试官追问："那你的系统怎么扩展？"你就没话说了。

**✅ 正确思路：**  
"这个系统的核心业务操作（X）需要强一致性，但（Y 和 Z）可以接受最终一致性。我会用 Saga 模式处理 X，用异步事件总线处理 Y/Z。"

---

## 📚 参考资料 / References

- [Consistency Models — Jepsen](https://jepsen.io/consistency)
- [Designing Data-Intensive Applications — Kleppmann](https://dataintensive.net/)
- [AWS re:Invent — Patterns for Distributed Systems](https://www.youtube.com/results?search_query=aws+reinvent+consistency+patterns)

## 🧒 ELI5

想象你和朋友在不同城市共享一个 Google Sheet。

- **强一致性** = 每次编辑都要对方确认才保存（超慢，超准）
- **最终一致性** = 你们各自编辑，等网络好了再合并（快，偶尔有冲突）
- **现实** = Google Docs 用的是"操作变换"（OT），既快又尽量准。

Strong consistency is like waiting for your friend to say "OK" before every edit. Eventually consistent is editing freely and syncing later. Real systems pick something in between.
