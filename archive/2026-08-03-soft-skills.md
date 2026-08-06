# 🗣️ 软技能 / Soft Skills — Day 107

> Synthesis Mode — Expert Level

---

## 新场景：当你被要求主导一个你不完全认同的技术方向
## New Scenario: Leading a Technical Direction You Don't Fully Agree With

这在 Staff+ 工程师的职业生涯中非常常见：你的 VP 或架构委员会做了一个决定，你有保留意见，但你被指定为执行负责人。你怎么办？

This is extremely common at Staff+ level: leadership makes a call you're not 100% behind, and you're tapped to own the execution. What do you do?

---

### 为什么这道题重要 / Why This Matters

面试官想看的不是"我永远支持决定"，也不是"我会强推自己的方案"。他们想看你能否在**战略执行**和**工程诚信**之间找到平衡。

The interviewer doesn't want "I always comply" or "I pushed until I got my way." They want to see if you can balance **strategic execution** with **engineering integrity**.

---

### STAR 拆解 / STAR Framework

**情境 (Situation)**
团队决定将核心服务从 Kafka 迁移到 Pulsar，理由是 Pulsar 原生支持多租户。你了解 Kafka 的运维成本更低，团队 Kafka 经验更深。

**任务 (Task)**
你被指定负责迁移方案设计和执行，同时需要确保 18 个下游服务不中断。

**行动 (Action)**
1. **先把反对意见结构化**：写一份单页技术备忘录，列出 3 个风险点（运维复杂度、团队学习曲线、迁移窗口）。上报一次，记录在案。
2. **一旦决定确认，全力执行**：设计双轨方案——Kafka → Pulsar bridge，逐步切流。
3. **建立回滚条件**：和 VP 对齐：如果 P99 延迟 > 200ms 超过 48 小时，触发回滚。
4. **同步下游团队**：周会公开进度，早暴露问题。

**结果 (Result)**
迁移成功，Pulsar 多租户确实简化了跨团队隔离。你的迁移方案成为公司内部 playbook。

---

### ❌ 差回答 vs ✅ 好回答

❌ *"我向上反馈了，但最终还是按要求做了。"*
— 没有展示主动性，像个执行机器

❌ *"我坚持推我的方案直到他们改变主意。"*
— 不懂组织决策；Staff 工程师需要会输赢都体面

✅ *"我把反对意见系统化地写成备忘录，确保风险被记录在案；一旦决定落定，我设计了降低这些风险的执行方案，并和决策者对齐了回滚条件。"*
— 有原则、可执行、有安全网

---

### Senior → Staff 的差异 / Senior vs Staff

| | Senior | Staff |
|--|--|--|
| 不同意时 | 私下说，然后执行 | 结构化备忘录，上浮风险 |
| 执行中 | 按规范完成 | 主动改造方案以降低风险 |
| 事后 | 继续下一个任务 | 提炼为团队 playbook |

---

### Key Takeaways

1. **异议要系统化**：口头抱怨 ≠ 专业反馈；书面备忘录才有影响力
2. **不同意但执行** ≠ 软弱；这是组织信任的基础
3. **设计安全网**：在你不确定的决策里，主动设定回滚条件
4. **事后复盘**：无论结果如何，提炼学习，更新团队知识库

---

### 🧒 ELI5

就像球队教练做了一个你不同意的战术安排。你可以在赛前跟教练说"我担心这点"，但一旦哨声响了，你要全力执行，还要想办法保护队友。赛后，赢了你帮总结经验，输了你帮复盘为什么。

---

### 📚 References
- https://staffeng.com/guides/staff-archetypes
- https://www.amazon.com/Crucial-Conversations-Talking-Stakes-Second/dp/1469266822
- https://lethain.com/work-on-what-matters/
