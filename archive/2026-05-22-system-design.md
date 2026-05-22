# 🏗️ 系统设计 / System Design — Day 49

**主题 / Topic:** Design a Real-Time Gaming Backend  
**难度 / Difficulty:** Advanced | **阶段 / Phase:** Mastery

---

## 想象你在设计... / Imagine you're designing...

你在设计一款实时多人射击游戏（想想《Apex Legends》或《Fortnite》）的后端。100 个玩家同时在同一个战场——每个人的移动、射击、状态都必须在 **100ms 内同步** 到所有其他玩家。  
You're designing the backend for a real-time multiplayer shooter (think Apex Legends or Fortnite). 100 players in the same match — every move, shot, and death must sync to all other players within **100ms**.

**核心挑战 / Core challenges:**
- 低延迟（Low latency）：游戏状态同步 < 100ms
- 高吞吐量（High throughput）：每个玩家每秒发送约 30-60 个状态包
- 作弊检测（Anti-cheat）：服务器端权威验证
- 状态一致性（State consistency）：所有玩家看到同一个世界

---

## ASCII 架构图 / Architecture Diagram

```
Players (100 clients)
     │  UDP packets (position, input)
     ▼
┌─────────────────────────────────────────┐
│         Game Server (Authoritative)     │
│  ┌──────────┐  ┌──────────────────────┐ │
│  │  Game    │  │  Physics Engine      │ │
│  │  Loop    │  │  (server-side tick)  │ │
│  │ (60 Hz)  │  │  Anti-cheat checks  │ │
│  └──────────┘  └──────────────────────┘ │
│         ↕ State deltas                  │
│  ┌─────────────────────────────────────┐│
│  │   In-Memory Game State (Redis)      ││
│  │   Position, Health, Inventory       ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
     │ Broadcast state deltas (UDP)
     ▼
All Players receive authoritative state

     ┌─────────────────────────────────┐
     │    Matchmaking Service          │
     │    (REST/gRPC + Redis queue)    │
     └────────────┬────────────────────┘
                  │ Assigns to Game Server
     ┌─────────────────────────────────┐
     │    Fleet Manager (Kubernetes)   │
     │    Auto-scales game server pods │
     └─────────────────────────────────┘

     ┌─────────────────────────────────┐
     │    Persistence (Async)          │
     │    Match results → PostgreSQL   │
     │    Replay data → S3             │
     └─────────────────────────────────┘
```

---

## 关键设计决策 / Key Design Decisions

### 1. UDP vs TCP — 为什么选 UDP？
UDP 没有重传保证，数据包可能丢失。但游戏是 **time-sensitive**：
- 位置数据过时 200ms 就没用了，不如直接丢弃
- 丢包率 < 5% 是可接受的
- 现代游戏使用 **QUIC 或自定义 UDP 协议** — 结合 UDP 速度 + 可靠性控制

### 2. 服务器权威模型 / Server-Authoritative Model
- 客户端预测（Client-side prediction）：玩家本地先渲染，减少感知延迟
- 服务器验证：服务器有最终决定权，防止作弊
- 客户端协调（Reconciliation）：客户端与服务器状态对比，差异时修正

### 3. 状态同步：Delta Compression
不发送完整状态（可能几 KB），只发送 **变化的部分**（delta）：
```
Full state:  {p1: {x:100, y:200, hp:100}, p2: {...}, ...}  ~4KB
Delta:       {p1: {x:103}}  ~20 bytes
```
100 玩家 × 60Hz × 20 bytes = **12 MB/s per game server** — 可管理

### 4. 地理分布 / Geographic Distribution
- 玩家应连接到 **最近的区域服务器** (AWS regions, CDN edge)
- 目标：玩家到游戏服务器 ping < 50ms
- 跨区域对战需要 **中继服务器** (relay)

---

## 为什么这样设计？/ Why this design?

| 决策 | 原因 |
|------|------|
| 独立 Game Server 进程 | 状态隔离，一场崩溃不影响其他场 |
| In-memory state (Redis) | 内存读写 < 1ms，磁盘扛不住 60Hz 写 |
| 异步持久化 | 比赛结果不需要实时写库，批量写即可 |
| Kubernetes 弹性扩缩 | 晚高峰 10x 流量，凌晨缩容省钱 |

---

## ⚠️ 别踩这个坑 / Common Mistakes

1. **用 TCP 做游戏同步** — TCP 的队头阻塞（head-of-line blocking）在网络抖动时造成卡顿
2. **客户端完全信任** — 不做服务器验证等于邀请作弊器
3. **同步写数据库** — 每帧写一次 DB 会让 DB 立刻爆炸
4. **单体 Game Server** — 一台机器跑所有对局，一个对局内存泄漏崩掉全服

---

## 📚 References
- [Gaffer on Games — Real-Time Multiplayer](https://gafferongames.com/post/state_synchronization/)
- [Riot Engineering — How League of Legends Handles Network](https://technology.riotgames.com/news/fixing-internet-ping-and-packet-loss)
- [Cloudflare — QUIC Protocol Overview](https://www.cloudflare.com/learning/performance/what-is-quic/)

## 🧒 ELI5
就像老师在课堂上维持秩序一样 — 每个同学（玩家客户端）都在做自己的事，但老师（游戏服务器）是裁判，他的话是最终答案。同学可以先猜老师会说什么（客户端预测），但如果猜错了就得听老师的纠正。
