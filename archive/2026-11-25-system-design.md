# Day 157 — System Design Expert Synthesis
## 高并发系统的五大核心设计张力
### Five Core Design Tensions in High-Scale Systems

---

🏗️ **系统设计专题综合 / System Design — Expert Synthesis**

*经过 60 个系统设计专题，今天综合回顾贯穿始终的 5 大核心权衡。*
*After 60 system design topics, today we synthesize the 5 fundamental tensions that run through all of them.*

---

## 想象你在设计一个面试白板系统...

每次面试官说"请设计 X"，他真正在考察的不是你记住了多少组件——而是你如何**在约束中做选择**。这 5 大张力贯穿了所有你学过的话题。

*Every time an interviewer says "design X," they're really testing whether you can make reasoned choices under constraints. These 5 tensions run through every system we've studied.*

---

## ⚡ 张力 1：一致性 vs 可用性
**Consistency vs. Availability (CAP Theorem)**

```
强一致性 ←————————————→ 最终一致性
  Zookeeper/etcd         DynamoDB/Cassandra
  分布式锁               DNS缓存
  金融账本               购物车
```

**覆盖话题链：** CAP定理 → 数据库复制 → 一致性哈希 → 分布式锁 → Raft/Paxos

**核心决策框架 / Decision framework:**
- 钱/库存/权限 → CP（宁可不可用，不要数据错）
- 社交点赞/浏览量/推荐 → AP（短暂不一致无所谓）
- 用户 session/购物车 → 最终一致性 + 客户端合并

**别踩这个坑：** 在面试中不要说"我用 Redis 保证一致性"——Redis 默认是异步复制，主挂了会丢数据。用 Redis Sentinel/Cluster 时要明确说明你接受了什么一致性级别。

---

## ⏱️ 张力 2：吞吐量 vs 延迟
**Throughput vs. Latency**

```
高吞吐量策略：批处理、异步队列、流式写入
低延迟策略：同步调用、内存缓存、连接池

              批处理/队列
高吞吐 ───────────────────── 高延迟
低吞吐 ─────────────────────  低延迟
              同步直连
```

**覆盖话题链：** 消息队列 → 限流 → 负载均衡 → 分布式任务队列 → 实时游戏后端

**核心公式（Little's Law）:**
> L = λ × W
> 系统中请求数 = 到达率 × 平均延迟

提高吞吐量 → 要么减少 W（优化每个请求延迟），要么接受更多 L（扩容）

**实战场景对比：**
- Kafka consumer: 批量 commit offset → 高吞吐，但崩溃可能重复处理
- 实时游戏帧同步: 20ms 内必须响应 → 牺牲吞吐，换取低延迟

---

## 💾 张力 3：存储 vs 计算
**Storage vs. Computation (Precompute Trade-off)**

```
纯计算：每次请求实时算
  ↓ 慢但省空间
预计算：提前算好存起来
  ↓ 快但占空间

例：推荐系统
  实时: 每次请求跑协同过滤 → 500ms
  预计算: 离线跑推荐结果存 Redis → 5ms
```

**覆盖话题链：** 缓存策略 → CDN → 推荐系统 → Autocomplete/Typeahead → 搜索引擎

**决策矩阵：**
| 场景 | 选择 |
|------|------|
| 结果变化频率低（<1天） | 预计算 |
| 结果高度个性化 | 混合（粗粒度预计算 + 细粒度实时） |
| 数据量极大无法全存 | 分层缓存（热/温/冷） |

---

## 🔄 张力 4：实时性 vs 成本
**Real-time vs. Cost**

```
Twitch直播: 必须实时 → WebRTC/WebSocket → 高成本
YouTube点播: 允许延迟 → CDN分发 → 低成本

实时 ←—[WebSocket]—[Long Poll]—[SSE]—[Polling]—→ 批处理
      贵                                               便宜
```

**覆盖话题链：** 聊天系统 → 直播系统 → 通知系统 → 协同编辑 → 股票交易所

**关键决策：** 用户能接受多少延迟？
- 聊天消息：<500ms 感知上是实时的
- 股票价格：<100ms，需要专用 TCP 连接
- 邮件通知：几分钟可接受，用 Kafka + 批处理

**成本优化实战：**
1. 分层推送：活跃用户 WebSocket，不活跃用户轮询
2. 消息聚合：1 秒内多条通知 → 合并为一条推送
3. 降级策略：WebSocket 断开 → SSE → Long Poll → 短轮询

---

## 🏗️ 张力 5：灵活性 vs 性能
**Flexibility vs. Performance (Architecture Trade-off)**

```
单体 Monolith        微服务 Microservices      平台工程
  · 简单                · 独立部署                · Service Mesh
  · 快速迭代             · 技术多样性               · API Gateway
  · 难以扩展             · 网络开销+复杂度           · GitOps/IDP
```

**覆盖话题链：** 微服务 vs 单体 → API 网关 → 服务网格 → 分布式追踪 → Feature Flag

**2026 年最佳实践 — 模块化单体（Modular Monolith）：**
> 在单一进程中按领域边界严格分模块，需要时再拆服务。
> "Start monolith, extract services when you feel pain."

**什么时候才应该拆微服务？**
- ✅ 不同组件有完全不同的扩展需求
- ✅ 团队规模 > 50 人，康威定律开始生效
- ✅ 有成熟的 DevOps/CD pipeline
- ❌ 团队 < 10 人 → 单体先走
- ❌ 还没清楚领域边界 → 拆了只会更乱

---

## 📐 综合架构原则 / Master Principle

> **没有最好的架构，只有最合适当前约束的架构。**
> *There is no best architecture, only the most appropriate one given current constraints.*

在面试中，每次做决策都说出你在哪个张力上做了权衡：
- "这里我选择可用性 over 一致性，因为..."
- "我们预计算这个结果，接受空间换时间，因为..."
- "我用消息队列解耦，吞吐量提升，但增加了延迟..."

---

## 📚 References
- [Designing Data-Intensive Applications — Martin Kleppmann](https://dataintensive.net/)
- [The System Design Primer](https://github.com/donnemartin/system-design-primer)
- [AWS Architecture Center — Tradeoffs](https://aws.amazon.com/architecture/)
- [Google SRE Book — Chapter 3: Embracing Risk](https://sre.google/sre-book/embracing-risk/)

## 🧒 ELI5
想象你在管一个超市：
- 一致性 vs 可用性 = 货架缺货时，你是关门等补货（一致性）还是继续卖但数量可能不准（可用性）？
- 吞吐量 vs 延迟 = 一次送一件 vs 等满一车再送？
- 存储 vs 计算 = 每次问妈妈 2+2 等多少，还是背下来？
- 实时性 vs 成本 = 专车接送 vs 公交？
- 灵活 vs 性能 = 瑞士军刀 vs 专业厨刀？

每个选择都有代价。好的系统设计师就是知道**在哪里值得付这个代价**。
