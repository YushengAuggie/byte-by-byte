# 软技能 / Soft Skills — Day 103 (Synthesis)

## 🗣️ 软技能 / Soft Skills — Staff-Level Synthesis

### 当你是房间里最资深的工程师：如何在没有头衔的情况下领导
### When You're the Most Senior Engineer in the Room: Leading Without a Title

---

这不是一道标准行为题——这是一道**场景题**，专门为准备 Staff/Principal 面试设计的。

This isn't a standard behavioral question — it's a **scenario question** designed for Staff/Principal-level interviews.

---

### 🎯 场景 / Scenario

> 你所在的团队有 8 名工程师，技术负责人最近离职了。你是团队里最资深的 IC（Individual Contributor），但你没有正式的"tech lead"或"manager"头衔。  
> 接下来的季度，团队需要交付一个关键的基础设施迁移项目（比如从老的内部 RPC 框架迁移到 gRPC）。产品经理依赖你做技术方向。新加入的工程师依赖你做代码审查。你的 manager 在做其他 org 的事，每周只有一次 1:1。
>
> **你如何在这个季度领导这个项目？**

---

### ⭐ STAR Framework 拆解

**Situation（情况）**：  
明确说清楚你获得的是**非正式权威**，不是指挥链。重要！面试官要听你如何在模糊权力结构中行动。

**Task（任务）**：  
三个并行目标：①项目按时交付 ②团队不 burn out ③让每个人都有成长  
关键：这些目标**相互冲突**，你需要权衡。

**Action（行动）——这是重点**：

1. **立即澄清 scope 和 ownership**  
   不等 manager 指派，主动召集 kickoff，建议用 DACI/RACI 矩阵明确谁 Decide、谁 Advise、谁 Consult

2. **建立技术决策记录（ADR）**  
   不在 Slack 做大决策。写下来，让异步讨论有据可查，减少"我以为我们说好了…"

3. **分解 ownership，而不是集中在自己身上**  
   让每个工程师 own 一个子系统的迁移，你负责接口设计和最终 review
   → 这样你不是 bottleneck，他们有成长机会

4. **为 manager 提供决策包，而不是问题**  
   1:1 时带着"Option A/B/C + 我的建议是 A，原因是……"，不是"我不知道怎么做"

**Result（结果）**：  
量化：项目按期交付，X 个子系统迁移完成；Y 个初级工程师在这个季度 own 了自己的模块，有 public PR 可看

---

### ❌ Bad Answer vs ✅ Good Answer

**❌ Bad**：  
> "我就把任务分配给大家，然后每天站会跟进进度。"  
→ 这是项目管理，不是技术领导力。面试官期待你谈**技术判断 + 影响力**，不是 PM 职责。

**✅ Good**：  
> "我写了一个迁移 RFC，列出了三种方案的 tradeoff，组织了一次异步 review。两天后大家在评论里达成了共识，我们避免了一周的来回扯皮。这样的决策记录后来也成了新成员 onboarding 的材料。"  
→ 展示技术思维 + 流程建立 + 影响超出项目本身

---

### 🔑 Senior/Staff Tips

- **影响力 ≠ 控制**：最好的技术领导者通过清晰的写作和框架影响决策，不是靠开会强推
- **Multiplier mindset**：你的工作是让团队的产出是 10x，不是你个人的 2x
- **可见度管理**：确保你的 manager 和 skip-level 知道你在做什么，不是为了个人邀功，而是保障团队的资源和优先级

---

### 📚 References
- https://staffeng.com/guides/staff-archetypes
- https://lethain.com/work-on-what-matters/
- https://www.industriallogic.com/blog/making-technical-decisions/

### 🧒 ELI5
你是班里最懂数学的同学，但你不是班长。老师出去了，同学们都看着你。好的做法不是"我来做所有题"，而是"我们分工，每人做一部分，有问题来找我"，然后在黑板上写下解题思路让大家都能学到。

You're the best math student but not the class monitor. Teacher leaves, everyone looks at you. The good move isn't "I'll solve everything" — it's "let's split the work, each person owns a section, come ask if stuck," and write the solution approach on the board so everyone learns.
