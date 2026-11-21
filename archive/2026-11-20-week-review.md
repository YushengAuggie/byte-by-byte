📅 **Week in Review — Week 36 (10 min read)**
📊 NeetCode: 119/150 · SysDesign: 60/60 · Behavioral: 60/60 · Frontend: 37/50 · AI: 30/30
🔥 1-day streak（本周 3 天内容，中间有空缺）

---

## 🗓️ 本周回顾 / This Week's Journey

**本周共完成 3 天内容（Day 151–153），中间有约 10 天空缺。**
*3 days of content this week (Days 151–153), with a ~10-day gap in the middle.*

- **周日 Nov 9（Day 151）：** Edit Distance (#72) + 分布式一致性模型全景 + AI 算力动态 + 技术债领导力场景 + Python 并发三大模型终极对决
- **周一 Nov 10（Day 152）：** Longest Increasing Path in Matrix (#329) + 混沌工程与韧性架构 + GPT-6/Anthropic 营收/Hinton 警告 + 跨时区工程领导力 + Python 内存模型深度解析
- **周五 Nov 20（Day 153）：** Distinct Subsequences (#115) + SAGA vs 2PC vs Outbox Pattern + Anthropic 正式上市/Gemini 4 Neon/Jensen Huang 离职 + 技术债 CTO 场景 + Python 对象生命周期完整图景

---

## 🧠 系统设计要点 / System Design: Key Takeaways

**本周主题：分布式系统如何处理不确定性——一致性、韧性、事务。**
*Theme: How distributed systems handle uncertainty — consistency, resilience, transactions.*

**核心三个概念 / Top 3 Concepts:**

**1. 一致性谱系 (Consistency Spectrum)**
从 Weak（Redis）→ Eventual（Cassandra）→ Strong（DynamoDB 强一致读）→ Linearizable（Spanner/etcd）。
关键决策维度不是 CAP，而是 PACELC——正常运行时，你选择延迟还是一致性？
*The key decision isn't just CAP but PACELC: when partitions aren't happening, do you optimize for latency or consistency?*

**2. 混沌工程 (Chaos Engineering)**
"主动破坏以验证自愈能力"。流程：定义稳态基线 → 假设韧性 → 注入故障（从单 Pod 到 AZ 到 Region 递进） → 观测影响 → 修复并固化到 Runbook。没有基线就没有验证。
*Chaos Monkey (pod) → Chaos Kong (AZ) → Chaos Gorilla (region). Start small, expand blast radius only after validating at smaller scope.*

**3. 分布式事务三大模式**
2PC 保强一致但协调者是单点；SAGA 高可用但需要幂等补偿事务；Outbox 保证"事件一定被发出去"。
Stripe → Outbox + Idempotency Keys；Uber → SAGA + Temporal。
*2PC = strong consistency but coordinator is SPOF. SAGA = high availability but every compensation must be idempotent. Outbox = guarantee event delivery without 2PC overhead.*

**连接点**：这三个话题构成"分布式系统应对不确定性"的完整闭环——一致性模型定义目标，混沌工程测试韧性，分布式事务保障原子操作。

---

## 💻 算法模式总结 / Algorithms: Patterns Mastered

**本周继续 2-D DP 专题（进度 7/11 → 9/11），连克三道 Hard 题。**
*Continued 2-D DP block (7/11 → 9/11), three consecutive Hard problems.*

| 题目 | DP 类型 | 关键洞察 |
|------|---------|---------|
| **Edit Distance (#72)** | 最小代价 / Min Cost | 3 方向 min：删除、插入、替换；画 5×5 表格手动追踪一次就懂 |
| **Longest Increasing Path (#329)** | DFS + 记忆化 / Top-down | 拓扑顺序不固定 → 用自顶向下 DP；`@lru_cache` 一行解决记忆化 |
| **Distinct Subsequences (#115)** | 计数 / Count | 转移用加法累积，不是 min/max；`dp[i][j] += dp[i-1][j-1]` when match |

**核心规律（背下来）/ Core Rule:**
- 问"最少操作" → **min**（Edit Distance）
- 问"能否实现" → **OR**（Interleaving String）
- 问"多少种方式" → **加法**（Distinct Subsequences、Coin Change II）

这条规律覆盖了 2D DP 90% 的转移判断。

---

## 🗣️ 软技能练习重点 / Soft Skills: What to Practice

**本周两个 Staff-Level 高难度压力场景，核心都是同一个能力：向上 push back 但带数据和方案。**
*Two high-pressure Staff-level scenarios, both requiring the same core skill: push back upward with data and alternatives.*

**场景 1：技术债 vs 交付时间线**
量化技术风险（不是"有债务"，是"DAU 超 50k 就会锁竞争导致 20% 超时"）→ 给三个选项 → 用业务语言汇报 → 让决策者选。
*Key move: translate technical risk to business impact, then give options — not problems.*

**场景 2：新 CTO 要求 6 个月清零技术债**
❌ 不要承诺全部清零；✅ 重新定义目标：消除 TOP 3 高风险债务 + 建立"不再产生新债"的机制。先审计后承诺，建债务登记册，固定技术债预算（30%）且不可随意取消。
*The real answer isn't "clear all debt" — it's "eliminate the highest-risk debt and build a system that stops accumulating new debt."*

**需要重点练习 / Practice Focus:**
用业务语言量化技术风险的能力。在镜子前练习："如果我们按期上线，Q2 有 70% 概率出现重大故障，影响 X 用户，修复需要 Y 工程师周。延期 2 周能把这个概率降到 15%。"

---

## 🎨 前端知识巩固 / Frontend: Concepts to Lock In

**本周无新 Frontend 内容，进度保持 37/50。**
*No new frontend content this week; progress holds at 37/50.*

下一个 Frontend 专题：**JavaScript 核心内功**
- Promises、async/await — 异步控制流
- Event Loop — Microtasks、Macrotasks、requestAnimationFrame
- Prototypes & `this` — JS 对象的真实运作方式

**快速自检 / Quick Self-Check:**
能口述 Microtask Queue 和 Macrotask Queue 的执行顺序差异吗？能解释 `this` 在箭头函数和普通函数中的区别吗？如果含糊，这是下周最值得巩固的点。

---

## 🤖 AI 知识点 / AI: What Stuck

> **注意：本节所有财务数字和人事变动均标注"据报道"，来源为新闻报道，未经原始数据直接验证。**
> *All financial figures and personnel changes in this section are from reported news sources.*

**本周 AI 大事件（三天三波新闻，行业剧变）：**

**1. Anthropic 正式上市（代码 ANT / NASDAQ）**
季度营收据报道接近 170 亿美元，算力承诺据报道约 8950 亿美元。AI 从"风险投资烧钱"阶段正式进入"公开市场问责"时代——现在需要向股东证明盈利。

**2. Google Gemini 4 Neon + Carbon**
Neon 定位"高推理低成本"；Carbon 专攻代码、调试、安全分析，对 GitHub Copilot 和 Cursor 形成直接竞争压力。

**3. Jensen Huang 据报道离开 Nvidia，CFO 接任**
AI 算力供应链的稳定性比模型本身更重要——没有 GPU，模型训练无从谈起。这次领导层变动值得持续关注。

**4. EU AI Act 12 月执行**
禁止 AI 生成非自愿性深度伪造和儿童性虐待材料。欧盟运营的 AI 产品需在 12 月前完成合规审计。

**工程师最重要的 takeaway:**
> **"Agentic Revolution" 正在加速。** AI 不再只是回答问题，而是自主规划、使用工具、执行多步长期任务。Tool Use + Orchestration 是后端工程师的下一个核心技能。

*The shift from "AI as Q&A" to "AI as autonomous agent" is the most important architectural change to understand right now.*

---

## ⚠️ 需要复习的内容 / What to Review

**按优先级排序 / Prioritized:**

1. **SAGA 补偿事务必须幂等** — 补偿操作可能因网络重试而多次执行。面试中最容易漏掉的细节：每个补偿操作都需要 idempotency key。
   *SAGA compensation transactions can run multiple times due to retries — idempotency is non-negotiable.*

2. **DFS + 记忆化 vs 自底向上 DP 的选择时机** — 什么时候用 top-down？答：当拓扑顺序不明确时（如 Longest Increasing Path）。能手写 `@lru_cache` 版本吗？
   *Use top-down DP when topological order isn't known in advance.*

3. **Cassandra Quorum 计算** — W + R > N 保证强一致。N=3, W=2, R=2 → 强一致但较慢；N=3, W=1, R=1 → 高性能弱一致。这个公式在系统设计面试里出现频率极高。
   *W + R > N guarantees strong consistency. Know the tradeoffs for different W/R combos.*

4. **Python asyncio 核心陷阱** — `time.sleep()` 在 async 函数里会阻塞整个事件循环；必须用 `asyncio.sleep()` 或 `loop.run_in_executor()`。
   *Calling synchronous blocking code inside async functions blocks the entire event loop — this is a classic interview gotcha.*

---

## 🏆 本周亮点 / Win of the Week

**2D DP 专题 7→9/11：连续三道 Hard，三种不同转移模式全部掌握！**

Edit Distance（最小代价）、Longest Increasing Path（DFS 记忆化变奏）、Distinct Subsequences（计数累积）——这三道题覆盖了 2D DP 最核心的三种思路。从现在起，看到字符串/矩阵/路径类 DP，第一步就能判断：这是求最优、判断可行性，还是数路径数量？这个判断能力就是 Hard 题破题的关键。

*Three back-to-back Hard 2D DPs, three distinct transition patterns. The judgment "am I minimizing, checking feasibility, or counting?" is now a reflex — that's the real win.*

---

## 🎯 下周预告 / Next Week Preview

**算法（当前 119/150）：**
- 2D DP 最后 2 道题收尾（Burst Balloons 区间 DP 变奏，Regular Expression Matching）
- 然后进入 Greedy 专题（Jump Game, Gas Station, Hand of Straights 等）

**系统设计：** 60/60 全部完成 ✅ — 进入综合巩固演练

**Python Craft：** 50/50 全部完成 ✅ — 进入 Expert Synthesis 阶段

**Frontend（37/50）：** JavaScript 核心内功专题开始
- Promises & async/await — 异步控制流
- Event Loop — Microtask vs Macrotask 执行顺序
- Prototypes & `this` — JS 对象的底层运作

**总体状态：** 已完成 SysDesign、Behavioral、AI、Python Craft 四个模块。最后冲刺阶段：NeetCode 还剩 31 题，Frontend 还剩 13 个话题。
