# 软技能 / Soft Skills — Day 137 (Synthesis)
## Staff-Level Scenario: 技术负债 vs 新功能的战略权衡

🗣️ **软技能 / Soft Skills**
**综合场景 / Synthesis Scenario**

---

### 题目 / The Question

> "你是某团队的 Staff Engineer。PM 要求在 Q4 交付三个高价值功能，但你的团队有一块关键服务的技术债务——如果不清理，Q1 可能发生大规模宕机。你怎么处理这个冲突？"

> "You're Staff Engineer. PM wants 3 high-value features in Q4, but your team has critical tech debt in a core service — if unaddressed, it risks a major Q1 outage. How do you handle this conflict?"

---

### 为什么这题重要 / Why It Matters

这是 Staff/Principal 级别最常考的题型：**技术判断 + 商业影响 + 跨职能影响力**。
初级工程师说"让我们先清技术债"——Senior 会衡量 ROI——Staff 会把技术风险翻译成业务语言让 PM/VP 做决策。

---

### STAR 拆解 / STAR Breakdown

**Situation (背景):** 
量化技术债风险。不要说"可能有问题"，要说"基于当前错误率趋势和容量预测，我们有 X% 概率在 Q1 遇到 Y 级别的事故，预计影响 Z 小时 SLA 和 N 个下游团队。"

**Task (任务):**
你的职责不是单方面决定优先级，而是帮助组织做出知情决策 (informed decision)。

**Action (行动) — 这是关键：**
1. **量化风险** — 用数据，不用感觉。写 1 页技术风险评估。
2. **提供选项** — 给 PM/VP 三个方案：① 先清债再做功能 ② 并行（需要额外资源）③ 接受风险（明确谁签字承担）
3. **找共识** — 与 PM 一起做优先级排序，不是单独宣判。
4. **建护栏** — 如果决定先交功能，争取"技术债 20% 时间" commitment。

**Result (结果):**
最终决策是组织的，你负责执行并设置好预警监控，在风险真正发生前拦截。

---

### ❌ 常见错误 vs ✅ 高分回答

**❌ 初级陷阱：**
"我跟 PM 说技术债很重要，他不听，所以我只能先做功能了。"

**✅ Staff 级回答：**
"我写了一页技术风险备忘录，附上了具体的失败概率估算和业务影响（$X 收入风险 / N 小时停机）。我和 PM、EM 开了一次对齐会，最终我们决定在 Q4 拆出一个 2-sprint 的还债 spike，同时推迟优先级最低的功能 4 周。我在 Q1 初设置了自动熔断，最终没有发生事故。"

---

### Senior/Staff 关键技能 / Key Insight

**把技术语言翻译成业务语言** 是 Staff 的核心竞争力：
- "服务响应时间 p99 > 2s" → "每秒额外流失 X% 用户"
- "数据库连接池耗尽" → "结账功能宕机，直接影响营收"
- "代码耦合度高" → "下次需求变更将需要 3× 工时"

### 📚 References
- https://staffeng.com/guides/work-on-what-matters
- https://www.amazon.com/Staff-Engineer-Leadership-beyond-management/dp/1736417916
- https://martinfowler.com/articles/is-quality-worth-cost.html

### 🧒 ELI5
PM 想快点出新功能，工程师知道地基有裂缝。Staff 的工作是把"地基裂缝"翻译成"如果不修，三个月后整栋楼可能塌"，让大家一起决定修还是赌，而不是自己偷偷修或者悄悄赌。
PM wants new features fast. Engineer sees cracks in the foundation. Staff's job: translate "foundation cracks" into "if unaddressed, 60% chance the building collapses in Q1" — and let everyone decide together, rather than acting alone.
