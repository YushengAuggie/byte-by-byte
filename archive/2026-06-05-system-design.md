# 🏗️ 系统设计 / System Design — Day 49
## 设计协同编辑器 / Design a Collaborative Editor (Google Docs)
> ⏱️ 预计阅读时间 / Est. read time: 3 min | 难度 / Difficulty: Expert

---

## 想象你在设计... / The Scenario

想象你在设计 Google Docs：两个人同时编辑同一份文档，双方的更改应该**实时同步**，不能覆盖对方的内容。

Imagine you're building Google Docs: two users editing the same doc simultaneously, changes must sync **in real time** without overwriting each other.

这是分布式系统里最难的问题之一——**并发冲突解决**。

This is one of the hardest distributed systems problems: **concurrent conflict resolution**.

---

## 核心挑战 / Core Challenge: Operational Transformation vs CRDT

协同编辑的本质问题：用户 A 和用户 B **同时**操作同一文档，服务器收到两个冲突的变更，怎么合并？

The core problem: Users A and B make **concurrent** changes, server receives two conflicting ops. How to merge?

**两种主流方案 / Two Main Approaches:**

| 方案 | OT (Operational Transformation) | CRDT (Conflict-free Replicated Data Type) |
|------|----------------------------------|-------------------------------------------|
| 代表 | Google Docs | Figma, Linear, Notion |
| 原理 | 变换操作以适应其他操作 | 数学上保证自动合并 |
| 复杂度 | 实现复杂，服务器有序 | 实现较简单，去中心化 |

---

## 架构图 / Architecture

```
Client A                  Server                   Client B
  │                         │                         │
  │──Op: insert("H",0)─────>│                         │
  │                         │──Op: insert("H",0)─────>│
  │<────────────────────────│<──Op: insert("W",0)─────│
  │                         │                         │
  │                   [OT Engine]                     │
  │                  transform ops                    │
  │                  → final order                    │
  │                         │                         │
  │<──broadcast final op────│──broadcast final op────>│

┌─────────────────────────────────────────────────────┐
│                   Architecture                      │
│                                                     │
│  WebSocket Gateway ──► Op Queue (Kafka)             │
│       │                    │                        │
│  Presence Service     OT/CRDT Engine                │
│  (who's editing)           │                        │
│                      Document Store                 │
│                      (PostgreSQL + snapshots)       │
│                            │                        │
│                      Version History                │
│                      (immutable log)                │
└─────────────────────────────────────────────────────┘
```

---

## 关键设计决策 / Key Design Decisions

### 1. OT 的工作原理
```
初始状态: "HELLO"

用户A: delete(0, 1)  → "ELLO"
用户B: insert("!", 5) → "HELLO!"

同时到达服务器，需要 transform:
  A 先执行: "ELLO"
  B 的 insert(5) → transform → insert(4): "ELLO!"  ✅
```

### 2. 文档存储策略
- **不存最终状态**，而是存**操作日志 (operation log)**
- 定期生成**快照 (checkpoint)**，加速重建
- 版本 = `(clientId, clock)` — 逻辑时钟，非物理时间

### 3. 实时传输: WebSocket
- HTTP 轮询延迟太高，Server-Sent Events 单向
- WebSocket 双向，持久连接，适合协作场景

---

## 为什么这样设计 / Why This Design?

**OT vs CRDT 选择**：
- Google Docs 用 OT，需要中央服务器做变换 — 简化客户端逻辑
- CRDT 允许离线操作后合并 — Figma 和 Linear 用它，支持离线/弱网

**操作日志 vs 状态快照**：
- 存操作日志 = 完整历史，可以实现"任意版本回滚"
- 只存最新状态会丢失协作上下文

---

## 别踩这个坑 / Common Mistakes

❌ **用时间戳排序并发操作** — 分布式系统时钟不可靠，两台机器的"同时"可能差几百毫秒

✅ **用逻辑时钟 / Lamport Clock** 或向量时钟建立因果顺序

❌ **直接用数据库乐观锁** — "最后写入者获胜"(LWW) 会丢失数据

✅ **OT 或 CRDT**，确保所有操作都被保留并正确合并

---

## 📚 References
- [Google's Operational Transformation paper](https://research.google/pubs/pub35605/)
- [CRDT explained](https://crdt.tech/)
- [Building a real-time collaborative editor](https://www.smashingmagazine.com/2020/07/practical-guide-to-crdt/)

## 🧒 ELI5

两个人同时改同一个 Google Doc，就像两个人同时在一张纸上写字。OT 就像一个裁判，看到两个人都写了东西，想办法把两份更改都保存下来，谁的也不丢。

Two people editing the same doc is like two people writing on the same piece of paper at once. OT is like a referee who sees both changes and figures out how to keep both without losing either.
