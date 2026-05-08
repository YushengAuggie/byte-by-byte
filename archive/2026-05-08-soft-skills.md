# 🗣️ 软技能 / Soft Skills — How Do You Approach System Design Trade-offs?

> Day 38 · Mastery Phase · ~2 min read

---

## 为什么这很重要 / Why This Matters

系统设计面试从来没有"标准答案"。面试官真正在评估的是：**你怎么思考，不是你背了多少**。能清晰表达权衡（trade-off）的工程师，才是 Senior/Staff 工程师的思维模式。

*System design interviews never have "correct" answers. Interviewers assess how you think, not what you've memorized. Engineers who can articulate trade-offs clearly demonstrate Senior/Staff-level thinking.*

---

## 核心框架 / Core Framework

用 **PAST 框架** 组织你的权衡讨论：

- **P**roblem: 先明确核心约束（读多写少？强一致性必须？延迟 vs 吞吐？）
- **A**lternatives: 列出 2-3 个方案，不要直接跳到答案
- **S**election: 说明为什么选这个方案（基于约束）
- **T**rade-offs: 主动说出你的选择放弃了什么

---

## STAR 拆解 / STAR Breakdown

**问题题干：** "How do you approach system design trade-offs?"

**Situation（情境）：**
"在设计 X 系统时，我们面临 A 和 B 两个选择..."

**Task（任务）：**
"我需要在强一致性和高可用性之间做出决定（CAP theorem），同时满足 <1s 的 p99 延迟要求..."

**Action（行动）：**
"我的方法是：先问清楚业务优先级——如果是金融交易，宁可不可用也不能数据不一致；如果是社交 feed，最终一致性完全可以接受。然后我会画出两种方案的架构，估算延迟和成本..."

**Result（结果）：**
"通过明确权衡，团队在 30 分钟内达成共识，避免了后来可能的重构..."

---

## ❌ 差回答 vs ✅ 好回答

**❌ Bad:**
> "我会选 microservices，因为它更好扩展。"

（没有说为什么，没有权衡，没有基于约束）

**✅ Good:**
> "这取决于几个维度：团队规模、一致性要求、和现有基础设施。如果团队只有 5 人，微服务的运维复杂度会拖累交付速度；如果有强 ACID 要求，分布式事务会很痛苦。在这个场景下，我会先从 modular monolith 开始，等扩展瓶颈出现后再拆分。"

---

## Senior/Staff 进阶技巧 / Senior/Staff Tips

1. **主动引导对话**："我想先明确几个约束，这会决定我的方向——DAU 是多少？数据一致性要求是什么？预算约束呢？"

2. **用数字锚定讨论**："如果写入 QPS 超过 10K，单机 MySQL 就到瓶颈了，我们需要 sharding 或 NoSQL"

3. **预判面试官的 follow-up**："我选择了 eventual consistency，这意味着用户可能看到短暂的不一致——我们可以用 client-side cache 或 read-your-write consistency 缓解这个问题"

4. **承认不确定性**："这我不确定，但我会这样评估..." — 这比假装确定更加分

---

## 关键要点 / Key Takeaways

- 权衡不是背答案，是展示**思维过程**
- 先问约束，再提方案——顺序很重要
- 主动说出"我选择 X 意味着放弃 Y"，比等面试官问更加分
- Staff 工程师的标志：能把技术决策和**业务影响**连接起来

---

## 📚 参考资料 / References

- [Designing Data-Intensive Applications — Martin Kleppmann](https://dataintensive.net/)
- [The Senior Engineer Checklist — blog.pragmaticengineer.com](https://blog.pragmaticengineer.com/the-senior-engineer-checklist/)
- [How to Answer System Design Questions — interviewing.io](https://interviewing.io/guides/system-design-interview)

---

## 🧒 ELI5

如果你妈问你"今晚想吃什么"，说"随便"是最差的回答。好的回答是："如果你不想花太多时间，我们吃面；如果想吃得健康，可以做沙拉；如果今天你很累，我来做简单的炒饭。你最看重哪个？"这就是系统设计权衡——先搞清楚优先级，然后给出基于约束的方案。

*If your mom asks "what do you want for dinner?", "anything" is the worst answer. A good answer: "If you don't want to spend much time, noodles; if you want healthy, salad; if you're tired, I'll make easy fried rice. Which matters most?" That's system design trade-offs — clarify priorities first, then propose based on constraints.*
