# 🗣️ 软技能 / Soft Skills — Day 34
## Tell me about a time you improved team velocity or productivity
> Mastery Phase · ~2 min read | Category: Process Improvement | Level: Senior/Staff

---

### 🎯 为什么这道题重要 / Why This Matters

面试官想知道：你是否有**主人翁意识**，能主动识别摩擦点并推动改变，而不仅仅执行任务。Senior+ 工程师被期待能让整个团队更好，不只是自己产出高。

Interviewers want to know: do you have ownership mentality? Can you identify friction proactively and drive change, rather than just executing tasks? Senior+ engineers are expected to make the whole team better, not just ship their own work.

---

### 📝 STAR 框架 / STAR Breakdown

**Situation（情境）：**
描述团队面临的具体低效问题。最好有数据支撑。
> "我们团队的 PR review cycle 平均需要 3 天，阻塞了 feature 交付。"

Describe a specific inefficiency with data if possible.
> "Our team's PR review cycle averaged 3 days, blocking feature delivery."

**Task（任务）：**
你的角色和目标。
> "我作为 Tech Lead 决定调查瓶颈，目标是将 cycle time 缩短到 1 天以内。"

Your role and goal.
> "As Tech Lead, I investigated the bottlenecks with a goal of cutting cycle time under 1 day."

**Action（行动）：**
你具体做了什么？这是最重要的部分。
> "分析 GitHub 数据发现 80% 延迟来自两个原因：(1) PR 太大（平均500行），(2) 没有 reviewer 分配规范。我推行了两个改变：PR 大小 < 200行的软性限制，并在 CODEOWNERS 里明确了自动指派规则。同时举办了一次团队 workshop 讲解如何拆分大 PR。"

What exactly did you do?
> "Analyzed GitHub data and found 80% of delays came from two root causes: (1) PRs too large (avg 500 lines), (2) no reviewer assignment norms. I implemented two changes: a soft 200-line PR size limit and explicit auto-assignment rules in CODEOWNERS. I also ran a team workshop on how to split large PRs effectively."

**Result（结果）：**
量化成果！
> "3个月后，平均 review cycle 从 3 天降到 18 小时。团队 throughput 提升了约 40%，按按每个工程师计算。"

Quantified outcomes!
> "3 months later, average review cycle dropped from 3 days to 18 hours. Team throughput improved by roughly 40% per engineer."

---

### ❌ 糟糕的回答 vs ✅ 好的回答

**❌ Bad:**
> "我优化了我们的开发流程，大家都很满意，效率提高了很多。"

模糊、没有数据、没有你具体做了什么、没有阻力。

**✅ Good:**
> "我们的 deployment 流程需要手动步骤，每次大约花1小时，还容易出错。我设计了一个 CI/CD pipeline，将部署时间从1小时降到8分钟，错误率降到零。过程中需要说服团队放弃熟悉的手动步骤，我用前两次的对比数据赢得了认可。"

有问题、有行动、有阻力、有量化结果。

---

### 💎 Senior/Staff 加分点

1. **系统性思考**：不是修一个 bug，而是修一个流程，影响全团队
2. **数据驱动**：用指标证明问题和结果，而不是主观感受
3. **影响力**：你需要说服别人改变，提一下你如何处理阻力
4. **可持续性**：变化是否被固化到流程/工具里，而不是靠个人英雄主义

---

### 🔑 Key Takeaways
- 用数字说话：cycle time、throughput、错误率
- 区分你的贡献 vs 团队贡献
- 说明你如何推动采纳（change management）
- 最好有"what you'd do differently"结尾，展示反思能力

---

### 📚 References
- https://www.loom.com/blog/engineering-team-velocity
- https://linearb.io/blog/engineering-metrics/
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

### 🧒 ELI5
这道题就是问你：你发现同事做事慢，你做了什么让大家都更快？要说清楚"原来多慢、你做了啥、现在多快"，三要素缺一不可。

This question asks: you noticed your team was slow — what did you do to make everyone faster? You need three elements: "how slow before, what exactly you did, how fast after." Missing any one makes the answer weak.
