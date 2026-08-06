# 🗣️ 软技能 / Soft Skills — Day 108 (Synthesis)

## 如何在压力下展示系统思维 / Demonstrating Systems Thinking Under Pressure

> 综合场景 / Synthesis Scenario — Staff Engineer Level

---

## 🎯 场景 / The Scenario

> 面试官问 / Interviewer asks:
> 
> *"我们的核心支付流程每天有 5% 的事务失败，工程师们认为是数据库问题，产品认为是前端 bug，运维认为是网络抖动。作为新上任的 Staff Engineer，你怎么处理这个局面？"*
>
> *"Our core payment flow has a 5% transaction failure rate daily. Engineers blame the database, product thinks it's a frontend bug, ops suspects network flakiness. As a newly promoted Staff Engineer, how do you handle this?"*

---

## ❌ 初级工程师的答案 / Junior Answer

"我会让大家开个会讨论，然后投票决定先查哪个方向。"

"I'd call a meeting, have everyone share their theories, and we'd vote on which direction to investigate first."

**为什么不够好**: 没有结构，没有数据驱动，容易陷入政治博弈而不是解决问题。

---

## ✅ Staff 级别的答案框架 / Staff-Level Framework

### Step 1: 先建立共同事实基础 (Before the debate)
```
"在我们讨论原因之前，我需要确认：
- 这 5% 是什么时间段的？全天均匀分布还是有峰值？
- 错误类型是什么？timeout？4xx？5xx？
- 最近有什么变更？（代码、配置、流量）"
```
**目的**: 把争论从"我的直觉 vs 你的直觉"转向"数据说明了什么"

### Step 2: 并行调查，不是串行 (Parallel investigation)
```
同时开三条线：
① 数据库团队：查慢查询日志，看 5% 失败时段的 DB 指标
② 前端团队：查 JS error log，失败是在 submit 前还是 submit 后？
③ 运维团队：查网络延迟监控，失败时是否有 packet loss spike

给出明确时间盒：2小时内各出一页数据报告
```

### Step 3: 相关性分析 (Correlation, not assumption)
```
把三条线的数据放在同一时间轴上：
- 如果 DB 慢查询 和 支付失败 完全重叠 → DB 是根因
- 如果前端错误发生在 network call 之前 → 前端 bug
- 如果所有指标都正常但失败率高 → 第三方支付 API 问题（被遗漏的假设！）
```

### Step 4: 短期 vs 长期 (Decouple mitigation from fix)
```
短期（今天）：
- 给支付加重试逻辑（idempotency key 确保安全重试）
- 监控告警：失败率 >2% 立即通知

长期（这周）：
- 找到根因，彻底修复
- 加分布式追踪（trace_id 贯穿全链路），避免下次猜谜
```

---

## 🎖️ Senior/Staff 关键能力展示 / What This Shows Interviewers

1. **不被政治裹挟** — 用数据而不是职位/声量决定方向
2. **系统性思维** — 想到被所有人遗漏的第三方 API 假设
3. **并行而非串行** — 不让组织陷入"等一个团队查完再查下一个"
4. **解耦缓解与根治** — 先保用户体验，再慢慢修复
5. **提升可观测性** — 解决问题的同时让下次更容易解决

---

## 💬 关键台词 / Phrases That Land Well

- *"Let's align on the facts before we align on the solution."*（先对齐事实，再对齐方案）
- *"I want to run these investigations in parallel to avoid 3 days of serial blame."*（并行调查，避免串行甩锅）
- *"What's our mitigation plan while we find the root cause?"*（找根因的同时怎么保住用户体验？）

---

## 📚 References
- https://www.atlassian.com/incident-management/postmortem/blameless
- https://sre.google/sre-book/postmortem-culture/
- https://charity.wtf/2020/11/14/the-engineer-staff-engineer-gap/

## 🧒 ELI5
三个人争论"为什么房间里有水"：一个说管道漏了，一个说窗户没关，一个说屋顶破了。聪明的人先拿手机看天气预报，再检查三个地方，而不是让大家吵架。

Three people arguing about why the room is wet: one blames pipes, one blames the window, one blames the roof. The smart person checks the weather forecast first, then inspects all three — instead of letting everyone argue.
