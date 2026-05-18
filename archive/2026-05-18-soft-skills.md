# 🗣️ 软技能 / Soft Skills — 如何评估和采纳新技术？

> 📅 Day 46 | ⏱️ 2 min read | 🔴 Senior/Staff | Category: Technical Vision

---

## ❓ 问题 / The Question

**"How do you evaluate and adopt new technologies for your team?"**

这道题考的不是你是否跟得上技术趋势，而是你是否有**系统性的判断框架**，以及是否能为团队的技术决策承担责任。

*This question isn't about whether you keep up with trends — it's about whether you have a systematic framework for judgment and whether you can own the consequences of your team's tech decisions.*

---

## 🌟 为什么这很重要 / Why This Matters

作为 Senior/Staff，你的技术选型决策会影响整个团队未来2-3年的工作。一个被炒作带偏的决策（"大家都在用 GraphQL！"）可能让团队陷入维护噩梦。一个过于保守的决策则会让团队错失生产力提升。

*Your tech adoption decisions shape how the team works for years. Hype-driven choices create maintenance nightmares; over-conservatism leaves productivity gains on the table.*

---

## ⭐ STAR 拆解 / STAR Breakdown

### Situation
"我们的数据管道用的是一套自研的 batch 系统，处理延迟达到 4 小时。团队里有人提议切到 Apache Flink 做实时流处理。"

*"Our data pipeline used an in-house batch system with 4-hour lag. A team member proposed migrating to Apache Flink for real-time streaming."*

### Task
"作为 tech lead，我需要评估这是一个真正的技术提升，还是为了技术而技术的冲动。"

*"As tech lead, I needed to evaluate whether this was a genuine improvement or technology for its own sake."*

### Action
**我用了一个四步框架 / I used a four-step framework:**

1. **问题优先 / Problem First**：先问"我们真正要解决的问题是什么？"是延迟？吞吐量？可维护性？  
   *Start with: "What problem are we actually solving?" Latency? Throughput? Maintainability?*

2. **成本全核算 / Total Cost of Ownership**：不只是性能，还有学习曲线、招聘难度、运维复杂度、迁移成本。  
   *Not just performance gains — learning curve, hiring difficulty, operational complexity, migration cost.*

3. **低风险验证 / Low-Risk Validation**：先在一个非关键管道上做 spike（时间盒限定1周），不上生产。  
   *Time-box a spike (1 week) on a non-critical pipeline. No production risk.*

4. **退出条件 / Exit Criteria**：事先定好"什么情况下我们会说不"，而不是做了一半骑虎难下。  
   *Define upfront: "Under what conditions do we walk away?" Don't let sunk cost drive decisions.*

### Result
"Spike 验证了 Flink 确实能解决延迟问题，但我们也发现 Kafka Connect + simple stream processors 能以 20% 的复杂度实现 80% 的收益。我们最终采用了简化方案，3 个月后延迟从 4h 降到了 10 分钟，没有新的运维负担。"

*"The spike confirmed Flink solved the latency problem, but we also found Kafka Connect + simple stream processors could get 80% of the benefit with 20% the complexity. We shipped the simpler solution — latency went from 4h to 10min with no new operational overhead."*

---

## ❌ Bad vs ✅ Good

**❌ "我们用 Kubernetes 因为所有人都在用。"**  
→ 这是 FOMO 驱动的决策，没有与业务问题挂钩。

**✅ "我们评估了 Kubernetes，发现它解决的问题我们没有（<10 个服务，单机可以运行），所以推迟到规模扩大再考虑。"**  
→ 这显示了技术判断，而不是盲目跟风。

---

## 💎 Senior/Staff 加分项 / Senior/Staff Tips

- 提到**技术债务**权衡：新技术引入也是在创造新的技术债务，要明确说出来
- 提到**团队知识分布**：如果只有一个人懂新技术，这是风险，不是优势
- 提到**可逆性**：好的技术决策应该尽量可逆（先用 feature flag，先做小模块）
- 说出你曾经**拒绝**采纳某个热门技术的经历，比"我推动了某某技术"更有说服力

---

## 🎯 Key Takeaways

1. **问题驱动，不是技术驱动** — Problem first, technology second
2. **全成本核算** — Performance is easy; operational cost is hard
3. **时间盒验证** — Spike before committing
4. **事先定好退出条件** — Define failure criteria upfront

---

## 🧒 ELI5

就像买车。不能因为邻居买了特斯拉你就买。先问自己：我主要在城里开还是跑长途？我有充电桩吗？我的预算是多少？答案对了，再选车型。

*It's like buying a car. Don't buy a Tesla just because your neighbor did. First ask: mostly city driving or highway? Do I have a charger? What's my budget? Answer those first, then pick the model.*

---

## 📚 References

- [Staff Engineer — Will Larson's Technology Radar Framework](https://staffeng.com/guides/work-on-what-matters)
- [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar)
- [Joel Spolsky — Things You Should Never Do (rewriting from scratch)](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/)
