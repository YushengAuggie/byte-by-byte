# 🗣️ 软技能 / Soft Skills — Architecture Conflict Resolution
*Day 52 · Expert Phase · ~2 min read*

---

## 问题 / Question

**"Describe a time you disagreed with a peer on architecture. How did you reach resolution?"**
*"描述一次你和同事在架构上产生分歧的经历。你是如何解决的？"*

---

## 为什么面试官问这个 / Why This Matters

架构分歧在工程团队中非常普遍。面试官想知道的不是谁"赢了"，而是：
1. 你能否**客观评估**技术权衡，而非固执己见
2. 你是否能在**保持关系**的同时推进正确的技术决策
3. Senior/Staff 工程师必须能在**没有权威**的情况下影响他人

*Architecture disagreements are universal. Interviewers want to know: can you objectively evaluate tradeoffs vs. being defensive? Can you advance the right decision while preserving relationships?*

---

## STAR 框架 / STAR Breakdown

**Situation（情境）:** 我们的团队在讨论新的通知服务架构。我倾向于用消息队列（Kafka）做异步处理，同事认为应该直接 HTTP 同步调用，更简单。

**Task（任务）:** 在不影响团队关系的前提下，推动一个技术上更合理的决定。

**Action（行动）:**
1. **先倾听，不急于反驳** — 我先请同事完整解释他的方案，找出合理之处（降低复杂度确实是有效考量）
2. **数据说话** — 我整理了具体场景：如果通知服务宕机，同步调用会导致上游服务超时；异步队列可以做到故障隔离
3. **提出折中** — 我们最终采用了消息队列，但同意先用 Amazon SQS 而非 Kafka，降低运维复杂度（部分采纳了他的顾虑）
4. **写下决策文档** — 记录了两个方案的权衡，未来有新人加入时可以理解背景

**Result（结果）:** 通知服务上线后，主服务的 P99 延迟降低了 40%（因为解耦了慢通知路径），同事也认可了这个方案。

---

## ❌ 坏回答 vs ✅ 好回答

❌ **"我坚持了自己的方案，因为我是对的，最后他接受了。"**
→ 听起来傲慢，无法展示影响力和协作能力

❌ **"我们让经理来决定。"**
→ 逃避，Senior 工程师不该总是上升到管理层

✅ **"我先理解了他的顾虑，发现有部分是合理的，找到了技术上更优但运维上更简单的折中方案。"**
→ 展示了技术深度 + 协作能力 + 成熟度

---

## Senior / Staff 加分点 / Advanced Tips

**如果对方是更资深的人：**
> "我会准备书面分析，列出两个方案的具体权衡（成本、风险、可维护性），而不是口头争辩。让数据做裁判。"

**如果团队陷入僵局：**
> 提出 **proof of concept** — "我们花两天分别实现，看看哪个在我们的约束下更合适"

**关键原则：**
- 分离技术判断和个人情绪
- 聚焦**系统目标**而非个人偏好
- 记录决策，避免未来再争同一个问题

---

## 关键收获 / Key Takeaways

1. 架构分歧要**先倾听再回应**，找出对方方案的合理之处
2. 用**具体数据和场景**论证，而不是"我觉得"
3. 寻找**技术上更优但兼顾对方顾虑**的折中方案
4. 把决策**写下来** — 这本身就是 Senior 工程师的标志

---

## 📚 参考资料 / References

- [Staff Engineer: Leadership beyond the management track — Will Larson](https://staffeng.com/book)
- [How to Disagree and Commit (Amazon Leadership Principle)](https://www.amazon.jobs/content/en/our-workplace/leadership-principles)
- [The Architecture Decision Record (ADR) pattern](https://adr.github.io/)

---

## 🧒 ELI5

两个工程师争架构，就像两个厨师争怎么做汤。聪明的做法不是谁嗓门大谁赢，而是：先尝对方的汤，找到好的部分，然后提议合并两个食谱里最好的地方，最后把这个"最终食谱"写下来，下次就不用再争了。

*Two engineers arguing about architecture is like two chefs arguing about a recipe. The smart move: taste each other's soup first, find the good parts, propose combining the best of both, then write down the final recipe so you never have to argue about it again.*
