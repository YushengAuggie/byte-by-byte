# 🗣️ 软技能 / Soft Skills — Day 23
**题目 / Question:** How do you approach designing systems for scale?
**类别 / Category:** Technical Vision | **级别 / Level:** Staff
**阶段 / Phase:** Growth

---

## 🎯 为什么重要 / Why This Matters

这道题不是在考你背了多少系统设计八股文——面试官真正想知道的是：**你是否有工程判断力**？你是否知道什么时候过度设计比没设计还危险？

This question isn't a test of how many system design patterns you've memorized. Interviewers want to know: **do you have engineering judgment**? Do you know when over-engineering is more dangerous than under-engineering?

对于 Staff 级别，这个问题还在考查你能否**影响团队的技术方向**，而不只是单独做出好决策。
At Staff level, this also tests whether you can **influence your team's technical direction**, not just make good decisions yourself.

---

## ⭐ STAR 框架 / STAR Breakdown

### Situation（背景）
"在我的上一个职位，我们的用户数从 10 万增长到 1000 万，历时 18 个月。早期的架构（单体 + 单数据库）开始出现问题——每次大促前工程师都要彻夜待命。"

"At my previous company, we grew from 100K to 10M users over 18 months. Our early architecture — a monolith with a single database — started showing cracks. Engineers were on-call every time there was a major traffic spike."

### Task（任务）
"我被要求制定一个技术路线图，在不停止功能开发的前提下，让系统支撑 10x 的增长。"

"I was asked to create a technical roadmap to support 10x growth without halting feature development."

### Action（行动）
1. **先测量，后优化 / Measure first, optimize later**
   - 用 profiling 工具找到真正的瓶颈，而不是凭直觉猜
   - "我们以为数据库是瓶颈，但实际上是缓存未命中率高达 80%"
   - Found the real bottleneck with profiling — cache miss rate was 80%, not DB itself

2. **分阶段演进 / Phased evolution**
   - Phase 1 (1个月): 加缓存层 → 立竿见影降低 DB 负载
   - Phase 2 (3个月): 读写分离 → 解放读压力
   - Phase 3 (6个月): 拆分最热的服务（用户服务、支付服务）为微服务
   - 不一步到位，每个 Phase 都有可量化的目标

3. **设计原则先行 / Establish design principles**
   - "任何新功能必须考虑 100x 流量下的行为"
   - 写进 ADR（Architecture Decision Records），让整个团队对齐

### Result（结果）
"系统平稳支撑了大促（峰值 50k RPS），工程师不再需要彻夜待命，且未延误任何计划功能的发布。"

"The system handled peak traffic of 50k RPS during major events without engineers being paged, while delivering every planned feature on schedule."

---

## ❌ Bad vs ✅ Good

❌ **"我会用微服务架构，然后加 Kafka、Redis、Kubernetes..."**
> 这是在背八股文，没有展示判断力。面试官会追问："为什么？你们当时有多少工程师？"

✅ **"我首先会问：我们现在的瓶颈在哪？距离下个量级的增长还有多久？我们团队的规模能支撑微服务的运维成本吗？"**
> 展示了系统性思维和对成本的清醒认识。

---

## 🌟 Senior / Staff 加分点

**1. 技术债务的主动管理**
"我会把可扩展性改进拆成小任务，混进每个 sprint，而不是等到出了大问题再救火。"

**2. 影响力而非权威**
"我写 RFC（Request for Comments）文档，让团队评审并达成共识，而不是单方面宣布决定。"

**3. 权衡的明确性**
"我们选择最终一致性而不是强一致性，因为我们的业务场景允许几秒的延迟——但我们把这个决定记录下来，以便未来的人理解为什么。"

---

## 📌 关键要点 / Key Takeaways

1. **先诊断再开药** — 用数据找瓶颈，不要凭直觉
2. **渐进式演进** — 分 Phase，每 Phase 有 metrics
3. **成本意识** — 过度设计和欠设计一样有害
4. **文档化决策** — ADR/RFC 让团队与未来的自己对话

---

## 📚 References

- https://martinfowler.com/articles/architect-resurgence.html
- https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/
- https://www.youtube.com/watch?v=Y-Gl4HEyeUQ (Martin Fowler on software architecture)

---

## 🧒 ELI5

就像建房子——你不会一开始就建一栋摩天大楼，因为你不确定是否会有那么多人住。但你会让地基足够结实，方便以后加层。先搞清楚现在哪里最拥挤，再一步一步扩建，每次扩建都要能量化效果。

It's like building a house — you don't start by building a skyscraper because you don't know yet if you'll need it. But you make sure the foundation is solid enough to add floors later. First figure out where things are most crowded, then expand step by step — and measure every step.
