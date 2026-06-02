# 🗣️ 软技能 / Soft Skills — Day 47
**"Tell me about a time you had to balance shipping fast vs. doing it right"**
*2026-06-02 | Expert Phase | Category: Decision Making*

---

## 为什么面试官问这个 / Why This Question

这是 Senior/Staff 工程师面试的高频题。面试官想知道：你是否理解**技术债务的本质是时间借贷**，以及你如何在商业压力和工程质量之间做出有理有据的权衡——而不是无脑选一边。

*This is a top question for Senior/Staff interviews. The interviewer wants to know: do you understand that tech debt is essentially borrowing time from your future self, and can you make a reasoned tradeoff between business pressure and engineering quality — rather than blindly choosing one side.*

---

## STAR 结构拆解 / STAR Breakdown

### Situation — 设置张力
描述一个有**真实压力**的场景：产品 deadline、竞争对手、客户承诺。
- ✅ "季度末发布，产品已承诺 demo 给客户"
- ✅ "竞争对手刚上线类似功能，CEO 希望一周内跟上"
- ❌ 避免"我们有一个功能要做" — 太平淡，没有张力

### Task — 你的角色和决策权
明确说明**为什么是你**来做这个决定。
- "我是负责这个模块的 Tech Lead"
- "PM 来找我，希望我评估风险"

### Action — 这是核心！
这部分需要展示**结构化思考**，不是感性选择：

**框架 / Framework: Risk-Weighted Decision**

```
1. 量化风险
   - 如果"快"上线：有哪些具体技术风险？发生概率？影响范围？
   - 例：没有限流 → 流量高峰宕机 (P30 likelihood, P1 impact)

2. 量化收益
   - 晚一周上线的业务损失？（客户流失？竞争劣势？）

3. 找折中方案（往往存在！）
   - 先上线核心路径（happy path）+ 降级策略
   - 做"足够好"的方案，同时立即创建 tech debt ticket
   - 设置 kill switch / feature flag 以便快速回滚

4. 对齐利益相关方
   - 明确告知 PM/stakeholder：我们在借什么债，还债计划是什么
```

### Result — 双维度结果
不只说"成功上线"，要说明：
- 业务结果：准时交付，满足了什么
- 工程结果：后续如何还了技术债

---

## ❌ Bad vs ✅ Good Answers

**❌ Bad:**
> "我们有时间压力，所以我选择了快速上线，但后来有一些 bug，我们就修了。"

问题：没有框架，没有权衡，没有主动性，结果模糊。

**✅ Good:**
> "Q3 末，我们承诺给大客户演示一个实时协作功能。距演示只有 9 天，但完整实现需要 3 周。
>
> 我做了一个风险矩阵：完整方案包括 OT（Operational Transformation）算法处理冲突，但 demo 场景是 2 人同时编辑。我评估了最高并发冲突率低于 5%，且 demo 环境可控。
>
> 我的决策：用 **last-write-wins** 临时替代 OT，加 feature flag 隔离，同时创建 Sprint+2 的 tech debt ticket，并在内部 runbook 里标注这个模块不能在正式 GA 前开放。
>
> 我主动向 PM 和 Eng Manager 说明了这个 tradeoff，他们知情并同意。Demo 顺利，客户签约。3 周后我们完整实现了 OT，并做了 A/B 测试验证。"

---

## Senior / Staff 加分项

- **主动管理 stakeholder 预期**：别等他们来问，主动说明"我们在借技术债"
- **有还债计划**：立即创建 ticket，设置 Sprint N+X 的时间盒
- **量化风险**：说 "P30/P1" 而不是 "can happen"
- **知道什么时候必须说"不"**：如果风险是数据丢失、安全漏洞、合规问题——这条线不能过

---

## Key Takeaways / 关键要点

1. **技术债 = 时间借贷，要利滚利**——短期可以，但要知情、要有计划
2. **找折中方案**：快 vs 好 往往不是二选一，feature flag / degraded mode 是你的朋友
3. **主动沟通**：让团队和 stakeholder 知道你在做什么权衡
4. **关键底线**：安全、数据完整性、监管合规 — 这些不能为了速度牺牲

---

## 📚 References
- [The Technical Debt Quadrant — Martin Fowler](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
- [Ship It vs. Do It Right — Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [STAR Method Guide — interviewing.io](https://interviewing.io/blog/star-method)

## 🧒 ELI5

就像用信用卡买东西——你可以先用，但要知道要还，还要付利息。"快速上线"就是刷卡，你得知道刷了多少、什么时候还、利息是多少。不能当作没有账单。

*It's like using a credit card — you can buy now, but you need to know what you owe and have a plan to pay it back. "Ship fast" is swiping the card. Just don't pretend the bill doesn't exist.*
