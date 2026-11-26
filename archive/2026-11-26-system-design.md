# 🏗️ 系统设计 / System Design — Day 158 · Synthesis
> Expert Level · Synthesis Mode · 3 min read

---

## 系统演进模型：从0到10亿用户，每个量级的关键决策
## System Evolution: 0 to 1B Users — The Right Tradeoff at Every Scale

**这道经典面试题的真正考点不是给出一个"完美设计"，而是：你能识别每个量级的真实瓶颈在哪里。**

The real insight isn't designing a perfect system upfront — it's knowing *which bottleneck matters at each scale* and evolving deliberately.

---

## 四个量级的决策矩阵 / Decision Matrix Across 4 Scales

### 📊 阶段 1 · Phase 1: 1–10K 用户 (单机时代 / Single Machine)

```
[User] → [Web Server + App + DB]  (all on one machine)
```

**瓶颈 / Bottleneck:** 垂直扩展到天花板  
**关键决策 / Key Decision:** 分离 Web Server ↔ App ↔ DB (三层架构)  
**别踩的坑 / Mistake to avoid:** 过早微服务化 — 1K 用户根本不需要分布式开销

---

### 📊 阶段 2 · Phase 2: 100K 用户 (水平扩展 / Horizontal Scale)

```
[Users]
   ↓
[Load Balancer]  ← 轮询 / 一致性Hash
   ↓
[App Servers × N]
   ↓
[DB Primary (写)] → [DB Replica × M (读)]
   ↓
[Redis Cache Layer]  ← 读多写少的核心武器
```

**瓶颈 / Bottleneck:** DB 读压力  
**关键决策 / Key Decision:**
- 读写分离 (Read replicas for 80%+ read workloads)
- 缓存热点数据 (Redis Cache-Aside pattern)

**权衡 / Tradeoff:** Replica lag → 读到旧数据，可用 "写后失效" 策略缓解

---

### 📊 阶段 3 · Phase 3: 10M 用户 (分布式时代 / Distributed Systems)

```
[CDN] → [API Gateway / Rate Limiter]
              ↓
    ┌─────────┼─────────┐
[UserSvc] [OrderSvc] [NotifSvc]   ← 微服务
    ↓           ↓           ↓
[DB Shard]  [DB Shard]  [Kafka]   ← 分片 + 消息队列
    ↓                       ↓
[Redis Cluster]      [Worker Pool]
```

**瓶颈 / Bottleneck:** 单点依赖 + 跨服务延迟  
**关键决策 / Key Decisions:**
- **一致性 Hash** (Day 11) → DB 分片，扩容不迁移大量数据
- **消息队列 Kafka** (Day 13) → 解耦削峰，异步化耗时操作
- **CDN** (Day 64) → 静态资源命中率 >95%，降低源站压力

---

### 📊 阶段 4 · Phase 4: 1B+ 用户 (全球化 / Multi-Region)

```
Region US-East          Region EU-West         Region AP-SE
[Services + DB]  ←→    [Services + DB]   ←→  [Services + DB]
     ↕                       ↕                      ↕
     └────────── Async Replication (Conflict Resolution) ──────┘
```

**瓶颈 / Bottleneck:** 跨地域延迟 (RTT ~200ms US↔AP) + 数据一致性  
**关键决策 / Key Decisions:**
- **CAP Theorem** (Day 12): 选 AP (高可用) 还是 CP (强一致)？
  - 社交/内容: AP (用户看到旧帖子可接受)
  - 金融/支付: CP (绝对不能双扣)
- **Active-Active** (Day 54): 每个 Region 均可写，最终一致性合并冲突
- **DNS 地理路由**: 用户自动路由到最近 Region

---

## 核心技术速查 / Technology Quick Reference

| 场景 Scenario | 技术方案 Solution | 曾覆盖 Covered Day |
|---|---|---|
| 读多写少 (Read-heavy) | CDN + Redis Cache-Aside | Day 6, 64 |
| 写多读少 (Write-heavy) | Message Queue + Async Workers | Day 13 |
| 数据量爆炸 (Data explosion) | DB Sharding + Consistent Hash | Day 11 |
| 实时通信 (Real-time) | WebSocket + Fan-out | Day 28, 61 |
| 高精度计数 (Exact counting) | Redis HyperLogLog / 计数服务 | Day 22 |
| 跨地域 (Multi-region) | Active-Active + CRDT | Day 54 |
| 防滥用 (Abuse prevention) | Rate Limiting + API Gateway | Day 17, 67 |

---

## 面试回答框架 / Interview Answer Framework

面试官问"设计一个支持X亿用户的系统"时，标准四步拆解：

1. **先估算 / Estimate first:** QPS? 数据量? 读写比? 存储TB? → 决定选型
2. **先画最简版 / Start simple:** 单机/单DB能撑多久？明确起点
3. **逐步演进 / Evolve progressively:** 点出每个瓶颈 → 引入对应技术
4. **权衡取舍 / State tradeoffs:** 没有完美方案，只有在约束下合适的方案

> 💡 **高分加分项:** 主动说出"这个方案的问题是…，可以通过…来缓解"

---

## 🧒 ELI5

像盖楼。1层平房 → 10层公寓 → 100层摩天楼，每次升级解决的问题不一样，用的材料也不一样。硬要在小平房里用摩天楼的设计，就是过度设计。

Building software is like building a tower. A 1-floor house needs different solutions than a 100-story skyscraper. Over-engineering a small house with skyscraper foundations is just waste.

## 📚 References
- [System Design Interview Vol.1 — ByteByteGo (Alex Xu)](https://bytebytego.com/courses/system-design-interview)
- [High Scalability — Real Architecture Case Studies](http://highscalability.com)
- [The Architecture of Open Source Applications](http://aosabook.org/en/index.html)
