🗣️ **软技能 / Soft Skills**
*Day 142 · Expert Synthesis — Staff Engineer 面试终极场景*

---

## 场景 / Scenario

> "你是一位 Staff Engineer，即将面试一个 Principal 岗位。面试官问你：**给我讲一个你主导了整个组织技术方向转型的故事。**"

> You're a Staff Engineer interviewing for Principal. The interviewer says: "Tell me about a time you led a technology direction change across the entire org."

这道题不是一个 behavioral question——它是**综合测试**：影响力、技术判断、跨组协作、战略眼光，全在一道题里。

---

## 为什么这是最难的题型

过去 60 个行为题测的是各种维度（冲突、失败、优先级、跨团队…）。这道题**全部叠加**：
- 需要有 **明确的技术判断** (不是"我们讨论了很久")
- 需要有 **跨团队影响** (不是"我说服了我的 manager")
- 需要有 **可量化结果** (不是"大家都很开心")
- 需要有 **阻力和克服** (没有阻力=不够大的决策)

---

## STAR 拆解 / STAR Breakdown

**情境 (Situation):**
"公司的微服务架构运行了 5 年，P95 延迟 800ms，部署需要协调 12 个团队，每次 incident 根因分析需要 3 天。3 个团队有各自的 'modernization' 计划，互相冲突。"

**任务 (Task):**
"作为 Infrastructure 的 Staff Engineer，我没有直线管理这 12 个团队，但被要求在 6 个月内拿出一个全公司认可的迁移路径。"

**行动 (Action) — 最关键：**
1. **技术审计**：先花 3 周亲自 on-call + 看监控，不听别人说，自己弄清楚真正的痛点
2. **建立工作组**：不是委员会（没有决策权），而是"每个团队出一个有代码提交权限的 IC"
3. **原型 > 提案**：做了两个真实原型（gRPC + service mesh vs event-driven），让数据说话
4. **处理阻力**：有一个 Senior Director 喜欢他团队的方案。我安排了 1:1，承认他方案的优点，展示数据差距，提出"他的核心需求可以在新架构里满足"——找到 **共同利益**
5. **RFC 流程**：写了公开 RFC，任何人可以提 comment，透明决策

**结果 (Result):**
"RFC 通过，18 个月后迁移完成。P95 延迟从 800ms 降到 120ms，部署频率提升 4×，incident MTTR 从 3 天降到 4 小时。"

---

## ❌ Bad vs ✅ Good

❌ "我写了一份提案，发给所有人，大家都同意了。"  
→ 没有冲突 = 决策规模太小，或者你跳过了困难部分。

✅ "我主动寻找反对声音，特别是最强的反对者，因为他们往往掌握我不知道的信息。"

❌ "我是最聪明的人，所以大家都听我的。"  
→ Principal 的影响力来自**信任和数据**，不是头衔。

✅ "我建立了一个让正确答案自然浮现的流程，而不是强推我的答案。"

---

## Senior/Staff 提升点

1. **Scope 信号**：面试官想看到的影响范围是 "多个团队" 或 "全公司"，不是你自己的团队
2. **阻力是加分项**：没有阻力的故事说明决策不够大。要主动讲你如何处理反对
3. **数据锚定**：每个决策背后要有数据，"感觉对" 是 IC L5 的答案，"数据显示" 是 Principal 的答案
4. **学到什么**：加一句 "如果重来，我会更早建立 RFC 流程而不是先私下游说"——展示元认知

---

## 📚 References

- https://staffeng.com/guides/staff-archetypes — Staff Engineer archetypes
- https://lethain.com/setting-engineering-org-direction/ — Setting org direction
- https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/ — Staff Engineer book

## 🧒 ELI5

想象一群人要一起决定去哪家餐厅吃饭，每个人都有偏好，有人很强势。Staff Engineer 不是说"我要去这家"，而是：先搞清楚大家真正在乎什么（口味？价格？距离？），然后找到一个满足大多数核心需求的选择，让最强烈的反对者变成支持者，最后写下来让所有人投票确认。这就是技术方向转型。
