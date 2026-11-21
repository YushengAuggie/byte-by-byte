# 🗣️ 软技能 / Soft Skills — Day 153 (Synthesis)
**Staff-Level Scenario: 你的团队欠了三年技术债，新 CTO 要求 6 个月内清零**

---

## 场景设定

> 新 CTO 刚上任，宣布要在 Q2 结束前"清掉所有技术债"。你是 Staff Engineer，负责一个有 300 万行代码的核心服务，里面有未迁移的 Python 2 代码、循环依赖的模块、以及一堆没有测试的关键路径。你怎么做？

这道题综合了我们覆盖过的多个主题：**技术债处理（Day 16）、优先级排序（Day 12）、向上管理（Day 3）、跨团队对齐（Day 14）**。

---

## STAR 框架拆解

### Situation — 建立共同语言
技术债不是一个技术问题，它是一个**沟通问题**。先量化：
- 把债务分类：安全风险 / 稳定性风险 / 开发速度阻碍
- 用业务语言翻译："Python 2 EOL 意味着 CVE 无人修补"
- 建立"债务登记册"（Debt Registry），每条记录关联业务影响

### Task — 重新定义目标
❌ 坏目标：**"6 个月清零技术债"**（不可能，会制造恐慌）
✅ 好目标：**"6 个月内消除 TOP 3 高风险债务，并建立不再累积新债的机制"**

向 CTO push back，但要带数据和替代方案。

### Action — 执行框架

```
Week 1-2: 审计 + 分级
  → 高风险（安全/稳定性）: 立即行动
  → 中风险（开发速度）: 季度计划
  → 低风险（代码质量）: 随机结对处理

Month 1-2: 并行战略
  → 新功能：50% 时间
  → 技术债：30% 时间 (固定 budget, 不 cancel)
  → 防新债：20% 时间 (lint rules, PR 模版, ADR)

Month 3-6: 进度可视化
  → 每两周向 CTO 汇报：已消除的业务风险 (not "lines fixed")
  → 建立"债务燃烧图" Burndown Chart
```

### Result — 预期成果

不要承诺"全部清零"，而是承诺：
1. **安全债务**：100% 消除（Python 2 迁移完成）
2. **稳定性债务**：关键路径测试覆盖率 >80%
3. **流程**：PR 中不引入新的 P0/P1 级债务

---

## ❌ 坏答案 vs ✅ 好答案

| | 答法 |
|-|------|
| ❌ | "我们按 CTO 要求，全力以赴 6 个月冲刺清零！" |
| ❌ | "技术债太多了，6 个月根本不可能，这个目标不合理。" |
| ✅ | "我理解紧迫感。让我在这周做完审计，带着数据回来，我们一起定一个既能控风险又不停止业务交付的计划。" |

---

## Senior/Staff 加分点

- **用 ADR (Architecture Decision Records) 防新债**：每个架构决策留记录，避免同样的债务再犯
- **把技术债变成可见资产**：在 roadmap 上展示，让 PM 也参与优先级排序
- **教团队识别债务**：Code Review checklist 里加入"这会产生技术债吗？"

---

## 关键提炼

1. **先审计后承诺**：没有数据的计划是空谈
2. **用业务语言**：CTO 关心风险和速度，不关心代码行数
3. **固定 budget，不 cancel**：技术债时间被随意取消是债务积累的根源
4. **建机制而非做一次性清理**：真正的解法是不再产生新债

---

## 📚 References
- https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- https://www.thoughtworks.com/insights/articles/managing-technical-debt
- https://architectelevator.com/architecture/technical-debt/

## 🧒 ELI5
技术债就像信用卡债。新 CTO 说"6 个月还清"。聪明的 Staff Engineer 会说："我们先看看欠了多少、利率多少，把高利贷先还了，同时设置自动还款防止继续刷卡，而不是所有收入都拿去还债导致生活停摆。"
