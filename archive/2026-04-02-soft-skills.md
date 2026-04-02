# 🗣️ 软技能 Day 14 / Soft Skills Day 14
## How do you handle technical debt? Give me a specific example
**类别 / Category:** Technical Leadership · Senior/Staff Level

---

### 🎯 为什么重要 / Why This Matters

每个工程团队都有技术债。面试官不想听你说"我们应该重构"——他们想听你如何**量化**债务、**说服**利益相关者、**执行**还债计划，同时不停业务开发。

Every eng team has tech debt. Interviewers don't want "we should refactor" — they want to hear how you **quantified** the debt, **persuaded** stakeholders, and **executed** payoff while keeping feature work moving.

---

### ⭐ STAR 框架示范 / STAR Example

**Situation 情境：**
我们的订单服务是 3 年前写的单体模块，每次改价格逻辑都要改 400 行 if-else，每月导致 2-3 次生产事故。

Our order service was a 3-year-old monolith module. Every pricing logic change touched 400 lines of if-else, causing 2-3 production incidents per month.

**Task 任务：**
作为 Tech Lead，我需要在 Q3 OKR 里推动重构，但产品经理有 12 个新功能排队。

As Tech Lead, I needed to push refactoring into Q3 OKRs while PM had 12 features queued.

**Action 行动：**
1. **量化痛苦 / Quantify the pain:** 统计过去 6 个月：incident 修复耗时 120 工程师小时，每次 pricing 功能开发耗时是预期的 3x
2. **用数据说服 / Data-driven pitch:** 向 VP Eng 展示"如果不还债，Q4 每个 pricing 功能要 3 周而不是 1 周"
3. **渐进式重构 / Incremental approach:** 不做 Big Bang，设计 Strangler Fig 模式——新功能走新架构，旧功能逐步迁移
4. **20% 规则 / 20% rule:** 每个 sprint 拿出 20% capacity 用于还债，写在 sprint contract 里

**Result 结果：**
3 个月后 incident rate 降了 70%，新 pricing 功能开发时间从 3 周降到 5 天。VP Eng 在季度 all-hands 上引用这个案例。

---

### ❌ Bad vs ✅ Good

```
❌ "技术债很重要，我们应该分配时间去重构。"
   → 太泛、没有 evidence、没有具体行动

✅ "我追踪了6个月的 incident 数据，发现每月120小时
   浪费在补丁上。我提出 Strangler Fig 方案，用20%
   sprint capacity 渐进还债，3个月后 incident 降70%。"
   → 有数据、有策略、有结果
```

---

### 🏅 Senior/Staff Tips

1. **永远先量化 / Always quantify first** — "技术债导致了 X 小时浪费 / Y 次事故 / Z% 速度下降"，不要用模糊感受
2. **关联业务指标 / Tie to business metrics** — "如果我们不修，下季度功能交付速度慢 40%"
3. **Strangler Fig > Big Bang** — 渐进式替换比全部重写风险低 10 倍
4. **建立持续机制 / Build ongoing mechanism** — 20% rule、tech debt sprints、quality budget 都是好策略
5. **展示 leadership / Show leadership** — 你不是在"要求时间做技术的事"，而是在"保护团队交付速度"

---

### 🔑 Key Takeaways
- 技术债 = 利息在涨的贷款，不是可有可无的清洁工作
- 量化 + 数据 + 渐进执行 = 让所有人 buy-in 的方程式
- 最好的还债方式：和新功能开发并行，不是"暂停一切来重构"

---

### 📚 References
- [Martin Fowler — Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html) — 技术债经典定义
- [Strangler Fig Pattern — Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig) — 渐进式迁移模式
- [Managing Technical Debt — Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch15.html) — Google 的技术债管理经验

---

### 🧒 ELI5
**中文：**技术债就像你房间越来越乱。你可以继续往里塞东西（加功能），但找东西越来越难（bug 越来越多）。聪明的做法不是某天请假大扫除，而是每天花10分钟整理一点。

**English:** Tech debt is like your room getting messier over time. You can keep stuffing things in (adding features), but finding anything gets harder (more bugs). The smart move isn't taking a day off to deep-clean — it's tidying up 10 minutes every day.
