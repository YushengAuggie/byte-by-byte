# 软技能合成 / Soft Skills Synthesis — Day 126

🗣️ **软技能合成 / Soft Skills Synthesis**
**第 126 天 · Expert 阶段 · Staff 级场景**

---

## 场景：你被要求评估一个 AI-first 重写提案
## Scenario: Evaluating an AI-First Rewrite Proposal

**背景 / Context:**
你是一个 200 人工程团队的 Staff Engineer。产品 VP 带着一个提案来找你：
> "竞争对手都在用 LLM，我们要把核心搜索系统用 AI 重写，6 个月内上线。"

这个提案有业务压力支撑、CEO 关注、$2M 预算。你被要求给出技术可行性评估并领导执行。

*You're a Staff Engineer. The VP of Product walks in with a proposal: rewrite the core search system with LLMs, 6 months, $2M. CEO is watching. How do you respond?*

---

### 为什么这个场景在 2026 年很重要

AI 重写是当前最常见的"诱人陷阱"之一：
- 技术上有可能性（LLM 确实能做语义搜索）
- 业务上有紧迫感（竞争压力真实存在）
- 工程上充满不确定性（推理成本、延迟、幻觉、可解释性）

Staff/Principal Engineer 的价值，就体现在能**区分"技术上可行"和"工程上合理"**。

*The AI rewrite trap: technically possible, business-urgency-justified, but engineeringly treacherous. Your value as Staff is separating "can we" from "should we, and how."*

---

### STAR 框架 / STAR Breakdown

**Situation:**
"我们的关键词搜索召回率不佳，竞品开始用语义搜索。VP 想要全面 LLM 重写。"

**Task:**
作为 Staff，我需要在不被政治压力推着走的情况下，给出清醒的技术判断，并提出一个既有进展感又控制风险的执行方案。

**Action — 我做了什么：**

1. **先做一周 spike，不是 6 个月项目**
   - 原型验证：同样的 query，关键词搜索 vs 向量搜索，召回率差多少？
   - 测量推理成本：每 1000 次搜索的 embedding 调用费用
   - 识别边界条件：LLM 在哪些 query 类型上比关键词差？

2. **提出渐进式路线，不是大爆炸重写**
   ```
   Phase 1 (4周): 混合搜索 — 关键词 + 向量并行，结果融合
   Phase 2 (8周): 在流量中 A/B 测试，收集真实指标
   Phase 3 (12周): 根据数据决定是否全面切换
   ```
   不是"重写"，而是"在现有系统上叠加 AI 层"。

3. **量化 5 个风险并提出缓解方案**
   - 推理延迟 → 缓存 embedding，异步预热
   - 成本失控 → 设定每日 cost cap，降级到关键词搜索
   - 幻觉问题 → 搜索不生成内容，只用 embedding 相似度
   - 可解释性 → 保留关键词得分作为 fallback 和日志
   - 人员能力 → 引入一名 ML Infra 工程师，不需要整个团队转型

4. **用数据赢得对话，不是用权威**
   "我不是在说 AI 不好——我在说这个方案让我们在 6 个月内有**可度量的进展**，而不是在交付日才发现延迟是 2 秒。"

**Result:**
VP 接受了 Phase 1 方案。4 周后 spike 结果显示语义搜索在长尾 query 上 +23% 召回，但在精确商品 ID 查询上差 15%。我们做了混合方案，6 个月后整体指标提升，没有发生一次全量回滚。

---

### ❌ 错误姿势 vs ✅ 正确姿势

**❌ Bad:**
> "好，6 个月，AI 重写，干！" — 政治正确，技术上在赌博。

**❌ Bad:**
> "这根本不可行，LLM 延迟太高。" — 过度悲观，错失业务机会，显得守旧。

**✅ Good:**
> "这方向是对的。让我们先用 1 周 spike 量化收益和成本，然后我给你一个有检查点的方案——4 周有东西上线，12 周有数据决策。"

---

### Senior/Staff 关键要点

- **永远先 spike，再 commit**：政治压力再大，不能绕过可行性验证
- **渐进式 > 大爆炸**：每个可以回滚的阶段都是风险控制
- **量化不确定性**：把"我觉得有风险"变成"P99 延迟预计 1.2s，超过我们 800ms SLA，这是缓解方案"
- **做桥梁，不做堡垒**：你的角色是让业务目标以可控方式实现，不是当守门人

*The Staff move: convert "rewrite everything" into "Phase 1 ships in 4 weeks with measured outcomes." You're not saying no — you're saying yes, with engineering discipline.*

---

📚 **References:**
- https://staffeng.com/guides/staff-projects — Will Larson on leading Staff-level projects
- https://www.amazon.science/blog/how-amazon-incorporates-ai-into-its-search-experience — Amazon hybrid search
- https://martinfowler.com/articles/patterns-of-distributed-systems/two-phase-commit.html — 渐进式迁移思想

🧒 **ELI5:** 老板说"把房子重建成玻璃的，6 个月"。聪明工程师说："先换一个窗户，看看效果和成本，然后决定是否继续。"
