# 🗣️ 软技能 / Soft Skills — How Do You Handle Scope Creep?

> Day 42 · Mastery Phase · ~2 min read

---

## 为什么这道题很重要 / Why This Matters

Scope creep 是项目失败的头号杀手。面试官问这题，不是想听你怎么"拒绝需求"，而是想看你**如何在交付压力、stakeholder 期望、工程质量之间找到平衡**。Senior+ 工程师要展示主动识别风险、结构化沟通的能力。

Scope creep is the #1 killer of engineering projects. Interviewers aren't testing whether you refuse requests — they want to see how you **balance delivery pressure, stakeholder expectations, and engineering quality**. Senior+ engineers must show proactive risk identification and structured communication.

---

## STAR 结构 / STAR Framework

### Situation（情境）
"我们在做一个新的支付对账系统，计划 8 周上线。第 4 周，PM 提出增加实时欺诈检测，这会引入 3 个新的外部 API 集成。"

"We were building a new payment reconciliation system, scoped for 8 weeks. In week 4, the PM proposed adding real-time fraud detection, requiring 3 new external API integrations."

### Task（任务）
识别风险、量化影响、向相关方清晰沟通，并推动达成一致决策。

Identify the risk, quantify the impact, communicate clearly to stakeholders, and drive a consensus decision.

### Action（行动）
1. **立即叫停，不要悄悄吸收** — 当场说"我需要先评估影响，不能直接答应"
2. **量化影响** — 写一页纸 impact analysis：+3 周工期，+2 名工程师，延期 2 个 sprint
3. **提出选项** — 不只说"不行"，给 3 个方案：
   - Option A: 推迟原计划上线，全做
   - Option B: 当前版本先上线，下个 sprint 加欺诈检测
   - Option C: 用第三方 SaaS（Stripe Radar）先填坑，内部方案等下季度
4. **推动决策** — 带着选项开会，让 stakeholder 做 informed decision

### Result（结果）
选了 Option C：原计划如期上线，用 Stripe Radar 临时方案。下季度我们自研方案完整上线，比临时方案准确率提高了 15%。

Chose Option C: original plan launched on time with Stripe Radar as stopgap. Next quarter, the in-house solution shipped with 15% better accuracy than the temporary solution.

---

## ❌ 不好的回答 vs ✅ 好的回答

❌ **"我会直接拒绝 scope 变更，告诉 PM 不行。"**
→ 听起来不灵活，不懂 business context

❌ **"我会默默加班把它做完。"**
→ 设错预期，可能最后两头不讨好

✅ **"我会先量化影响，再提出多个方案，让 stakeholder 做知情决策。"**
→ 展示工程判断力 + 沟通技巧 + 主人翁意识

---

## Senior/Staff 加分项 / Senior/Staff Signals

- **提前预防** — 在 kickoff 时就建立 change control 流程，不是等 scope creep 发生才处理
- **区分 want vs need** — 追问"这个功能不上，业务目标能达成吗？"往往 30% 的 scope 是 nice-to-have
- **建立信任储蓄** — 平时交付靠谱，说"这次先砍"才有说服力
- **用数据说话** — "加 3 个 API 集成 = +3 周 = Q3 OKR miss" 比"感觉很复杂"有力得多

---

## 关键要点 / Key Takeaways

1. **量化先于拒绝** — 先评估影响，再做决定
2. **提供选项，不只说"不"** — options-based communication
3. **让 stakeholder 做决策** — 你提供信息，他们对结果负责
4. **事后复盘** — scope creep 往往暴露需求分析不足，下次在 kickoff 阶段就对齐

---

## 📚 References

- [Shape Up — 37signals](https://basecamp.com/shapeup) — 如何用 appetite 控制 scope
- [Staff Engineer: Leadership Beyond the Management Track](https://staffeng.com/) — Will Larson
- [The Art of Saying No Without Saying No](https://www.svpg.com/the-art-of-saying-no/) — Marty Cagan

## 🧒 ELI5

你和朋友说好一起做一个 4 层蛋糕，中途朋友说"再加冰淇淋吧！"你不是直接说不行，而是说："加冰淇淋要多买材料，要多 2 小时，我们要不要换个方案：先做好蛋糕，下次单独做冰淇淋？"

You and a friend agreed to bake a 4-layer cake. Halfway through, they say "let's add ice cream too!" Instead of saying no, you say: "Adding ice cream needs more ingredients and 2 more hours — should we finish the cake first and make ice cream separately next time?"
