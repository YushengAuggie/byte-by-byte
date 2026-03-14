# 🗣️ Soft Skills · Day 1
**"Tell me about a time you had to make a critical technical decision with incomplete information"**
**在信息不完整的情况下做出关键技术决策**

*Level: Senior / Staff Engineer*

---

## 🎯 为什么面试官喜欢问这道题 / Why interviewers love this question

这道题不是在考你的技术能力——是在考你在**不确定性**下的判断力。

Senior 工程师最常面对的就是：需求模糊、数据不全、时间紧迫，但决策不能等。面试官想知道：**当你只有60%的信息时，你怎么做决定？**

*This question doesn't test your technical skills — it tests your judgment under **uncertainty**.*

*Senior engineers constantly face: vague requirements, incomplete data, tight deadlines, and no time to wait. Interviewers want to know: when you only have 60% of the information, how do you decide?*

---

## 📐 STAR 框架 / STAR Framework

```
S — Situation  背景    设置舞台，让面试官代入
T — Task       任务    你具体负责什么？
A — Action     行动    ← 重点！你做了什么、怎么想的
R — Result     结果    量化的结果 + 你学到了什么
```

*S — Situation: Set the stage*
*T — Task: What specifically were you responsible for?*
*A — Action: ← THE MEAT. What did you do and why?*
*R — Result: Quantified outcome + what you learned*

---

## ❌ 糟糕的回答 / Bad Answer

> "我们需要选一个数据库，我调研了几个选项，然后选了 PostgreSQL。最后上线了，运行得还不错。"

**为什么差？**

- 🚫 没有体现"不完整信息"的挑战
- 🚫 没有说你如何在不确定性中决策
- 🚫 结果模糊（"还不错"≠量化）
- 🚫 听起来像在描述一个普通任务，没有展示 Senior 的思维

*Why it's bad:*
- *No mention of what information was missing*
- *No reasoning process under uncertainty*
- *Vague outcome — "not bad" is not a result*
- *Sounds like a routine task, not senior-level judgment*

---

## ✅ 好的回答框架 / Good Answer Template

**Situation（背景）:**
> "2023年底，我们的推荐系统延迟突然飙升到800ms，直接影响用户的购买转化率。我们需要在两周内决定是优化现有架构还是迁移到新系统。"

*"In late 2023, our recommendation service latency spiked to 800ms, directly impacting purchase conversion. We had two weeks to decide: optimize in place or migrate to a new architecture."*

**Task（任务）:**
> "我是负责这个系统的 tech lead，需要给出明确的技术方案和时间表——但我们没有负载预测数据，因为市场团队还没公布下一季度的推广计划。"

*"As tech lead, I had to commit to a technical plan and timeline — but we had no load projections, because marketing hadn't yet announced next quarter's campaign scale."*

**Action（行动）——这里是关键:**
> "我采用了几个策略来降低决策风险：
>
> 1. **定义关键假设**：我列出了我们决策依赖的3个核心假设，包括'流量增长不超过5倍'。
>
> 2. **设定触发条件**：我们决定先做局部优化，但同时制定了一个明确的迁移触发标准——如果P99延迟在优化后仍超过500ms，立刻切换方案。
>
> 3. **并行小实验**：我让一个工程师花3天在 staging 环境验证新架构的关键风险点，而不是全面迁移。
>
> 4. **对齐利益相关方**：我把这套思路写成一页决策文档，明确说明了'我们还不知道什么'和'这些未知因素对决策的影响'，发给了 PM 和 VP Eng。"

*"I used several strategies to reduce decision risk:*
*1. **Named the assumptions**: listed 3 key assumptions our decision relied on, including 'traffic won't grow more than 5x'*
*2. **Set trigger conditions**: chose partial optimization first, but defined a clear migration trigger — if P99 remains above 500ms post-optimization, switch immediately*
*3. **Parallel micro-experiment**: had one engineer spend 3 days validating the highest-risk assumptions of the new architecture in staging — not a full migration*
*4. **Aligned stakeholders**: wrote a 1-page decision doc that explicitly named 'what we don't know yet' and how those unknowns affect the decision"*

**Result（结果）:**
> "优化方案将延迟降低到了320ms，满足了当季需求。两个月后市场数据出来，流量预测远超预期，我们启动了迁移——但因为有了之前的实验，迁移只用了3周而不是3个月。整个项目没有一次生产事故。"

*"The optimization brought latency down to 320ms, meeting current needs. Two months later when marketing data arrived, projected traffic far exceeded our threshold — we triggered the migration. Because of our earlier experiments, it took 3 weeks, not 3 months. Zero production incidents."*

---

## 🔑 让回答脱颖而出的关键 / What makes an answer stand out

```
普通工程师 / Junior-Mid:          Senior+ 工程师:
"我做了调研，选了方案"            "我主动识别了哪些信息缺失"
"I researched and chose"         "I named what we didn't know"

"我们等到有更多数据"              "我设计了触发条件和回退方案"
"We waited for more data"        "I designed triggers and rollbacks"

"最后成功了"                     "这是量化的结果，这是我学到的"
"It worked out"                  "Here's the metric; here's what I learned"
```

---

## 🎭 展示这些 Senior 特质 / Senior qualities to demonstrate

1. **拥抱不确定性** — 你不会因为信息不全就瘫痪
   *Embrace uncertainty — you don't freeze when data is missing*

2. **风险可视化** — 你能说清楚"已知"和"未知"
   *Risk visualization — you can articulate knowns vs unknowns*

3. **可逆决策优先** — 在不确定时，选择更容易撤销的方案
   *Prefer reversible decisions — when uncertain, pick the more reversible option*

4. **沟通透明** — 你让所有人都理解决策的依据和限制
   *Communicate transparently — everyone understands the basis and limits of your decision*

---

## 📝 你的回答结构 / Your Answer Structure

准备时请填写：

```
背景 Situation:
  时间: ___________  公司规模: ___________
  问题: ___________  时间压力: ___________

缺失的信息 Missing info:
  我们不知道: ___________
  这影响了: ___________

我的决策框架 My framework:
  假设: ___________
  触发条件: ___________
  降低风险的实验: ___________

结果 Result:
  量化指标: ___________  (延迟降低X%, 节省$X, 用户增长X%)
  学到了: ___________
```

---

## ⚠️ 常见陷阱 / Common Pitfalls

- **别说"我等到有足够信息"** — 在真实世界里，信息永远不够
  *Don't say "I waited until I had enough info" — in the real world, there's never enough*

- **别把决策权推给别人** — "我们团队决定了..." 是什么意思？你的角色呢？
  *Don't diffuse ownership — "we decided" is weak. What did YOU specifically do?*

- **别跳过失败或教训** — 如果结果不完美，说出来。成长的叙事比完美的结果更有说服力。
  *Don't skip failures or lessons. A growth narrative beats a perfect outcome.*

---
*⏱️ 阅读时间 ~3分钟 / Read time ~3 min*
