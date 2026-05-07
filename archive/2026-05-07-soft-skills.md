# 🗣️ 软技能 / Soft Skills — Day 37
**题目 / Question:** Tell me about a time you over-engineered something. What did you learn?
**类别 / Category:** Failure & Growth | **级别 / Level:** Senior/Staff

---

## 为什么面试官问这个 / Why Interviewers Ask This

这题考察的不是失败本身，而是你的**工程判断力**和**自我认知**。Senior 工程师必须知道：简单够用的方案 > 技术上完美的方案。能坦诚承认过度设计，说明你对"工程权衡"有成熟的理解。

This question isn't about failure — it's about **engineering judgment** and **self-awareness**. Senior engineers must internalize: simple and sufficient > technically perfect. Honestly acknowledging over-engineering shows maturity in understanding tradeoffs.

---

## STAR 拆解 / STAR Breakdown

### Situation（情境）
> "In my previous role, we were building an internal analytics dashboard used by ~20 people. I proposed — and built — a full event-sourcing + CQRS architecture with Kafka, separate read/write models, and eventual consistency."

### Task（任务）
> "My goal was to make the system 'future-proof' for scale. I estimated we might grow to 10K users eventually."

### Action（行动）
> "I spent 6 weeks building the infrastructure: Kafka topics, event store, two separate databases, replay logic. The actual feature work took another 4 weeks on top of that."

### Result（结果）
> "We shipped 10 weeks late. The team struggled to understand the codebase. Two engineers needed me to explain the system before any change. Three months later, the dashboard was deprecated because the product direction changed. The actual peak load was 20 concurrent users — a SQLite database would have been fine."

---

## ❌ Bad Answer vs ✅ Good Answer

**❌ 避免 / Avoid:**
- "I once wrote very detailed documentation" ← 这不是过度设计
- "Everything turned out fine" ← 没有 growth
- Making it sound like a humble-brag ("I was TOO thorough")

**✅ 好的回答要包含 / Good answer includes:**
1. **具体技术细节** — 说清楚用了什么技术，为什么是 overkill
2. **业务代价** — 延期、复杂度、维护成本
3. **根因分析** — "我当时的假设是...但实际是..."
4. **改变了什么** — 之后如何做决策不同了

---

## 根因 & 教训 / Root Cause & Lessons

过度设计往往源于：
- **担心被批评不够"高级"** — 想证明自己懂分布式系统
- **为假设的未来优化** — YAGNI (You Aren't Gonna Need It)
- **缺乏问题约束条件** — 没有先问"这个系统的 SLO 是什么？用户规模多大？"

**改变后的决策框架 / Post-lesson decision framework:**
```
Before architecting, ask:
1. What's the actual current load? (not hoped-for future load)
2. What's the maintenance cost if I leave?
3. Can we start simple and migrate later?
4. What's the cost of being wrong?
```

---

## Senior/Staff 加分 / Senior/Staff Tips

**加分回答：** 聊到你如何把这个教训传递给团队。

> "After this, I started running 'complexity audits' before kick-off: we write down our load assumptions, then ask 'what's the simplest thing that could work?' We only add complexity when we've hit a measurable constraint."

**Staff 级别加分：** 谈 organizational impact — 过度设计不只是你的问题，它是 team velocity 的杀手。

---

## 关键要点 / Key Takeaways

1. **YAGNI 原则** — 不需要的功能就不要设计，即使你觉得"以后会用到"
2. **复杂度是负债** — 每个系统决策都有维护成本，要收益 > 成本
3. **先问约束条件** — 用户规模、SLO、团队规模、系统寿命
4. **成熟 = 选简单** — 能用简单方案解决问题，才是真正的技术能力

---

## 📚 References
- [The Wrong Abstraction — Sandi Metz](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)
- [YAGNI — Martin Fowler](https://martinfowler.com/bliki/Yagni.html)
- [Simple Made Easy — Rich Hickey (Strange Loop Talk)](https://www.youtube.com/watch?v=SxdOUGdseq4)

## 🧒 ELI5
就像你要烤一个生日蛋糕，结果造了一个商业烘焙工厂。工厂确实可以做蛋糕，但造工厂花了3个月、花了100万，蛋糕的生日早过了。

Like building a commercial bakery when someone asked for a birthday cake. The bakery can definitely make cakes — but it took 3 months and a million dollars, and the birthday was last week.
