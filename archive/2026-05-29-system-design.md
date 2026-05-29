# 🏗️ 系统设计 / System Design — Day 45
## 多区域 Active-Active 系统设计 / Design a Multi-Region Active-Active System

---

### 🌍 真实场景 / Real-World Scenario

想象你在 Stripe 负责支付基础设施。黑色星期五来临，单个数据中心每秒处理 10 万笔交易。一场区域性断电会让全球业务瘫痪、损失数亿美元。你的任务：设计一个多区域 active-active 系统，让任何一个区域挂掉都不影响全局。

*Imagine you're at Stripe running payment infrastructure. Black Friday arrives, your single data center processes 100K TPS. One regional outage costs hundreds of millions. Your job: design a multi-region active-active system where any single region can fail without global impact.*

---

### 📐 架构图 / ASCII Architecture

```
         ┌─────────────────────────────────────────────┐
         │          Global Load Balancer (Anycast IP)   │
         │              GeoDNS / AWS Global Accelerator │
         └──────────┬──────────────┬────────────────────┘
                    │              │
          ┌─────────▼──────┐  ┌───▼─────────────┐
          │  Region: US-W   │  │  Region: EU-W    │
          │ ┌─────────────┐ │  │ ┌─────────────┐ │
          │ │  API Layer  │ │  │ │  API Layer  │ │
          │ │  (AZ × 3)   │ │  │ │  (AZ × 3)   │ │
          │ └──────┬──────┘ │  │ └──────┬──────┘ │
          │ ┌──────▼──────┐ │  │ ┌──────▼──────┐ │
          │ │  DB Primary │ │  │ │  DB Primary │ │
          │ │  (writes)   │◄├──┼─┤► (writes)   │ │
          │ │  + Replicas │ │  │ │  + Replicas │ │
          │ └─────────────┘ │  │ └─────────────┘ │
          │ ┌─────────────┐ │  │ ┌─────────────┐ │
          │ │    Cache    │ │  │ │    Cache    │ │
          │ │   (Redis)   │ │  │ │   (Redis)   │ │
          │ └─────────────┘ │  │ └─────────────┘ │
          └────────┬────────┘  └────────┬─────────┘
                   │                    │
          ┌────────▼────────────────────▼─────────┐
          │    Async Replication / CDC (Kafka)     │
          │    Global Control Plane (consensus)    │
          └────────────────────────────────────────┘
```

---

### ⚖️ 关键权衡 / Key Tradeoffs

**为什么要 Active-Active 而不是 Active-Passive？**
*Why Active-Active instead of Active-Passive?*

| 维度 | Active-Passive | Active-Active |
|------|---------------|---------------|
| RTO | 分钟级（需要故障转移）| 秒级（流量即时切换）|
| 读吞吐 | 仅主区域 | 全球就近读 |
| 写冲突 | 无 | 需要处理！|
| 复杂度 | 低 | 高 |

**写冲突解决 / Conflict Resolution：**
1. **最后写入胜（LWW）** — 简单但可能丢数据，适合 metrics/logging
2. **向量时钟（Vector Clocks）** — 检测并发写，应用层解决，适合文档
3. **CRDT（Conflict-free Replicated Data Types）** — 自动合并，适合计数器、集合
4. **事务路由（Transaction Routing）** — 按 user_id 哈希路由到固定区域写，消除冲突（推荐用于支付）

**数据分区策略 / Data Partition Strategy：**
- **用户就近原则**：欧洲用户数据写 EU 区域，通过 GDPR 合规
- **全局实体**（如商品库存）：需要真正的分布式事务，代价极高
- **本地实体**（用户会话、订单）：路由到固定区域，避免冲突

---

### 🎯 三大核心挑战 / Three Core Challenges

**1. 复制延迟 / Replication Lag**
- 跨大陆延迟 ~100-150ms，数据不一致窗口真实存在
- 方案：读自己的写（read-your-writes）—— 写完后短暂路由到同一区域读

**2. 脑裂 / Split Brain**
- 网络分区时两个区域都认为自己是主
- 方案：引入 Global Control Plane（用 Raft 共识），检测分区后降级为 active-passive

**3. 故障检测 / Failure Detection**
- 不要依赖单点健康检查，用 Route 53 Health Checks + 跨区域 ping
- 自动 failover 配合熔断器，避免雪崩

---

### 🚫 别踩这个坑 / Common Mistakes

1. **坑：假设网络总是通的** — 设计时必须考虑分区（P in CAP）
2. **坑：所有数据都做 active-active** — 区分全局实体 vs 局部实体，局部实体不需要跨区同步
3. **坑：忽视时钟偏移** — 分布式系统里不要用本地时间做排序，用混合逻辑时钟（HLC）或 CockroachDB 的 TrueTime
4. **坑：过度工程** — 大多数公司在到达 active-active 需要之前就 IPO 了；先做 active-passive + 快速 failover

---

### 📚 References

- [Google Spanner: Globally-Distributed Databases](https://research.google/pubs/pub39966/) — 混合时钟的权威论文
- [Amazon DynamoDB Global Tables](https://aws.amazon.com/dynamodb/global-tables/) — LWW 在生产的实践
- [CockroachDB Multi-Region](https://www.cockroachlabs.com/docs/stable/multiregion-overview.html) — 生产可用的 active-active SQL

---

### 🧒 ELI5

想象一家全球连锁餐厅。**Active-Passive** 就像只有北京总店能接单，其他城市的店只是备份。**Active-Active** 就像每个城市都能独立接单、做菜，但偶尔菜单更新要同步，如果北京和上海同时修改了同一道菜的价格，得有个规则决定谁的算数。

*Think of a global restaurant chain. Active-Passive: only HQ takes orders, others are on standby. Active-Active: every city takes orders independently, but when two cities update the same menu item simultaneously, you need a rule for whose version wins.*
