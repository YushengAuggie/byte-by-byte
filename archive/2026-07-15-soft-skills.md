# 软技能 / Soft Skills — Day 91 (Synthesis)
**Date:** 2026-07-15 | **Phase:** Expert | **Mode:** Synthesis

---

## 🗣️ 软技能 / Soft Skills
**综合场景：当技术债和新项目同时紧急 / When Tech Debt and New Features Collide**

---

### 场景 / Scenario

面试官问：  
*"你的团队有大量技术债，但产品团队刚提了一个高优先级的新功能。你作为 Staff Engineer，如何决策？"*

Interviewer asks:  
*"Your team has significant tech debt, but product just landed a high-priority feature. As Staff Engineer, how do you navigate this?"*

---

### 为什么难 / Why It's Hard

这不是技术问题——是**优先级冲突 + 利益相关方管理 + 长期 vs 短期**的三角难题。  
错误选择：
- 🚫 全做新功能 → 债越堆越高，最终系统崩塌
- 🚫 全还技术债 → 产品不买账，业务受损，团队被质疑
- ✅ **框架：量化、谈判、分摊**

This isn't a technical problem—it's a **priority conflict + stakeholder alignment + long vs short-term** triangle.  

---

### STAR 拆解 / STAR Breakdown

**Situation:**  
我们的支付服务有 3 年历史，每个 sprint 有 20% 时间处理 incident。产品希望我们 6 周内交付实时结算功能。

Our payment service had 3 years of tech debt; 20% of sprint capacity was incident triage. Product wanted real-time settlements in 6 weeks.

**Task:**  
作为 Staff，平衡团队可持续性和产品交付节奏。

Balance team sustainability with product delivery cadence.

**Action:**

```
步骤 1: 量化技术债的成本
Step 1: Quantify tech debt cost
→ "20% sprint capacity = 每月 X 工程师周，折合 $Y 运营成本"
→ 把"感觉"变成数字。数字说服产品。

步骤 2: 提方案而非问题
Step 2: Bring proposals, not complaints
→ Option A: 6周纯功能，后续2 sprint 专门还债
→ Option B: 8周，每周30%还债，70%新功能
→ 让产品选，而不是你单独决定

步骤 3: 谈判"债务预算"
Step 3: Negotiate a "debt budget"
→ 争取每季度 1 sprint 专门技术投资
→ 写进团队协议，而非每次都重新谈判

步骤 4: 可视化技术债
Step 4: Make debt visible
→ Dashboard 显示：代码覆盖率、平均 MTTR、incident 频率
→ 高层看到数据，而不只是"工程师抱怨"
```

**Result:**  
选了 Option B，8周交付。债务率从 20% 降到 8%，下一季度新功能速度反而提升了 30%（因为 incident 少了）。

---

### ❌ 差回答 vs ✅ 好回答

**❌ 差：**  
"我跟产品说技术债很重要，我们需要时间处理。"  
*→ 没有数字，没有方案，听起来是借口*

**✅ 好：**  
"我量化了技术债的成本：每月 40 小时 incident 响应 = 相当于 1 个工程师的产出。我带着两个方案找产品团队，数据摆在桌上，让他们参与决策——而不是强迫接受。"

---

### Staff/Principal 级别要点 / Staff+ Insights

1. **量化一切** — "感觉慢"不如"P50 latency 从 80ms 升到 450ms"
2. **造选择，而非提要求** — 给 2-3 个方案，各自量化 tradeoff
3. **让技术债可见** — 工程指标进入产品/管理层的 review cycle
4. **建立系统，而非每次谈判** — 季度"innovation sprint"写进 charter

---

### 综合：你已学过的相关主题 / Synthesis: Related Topics You've Covered

| Day | 主题 | 连接 |
|-----|------|------|
| 16 | 如何处理技术债 | 直接相关 |
| 8  | 模糊需求 | 需求不清时的框架 |
| 38 | 系统设计 tradeoff | 同样的决策框架 |
| 21 | 如何说 No | 拒绝的艺术 |
| 13 | 传达坏消息 | 给利益相关方呈现不好的数字 |

---

### 📚 References

- [StaffEng.com — Staff stories on tech debt](https://staffeng.com/guides/managing-technical-quality)
- [Will Larson — An Elegant Puzzle (tech debt framing)](https://lethain.com/elegant-puzzle/)
- [Increment Magazine — Engineering prioritization](https://increment.com/)

### 🧒 ELI5

技术债就像家里乱掉的玩具。你可以继续玩新游戏（新功能），但总有一天找不到东西了（系统崩掉）。  
聪明的做法：**边玩新游戏，边每天收拾一点**——而不是等到全乱了再大扫除。

Tech debt is like a messy room. You can keep playing new games (new features), but eventually you can't find anything (system fails).  
The smart move: **play new games AND tidy a little each day** — don't wait for a big cleanup.
