# Soft Skills Day 1 — Decision Making Under Uncertainty
*Date: 2026-03-14 | Category: Decision Making | Level: Senior/Staff*

---

🗣️ **软技能 Day 1 / Soft Skills Day 1**
**在信息不完整时做出关键技术决策**
**Making Critical Technical Decisions with Incomplete Information**

---

**为什么这很重要 / Why This Matters**

初级工程师等信息齐全再行动。高级工程师知道：信息永远不会完全齐全。

系统随时会挂，竞争对手随时会发布，产品上线时间表不会等你做完全量分析。Senior/Staff 工程师和 L3 工程师最大的差距，不是编码能力，而是在模糊中决断的能力。

*Junior engineers wait for complete information. Senior engineers know it never arrives. The gap between L3 and Staff isn't coding — it's the ability to make good decisions under uncertainty and own the outcome.*

---

**STAR 框架拆解 / STAR Framework**

**Situation（情境）**
描述背景，但要聚焦：有什么压力？为什么信息不完整？
⚠️ 不要花超过 20% 的时间在这里

**Task（任务）**
你需要做什么决定？有什么约束？时间线？
清楚说明为什么这个决定很难。

**Action（行动）** ← 这是重点，占 60-70%
- 你如何快速收集最关键的信息？
- 你评估了哪些方案？
- 你如何在时间压力下做出判断？
- 谁参与了决策，如何达成共识？
- 你如何记录决定和理由（ADR）？

**Result（结果）**
具体指标。但如果结果不完美，更要说清楚你学到了什么。

---

**❌ 糟糕的回答 / Bad Approach**

> "我们的数据库响应变慢了，我研究了一下，最后升级了实例类型，问题解决了。"

问题出在哪里：
- 没有体现「信息不完整」的挑战
- 没有说明评估过的其他方案
- 没有数字
- 听起来是一个人默默解决，没有体现协作
- 面试官不知道你的思维过程

---

**✅ 好的回答结构 / Good Approach**

> "2024年Q3，我们的支付服务在高峰期 p99 延迟从 80ms 跳到了 800ms，但我们不知道根因——可能是代码、数据库、还是下游 API。问题是周五下午5点发生的，我们有个重要的 launch 在下周一。"
>
> "我需要在没有完整 tracing 数据的情况下（我们当时监控覆盖率只有60%）决定：是回滚最近的部署、扩容数据库、还是限流？"
>
> "我做了三件事：第一，让团队15分钟内各自排查一个方向，并行收集证据。第二，设定了一个阈值——如果30分钟内找不到根因，就先限流保护系统，再继续排查。第三，在 Slack 里实时记录我们的假设和证据，方便团队同步。"
>
> "结果是我们在22分钟内发现是一个 N+1 查询问题被一次数据迁移触发了。我们加了一个临时索引，延迟降到了 95ms，顺利支撑了周一 launch。事后我们补了完整的 APM tracing。"

---

**场景模板 / Scenario Template**

```
背景: [系统 X] 在 [时间点] 出现了 [问题/机会]
信息缺口: 我们不知道 [关键未知项]，因为 [原因]
约束: [时间/资源/风险约束]
我的决策框架:
  - 快速信息收集: [做了什么]
  - 方案评估: [A vs B vs C，为什么选A]
  - 风险缓解: [如何降低决策风险]
  - 沟通对齐: [如何同步团队/stakeholders]
结果: [具体数字] + [事后学到的]
```

---

**Senior/Staff 加分项 / Level-Up Tips**

1. **提到 ADR（架构决策记录）**
   "我们写了一个 ADR 记录了这个决定和我们当时的信息状态，方便3个月后的人理解为什么这么做。"

2. **主动承认决定的局限性**
   Staff 级别的工程师不假装自己的决定完美，他们说："这是基于当时信息的最优解，我们设置了一个检查点在30天后重新评估。"

3. **体现系统性思维**
   不只解决这次的问题，还要防止下次同类问题发生。

---

**关键要点 / Key Takeaways**

- 面试官想看的是你的**思维过程**，不只是结果
- 信息不完整≠瘫痪，要展示你如何**快速收集关键信息**
- 好的决定有**明确的理由**，坏的结果有**清晰的复盘**
- 量化一切：延迟数字、时间窗口、影响用户数

*The interviewer wants to see: structured thinking under pressure, ability to make good-enough decisions fast, and ownership of outcomes regardless of result.*
