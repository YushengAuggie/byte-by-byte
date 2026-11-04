# 🗣️ 软技能 / Soft Skills — Day 147

**综合场景 / Synthesis Scenario — Senior/Staff Level**

*今天是综合日：跨越过去60道行为题，整合成一道复合题。*
*Synthesis Day: combining themes across 60 behavioral questions.*

---

## 今日场景 / Scenario

> **"你是一个新加入的 Staff Engineer，被要求 6 个月内将服务 P99 延迟从 800ms 降到 200ms，同时不能停服。技术团队对方向意见不一，产品要求不能 block 任何新功能。你如何推进？"**

这道题同时考察：决策（Day 1）、优先级（Day 12）、影响力（Day 1）、技术债（Day 16）、跨团队协作（Day 39）、压力沟通（Day 13）。

---

## STAR 框架拆解 / STAR Breakdown

### 🌟 情境 / Situation
新来的 Staff，没有直接汇报关系，800ms p99 已影响转化率，但每个工程师对根因判断不同——有人说是 DB 慢查询，有人说是第三方 API，有人说是 N+1 请求。

### 📋 任务 / Task
在 **6 个月内** 将 p99 从 800ms → 200ms，同时：
1. 不停服
2. 不影响产品新功能交付

### ⚡ 行动 / Action

**Phase 1：用数据结束争论（第 1-2 周）**
- 部署分布式追踪（Jaeger/Datadog APM），生成 flame graph
- 画出 p95/p99/p999 分布曲线，找出是高频慢还是偶发极慢
- 以事实说话，终止"感觉是 DB"之类的争论

**Phase 2：找最大杠杆点（第 3-4 周）**
- 发现 60% 延迟来自同一批 3 个端点，且都触发了 N+1 查询
- 优先解决：不需要重架构，风险低，预估可改善 300-400ms

**Phase 3：并行推进，不 block 产品（第 5-16 周）**
- 把优化工作切成 2 周 sprint，每 sprint 一个可测量目标
- 给产品团队每周一更新："本周 p99 降了 X ms，你们的功能 Y 我们协调好时间窗"
- 建立 feature flag — 优化版上线先灰度 5%，有问题立即回退

**Phase 4：巩固与防退化（第 4-6 月）**
- 在 CI 中加 performance regression test，新 PR 不能让 p99 回升
- 写内部 RFC 记录决策，避免新人重踩同一个坑

### 📊 结果 / Result
5 个月时达标（p99: 190ms），产品零功能延期，团队形成了"先量化再动手"的文化共识。

---

## ❌ 差答案 vs ✅ 好答案

| ❌ 常见失误 | ✅ 正确做法 |
|------------|------------|
| "我重构了整个架构" | 先用 observability 找根因，最小化改动 |
| "我说服大家用我的方案" | 让数据说话，不是靠权威 |
| "要求产品暂停新功能 3 个月" | 并行，feature flag，协商优先级 |
| 只说技术，不说沟通 | 主动更新进度，建立信任 |

---

## Senior/Staff 加分点 / Senior/Staff Tips

1. **从 Staff 角度**：你的价值不在于 code，在于解锁团队。如果你亲自改每一行 SQL，你没有杠杆。
2. **可逆 vs 不可逆决策**（Day 63）：先做可逆的（加缓存、加索引），再做不可逆的（重架构）
3. **量化承诺**：不说"我会让它变快"，说"第 8 周 p99 目标是 500ms，我们每周对齐"
4. **影响圈 vs 关注圈**：产品要求不 block 功能是你的关注圈，怎么优化是你的影响圈，聚焦影响圈

---

## 关键 Takeaways / Key Takeaways

- 用观测数据替代意见战
- 分解大目标为可验证的小里程碑
- 并行推进，用 feature flag 降风险
- Staff 的价值 = 技术决策 × 组织影响力

---

## 📚 References
- https://www.staffeng.com/guides/what-do-staff-engineers-actually-do/
- https://lethain.com/trunk-and-branches/
- https://charity.wtf/2022/08/24/the-hierarchy-is-bullshit-and-bad-for-business/

## 🧒 ELI5
想象你是新来的大厨，餐厅出菜很慢，老板叫你在 6 个月内把等待时间缩短 4 倍，而且不能停业。你不能随便乱改菜谱——先去厨房站一天，看哪个环节最慢（观测），再先解决最大的卡点（优先级），改的时候先在一张桌子试，没问题再推全厅（灰度）。
