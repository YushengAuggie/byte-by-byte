# 🗣️ 软技能 / Soft Skills — Day 156 (Synthesis)
## 高级场景: 你被要求接手一个技术债务严重的核心系统
## Senior Scenario: Taking Ownership of a Critical System Drowning in Tech Debt

> 综合主题: Day 16 (技术债务), Day 56 (快速上手陌生代码库), Day 51 (迁移/废弃), Day 32 (技术决策推动)

---

### 🎯 场景 / The Scenario

你新加入一个团队，第一周就被告知：你需要负责公司最核心的订单处理服务。这个服务已经7年没有重大重构，测试覆盖率 12%，P0 故障平均每月一次。你的老板说："我知道这很难，但我们需要你让它稳下来，同时不能停止新功能交付。"

You join a team and within your first week, you're handed ownership of the company's most critical order processing service. 7 years of accumulated debt, 12% test coverage, one P0 per month. Your manager says: "I know it's messy, but we need stability without stopping feature delivery."

---

### 🌟 STAR 拆解 / STAR Framework

**Situation:**
接手时：5000行无文档 Python 代码，依赖注入靠全局变量，DB 查询散落在业务逻辑里，无任何 metrics。

**Task:**
目标：6个月内把 P0 频率降到每季度一次，同时不延误产品 roadmap。

**Action (分阶段策略):**

```
第1-2周: 观察，不动 (Observe, Don't Touch)
├── 读代码，画出数据流图（不改代码）
├── 在 staging 跑所有已有测试，记录 flaky 的
└── 读最近3个月的 incident post-mortems

第3-4周: 插装，不重构 (Instrument, Don't Refactor)
├── 加 structured logging（不改逻辑）
├── 加 Datadog APM traces 到每个 DB 调用
└── 建立基线：p99 latency、error rate、call graph

第5-8周: 外科手术式修复 (Surgical Fixes)
├── 找出导致50%故障的根因（通常只有2-3个）
├── 只改高风险代码，每改一块先写测试
└── Code freeze: 新功能走 feature flag，旧路径不动

第9-24周: 渐进重构 (Strangler Fig Pattern)
├── 新逻辑写在新模块，旧代码调用新模块
├── 每个 sprint 至少一个"测试覆盖率提升"任务
└── 每季度给上级一个覆盖率/稳定性报告
```

**Result:**
4个月后，P0 降至每季度1次；测试覆盖率从12%→41%；没有延误任何 roadmap 里程碑。

---

### ❌ vs ✅

| ❌ 新人常犯 / Junior Mistake | ✅ Senior 做法 |
|---|---|
| "这代码太烂了，我要重写" | 先理解，再重构；Big Bang 重写风险极高 |
| 第一周就提大量 PR 改代码风格 | 先建立信任，再推变化 |
| 把技术债务当纯技术问题 | 量化业务影响（每次 P0 损失多少 GMV）才能说服上级投资 |
| 一次性重构所有问题 | Strangler Fig：新旧并行，渐进迁移 |

---

### 💡 Senior/Staff 加分点

1. **用业务语言谈技术债**："每次 P0 我们损失约 $X 收入 + $Y 工程师时间" > "代码质量很差"
2. **主动建立 service reliability 目标**，不等上级指派 SLO
3. **把改善过程做成可见的**：weekly tech debt burn-down chart 发给 stakeholders

---

### 🧒 ELI5

就像接手一套老房子：别第一天就砸墙。先住几周，找出哪里漏水、哪里电路有问题，然后先修最危险的，再慢慢翻新，整个过程不影响你住人。

---

### 📚 References
- https://martinfowler.com/bliki/StranglerFigApplication.html
- https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/ (Technical Debt chapter)
- https://sre.google/sre-book/eliminating-toil/
