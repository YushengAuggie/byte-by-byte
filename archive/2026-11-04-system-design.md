# 🏗️ 系统设计 / System Design — Day 147

**架构选型决策树：从单体到微服务的演进路径**
**Architecture Decision Tree: The Evolution from Monolith to Microservices**

*📊 Synthesis Day — Expert Level | 综合之前覆盖的所有架构主题*

---

## 想象你在设计... / The Scenario

你是某 500 人公司的 Staff Engineer。CEO 问你："我们该不该把单体拆成微服务？"

这不是一个技术问题——这是一个**商业决策**。正确答案取决于你所处的阶段。

---

## 架构演进的四个阶段 / Four Stages of Architecture Evolution

```
Stage 1: 单体起步                 Stage 2: 数据库成为瓶颈
┌─────────────────────┐           ┌───────┐    ┌────────┐
│   Monolith          │           │  App  │    │  App   │
│   [All-in-one]      │   →       └───┬───┘    └───┬────┘
│   Single DB         │               └──────┬──────┘
└─────────────────────┘              ┌───────▼──────┐
                                     │  DB Primary  │
                                     │  + Replica(s)│
                                     └──────────────┘

Stage 3: 读写分离 + 缓存           Stage 4: 服务按业务边界拆分
┌──────────────────────┐           ┌──────────┐  ┌──────────┐
│  App                 │           │ Service A│  │ Service B│
│  ↕ Redis Cache       │   →       └────┬─────┘  └────┬─────┘
│  DB Primary (writes) │                │   Message    │
│  DB Replica (reads)  │                └───► Queue ◄──┘
└──────────────────────┘            ┌──────────────────┐
(Day 6: Caching)                    │  DB per service  │
(Day 7-8: Indexing/Replication)     │ (or shared+split)│
                                    └──────────────────┘
                                (Day 11: Consistent Hashing)
                                (Day 12: CAP Theorem)
```

---

## 关键决策节点 / Key Decision Points

### 🟢 何时保持单体 (Stay Monolith)
- 团队 < 50 人，代码库可以在一个 IDE 里全部理解
- 每个模块的负载相似，没有明显的性能热点
- **真实案例：Shopify、Stack Overflow 长期跑单体，业务仍然健康**

### 🟡 何时优先扩展数据库（不拆服务）
- 触发点：DB 成为瓶颈（监控 `slow_query_log`，p99 延迟上升）
- 动作顺序：加索引 → 读写分离 → 引入缓存层 (Day 6, 7, 8)
- **这一步收益最大，架构代价最小，优先于微服务拆分**

### 🔴 何时真正需要微服务
- 不同模块有**截然不同的扩展需求**（搜索 vs 支付 vs 通知）
- 不同团队需要**独立部署节奏**，部署耦合成为业务瓶颈
- 触发点：不是"感觉需要"，是 oncall 告诉你哪个服务在拖累全局

---

## 权衡对照表 / Tradeoff Matrix

| 选项 | 优势 | 代价 | 参考天 |
|------|------|------|--------|
| 单体 | 事务简单，调试容易 | 部署耦合，语言锁定 | Day 14 |
| DB 读写分离 | 渐进可行，风险低 | 主从延迟 | Day 9 |
| 加缓存层 | 降低 DB 压力 | 缓存失效逻辑复杂 | Day 6 |
| 微服务 | 独立扩展/部署 | 网络延迟，分布式追踪复杂 | Day 14 |
| Active-Active 多区域 | 极高可用性 | 最终一致性 (CAP) | Day 12, 54 |

---

## 为什么这样设计？/ Key Insight

**核心原则：架构决策应该跟随组织规模，而不是超前于它。**

Conway's Law 说：系统的架构会镜像产生它的组织通信结构。
- 团队还没分组？单体自然。
- 团队按业务线分组？微服务自然。
- 强行逆势而为 → 要么无人维护的服务，要么紧耦合的"分布式单体"。

---

## 常见错误 / Common Mistakes

❌ **"Microservices-first"** — 未验证产品需求就开始拆分。Netflix 也是先跑了多年单体才拆的。

❌ **拆了服务没拆数据** — 多个服务共享同一个 DB schema。这不是微服务，这是分布式单体，两套代价、一套收益。

❌ **跳过 Stage 2/3** — 直接从单体跳到微服务，忽略了成本更低的数据库优化阶段。

❌ **忽略 Consistent Hashing (Day 11)** — 水平扩展时缓存失效，命中率崩溃，流量全压到 DB。

✅ **正确姿势**：Profile 真实瓶颈 → 最小化改动解决 → 验证效果 → 再下一步。

---

## 📚 References
- https://martinfowler.com/articles/microservice-premium.html
- https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity
- https://www.infoq.com/articles/microservices-when-to-avoid/

## 🧒 ELI5
就像开餐厅：刚开始你自己煮所有菜（单体）。生意大了先买一台洗碗机（缓存）、再加个帮厨（DB 副本）。规模再大了才雇专门的厨师负责不同菜系（微服务）。别刚开业就把厨房分成 20 个小隔间——服务员光跑来跑去菜就凉了。
