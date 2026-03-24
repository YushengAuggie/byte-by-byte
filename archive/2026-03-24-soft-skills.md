# 🗣️ 软技能 Day 9 / Soft Skills Day 9

**主题 / Topic:** 利益相关方管理 / Stakeholder Management
**问题 / Question:** Describe a time you had to push back on a feature or requirement. Why?

---

## 💡 为什么这道题很重要 / Why This Matters

在高级工程师面试中，面试官不只想知道你"会写代码"——他们想知道你能不能独立判断、有没有勇气说出"这个需求有问题"。盲目执行坏需求是初级工程师的行为；能够用数据和逻辑推动正确方向，是 Senior/Staff 的核心能力。

Interviewers want to know you're not just a "feature factory." Senior engineers own outcomes, not just outputs. Pushing back constructively — with data, not attitude — is a core competency at L5+.

---

## ⭐ STAR 拆解 / STAR Breakdown

### Situation（情境）
> 设置背景：什么团队？什么项目阶段？紧迫程度？

"我们的 PM 要求在发布前两周新增一个实时用户追踪功能，当时系统负载已经接近上限。"

"Our PM requested a real-time user tracking feature two weeks before a major launch, when our system load was already near capacity."

### Task（任务）
> 你的职责是什么？你为什么有发言权？

"作为负责后端基础设施的 Senior Engineer，我需要评估这个需求的可行性和风险。"

"As the Senior Engineer owning backend infra, I needed to assess feasibility and surface the technical risk."

### Action（行动）
> 这是核心！展示你如何**有据可查地**推回，而不是情绪化地拒绝。

1. **量化风险：** 我跑了负载测试，展示新功能会把 P99 延迟从 120ms 推高到 650ms
2. **提出替代方案：** 建议将实时追踪改为批量日志，延迟 24h 但不影响核心体验
3. **对齐业务目标：** 确认 PM 真正想要的是"数据分析能力"而不是"实时性"——批量方案完全满足
4. **共识达成：** 带着数据找 PM + 工程总监开了 30 分钟会议，最终采用我的方案

"I ran load tests showing P99 latency would spike from 120ms to 650ms. I proposed batch logging instead — same data, 24h delay, zero performance impact. I aligned with PM on the real goal (analytics, not real-time), and brought data to a 30-min meeting with PM and Eng Director. We shipped the batch solution."

### Result（结果）
> 用数字说话。

"发布如期进行，零性能事故。批量数据方案在发布后三个月上线，PM 反馈数据质量超出预期。这次经验也推动团队建立了需求评审中的技术可行性评估流程。"

"Launch shipped on time with zero incidents. The batch analytics shipped 3 months post-launch and exceeded data quality expectations. The experience led to establishing a technical feasibility step in our requirements review process."

---

## ❌ 别这么说 / Bad vs ✅ 这么说 / Good

| ❌ 踩坑 | ✅ 正解 |
|--------|--------|
| "我直接告诉 PM 这个要求太蠢了" | "我跑了测试，把风险用数据量化" |
| "我认为这不重要，所以不做" | "我先理解他们的真实目标，再提替代方案" |
| "最终我没能阻止，还是做了" | "我确保所有决策者都了解风险，决策有据可查" |
| "我们就这么做了" → 没有结果 | 说清楚结果：上线情况、用户影响、后续改进 |

---

## 🚀 Senior/Staff 加分点 / Senior+ Tips

1. **系统化推回，而非感情化拒绝。** 数据 > 直觉。Load test、cost model、用户影响分析——让数字说话。
2. **先理解"为什么"，再评估"怎么做"。** 很多"坏需求"背后有合理的业务原因，找到根本目标才能提出真正有价值的替代方案。
3. **建立信任储备。** 平时 deliver 靠谱，关键时刻的推回才会被认真对待。
4. **把决策过程文档化。** 即使你没能推回成功，确保风险已被知晓和记录，保护自己也保护团队。

---

## 🎯 Key Takeaways

- 推回 ≠ 拒绝。推回 = 用专业判断守护产品质量。
- Push back = professional judgment, not obstruction.
- 永远带着数据和替代方案去谈，而不是空手说"不行"。
- Always come with data + alternatives, never just "no."
- 好的推回最终是双赢：工程质量 + 业务目标都得到保护。

---

## 📚 参考资料 / References

1. [The Engineering Manager's Handbook — Pushing Back Effectively](https://www.engmanager.com/)
2. [Staff Engineer: Leadership Beyond the Management Track (Will Larson)](https://staffeng.com/book)
3. [How to Disagree Productively — First Round Review](https://review.firstround.com/how-to-disagree-productively-and-find-common-ground/)

---

## 🧒 ELI5 / 用小孩能理解的话说

如果你的朋友说"我们现在去游泳吧"，但你知道外面在下大雨，你不是直接说"不去"，而是说"你想游泳吗？那我们去室内游泳池！"——这就是有建设性的推回。

If a friend says "let's swim now!" but it's raining, you don't just say "no" — you say "want to swim? Let's go to the indoor pool!" That's constructive pushback.
