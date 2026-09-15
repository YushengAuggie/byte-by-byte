# 软技能 / Soft Skills — Day 133
**日期 / Date:** 2026-09-15 | **阶段 / Phase:** Expert | **模式 / Mode:** Synthesis

---

## 🗣️ 软技能 / Soft Skills — Staff-Level 场景综合
### Fresh Scenario: Navigating a Major Org Reorg Mid-Project

---

### 🎯 场景 / Scenario

> 你是 Staff Engineer，正在领导一个已进行到 60% 的关键基础设施迁移项目。公司突然宣布重组：你的团队被拆分，部分成员去了另一个 BU，你的新 manager 对这个项目背景完全陌生。如何让项目继续推进并维护信任？
>
> You're a Staff Engineer, 60% through a critical infrastructure migration. The company announces a reorg: your team is split, some members move to another BU, your new manager has zero context on the project. How do you keep it moving and maintain trust?

---

### ⭐ STAR 框架拆解 / STAR Breakdown

**Situation (背景):**
- 项目进行中、人员流失、新 manager 无上下文
- 关键 context：你的 credibility 是基于旧结构建立的

**Task (任务):**
- 维持项目交付不 slip
- 让新 manager 在 48 小时内建立足够信任
- 保留关键知识，防止 team 离散时知识流失

**Action (行动) — Senior 水平的做法：**

1. **立即行动：写一份 "Project Health Doc"**（不等新 manager 来问）
   - 当前状态、风险、决策历史、依赖方、剩余工作 → 一页纸
   - 目的：让任何人 15 分钟内能 onboard

2. **主动 1:1 新 manager，带着明确议程**：
   - "这是我们的状态，这是最大的 3 个风险，这是我需要你帮助解封的 1 件事"
   - 不 dump 所有历史，只给他们"决策所需的最小上下文"

3. **与离队成员快速知识迁移**：
   - 写 ADR（Architecture Decision Records）补全缺失文档
   - 用 pair programming 把隐性知识显性化

4. **调整计划，但守住交付日期**：
   - 主动提出"我们可以 descope X 以保证核心目标"，而不是要求延期
   - Staff 水平：你要提方案，不是汇报问题

**Result (结果):**
- 新 manager 在第一周末就能独立向上汇报项目状态
- 项目按时交付，只 descoped 了非关键功能
- 你建立了在模糊环境下的可靠性声誉

---

### ❌ Bad vs ✅ Good

```
❌ 等新 manager 来找你要状态更新
   "我在等新的组织架构确认后再推进"
   抱怨 reorg 打断了项目节奏

✅ 主动写 Project Health Doc，第一天就发
   "不管结构如何变，我的目标不变，这是我的计划"
   把 reorg 当作展示 Staff 级别 resilience 的机会
```

---

### 🎓 Senior/Staff 级别的洞察 / Senior/Staff Insight

**为什么这道题在 Staff 面试很常见？**

它测试的是：
1. **Organizational resilience** — 你在混乱中的可靠性
2. **Influence without authority** — 新 manager 是 blank slate，你要快速建立 credibility
3. **Proactive vs reactive** — Staff 不等问题找你，你找问题

> **关键词 / Key Framing:** "我把每一次 reorg 当作机会，而不是障碍。混乱时期，谁能提供清晰度，谁就有影响力。"
>
> "I treat every reorg as an opportunity. In chaos, whoever provides clarity gains influence."

---

### 💡 Key Takeaways

1. **写下来胜过说出来** — 文档是你在场时和不在场时都有效的影响力工具
2. **给新老板"最小可决策上下文"**，不是历史课
3. **主动提 descope，不等被要求延期** — 控制叙事
4. **Reorg 是 Staff 的考场**，不是障碍

---

### 📚 References
- https://staffeng.com/guides/staff-projects — Will Larson on Staff-level projects
- https://lethain.com/navigating-ambiguity/ — Navigating ambiguity at senior levels
- https://www.amazon.com/Staff-Engineer-Leadership-beyond-management/dp/1736417916 — Staff Engineer book

### 🧒 ELI5
就像你正在盖一栋楼，突然换了个新包工头，他完全不知道楼的设计图。你要做的不是抱怨，而是先给他画一张简明地图，告诉他：现在到哪了、剩下什么、最大的风险是什么。这就是 Staff 工程师的样子——在混乱中制造清晰。

Imagine you're building a house and suddenly get a new foreman who knows nothing about the design. Don't complain — hand them a simple map: where we are, what's left, what's risky. That's Staff-level: creating clarity in chaos.
