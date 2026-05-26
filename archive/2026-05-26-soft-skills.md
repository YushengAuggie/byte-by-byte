# 🗣️ 软技能 / Soft Skills — Day 42
**Topic:** Service Deprecation & Migration
**Date:** 2026-05-26 | **Phase:** Expert

---

## 🗣️ 软技能 / Soft Skills — 下线服务与迁移
**⏱️ 预计阅读时间 / Estimated reading time: 2 min**

**问题 / Question:**
> Tell me about a time you had to deprecate or sunset a service. How did you handle the migration?

---

### 为什么这个问题很重要 / Why This Matters

Senior/Staff 工程师不只是构建系统，还需要**安全地结束系统的生命周期**。服务下线是比上线更难的工程问题：你有未知的依赖方、不愿迁移的用户、以及"删掉就出故障"的恐惧。

Deprecating a service is often harder than building one. Unknown callers, resistant stakeholders, fear of breaking prod — this question tests operational maturity and communication skills, not just technical depth.

---

### STAR 结构 / STAR Breakdown

**Situation（情境）:**
描述为什么需要下线：技术债、安全风险、维护成本、重复功能、云迁移...

> "我们有一个 5 年历史的 v1 内部 RPC 服务，没有 SLA、没有监控、没有鉴权。维护它每月消耗 2 人周，且影响了新功能的迭代速度。"

**Task（任务）:**
你的职责范围——是否跨团队、是否有 hard deadline、是否有外部依赖？

> "作为 Tech Lead，我负责协调 3 个依赖团队的迁移，目标是 6 个月内完成下线。"

**Action（行动）— 这是核心：**

1. **发现阶段：搞清楚谁在用**
   - 在网关/日志层加 instrumentation，统计调用方
   - 发现 2 个团队的 "legacy batch jobs" 每天深夜还在调用

2. **沟通：不要直接 email 说"我们要关掉你的依赖"**
   - 设置 deprecation timeline，给足够的缓冲时间（建议 3-6 个月）
   - 提供迁移指南和迁移工具，主动帮对方团队迁移

3. **渐进式关闭：不要一刀切**
   ```
   Phase 1: 新流量禁止接入 (freeze new clients)
   Phase 2: 已有流量加 deprecation warning header
   Phase 3: 限流 + 增加延迟（让依赖方感到"痛苦"）
   Phase 4: 真正关闭
   ```

4. **监控退出流量：**
   - 在 Grafana 看 request count 趋势，趋近 0 时才真正下线

**Result（结果）:**
> "6 个月内，所有依赖完成迁移，关闭前最后一周流量为 0。释放了约 15% 的基础设施成本，v1 的安全漏洞彻底消除。"

---

### ❌ 不好的回答 / Bad Answer
> "我们直接在 flag day 关了服务，然后收到了很多 oncall 报警。"

告诉面试官你会直接关掉服务而不考虑下游影响——这是 flag。

---

### ✅ 好的回答要素 / Good Answer Elements
- 主动发现未知依赖（Instrumentation）
- 提前沟通，给充足 runway
- 渐进式下线，有监控和 rollback plan
- 定量结果（迁移时间、成本节省、故障数）

---

### Senior/Staff 加分点 / Senior/Staff Tips

- **政治敏感性**：有些团队不愿迁移，因为"这不在我的 OKR 里"。你的解法是把迁移工作帮他们做掉，或者让他们的老板 buy in。
- **技术策略**：先提供一个"兼容层" adapter，让依赖方零修改迁移，再异步推动他们升级。
- **提到 "strangler fig pattern"**：面试官会印象深刻。

---

### Key Takeaways
1. 下线和上线一样需要 planning，甚至更难
2. 发现未知依赖 > 假设你知道所有依赖
3. 渐进式关闭降低风险，监控是保障

---

### 📚 References
- [Strangler Fig Pattern (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [Google SRE Book — Chapter on Service Lifecycle](https://sre.google/sre-book/table-of-contents/)
- [API Deprecation Best Practices (Stripe Engineering)](https://stripe.com/blog/api-versioning)

### 🧒 ELI5
就像老家的老房子要拆迁，你不能直接挖掉地基——得先确认屋里没人，把家具搬走，切断水电，再慢慢拆。服务下线也一样：先找到所有"住户"，帮他们搬家，最后才能关门。
