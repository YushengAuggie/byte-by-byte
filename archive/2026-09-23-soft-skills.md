# 🗣️ 软技能 / Soft Skills — 综合 Day 61: 技术与影响力的交汇

> **综合模式 / Synthesis Mode:** 全新 Senior/Staff 级场景题，跨越之前多个主题。

---

## 今日场景题 / Today's Scenario

**"你被要求在6个月内把一个 5 年历史的单体应用迁移到微服务。工程团队怀疑，产品团队催进度，你是 TL。你怎么做？"**

*"You're asked to migrate a 5-year-old monolith to microservices in 6 months. Engineers are skeptical, product is pushing hard. You're the TL. What do you do?"*

---

## 为什么这题难 / Why It's Hard

这不是纯技术题——它考察的是**在技术不确定性与组织压力之间如何做决策并获得信任**。许多人要么全盘接受（committing without data），要么全盘拒绝（saying no without alternatives）。

---

## STAR 拆解

**Situation:**
历史债务多、团队信心不足、截止日期激进。

**Task:**
既不能空承诺，也不能直接说"不行"——需要建立可信度和可执行计划。

**Action:**
1. **先做技术摸底（Discovery Sprint）**：2周了解耦合度、依赖图、核心瓶颈
2. **识别"绞杀者模式"切入点**（Strangler Fig Pattern）：找边界清晰、独立性强的第一个服务候选
3. **向上管理期望**：带数据（代码行、依赖数、测试覆盖）和产品对话，展示风险而非只说"很难"
4. **定义成功的里程碑**：不是"完成迁移"，而是"第一个服务上线、流量切换、监控就绪"
5. **赋能团队**：让持怀疑态度的工程师成为第一个服务的 owner，而非强推

**Result:**
6个月内完成核心服务解耦（而非全部），团队建立信心，后续迁移自主推进。

---

## ❌ 踩坑回答 vs ✅ 高分回答

❌ "我会分解任务分配给每个工程师然后每周开会跟进"
— 没有处理怀疑情绪，没有风险意识

❌ "我会告诉产品6个月不现实，需要18个月"
— 正确但无建设性，没有替代方案

✅ "我先用 2 周建立事实基础（代码依赖分析），然后带着数据和产品对话：不是说不行，而是说'这是我们能6个月内交付的最大价值子集，这是风险，这是我们需要的取舍'。"

---

## Senior → Staff 跨越点

| Senior TL | Staff+ |
|---|---|
| 专注执行计划 | 重塑问题框架（"6个月能做什么"而非"全做完") |
| 向上汇报进展 | 主动管理风险和期望 |
| 保护团队不受干扰 | 让团队的怀疑成为前进动力 |
| 技术决策 | 组织层面的信任建设 |

---

## Key Takeaways

1. **Discovery before commitment** — 用数据说话，不靠直觉答应
2. **Reframe, not refuse** — 不说"不行"，说"在约束下最优解是什么"
3. **Make skeptics owners** — 把抵触的人变成方案的负责人
4. **Milestone > timeline** — 里程碑驱动比死板时间表更可信

---

## 📚 References
- https://martinfowler.com/bliki/StranglerFigApplication.html — Strangler Fig 模式（经典必读）
- https://www.staffeng.com/stories/ — Staff 工程师真实案例集
- https://lethain.com/migrations/ — Will Larson 谈技术迁移管理

## 🧒 ELI5
老房子要改建，但6个月太紧。聪明的做法是：先搞清楚房子有多破（评估），选一间最独立的房间先改（Strangler），再跟房东说"这6个月我们能改3间，不是全部"——带着数据谈，不是硬说不行。
