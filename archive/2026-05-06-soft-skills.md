# 🗣️ 软技能 / Soft Skills — Day 30
## Technical Vision — Staff Level
### Q: Describe how you've set technical direction for a team or organization

---

### 为什么这个问题重要 / Why This Matters

Staff+ 工程师区别于 Senior 工程师的核心：不只是解决眼前的技术问题，而是**定义哪些问题值得解决**、**如何构建能让整个团队更快的系统**。这道题考察的是 technical leadership，而不只是技术能力。

*The Staff+ differentiator: not just solving technical problems, but defining which problems matter and building systems that multiply team velocity. This question probes technical leadership, not just technical ability.*

---

### STAR 框架 / STAR Breakdown

**Situation（背景）：** 描述当时的技术现状和痛点——团队在哪里卡住了？为什么现有方向不够？  
*Describe the technical status quo and pain point — where was the team stuck, and why was the current direction insufficient?*

**Task（任务）：** 你的角色是什么？是被指派的还是主动发现的问题？  
*What was your role? Did you identify the gap proactively, or were you assigned to it?*

**Action（行动）：** 这是重点。要包含：
- 你如何**诊断**问题（数据、用户访谈、系统深入分析）
- 你如何**构建共识**（1:1 对话、RFC 文档、原型 demo）
- 你如何**处理反对意见**（谁不同意，为什么，如何化解）
- 你如何**分解执行**（roadmap、里程碑、accountability）

*The action is the crux. Include: diagnosis (data/interviews/deep dives), building consensus (1:1s, RFC docs, prototypes), handling dissent, and breaking down execution into milestones.*

**Result（结果）：** 量化影响。工程效率提升多少？系统可靠性如何改变？团队文化有什么变化？  
*Quantify the impact: engineering efficiency gains, reliability improvements, cultural shifts.*

---

### ❌ 弱回答 vs ✅ 强回答 / Bad vs Good

**❌ 弱回答：**
> "我提出了迁移到微服务的想法，大家都同意了，然后我们执行了。"

这个答案缺乏：诊断过程、如何说服别人、遇到了什么阻力、结果的量化。

**✅ 强回答：**
> "2022年我们的 monolith 部署时间从45分钟增长到90分钟，每次有人合并代码都要等2小时才能验证。我通过分析 CI 日志发现瓶颈在3个重度耦合的模块。我写了一个 RFC 提议提取这3个服务，但有2个 senior engineer 反对（担心分布式复杂性增加）。我做了一个小型 PoC 用 2 周时间证明通信开销可控，并邀请反对者一起 review 结果。最终我们用6个月完成迁移，部署时间降到8分钟，团队可以独立发布，季度 feature velocity 提升了40%。"

*Weak: "I proposed microservices and everyone agreed." Strong: Specific pain point data, RFC with dissent, PoC to build trust, measurable outcome.*

---

### 📈 Senior vs Staff 级别差异 / Senior vs Staff Differentiation

| 维度 | Senior Engineer | Staff Engineer |
|------|----------------|----------------|
| 范围 | 单个系统/服务 | 跨团队/多系统 |
| 时间 | 季度内 | 1-2年愿景 |
| 共识 | 说服自己团队 | 影响多个团队 |
| 指标 | 系统指标（latency） | 组织指标（velocity, reliability SLA） |

Staff 答案要展示 **跨组织的影响力** 和 **multi-quarter 的时间视角**。

*Staff answers must show cross-organizational impact and multi-quarter time horizons.*

---

### 关键要点 / Key Takeaways

1. **数据先行**：技术方向必须基于实测数据，不是直觉 / *Lead with data, not intuition*
2. **异见是礼物**：最强的反对意见往往暴露了你没想到的风险 / *Dissent reveals blind spots — embrace it*
3. **写下来**：RFC/ADR 文档是建立共识的最有效工具 / *Written proposals build consensus at scale*
4. **度量变化**：没有量化结果，就没有证明 / *No measurement = no proof*

---

### 📚 References
- [Staff Engineer: Leadership Beyond the Management Track — Will Larson](https://staffeng.com/book)
- [RFC Culture at Engineering Companies — Gergely Orosz](https://newsletter.pragmaticengineer.com/p/software-architecture-document)
- [How to Write an Architectural Decision Record (ADR)](https://adr.github.io/)

### 🧒 ELI5
设技术方向就像给登山队选路线。Senior 工程师会爬好自己的那段路。Staff 工程师需要看完整的山，决定哪条路对整个队伍最安全、最快，还要说服所有人这条路才是对的——即使有人喜欢走另一条。

*Setting technical direction is like choosing a route for a climbing team. Senior engineers climb their own section well. Staff engineers survey the whole mountain, pick the best route for the entire team, and convince everyone it's right — even when some prefer a different path.*
