# 🗣️ 软技能 / Soft Skills — Day 159 (Synthesis)
**场景 / Scenario:** 上线前一周发现根本性设计缺陷——Staff Engineer 的关键时刻

---

## 为什么这个场景重要

这不是"有没有犯过错"的问题，是"你在极端压力下如何做决策和沟通"。

Senior/Staff 面试官想看的：**你会不会掩盖问题？遇到 bad news 能不能直接说？**

---

## 场景设定

> "你的团队花了 5 个月构建了一个新的订单处理系统，计划下周上线。你在最后一次压测中发现，当并发超过 500 TPS 时，系统会出现数据不一致——根本原因是当初的分布式锁设计有漏洞，修复需要 3-4 周。你会怎么做？"

---

## STAR 拆解

### Situation（情况）
> "我们的支付结算系统计划在双十一前上线，距离上线剩 8 天。在最后一轮压测时，我发现在 600 TPS 峰值下，约 0.3% 的交易会出现重复扣款，原因是 Redis 分布式锁的 expire 时间在某些网络抖动情况下会失效。"

### Task（任务）
> "我需要在极短时间内：(1) 评估风险和修复路径，(2) 决定是否推迟上线，(3) 向 PM、CTO 和业务方沟通。"

### Action（行动）— 这里是重点

**立刻做的事（前 2 小时）：**
1. **不要自己扛**：马上告诉 tech lead 和 PM，不要等到"我再确认一下"
2. **量化风险**：0.3% at 600 TPS = 1.8 笔/秒异常，一天 155,000 笔错误交易——不可接受
3. **提出选项，不是问题**：
   - Option A：推迟 3 周彻底修复（质量最高，损失时机）
   - Option B：上线但限流在 200 TPS，问题不出现，2 周内补丁 （有限功能上线）
   - Option C：上线时加补偿事务层（对账任务），接受少量错误并修复 （最激进）

4. **给推荐**：我推荐 Option B，附上风险评估文档，让决策者决定

**沟通方式：**
> "发现 bug 的当天，我写了一个 1-page 的 Risk Doc：问题描述、影响范围、3 个选项的 pros/cons，以及我的推荐。直接发给 PM、Engineering Manager 和 CTO，标题写 '[需要决策] 支付系统上线风险评估'。"

### Result（结果）
> "决定了 Option B（限流上线）。我们在 2 周内发布了完整修复，没有发生任何生产事故。事后 PM 说，最让他信任的不是我们解决了问题，而是**我们在第一时间就报告了问题**。"

---

## ❌ Bad vs ✅ Good

**❌ 危险回答：**
> "我加班加点，3 天把它修了，没有推迟上线。" — 听起来厉害，实则红旗：你掩盖了风险。

**✅ 强回答的关键：**
1. 第一时间透明汇报，不等到"有把握了再说"
2. 带着**选项和推荐**去谈，不是带着问题
3. 量化影响（数字说话）
4. 决策后 100% 执行，不二次质疑

---

## Senior/Staff 加分项

> **"我后来把这个场景写进了 team 的 on-call runbook 和 design review checklist，确保以后每个分布式锁设计都要覆盖 network partition 场景。"**

把个人教训转化为系统改进，才是 Staff Engineer 思维。

---

## Key Takeaways

1. **Bad news 越早说越好**，掩盖问题是职业生涯的慢性毒药
2. **带着方案，不只是问题**：Problem + Options + Recommendation
3. **量化影响**：不要说"可能有问题"，要说"预计影响 X 用户/Y 笔交易"
4. **决策后执行，不抱怨**：你可以 disagree，但要 commit

---

## 📚 References
- [Amazon Leadership Principle: Have Backbone](https://www.amazon.jobs/content/en/our-workplace/leadership-principles)
- [Staff Engineer: Leadership Beyond the Management Track — Will Larson](https://staffeng.com/book)
- [The Art of the Difficult Conversation — HBR](https://hbr.org/2015/01/how-to-handle-difficult-conversations)

## 🧒 ELI5
如果你不小心打破了家里的花瓶，第一时间告诉爸妈（附带"我打算用零花钱赔一个新的"的方案），比等他们自己发现要好 100 倍。工作也一样——早说、带方案，是成熟的标志。
