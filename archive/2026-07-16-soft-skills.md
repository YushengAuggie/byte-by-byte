# 软技能综合 — 高阶领导力场景 / Soft Skills Synthesis — Senior Leadership Scenario

> Day 92 · Expert · Synthesis Mode

---

## 🗣️ 软技能 / Soft Skills — 综合场景：Staff Engineer 的技术债 vs 速度困境

### 场景 / Scenario

> "你刚加入一家公司担任 Staff Engineer。核心支付服务有严重技术债（10年老代码，无测试，每季度有3-4次 P0 故障），但 PM 希望你帮助团队在未来 6 个月内 2x 交付速度。你怎么做？"

> "You just joined as a Staff Engineer. The core payments service has severe technical debt (10-year-old code, no tests, 3-4 P0 incidents per quarter), but the PM wants you to help the team 2x delivery speed in the next 6 months. What do you do?"

---

### 为什么这个问题很难 / Why This Is Hard

这不是简单的技术问题，而是**战略性权衡**：
- 短期: 继续叠 feature，技术债越来越重，最终崩溃
- 中期: 重构但不交付，PM 和 C-suite 失去耐心
- 长期: 技术债 = 速度的负债，不还早晚要还

This isn't just a tech problem — it's a **strategic negotiation** between engineering health and business velocity.

---

### STAR 框架 / STAR Breakdown

**Situation:** 新来的 Staff，支付服务技术债严重，PM 要 2x 速度

**Task:** 在不拖延 PM 的情况下，说服组织投资技术健康，同时实际提速

**Action (关键步骤 / Key Steps):**

```
Week 1-2: 诊断，建立事实基础
  → 量化技术债的成本: P0 故障 × MTTR × eng时间 = ¥X/季度
  → 统计 cycle time (PR merge to deploy): 当前 vs 行业基准
  → 找出 top 3 pain points (deploy 慢? 测试覆盖率 <20%? 单点故障?)

Week 3: 构建叙事 (narrative matters!)
  → "当前速度 = 30%时间在修 bug，70%才在建功能"
  → "投资 3 个月技术基础设施 → 未来 9 个月 2x 速度"
  → 用数据说话，而不是工程师的直觉

Week 4: 提议"嵌入式重构" (不是大重写)
  → Boy Scout Rule: 每个 PR 顺手改一块坏代码
  → 新功能用新架构写，老代码逐步迁移
  → 先加测试，再重构 (make it testable first)

Month 2-3: 执行 + 可见进展
  → 每两周给 PM 展示: 部署频率 ↑, incident 数 ↓
  → 把技术工作翻译成业务影响
```

**Result:** 
- 不强求"先重构再交付"的二元对立
- 用数据赢得信任，再用信任换来空间

---

### ❌ Bad vs ✅ Good 回答对比

```
❌ 初级/中级答案:
"我会告诉 PM 我们必须先清理技术债，功能开发需要等3个月。"
问题: 没有业务意识，没有数据，没有协商

❌ 中级陷阱:
"我会把重构放进 sprint，每次 20% 时间用于技术债"
问题: 太模糊，无法追踪，PM 会渐渐侵蚀这 20%

✅ Staff级答案:
1. 先量化：把技术债翻译成业务成本 ($, 时间, P0频率)
2. 再提案：不是"重构 vs 功能"，而是"如何用技术投资提速"
3. 渐进式：Boy Scout Rule + Strangler Fig Pattern (vs Big Rewrite)
4. 透明化：双周展示进展，让 PM 和 EM 成为盟友，而不是障碍
```

---

### Senior/Staff 核心能力体现 / Senior/Staff Level Signals

1. **技术债量化能力**: 能把工程问题翻译成 CFO 听得懂的语言
2. **渐进式架构改造**: Strangler Fig > Big Bang Rewrite
3. **影响力而非权力**: 说服 PM，不是对抗 PM
4. **系统性思维**: 不只看眼前的 ticket，看整个系统的健康

---

### Key Takeaways

- 技术债的正确处理不是"停下来重构"，而是"让重构成为日常工作的一部分"
- 用数据建立公信力，再用公信力换来工程自主权
- Staff Engineer = 技术 × 业务 × 影响力的交叉点

---

### 📚 References
- https://martinfowler.com/bliki/StranglerFigApplication.html
- https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052 (Working Effectively with Legacy Code)
- https://charity.wtf/2023/01/06/engineers-should-own-the-results-of-their-code/

### 🧒 ELI5
Imagine your bedroom is super messy. You can either: (A) stop everything and clean for a week, (B) clean a little every time you're in your room. Option B is "technical debt management." The trick is convincing your parents (PM) that cleaning while you go actually means you can find your toys faster — which is like 2x speed!
