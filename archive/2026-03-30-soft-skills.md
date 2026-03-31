# 🗣️ 软技能 Day 13 / Soft Skills Day 13
## Leadership — 跨团队推动大型项目 / Driving a large cross-team initiative (Staff)

**📊 Day 14/150 · NeetCode: 13/150 · SysDesign: 12/40 · Behavioral: 12/40 · Frontend: 12/50 · AI: 5/30**
**🔥 2-day streak!**

---

## 为什么重要 / Why this matters

跨团队项目失败，通常不是因为技术不够强，而是因为：
- 目标不清晰（每个团队理解不一样）
- 激励不一致（你觉得重要，别人觉得“这不是我 OKR”）
- 沟通成本爆炸（会议太多、信息丢失、决策反复）

在 Staff/Lead 级别，**你的影响力 = 你让多少个团队朝同一个方向稳定前进**。

Cross-team initiatives fail less from tech issues and more from misalignment: unclear goals, mismatched incentives, and communication overhead. At Staff/Lead level, impact is measured by how well you align multiple teams toward a shared outcome.

---

## STAR 拆解（建议结构）/ STAR breakdown (recommended structure)

### S — Situation（背景）
中文要点：
- 业务压力是什么（增长、合规、成本、稳定性）
- 涉及哪些团队（平台、客户端、数据、SRE、法务…）

English cues:
- What business pressure triggered it?
- Which teams were involved and why?

### T — Task（你的任务）
中文要点：
- 你负责“对齐目标 + 拆解路径 + 推动落地”
- 明确成功指标（SLO、迁移比例、成本、时延、事故率）

English cues:
- Your mandate: align goals, create a plan, drive execution
- Define success metrics clearly

### A — Action（关键动作）
按“领导力动作”讲，而不是“我写了很多代码”。

1) **先对齐“Why”和指标**
- 写 1 页 RFC：问题、非目标、指标、范围、风险
- 用指标做 tradeoff：例如 p95 latency vs cost

2) **拆成可并行的里程碑**
- 让每个团队有明确 owner、deliverable、deadline
- 设计接口契约（API schema、事件契约、数据字段）

3) **建立节奏与可见性**
- 每周短 sync（15 分钟）+ 异步状态板（Jira/Notion）
- 风险清单（Risk register）：每个风险有 owner + 缓解方案

4) **处理冲突与激励**
- 先理解对方成本（人力、上线窗口、风险）
- 用“共同收益”重构问题：减少 oncall、减少重复实现

5) **把决策写下来**
- Decision log：为什么这么选，什么情况下会改

Explain actions as leadership moves, not just coding:
- Align on “why” and metrics (1-page RFC)
- Break into parallel milestones with clear owners
- Create operating cadence and visibility
- Resolve conflicts by understanding incentives
- Document decisions (decision log)

### R — Result（结果）
尽量量化：
- 迁移完成率、性能提升、成本下降、事故减少
- 以及“组织性结果”：减少团队摩擦、形成可复用模板

Quantify outcomes (migration %, latency, cost, incident rate) and organizational impact (repeatable playbooks, reduced friction).

---

## ❌ Bad vs ✅ Good（对比示例）/ Example contrast

❌ **Bad（像项目协调员）**
- “我组织了很多会议，跟进大家进度，最后做完了。”

✅ **Good（像 Staff leader）**
- “我先把目标收敛到两个指标（p95 时延 + 失败率），写了 RFC 并让各团队签字确认；然后把工作拆成 3 个可并行里程碑，并用接口契约减少依赖；过程中我维护风险清单并提前升级资源冲突，最后在 6 周内完成迁移，事故率下降 40%，同时沉淀了后续可复用的迁移模板。”

Bad sounds like meeting coordination. Good demonstrates alignment, structured execution, risk management, and measurable impact.

---

## Staff / Senior tips
- **用“指标”而不是“意见”去对齐**：指标是共同语言。
- **先拿一个“可见的早期胜利”**：降低阻力，建立信任。
- **边界清楚：什么是非目标**（避免 scope creep）。
- **接口契约先行**：跨团队最大的坑是隐性假设。
- **升级不是甩锅**：是给决策者更早的选择权。

Use metrics as a shared language, secure an early win, define non-goals, lead with contracts, and escalate early as a decision-enabling move.

---

## Key Takeaways
- 讲跨团队项目：**对齐（metrics）→ 拆解（milestones）→ 可见性（cadence）→ 风险（register）→ 结果（quantify）**
- 让面试官看到：你能把混乱变成可执行的系统。

---

## 📚 References
- Google — Effective Triggers for Leadership / Engineering leadership concepts: https://rework.withgoogle.com/ 
- Atlassian — Working agreements & team alignment: https://www.atlassian.com/team-playbook
- Amazon — Leadership Principles (framing for ownership & influence): https://www.amazon.jobs/content/en/our-workplace/leadership-principles

## 🧒 ELI5
你要带很多同学一起做大作业：先写清楚“我们要拿多少分”（指标），再分工（里程碑），每周看一次进度（节奏），遇到问题提前说（风险），最后把成绩讲清楚（结果）。

It’s like leading a group project: agree on the grade goal (metrics), split tasks, check in regularly, call out risks early, and clearly report the final result.
