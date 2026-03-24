🗣️ **软技能 Day 8 (2 min read) / Soft Skills Day 8**
**处理模糊需求："Tell me about a time you worked with ambiguous requirements"**
**"讲一个你在需求不明确时如何推进工作的经历"**

---

**为什么这很重要 / Why This Matters**

现实中，完美的 PRD 不存在。Senior 工程师的核心能力之一：**在不确定中前进**。这道题考查：
1. 你会等别人给答案，还是主动去找答案？
2. 你能区分"必须现在确认"和"可以先做再调"吗？
3. 你怎么管理风险 — 不是消除不确定性，而是降低不确定性的成本。

---

**STAR 框架拆解**

**Situation:** 项目背景 + 为什么需求模糊（新市场？跨团队？PM 离职？）
**Task:** 你的角色 + 为什么不能等（deadline、依赖关系）
**Action:** 最重要！展示：
  - 如何拆解模糊性（哪些部分确定？哪些不确定？）
  - 主动沟通：找谁确认？怎么问的？
  - 决策框架：先做确定的部分，不确定的用接口隔离
  - 风险管理：feature flags、可逆决策、spike/prototype
**Result:** 量化！交付时间、返工率、客户反馈

---

**❌ Bad vs ✅ Good**

❌ *"需求不清楚，我就去问 PM，等他给我明确的 spec 再开始做。"*
→ 被动等待，没有展示独立判断力

✅ *"接手支付重构时，PM 只说'支持国际化'，没有具体国家列表。我做了三件事：(1) 分析现有用户数据，发现 80% 国际流量来自 5 个国家；(2) 和 PM 确认优先级 — 先做这 5 个，架构预留扩展；(3) 用 Strategy Pattern 隔离货币/税率逻辑，新增国家只需加配置文件。结果：2 周交付 MVP，后续 3 个月扩展到 15 个国家，零架构改动。"*

---

**Scenario Template / 可复用模板**

```
[项目名] 的需求是 [模糊描述]，
缺少 [具体缺失信息]。

我通过 [数据分析/用户调研/竞品分析] 缩小范围，
与 [角色] 确认了 [关键决策]，
用 [技术方案] 隔离不确定性。

结果：[时间指标]，[质量指标]，[扩展性指标]。
```

---

**Senior/Staff 加分点**

🎯 **区分可逆 vs 不可逆决策** — "这个决定错了容易改吗？" 可逆的就先做，不可逆的才需要等确认
🎯 **展示 spike/prototype 思维** — "我花 2 天做了个 prototype 验证假设"
🎯 **主动对齐而非被动等待** — 写 RFC/设计文档，让利益相关方评审

---

**关键要点 / Key Takeaways**
1. 模糊 ≠ 停下来等 — 拆解模糊性，找到可以先动的部分
2. 用数据缩小范围 — 80/20 法则找到最重要的 case
3. 架构隔离不确定性 — 接口、策略模式、feature flags
4. 主动沟通 > 被动等待 — 带着方案去讨论，不是带着问题

---

📚 **深入学习 / Learn More:**
• [Making Decisions Under Uncertainty — First Round Review](https://review.firstround.com/making-decisions-under-uncertainty)
• [The Manager's Path — Camille Fournier](https://www.oreilly.com/library/view/the-managers-path/9781491973882/)
• [Reversible vs Irreversible Decisions — Jeff Bezos](https://www.aboutamazon.com/news/company-news/2015-letter-to-shareholders)

🧒 **ELI5:** Working with unclear instructions is like building with LEGOs when you only see part of the picture on the box — you start with the pieces you can figure out, and leave room to add more later when you see the rest!
