# 🗣️ 软技能 / Soft Skills — Day 146 (Synthesis)
**Fresh Senior/Staff Scenario: 跨职能系统重构的利益相关者管理**
**Cross-Functional System Rewrite: Stakeholder Alignment at Staff Level**

---

## 🎯 今日场景 / Today's Scenario

> "你发现公司核心支付服务是 10 年前的老代码，技术债严重，已经影响到新功能交付速度和稳定性。但 PM 说 Q4 必须上线 3 个大功能，CFO 不想批预算做'看不见的工作'，你的团队已经精疲力竭。作为 Staff Engineer，你会怎么做？"

> "You discover the core payment service is 10-year-old legacy code with severe tech debt impacting feature velocity and stability. PM says 3 major features must ship in Q4, CFO won't fund 'invisible work,' and your team is burned out. As Staff Engineer, what do you do?"

---

## ⭐ STAR Framework

### Situation — 诊断清楚再开口

**先量化，不要凭感觉 / Quantify before you speak:**
- "过去 6 个月，支付服务相关 incident 导致了 47 小时工程师 on-call 时间"
- "新功能平均开发周期从 Q1 的 2 周增加到 Q3 的 5 周，其中 60% 时间花在绕过老系统"
- "上季度有 2 次 P1 故障，各自造成约 $X 营收损失"

**核心原则：把技术债翻译成业务语言**
If you say "the code is unmaintainable," nobody cares.
If you say "tech debt cost us $800K in lost velocity and incidents last quarter," now you have attention.

---

### Task — 你的实际目标是什么

不是"重构代码"（这是手段）。

真正的目标：
1. 恢复特性交付速度（PM 关心）
2. 降低系统风险（CTO/CFO 关心）
3. 保护团队，避免更多流失（EM/CPO 关心）

**Staff 思维 / Staff-level framing:** 你的 job 不是写代码，是让整个系统（包括人和技术）更健康。

---

### Action — 具体做了什么

**Step 1: 建立"技术债成本模型"**

```
季度技术债成本 =
  直接成本: incident 小时数 × 工程师时薪 + 营收损失
+ 机会成本: 特性延迟交付 × 商业价值
+ 风险成本: 估算下次 P1 概率 × 潜在损失
```

**Step 2: 提出"扼杀者无花果"策略**（Strangler Fig Pattern）

不是推倒重来（风险太高），而是：
- 在新服务旁边构建，逐步迁移流量
- 每个 sprint 同时交付业务功能 + 迁移旧模块的一部分
- 向 PM 展示：新架构部分的特性开发速度已经快了 3 倍

**Step 3: 利益对齐 / Stakeholder alignment**

| 角色 | 他们关心的 | 你的说法 |
|------|-----------|---------|
| PM | 功能交付 | "重构第 1 个模块后，后续功能开发快 3x" |
| CFO | ROI | "投入 6 人月，换回每季度节省 $X 工程成本" |
| CTO | 风险 | "不动的话，下次 P1 概率从 15% 升到 40%" |
| 团队 | 不再痛苦 | "我们会逐步减少 on-call 负担" |

**Step 4: 提供两个选项，不是一个**

❌ 坏做法："我们必须重构，需要 6 个月"
✅ 好做法：
- **选项 A** (推荐): 20% 时间持续重构 + 正常功能交付。6 个月内迁移 80%，第 3 个月起速度提升可见
- **选项 B** (保守): 只修最关键的稳定性问题。Q4 功能按时交付，但技术债继续累积，明年再评估

给 leadership 选择权，他们更容易接受你的推荐方案。

---

### Result — 结果和学到的

- Q4 功能按时交付 ✅（给了 PM 他们想要的）
- 同时完成 30% 旧系统迁移 ✅
- Incident 率下降 40%，on-call 时间减半 ✅
- 团队 engagement 改善（有进展感，不再是纯救火）✅

---

## ❌ 坏 vs ✅ 好

**❌ 工程师思维:**
"老代码太烂了，我们需要 6 个月全面重写，不然我要辞职了。"

**✅ Staff 思维:**
"我做了一个分析，当前技术债每季度让我们损失约 X。我有两个方案给你——我推荐方案 A，因为它在最小化 Q4 风险的同时开始偿还债务。能给我 30 分钟走一遍这个分析吗？"

---

## 🔑 Senior/Staff 关键洞察 / Key Takeaways

1. **量化一切** — 技术问题不说业务语言，就等于在说方言
2. **扼杀者无花果优于大爆炸重写** — 持续交付价值，降低风险
3. **给选项，不给命令** — 让 stakeholder 感觉他们在决策
4. **对齐激励** — 每个角色的痛点不同，说他们听得懂的话
5. **用数据推动，不用情绪** — "我们很痛苦" < "上季度损失了 $X"

---

## 📚 References

1. [Staff Engineer — Will Larson](https://staffeng.com/book)
2. [Strangler Fig Pattern — Martin Fowler](https://martinfowler.com/bliki/StranglerFigApplication.html)
3. [Articulating Technical Debt to Stakeholders — LeadDev](https://leaddev.com/technical-direction-strategy/articulating-technical-debt-non-technical-stakeholders)

---

## 🧒 ELI5

你家的水管老化了，总是漏水，修起来要断水 6 个月。
聪明的做法不是说"必须断水 6 个月"，而是说："我们可以边用水边换管子，每周换一段，不影响正常生活，半年后全换好。"
这就是 Strangler Fig：慢慢扼死老系统，让新系统接管。
