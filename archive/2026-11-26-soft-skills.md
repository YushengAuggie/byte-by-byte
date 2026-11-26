# 🗣️ 软技能 / Soft Skills — Day 158 · Synthesis
> Expert Level · Synthesis Mode · 2 min read

---

## 新鲜场景题：你是如何处理"隐性技术债"的？
## Fresh Senior Scenario: How Do You Handle "Silent Technical Debt"?

**显性技术债** (explicit debt) 大家都知道 — 它在 JIRA 里，有 ticket，有 owner。  
**隐性技术债** (silent debt) 才是真正危险的 — 没人记录，没人负责，直到它炸掉生产。

Explicit debt is in JIRA. *Silent debt* is the kind nobody talks about — undocumented workarounds, "temporary" configs that become permanent, shared tribal knowledge that lives only in one person's head.

---

## 场景设定 / Scenario

> *"You join a team and notice a core service has zero observability — no metrics, no traces, no alerts. It's been running for 2 years. The team 'knows how to watch it' but nothing is written down. How do you handle it?"*

---

## STAR 拆解 / STAR Breakdown

**🎯 Situation (背景)**
描述你接手或发现一个系统/流程有隐性风险的场景，不要泛泛而谈 — 越具体越有说服力。

> "我加入 payments 团队后发现，我们的 settlement 服务没有任何 SLO，只有一位工程师知道如何手动触发 reconciliation job。"

**📋 Task (任务)**
说明你的角色和你设定的目标。别只说"我决定修它"— 说明**为什么这是优先项**，以及你是如何向团队和管理层定义风险的。

> "我的目标不只是修复一个点，而是推动团队建立一个系统化流程，把隐性知识显性化，降低关键人风险。"

**⚡ Action (行动) — 分层推进**
1. **审计 (Audit):** 花1周列出所有"只有某人知道"的操作 → 形成 risk register
2. **量化 (Quantify):** 把风险翻译成业务语言 — "如果这个人请假，我们有 48 小时内无法触发 settlement 的风险"
3. **小步推进 (Incremental):** 不申请大 sprint 重构，而是每个 PR 顺手加一条 runbook/alert
4. **共识 (Alignment):** 在 eng review 中展示进度，把它变成团队文化而不是个人项目

**📈 Result (结果)**
具体数字优先：
- 关键人风险从 N 人 → M 人覆盖
- P0 incident 中恢复时间从 X min → Y min（因为有 runbook）
- 新人 onboarding 时间缩短

---

## ❌ 坏答案 vs ✅ 好答案

| ❌ Bad | ✅ Good |
|---|---|
| "我告诉我的经理，然后他们修了它" | "我先用数据量化了风险，然后推动了一个渐进式的改进计划" |
| "我重写了整个服务" | "我在三个 sprint 内完成了：1) 文档化 2) 加监控 3) 轮换 on-call" |
| "这是个技术债，我们需要时间修" | "我找到了一个 20% 的改动，能消除 80% 的风险" |

---

## Senior/Staff 加分 / Senior+ Tips

**🔑 把风险翻译成业务语言:**
工程师说"这里没有 observability"，高级工程师说"如果这里出故障，我们要多花 X 小时才能发现，影响 Y 个下游服务和 Z 万美元收入"。

**🔑 建立系统，而不是修单点:**
一个 Staff 工程师不只是修一个 bug —— 他们会问"**为什么**这类债会积累？是我们的 PR 流程？Design review？"然后提出流程级别的改进。

**🔑 做到"不破坏现有节奏":**
把债务偿还嵌入日常工作流 (每个 PR 至少加一个 test/runbook/alert)，而不是申请一个独立的"还债 sprint"，后者通常会被高优先级功能挤掉。

---

## 举一反三 / Related Themes

这道题考查的核心能力可以迁移到其他 behavioral 题：
- **"Tell me about a time you improved reliability"** → 同框架
- **"How do you handle bus factor risk?"** → 关键人风险就是隐性债的一种
- **"How do you balance new features vs. technical debt?"** → 量化风险 + 渐进式计划

---

## 🧒 ELI5

就像家里有个漏水的管道，大家都知道，但因为没大水漫出来就一直不修。Senior 工程师是那个先量一下"每天漏多少水，多少天后会淹地下室"，然后找周末修了它的人。

Like a slow leak everyone ignores. The senior engineer is the one who measures how fast it's filling up, estimates when it floods, and fixes it before it becomes an emergency.

## 📚 References
- [Staff Engineer — Will Larson (staffeng.com)](https://staffeng.com/book)
- [The Document Culture of Amazon — Justin Garrison](https://www.justingarrison.com/blog/2021-03-15-the-document-culture-of-amazon/)
- [Accelerate — DORA Metrics & Tech Org Health](https://dora.dev/research/)
