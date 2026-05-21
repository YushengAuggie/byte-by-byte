# 🏗️ 系统设计 / System Design — Day 48
## 设计实时游戏后端 / Design a Real-Time Gaming Backend

> **难度 / Difficulty:** Advanced | **Phase:** Mastery | **预计阅读时间 / Read time:** 3 min

---

## 🎯 场景 / Scenario

想象你在设计一款多人在线对战游戏后端（类似王者荣耀或 Valorant）。
*Imagine you're designing the backend for a multiplayer online battle game (like League of Legends or Valorant).*

**核心挑战 / Core challenges:**
- 每帧同步玩家状态，延迟 < 100ms
- 支持 100万+ 并发在线玩家
- 处理游戏状态、匹配、排行榜、战斗日志

---

## 🏗️ 架构图 / Architecture Diagram

```
Players (Mobile/PC)
       │  WebSocket / UDP
       ▼
┌─────────────────────────────────┐
│       Edge Gateway              │  ← GeoDNS 路由到最近节点
│  (AWS CloudFront / Anycast)     │
└────────────────┬────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│  Game Server │   │  Matchmaking │
│  (Stateful)  │   │  Service     │
│  1 server =  │   │  (ELO-based) │
│  1 game room │   └──────┬───────┘
└──────┬───────┘          │
       │             Redis Sorted Set
       │             (Skill Ratings)
       ▼
┌──────────────────────────────────┐
│         State Sync Layer         │
│  Redis (hot state, TTL=1 game)   │
│  Kafka (event stream, replay)    │
└──────┬───────────────────────────┘
       │
  ┌────┴──────┐
  ▼           ▼
Cassandra   ClickHouse
(game logs) (analytics)
```

---

## 🔑 关键设计决策 / Key Design Tradeoffs

### 1. UDP vs WebSocket
| | UDP | WebSocket |
|---|---|---|
| **延迟** | 极低 | 较低 |
| **可靠性** | 不可靠，需自建重传 | 可靠 (TCP) |
| **适用** | FPS 游戏（每帧位置） | 策略游戏（指令为主）|

**为什么这样设计？** FPS 类游戏用 UDP + 自建 ACK；MOBA 类用 WebSocket 足够。
*Why this design? FPS games need UDP + custom ACK; MOBA-style games can use WebSocket.*

### 2. 游戏服务器有状态 / Stateful Game Servers
每个游戏房间绑定一个 Game Server 进程，游戏状态在内存中。不走数据库——延迟太高。
*Each game room binds to one Game Server process; game state lives in memory. No DB reads mid-game—latency would be fatal.*

### 3. Authoritative Server Model（权威服务器）
服务端计算真实状态，客户端做预测渲染 (Client-Side Prediction)，服务端定期校正。
*Server computes ground truth; client predicts locally and server reconciles periodically.*

---

## ⚠️ 别踩这个坑 / Common Mistakes

1. **用 REST API 同步游戏状态** — 每帧一次 HTTP 请求？延迟会让玩家愤怒。
   *Using REST for state sync — one HTTP call per frame = unacceptable latency.*

2. **单点 Game Server** — 游戏服务器挂了，房间全崩。需要健康检查 + 快速重分配。
   *Single Game Server with no failover — one crash wipes all active rooms.*

3. **匹配队列用关系型数据库** — Redis Sorted Set 的 `ZADD`/`ZRANGEBYSCORE` 专为 ELO 匹配设计。
   *Using RDBMS for matchmaking queues — Redis Sorted Set is built for ELO-based matching.*

4. **忽略反作弊** — 服务端必须校验所有关键动作，不能信任客户端输入。
   *Ignoring anti-cheat — server must validate all critical actions, never trust client input.*

---

## 📚 References
- [Riot Games Engineering — How League handles matchmaking](https://technology.riotgames.com/news/fixing-league-client-networking)
- [Valve — Source Multiplayer Networking (UDP + client prediction)](https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking)
- [AWS GameTech — Building real-time game backends](https://aws.amazon.com/gametech/)

---

## 🧒 ELI5
游戏后端就像裁判员。你的手机只是显示画面，但裁判在服务器上，他说你在哪就在哪，客户端只是"猜"你下一步在哪来减少卡顿感。
*The game backend is like a referee. Your phone just renders pixels, but the referee (server) decides where you truly are. The client just "predicts" to reduce the feeling of lag.*
