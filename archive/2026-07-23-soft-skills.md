# 🗣️ 软技能 / Soft Skills — Day 98 (Synthesis)
**Expert Phase — Fresh Senior/Staff Scenario**

---

## 新情景题 / Fresh Scenario: 技术路线分歧

**问题 / Question:**
> 你是 Staff Engineer。产品团队和你的直属团队在下一个大版本的技术路线上产生了严重分歧——产品团队要求用一套更快交付的第三方 SaaS 方案，而你的工程团队认为应该自研以保持长期控制权和成本优化。两边都有充分的理由，而 VP 要求你在下周的全员会上给出推荐方案。你会怎么做？

---

## 为什么这道题很重要 / Why This Matters

这是 Staff/Principal 级面试的核心题型：**跨组织对齐 + 技术决策 + 向上管理**。它考察你是否能：
- 在不确定性下做出有依据的推荐
- 建立信任而不是制造胜负
- 以数据和框架代替情绪和直觉

---

## STAR 分解 / STAR Framework

**Situation:** 两个有合理立场的团队，高压时间线，VP 期待你的推荐

**Task:** 在一周内给出可辩护的技术路线决策

**Action (Staff 级别的打法):**

**第一步：信息收集（2天）**
```
- 和产品团队：为什么急？SaaS 方案的具体选项是什么？vendor lock-in 风险是否评估过？
- 和工程团队：自研的资源估算是多少？维护成本？谁来 own it？
- 数据：现有系统的 pain points，用户规模，预期增长
```

**第二步：决策框架（不是"谁赢"，是"什么条件下用哪个"）**
```
                  Make (自研)          Buy (SaaS)
--------------+-------------------+------------------
短期交付速度   |      ❌ 慢         |      ✅ 快
长期成本       |      ✅ 可控       |      ❌ 随规模增
定制化能力     |      ✅ 完全控制   |      ❌ 受限
维护负担       |      ❌ 需要团队   |      ✅ vendor 负责
数据主权       |      ✅ 自有       |      ❓ 取决于合同
```

**第三步：给出有条件的推荐（"It depends + here's the framework"）**

✅ **好的推荐措辞：**
> "在当前 18 个月的产品冲刺周期内，我推荐使用 SaaS 方案，但附带三个条件：数据导出 API 必须可用、合同有明确的退出条款、我们在第 12 个月做 build/buy 再评估。如果这三个条件无法满足，风险太高，我们应该在接下来 6 周内启动自研 MVP 验证。"

---

## ❌ 不好的回答 vs ✅ 好的回答

**❌ Bad:**
> "我支持工程团队，自研更灵活。"（过于简单，没有数据支撑，显得偏袒）

**❌ Also Bad:**
> "我支持产品团队，我们需要快速交付。"（放弃了技术视角，不像 Staff）

**✅ Good:**
> "这不是二选一，是在特定约束下的优先级选择。我会用 3 天收集数据，建立决策矩阵，并在全员会上呈现：在什么条件下 SaaS 是对的，在什么条件下自研是对的，以及我的推荐和背后的 assumptions。"

---

## Senior/Staff 级加分点 / Senior Signals

- **建立 decision criteria 而不是 opinions** — 面试官想看到结构化思维
- **主动对齐利益相关方** — 在会议前而不是在会议上暴露分歧
- **给出可撤销的决定** — "我们先 SaaS，第 12 月评估" 比 "永远 SaaS" 更有弹性
- **量化风险** — "vendor lock-in 可能导致未来 2 年的迁移成本超过自研成本" 比 "vendor lock-in 不好" 有力

---

## Key Takeaways

1. **Staff 不 pick sides — Staff builds decision frameworks**
2. 用数据+条件推荐，而不是情绪化立场
3. 向上管理：让 VP 看到你的思考过程，而不只是结论
4. 为决定设置"触发器"——什么条件下推翻这个决定

---

## 📚 References
- https://staffeng.com/guides/deciding-technical-direction
- https://pragmaticengineer.com/blog/making-technical-decisions
- https://aws.amazon.com/blogs/enterprise-strategy/build-vs-buy-a-few-lessons-learned/

## 🧒 ELI5
想象你是班级的"调解员"：A 同学说"我们去打球"，B 同学说"我们去图书馆"。最好的做法不是站队，而是问清楚"我们今天的目标是什么？"，然后根据目标推荐最合适的方案。
