📊 NeetCode: 23/150 · SysDesign: 22/40 · Behavioral: 22/40 · Frontend: 22/50 · AI: 11/30
🔥 1-day streak!

🗣️ **软技能 / Soft Skills**
# 如何在新团队建立信任？/ How do you build trust with a new team?

## 为什么重要 / Why this matters
中文：在新团队里，信任不是“人好就有”，而是一个**降低协作摩擦的系统**：大家相信你会按时交付、沟通透明、在关键时刻站得住。

English: Trust reduces coordination cost. People rely on you to deliver, communicate clearly, and act predictably under pressure.

---

## STAR 拆解 / STAR breakdown
### S (Situation)
中文：刚加入团队/跨组接手一个服务，代码和 ownership 都不熟，大家担心你会“乱改”。

English: You join a new team or inherit a service; ownership is unclear and people fear risky changes.

### T (Task)
中文：在不打扰团队节奏的前提下，快速形成可靠产出，并让关键同事愿意与你协作。

English: Become productive without disrupting flow, and earn collaboration from key partners.

### A (Action)
中文（可直接照着说，偏 Senior/Staff）：
1. **先对齐“成功定义”**：1:1 问清楚本季度最重要的指标、风险点、谁是决策者。
2. **用小而稳的交付建立信用**：先做一两个低风险改动（修 bug、补监控、改善 oncall runbook），在 PR 里解释“为什么”。
3. **默认透明**：写 short design doc / RFC，记录 tradeoff；在 standup 里讲进展 + 阻塞 + 下一步。
4. **让别人更容易跟你合作**：缩短 review turnaround；把复杂问题拆成可并行的 task；把“需要谁决定什么”写清楚。
5. **遇到问题先扛责再复盘**：出事故时先稳定系统、同步影响面，再做 blameless postmortem。

English:
1. Align on what “success” means (metrics, risks, decision makers).
2. Build credibility with small, low-risk wins (bugfixes, monitoring, runbooks) and explain the “why” in PRs.
3. Default to transparency (short RFCs, tradeoffs, steady status updates).
4. Make collaboration easy (fast reviews, parallelizable tasks, explicit decisions needed).
5. In incidents: stabilize first, communicate clearly, then run a blameless postmortem.

### R (Result)
中文：你会得到两类信任：
- **执行力信任**（你说到做到）
- **判断力信任**（你做的选择是靠谱的）

English: You earn both execution trust (you deliver) and judgment trust (your decisions are sound).

---

## ❌ Bad vs ✅ Good（示例回答对比）/ Bad vs Good
❌ 中文：
“我会多和大家沟通，努力融入团队。”（太空、不可验证）

✅ 中文：
“前两周我先做两件事：补齐关键指标监控 + 写 oncall runbook，并在每个 PR 里把风险和 rollback 写清楚。第三周开始我会发一个 1 页的 feed latency 优化 RFC，列出 2 个方案和 tradeoff，请 tech lead 做决策。”

❌ English:
“I communicate a lot and try to fit in.” (vague)

✅ English:
“In the first two weeks I shipped monitoring + an oncall runbook, and every PR included risk + rollback. In week three I proposed a 1-page latency RFC with two options and tradeoffs for the TL to decide.”

---

## Senior / Staff 加分点 / Senior/Staff tips
- 中文：**把信任当成 SLO**：可预测的节奏（updates、designs、rollbacks）就是可靠性。
- 中文：**用“决策日志”建立判断力**：记录你为什么选 A 不选 B，半年后复盘你是否在提升。
- English: Treat trust like an SLO: predictable cadence beats charisma.
- English: Keep a decision log to demonstrate and improve judgment.

---

## Key Takeaways
- 中文：信任=可预测 + 透明 + 稳定交付。
- 中文：先小胜建立信用，再啃硬骨头。
- English: Trust = predictability + transparency + delivery.
- English: Start with small wins, then tackle the hard problems.

---

## 🧒 ELI5
中文：你刚加入新班级，大家不认识你。你先按时交作业、说话算数、遇到问题会解释清楚，大家自然就信你。

English: In a new class, you earn trust by doing what you say, on time, and explaining things clearly.

---

## 📚 References
- https://staffeng.com/guides/staff-archetypes/
- https://www.pmcouncil.org/insights/psychological-safety/
- https://hbr.org/2019/01/the-fundamental-attribution-error
