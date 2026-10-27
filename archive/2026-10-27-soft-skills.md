# 🗣️ 软技能 / Soft Skills — Day 143 | Expert Synthesis

**高级场景：你要重构一个核心系统，但没人给你时间**
**Senior Scenario: You need to refactor a critical system but nobody will give you time**

---

## 为什么这道题难 / Why This Question Is Hard

这不是一道普通的"怎么处理冲突"题。它考查的是：**在没有授权的情况下，如何推动技术必要性与业务优先级之间的博弈**。Staff+ 工程师每周都面对这个。

This isn't a standard conflict question. It tests: **how do you drive technical necessity against business priority without top-down authority?** Staff+ engineers face this weekly.

---

## 场景 / Scenario

> "你发现核心支付服务有严重的技术债，任何新功能都要花 3x 时间。但 PM 说 Q3 有 5 个 feature 要上，没有时间重构。你怎么做？"

---

## STAR Framework

**Situation（背景）:**  
在某次 sprint，我意识到我们的 checkout service 已经积累了 4 年的 spaghetti code — 没有单元测试，所有状态都耦合在一个 God Object 里，每次改动都要同时改 8 个文件。

**Task（任务）:**  
我需要在不阻塞 Q3 roadmap 的情况下，让团队和 PM 认识到这个问题的代价，并争取到合理的重构时间。

**Action（行动）:**
1. **量化技术债成本**：我统计了过去 3 个月的 bug rate 和开发速度 — 每个新 feature 平均多花 40% 时间，有 60% 的 hotfix 来自这个模块。
2. **翻译成业务语言**：不说"代码烂"，说"这模块每季度让我们少交付 2 个 feature"。
3. **提出"嵌入式重构"方案**：不要求独立 sprint，而是在每个 feature 旁边带着做 — Strangler Fig Pattern，逐步替换而不是大爆炸。
4. **找到盟友**：先说服 TL 和 EM，再一起去 PM 谈。
5. **设置检查点**：每两周 demo 一次进展，确保重构和 feature 同步推进。

**Result（结果）:**  
PM 同意每个 sprint 留出 20% 的时间做"连续改进"。3 个月后，bug rate 降低了 45%，新 feature 交付速度提高了 30%。

---

## ❌ Bad Answer vs ✅ Good Answer

❌ "我告诉 PM 技术债很严重，但他们不听，所以我只能继续做 feature。"  
→ 被动，无量化，无影响力。

✅ "我把技术债翻译成业务影响，提出嵌入式方案，找到共同利益点，推动渐进式改善。"  
→ 主动、数据驱动、展示了跨职能影响力。

---

## Senior/Staff Tips

- **数字是你的武器**：开发速度、bug 率、oncall 频率 — 把技术问题量化成时间和金钱
- **Strangler Fig > Big Bang**：永远不要说"我们要停工 3 个月重写"
- **培养 PM 信任**：先按时交付几个 feature，再提技术改进，你的话才有分量
- **写 ADR**：把技术决定记录下来（Architecture Decision Records），未来有据可查

---

## Key Takeaways / 核心要点

1. 量化技术债 → 业务语言
2. 嵌入式重构（Strangler Fig），不做大爆炸
3. 先找盟友，再找决策者
4. 用数据证明投资回报

---

## 📚 References
- [Martin Fowler: Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [Google SRE Book: Managing Technical Debt](https://sre.google/workbook/managing-incidents/)
- [Will Larson: Staff Engineer Book (Excerpt)](https://staffeng.com/guides/staff-projects)

## 🧒 ELI5
就像家里下水道堵了，你不能停水一个月大修，但可以每周修一段管道。先告诉大家"不修就越来越慢"，然后边住边修，才是成年人的方法。
