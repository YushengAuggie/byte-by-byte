# Day 64 — Soft Skills: How do you keep a long-running project on track when momentum stalls?

🗣️ **软技能 / Soft Skills** — Project Management: Keeping Momentum

---

## 为什么这很重要 / Why This Matters

长期项目 (3个月+) 几乎必然遭遇动力衰退——范围蔓延、依赖方失联、团队疲惫、优先级漂移。Senior/Staff 工程师被考察的不只是「能不能交付」，而是**在逆境中维持团队信心和执行力的能力**。

Long-running projects (3+ months) almost always hit momentum stalls — scope creep, disengaged dependencies, team fatigue, priority drift. Senior/Staff engineers are evaluated not just on "can you deliver" but **the ability to maintain team confidence and execution under adversity**.

---

## STAR 框架 / STAR Breakdown

**Situation (情境)**:  
项目推进到第 3 个月，遇到一个外部依赖团队连续 4 周未交付关键 API 接口，导致我们的进度完全卡住，团队士气低落，发布日期岌岌可危。

We were 3 months into a project. A critical external team missed their API delivery for 4 consecutive weeks. Our progress was completely blocked, team morale dropped, and the release date was in jeopardy.

**Task (任务)**:  
作为项目技术负责人，需要在不失去发布时间窗口的情况下，重建团队执行力。

As tech lead, I needed to rebuild execution momentum without losing the release window.

**Action (行动)**:
1. **诊断真实阻塞** — 开 1:1 了解阻塞真相：外部团队 API 文档不全 → 帮他们写好 spec，降低他们的摩擦
2. **解耦依赖** — 用 mock server + contract testing 让我们的开发不再等待真实 API
3. **重新切分里程碑** — 把一个大 milestone 拆成 2 周一个的「进度锚点」，每个都有可演示的产出
4. **对上管理预期** — 主动向 PM 和管理层提前报告风险，附带缓解方案 (不是光报告问题)
5. **庆祝小胜利** — 每完成一个进度锚点，在 Slack 公开认可团队贡献

**Result (结果)**:  
延期 2 周但完整交付，团队没有人离开项目。事后复盘时，这个「解耦+小里程碑」模式被推广到部门其他团队。

Shipped 2 weeks late but with full scope. Zero team attrition during the crisis. The "decouple + small milestones" pattern was adopted across the org after the retrospective.

---

## ❌ Bad vs ✅ Good

**❌ 糟糕回答 / Bad Answer**:  
"我们加班把落后的进度赶回来了，团队非常努力。"  
→ 只展示了执行力，没展示**系统思维和主动风险管理**。

**✅ 优秀回答 / Good Answer**:  
展示三层能力：  
1. 诊断根本原因 (不只是症状)  
2. 创造可执行的替代路径  
3. 管理上下左右的预期

---

## Senior/Staff 加分项 / Senior-Level Tips

- **提前报警，不要晚节不保** — 每 2 周做一次 risk review，发现趋势立即升级，而不是等到危机爆发
- **让「不确定性」可视化** — 用置信区间代替单点估算："我们 80% 概率在 Q3 结束前交付，有 20% 风险延到 Q4 第一周，原因是 X"
- **投资团队能量** — 「战时」也要保持 1:1，了解谁在 burn out，提前换人比临阵崩溃好
- **构建交付肌肉记忆** — 坏消息要比好消息早到达管理层，这样你的信用额度才足够扛过危机

---

## Key Takeaways / 关键要点

1. **解耦优先** — 外部依赖阻塞时，先想「我怎么在没有它的情况下继续前进？」
2. **大里程碑 → 小锚点** — 可见进展本身就能维持士气
3. **主动管理 vs 被动汇报** — 带方案报告问题，不带方案只是转移焦虑
4. **动力 = 进展感** — 团队需要感受到「我们在往前走」

---

## 📚 References
- https://www.manager-tools.com/2005/07/the-feedback-model
- https://www.amazon.com/Making-Work-Visible-Exposing-Optimize/dp/1942788150
- https://paulgraham.com/mean.html

## 🧒 ELI5
项目卡住就像自行车链条脱落。不是踩得更用力 (加班)，而是先下车把链条挂回去 (解除阻塞)，然后把长途旅程分成几个小段 (里程碑)，每段终点都有可以休息和庆祝的地方。

A stalled project is like a bicycle chain falling off. Don't pedal harder (overtime) — get off and reattach the chain (unblock), then split the long journey into short segments (milestones), each with a rest stop where you can celebrate progress.
