# 🗣️ 软技能 / Soft Skills — Day 112
## 综合场景 / Synthesis Scenario: Staff Level

**场景 / Scenario**: 你如何在没有直接汇报关系的情况下，推动整个工程组织采用一个新标准（比如新的 API 设计规范、可观测性框架、或安全最佳实践）？

How do you drive adoption of a new engineering standard across an entire organization — without direct authority over the teams?

---

## 为什么这道题重要 / Why This Matters

Staff/Principal Engineer 的核心影响力 = **技术领导力 × 横向影响力**。
面试官想看的是：你不靠职位权威，而是靠说服力、工具、激励机制来推动变革。

The core of Staff+ engineering is **technical leadership × horizontal influence**.
Interviewers want to see: driving change through persuasion, tooling, and incentives — not authority.

---

## STAR 框架示例 / STAR Example

**Situation:**
公司有 12 个微服务团队，每个团队的 API 设计风格各异。新来的平台客户反映集成成本极高——每个 API 的错误格式、分页方式都不同。

12 microservice teams, each with their own API design conventions. New platform clients complaining about high integration cost — every API had different error formats, pagination styles.

**Task:**
作为 Staff Engineer，你没有直接管辖权，但被期望推动全公司 API 标准化。

As a Staff Engineer with no direct authority, but expected to drive API standardization company-wide.

**Action:**

1. **先理解现状**: 做了一轮快速调研，收集各团队痛点和现有模式
   *First understood the landscape: quick survey, collected team pain points and existing patterns*

2. **找盟友**: 识别出3个"影响者团队"（公司内部被其他团队参考最多的）
   *Found allies: identified 3 "influential teams" others looked to*

3. **提案驱动**: 起草了 RFC（Request for Comments），用"提案 + 公开讨论"代替"自上而下命令"
   *Proposal-driven: wrote an RFC, used "proposal + open discussion" instead of "top-down mandate"*

4. **降低采用成本**: 提供了 code linter、OpenAPI 模板、迁移指南
   *Reduced adoption cost: provided code linter, OpenAPI templates, migration guide*

5. **激励 early adopters**: 帮第一批采用的团队做集成，publicize 他们的成果
   *Incentivized early adopters: helped first teams with integration, publicized their wins*

6. **设定合理时间线**: 不要求立刻迁移，新 API 必须符合标准，旧 API 下季度前迁移
   *Reasonable timeline: new APIs must conform, legacy APIs migrate next quarter*

**Result:**
6个月后，10/12 团队完全采用，平台集成时间从平均3天降到半天。另外2个团队有 legacy 问题，制定了专项计划。

6 months later, 10/12 teams fully adopted. Platform integration time dropped from avg 3 days to half a day. 2 remaining teams had legacy constraints — dedicated migration plan created.

---

## ❌ Bad vs ✅ Good

| ❌ 弱回答 | ✅ 强回答 |
|-----------|-----------|
| "我发了一封邮件告诉大家要遵守新规范" | "我先做了调研，理解了每个团队的阻力来源" |
| "因为我是 Staff 所以他们应该听我的" | "我把采用成本降到最低，让变革变得'顺势而为'" |
| 没有量化结果 | 有具体指标：采用率、集成时间减少、团队数量 |

---

## Senior/Staff 思维框架

**影响而非命令** → RFC > 会议室命令
**降低摩擦** → 工具链 + 模板 + 文档
**找杠杆点** → 影响者团队 + 平台层面的约束
**可见成果** → 内部博客、Slack 分享、季度回顾

---

## 📚 References
- [Staff Engineer: Leadership beyond the management track](https://staffeng.com/book)
- [Writing RFC Documents — Increment Magazine](https://increment.com/planning/when-to-write-design-documents/)
- [Influencing Without Authority — HBR](https://hbr.org/2018/02/how-to-build-your-reputation-as-an-expert)

## 🧒 ELI5
没有权力怎么推动改变？就像推广一个新游戏规则：先让最受欢迎的朋友玩，帮他们玩得开心，然后其他人自然就跟着来了。强迫不如吸引。

How to drive change without authority? Like spreading new game rules: get the most popular kids to play first, make it fun for them, and others naturally follow. Attraction beats coercion.
