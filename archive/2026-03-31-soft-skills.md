# 🗣️ 软技能 Day 14 / Soft Skills Day 14
## Tell me about a time you drove a large cross-team initiative

> **级别 / Level:** Staff · **主题 / Category:** Leadership · **Read time:** 2 min

---

## 为什么重要 / Why this matters

**中文：**
跨团队项目（例如：统一身份认证、支付迁移、数据平台升级、全站性能治理）最大的风险往往不是技术，而是**对齐、节奏、依赖、沟通成本**。Staff 级别面试官想听到的是：你如何在没有“直接汇报关系”的情况下，把很多人带到同一条船上。

**English:**
For cross-team initiatives, the hardest part is rarely the technical design—it’s alignment, dependencies, cadence, and communication overhead. Interviewers want evidence you can lead without formal authority.

---

## ⭐ STAR 结构（建议 90 秒回答）/ STAR structure (aim for 90 seconds)

### S — Situation（背景）
- 中文：项目是什么？影响范围多大？涉及哪些团队？
- English: What was the initiative? Scope? Which teams?

### T — Task（你的职责）
- 中文：你具体负责什么？目标/成功标准是什么（SLO、迁移比例、成本、上线日期）？
- English: What did you own? What were the success metrics?

### A — Action（你做了什么）
用“可复制的方法论”讲：
1) **定义北极星指标 / Define a north-star metric**：例如 p95 latency、error budget、migration completion。
2) **把问题拆成工作流 / Break into a plan**：里程碑、风险清单、依赖图、RACI（谁负责/批准/咨询/知会）。
3) **建立节奏 / Create operating cadence**：每周 cross-team sync、异步周报、决策记录（ADR）、升级通道。
4) **提前拆雷 / De-risk early**：先做 POC / pilot、灰度、回滚预案、观测（dashboards + alerts）。
5) **对齐激励 / Align incentives**：明确“对他们有什么好处”（减少 oncall、降低成本、提高转化）。

English (same content):
1) Define a measurable north-star metric.
2) Turn ambiguity into a concrete plan (milestones, dependency map, RACI).
3) Establish cadence (syncs, async updates, decision logs).
4) De-risk early (pilot, gradual rollout, rollback plan, observability).
5) Align incentives so partner teams want to participate.

### R — Result（结果）
- 中文：用数字结尾：提前/按期上线、迁移比例、故障率下降、成本节省、开发效率提升。
- English: Close with numbers: completion %, latency improvement, incidents reduced, cost savings.

---

## ❌ Bad vs ✅ Good（面试官一听就懂）/ Bad vs Good

**❌ Bad（空泛）**
- “我组织了很多会议，大家最后达成一致，然后上线了。”

**✅ Good（可验证）**
- “我先把目标写成 p95 从 800ms 降到 400ms，并把依赖拆成 3 条迁移路径；每周一次跨团队同步 + 每两天异步进度；关键风险是 X 团队的 schema 变更，于是先做了两周 pilot 和双写；最终 6 周内迁移 92%，相关 oncall 事故从每周 5 起降到 1 起。”

---

## Senior/Staff 加分点 / Senior/Staff-level tips

- **把决策写下来**：用 ADR 记录 tradeoffs，不靠“口口相传”。
- **沟通要“分层”**：IC 关注任务与风险，Manager 关注里程碑与资源，Exec 关注指标与 ROI。
- **处理冲突的方式**：先找共同目标，再用数据/实验说话；必要时明确升级路径。
- **让系统自动运行**：好的机制（dashboard、SLO、自动化迁移工具）比个人英雄更可靠。

---

## Key Takeaways
- 中文：跨团队项目 = 目标清晰 + 依赖可视化 + 节奏稳定 + 风险前置 + 激励对齐。
- English: Cross-team success = clear metrics + dependency visibility + steady cadence + early de-risking + aligned incentives.

---

## 📚 References
- Google SRE Book — Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
- RACI matrix overview (Atlassian): https://www.atlassian.com/team-playbook/plays/roles-and-responsibilities
- Amazon Working Backwards (concept): https://www.aboutamazon.com/news/company-news/working-backwards-how-amazon-starts-with-the-customer

## 🧒 ELI5

中文：你要做一件很多同学一起完成的大作业。你得先说清楚“最终要拿多少分”（指标），再把任务分好、规定每周检查一次进度、提前发现最难的部分先做小实验，最后大家才会真的按同一个计划走。

English: It’s like a big group project. First define what “success” means, split work and owners, check progress regularly, test the risky parts early, and keep everyone moving together.
