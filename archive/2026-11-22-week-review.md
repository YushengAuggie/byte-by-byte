📅 **Week in Review — Week 47 (10 min read)**
📊 NeetCode: 119/150 · SysDesign: 60/40 · Behavioral: 60/40 · Frontend: 37/50 · AI: 30/30
🔥 2-day streak!

---

## 🗓️ 本周回顾 / This Week's Journey

**本周共完成 2 天内容（Day 153–154），周一至周四为休息日。**
*2 days of content this week (Days 153–154), Monday–Thursday were rest days.*

- **周五 Nov 20（Day 153）：** Distinct Subsequences (#115) · SAGA vs 2PC vs Outbox Pattern · Anthropic IPO 等 AI 大事件 · 技术债 CTO 场景 · Python 对象生命周期完整图景
- **周六 Nov 21（Day 154 · Deep Dive）：** Burst Balloons (#312) — 区间 DP 反向思维完全精讲（18 min）

---

## 🧠 系统设计要点 / System Design: Key Takeaways

**本周主题：分布式事务——如何在微服务间保证一致性。**
*This week's theme: distributed transactions — ensuring consistency across microservices.*

**三大模式对比 / Three Patterns Compared：**

1. **2PC（两阶段提交）**：强一致性，但协调者是单点故障；适合同数据中心的金融核心账本。*Strong consistency, but coordinator = single point of failure; best for same-datacenter financial ledgers.*
2. **SAGA（补偿事务）**：最终一致性，高可用，每步操作失败后执行补偿逻辑（必须幂等）。*Eventual consistency, high availability; compensating transactions must be idempotent.*
3. **Outbox Pattern**：在同一本地事务内原子写入 DB + Outbox 表，CDC（如 Debezium）异步拉取发布——保证"事件一定发出去"。*Atomic write to DB + Outbox table in one local transaction; CDC asynchronously publishes — guarantees at-least-once event delivery.*

**贯穿线 / The Thread：** 这三种模式都是 CAP 定理的实践体现——没有一种方案能同时保证强一致性 + 高可用 + 分区容错。Stripe 用 Outbox + 幂等 Key，Uber 用 SAGA + Temporal。*All three patterns are CAP theorem in practice. Choose based on consistency vs. availability trade-off. Stripe uses Outbox + Idempotency Keys; Uber uses SAGA + Temporal.*

---

## 💻 算法模式总结 / Algorithms: Patterns Mastered

**本周模式：二维 DP 收官 — 计数型 DP + 区间 DP**
*This week's pattern: 2D DP finale — Counting DP + Interval DP*

### Distinct Subsequences (#115) — 计数型 2D DP
- **核心洞见**：`dp[i][j]` = s 前 i 字符中 t 前 j 字符作为子序列出现的次数。字符匹配时，既可"用"也可"跳过"，两条路径相加。*Key insight: when characters match, choices accumulate via addition (count paths); when they don't, only carry forward.*
- **与其他 2D DP 的区别**：Edit Distance → 最小代价（min）；Interleaving String → 可行性（OR）；Distinct Subsequences → 计数（加法）。*2D DP variants: minimize = min(), feasibility = OR, count = sum().*

### Burst Balloons (#312) — 区间 DP（Deep Dive）
- **核心反转**：不问"先戳哪个"，而问"**最后**戳哪个"。当气球 k 是区间 (i,j) 内最后被戳破的，它的左右邻居就固定为边界值 `nums[i]` 和 `nums[j]`，子问题独立。*The mental flip: think about which balloon to pop LAST, not first. The last balloon's neighbors are fixed = the interval boundaries, making subproblems truly independent.*
- **模版**：`dp[i][j] = max(dp[i][k] + nums[i]*nums[k]*nums[j] + dp[k][j])` — 枚举 k 作为区间内最后一个气球。按区间长度从小到大填表。*Fill order: interval length 2 → n+1. Complexity: O(n³) time, O(n²) space.*
- **推广**：合并石子、矩阵链乘法、SQL join ordering 优化器——凡是"区间内寻找最优分割"都是这个模式。*Generalizes to Stone Merge, Matrix Chain Multiplication, SQL query planner join ordering.*

---

## 🗣️ 软技能练习重点 / Soft Skills: What to Practice

**本周场景：Staff Engineer 应对"6 个月清零技术债"的 CTO 要求。**
*This week: Staff Engineer navigating a new CTO's demand to eliminate all tech debt in 6 months.*

**关键框架 / Key Framework：**
1. **先审计后承诺**：用债务登记册量化，按安全/稳定性/开发速度三类分级。*Audit first, commit second: use a Debt Registry with business-impact classification.*
2. **重定义目标**：把"6 个月清零"推回成"消除 TOP 3 高风险债务 + 建立不再累积新债的机制"。*Reframe: not "zero tech debt" but "eliminate top 3 risks + build mechanisms to prevent new debt."*
3. **用业务语言**：CTO 关心风险和速度，不关心代码行数。把"Python 2 未迁移"翻译成"CVE 无人修补"。*Translate for executives: code facts → business risk. "Python 2 EOL" = "unpatched CVEs."*
4. **固定 budget**：技术债时间被随意取消是债务积累根源——30% 时间不 cancel。*Fixed allocation: debt work never gets canceled mid-sprint. 30% locked.*

**需要练习 / Practice Needed：** 在压力下如何向上 push back——带数据、带替代方案、带时间表。这是 Staff 和 Senior 的核心分水岭。*How to push back upward under pressure — with data, alternative plans, and timelines. This is the Staff vs. Senior divide.*

---

## 🎨 前端：本周无新内容 / Frontend: No New Content This Week

前端指数维持在 37/50。下周继续推进 Frontend 部分。
*Frontend index remains 37/50. Expected to advance next week.*

---

## 🤖 AI 知识点 / AI: What Stuck

**本周为 AI News Roundup 日。以下均来自新闻报道，据报道：**
*This was a news day. All items below are reported news — 据报道 (as reported):*

1. **据报道：Anthropic 完成 IPO（代码 ANT）**——据报道其 2026 前九个月收入 332 亿美元。标志着 AI 进入"公开市场问责"阶段。*Anthropic reportedly went public (ticker ANT); reportedly $33.2B revenue in first 9 months of 2026. Marks AI's entry into public-market accountability.*
2. **据报道：Google Gemini 4 Carbon 正式 GA**——定位"复杂技术工作 + 长任务 Agent"，据报道对 Copilot/Cursor 形成直接竞争。*Gemini 4 Carbon reportedly GA; positioned for complex technical work and long-horizon agents.*
3. **据报道：Jensen Huang 辞去 Nvidia CEO 职位**——CFO Colette Kress 出任临时 CEO。*Jensen Huang reportedly resigned as Nvidia CEO; CFO taking interim role.*
4. **据报道：EU AI Act 关键条款 12 月 2 日起执行**——全球首个强制规范生成式 AI 的法律框架。*EU AI Act key provisions reportedly taking effect December 2 — first mandatory generative AI regulation globally.*

**最重要的 takeaway / Most Important Insight：** AI 正从"回答问题"向"自主规划 + 工具使用 + 多步执行"演进——Agentic 架构将成为后端工程师的核心技能。*The shift from "answer questions" to "plan + use tools + execute autonomously" = agentic architecture is becoming core backend engineering knowledge.*

---

## ⚠️ 需要复习的内容 / What to Review

1. **2D DP 完整家族**：Edit Distance、Interleaving String、Distinct Subsequences、Burst Balloons 四题的转移方程和各自的"类型标志"（min/OR/sum/区间分割）——能在面试开始时 30 秒内区分哪题用哪种。*Review the 4 2D DP problem types and their transition "signatures" — be able to identify in 30 seconds which variant applies.*
2. **SAGA 补偿事务的幂等设计**：补偿操作被重试时不能产生副作用——具体怎么实现？（幂等 key、版本号、状态机）。*SAGA compensation idempotency: how do you ensure compensating transactions are safe to retry?*
3. **区间 DP 填表顺序**：为什么必须从小区间到大区间？自己能不看代码写出 Burst Balloons 的嵌套循环结构吗？*Interval DP fill order: can you write the nested loop structure for Burst Balloons from memory?*

---

## 🏆 本周亮点 / Win of the Week

**Burst Balloons 深潜完成！**

这是整个 NeetCode 150 中公认最难的 DP 题之一。通过深度精讲，彻底掌握了"区间 DP 反向思维"——这个思维模式不只是解一道题，而是打开了矩阵链乘法、SQL join 优化器、外部排序归并等一系列工程问题的通用钥匙。

*Burst Balloons deep dive complete! This is one of the hardest DP problems in NeetCode 150. The "last balloon" reversal insight isn't just for this problem — it's the master key for Matrix Chain Multiplication, SQL join ordering, and external sort merge optimization.*

---

## 🎯 下周预告 / Next Week Preview

基于当前进度指数，下周预计：
*Based on current indices, next week likely covers:*

- **算法**：2D DP 收尾 — Regular Expression Matching (#10)（最后一道 Hard 2D DP），随后进入贪心（Greedy）章节。*Algorithms: finish 2D DP with Regular Expression Matching (#10), then enter Greedy section.*
- **系统设计**：继续 Synthesis 模式——可能综合复习分布式系统中的可观测性主题（Tracing + Logging + Metrics 三位一体）。*System Design: Synthesis continues — likely observability trilogy (Tracing + Logging + Metrics).*
- **前端**：Frontend 指数 37/50，下周应推进新 Frontend 内容。*Frontend: index at 37/50, new content expected.*
- **Python Craft**：Synthesis 阶段，继续深度专题。*Python Craft: Synthesis phase continues.*
- **AI**：下周为 News or Synthesis 日，取决于周期轮换。*AI: News or Synthesis depending on rotation.*

加油！距离 NeetCode 150 完成还有 31 题。🚀
*Keep going! 31 problems left to complete NeetCode 150.* 🚀
