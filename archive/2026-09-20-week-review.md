📅 **Week in Review — Week 38 (8 min read)**
📊 NeetCode: 104/150 · SysDesign: 60/40✅ · Behavioral: 60/40✅ · Frontend: 37/50 · AI: 30/30✅
🔥 Day 134 — Expert Phase!

---

## 🗓️ 本周回顾 / This Week's Journey

| 日期 | Day | 主题概要 |
|------|-----|---------|
| 周一 Sep 15 | 133 | 事件驱动 vs 请求驱动架构终极综合 · Palindromic Substrings（中心扩展法）· Org Reorg 中 Staff 级应对 · Python 字节码与 dis 模块 · AI新闻：DeepSeek/GPT-6/Claude Enterprise |
| 周六 Sep 19 | 134 | 🔬 Saturday Deep Dive — Decode Ways (LC #91 + #639)：从暴力递归到 O(1) 空间 DP，含通配符完整变体 |

**本周节奏较缓，内容集中在质量深度而非数量覆盖。2 个活跃日，但每一天的深度都在线。**

---

## 🧠 系统设计：本周要点 / System Design: Key Takeaways

**Day 133: 事件驱动 vs 请求驱动架构终极对比**

本周系统设计是跨越全程的架构综合——把支付、通知、聊天、股票交易所等过去所有设计题背后的架构选型逻辑串联起来，提炼出可复用的决策框架。

**三大核心洞察 / Top 3 Insights:**

1. **选型核心问题只有一个**：调用方是否需要等待结果？需要 → 请求驱动（同步 HTTP/gRPC）；不需要 → 事件驱动（Kafka/SQS）。支付走同步，通知走异步，聊天混用（WebSocket 在线 + MQ 离线）。
   
   *The deciding question: does the caller need to wait for the result? Yes → request-driven. No → event-driven. Payments are phone calls; notifications are group texts.*

2. **事件驱动四大必踩坑**：消息幂等性缺失 → 重消费副作用；顺序假设错误 → 跨分区乱序；schema 演进无保护 → 消费者崩溃；没有 DLQ → 毒消息永久卡住。
   
   *At scale, event-driven systems fail in four predictable ways: non-idempotent consumers, ordering assumptions, unprotected schema evolution, and missing dead-letter queues.*

3. **Saga = 微服务时代分布式事务的标准答案**：本地事务 + 补偿事务替代 2PC，以最终一致性换可用性。面试中凡是被问"分布式事务怎么做"，Saga + 补偿事务就是框架。
   
   *Saga Pattern replaces 2PC with local transactions + compensating transactions. The go-to answer for "how do you handle distributed transactions in microservices?"*

---

## 💻 算法：模式总结 / Algorithms: Patterns Mastered

**本周题目：**
- Day 133: #647 Palindromic Substrings (Medium) — 1-D DP 模式 6/12
- Day 134 Deep Dive: #91 Decode Ways + #639 Decode Ways II (Hard)

**模式对比表 / Pattern Comparison:**

| 题目 | 核心技术 | 关键变化 |
|------|---------|---------|
| #5 Longest Palindromic Substring | 中心扩展法 | 记录最长，返回字串本身 |
| #647 Palindromic Substrings | 中心扩展法 | 每次扩展 count++，返回数量 |
| #91 Decode Ways | 爬楼梯 + guard | `dp[i-1]`（单位有效）+ `dp[i-2]`（两位有效） |
| #639 Decode Ways II | 同上 + 乘法因子 | `*` 通配引入 9/6/15 倍率，枚举 4 种 case |

**本周最重要的算法洞察：**
- #647 和 #5 是同一技术的两种输出形式 — 中心扩展掌握一次等于两道题免费
- Decode Ways 本质 = "带禁行台阶的爬楼梯"，转移方程与 Climbing Stairs 完全同构
- `dp[0] = 1` 是最容易忘的 base case — 漏掉它所有两位解码永远贡献 0
- LC #639 通配符：`*`+`*` → 15种，`1`+`*` → 9种，`2`+`*` → 6种，`*`+`c` → ×2（c≤6）或 ×1（c>6）

*Master insight: Decode Ways is Climbing Stairs on a broken staircase. The recurrence is identical — the only difference is guards that zero out invalid steps.*

---

## 🗣️ 软技能：练习重点 / Soft Skills: What to Practice

**Day 133 场景：Org Reorg 中途，如何维持 Staff 级项目交付**

**覆盖场景 / Scenario Covered:**
项目进行到 60%，公司突然重组：团队拆散、新 manager 零上下文。如何保证交付不 slip + 48 小时内建立新 credibility？

**Staff 级标准动作（按优先级）：**
1. **第一动作是写，不是说** — 发出 Project Health Doc：状态、风险、决策历史、依赖方、剩余工作，一页纸，15 分钟任何人可 onboard
2. **给新 manager 最小可决策上下文** — 不是历史课，是"现状 + 3 大风险 + 1 件需要你解封的事"
3. **主动提 descope，不等被要求延期** — Staff 控制叙事，不汇报问题
4. **离队成员知识迁移** — ADR + pair programming，把隐性知识显性化

**金句 / Key Framing:** 
> "混乱时期，谁能提供清晰度，谁就有影响力。"  
> *In chaos, whoever provides clarity gains influence.*

**需要练习的点：**
- 能否 2 分钟内用完整 STAR 讲出这个场景，突出 proactive 动作？
- 有没有真实 reorg 经历可以替换进来，让故事更有说服力？

*The Staff tell: you hand your new manager a one-page project health doc before they ask — then show up to the 1:1 with an agenda, not a status update.*

---

## 🎨 前端：知识巩固 / Frontend: Concepts to Lock In

**本周前端内容：** 无新专项内容（综合阶段，本周无独立前端章节）

**快速自检 — 近期前端知识点是否还在：**
- `useTransition` vs `useDeferredValue`：哪个是"我主动触发的低优先级更新"，哪个是"我响应别人触发的延迟"？
- React Server Components 下，哪些 hooks 不能用？为什么？
- 当前进度：37/50，剩余 13 个主题

*Frontend stalled this week. Quick check: can you explain useTransition vs useDeferredValue without looking it up? If not, that's the first thing to revisit.*

---

## 🤖 AI：知识点 / AI: What Stuck

**Day 133 AI 新闻要点（以下具体数字/声明均来自新闻整理，据报道）：**

1. **据报道 DeepSeek V4.1 Flash 缓存定价 $0.003/M tokens** — AI 推理成本正从"稀缺资源"变成"近乎免费的工具"，产品选型框架应从"哪个最好"转向"哪个性价比最优、风险最低"。
   
   *Reportedly $0.003/M cached input tokens — AI inference is becoming a commodity utility. Shift your model selection framework to risk-adjusted cost-performance.*

2. **据报道 OpenAI GPT-6 Astra 在发布时被评为网络安全"关键级别"风险** — 首次公开发布时承认达到 Critical 安全阈值，检验 Preparedness Framework 是否真有约束力的实战信号。
   
   *Reportedly classified as "Critical" cybersecurity risk at launch — a live test of whether AI safety frameworks translate into real constraints.*

3. **据报道 Claude Enterprise 支持 50 万词上下文窗口** — 重新评估 RAG 必要性：若文档集能直接 fit 进上下文，RAG 的额外复杂度可能得不偿失。但成本依然是关键变量（长上下文 = 更多 token）。
   
   *500K-word context changes the RAG calculus: when the corpus fits directly, added RAG complexity may not pay off — but watch the token bill.*

**本周最重要的 AI 洞察 / Most Important Takeaway:**
能力上限在涨，单价在崩 — **性价比与风险控制**将是未来 AI 选型的核心维度，而不再是"哪个模型最强"。

*Capabilities and costs are compressing in opposite directions. Risk-adjusted cost-performance is the new selection criterion.*

---

## ⚠️ 需要复习的内容 / What to Review

**优先级排序：**

1. **🔴 Decode Ways II 的 `*` case 枚举需要能流利背出** — 4 种 case 组合（`**` → 15, `1*` → 9, `2*` → 6, `*c` → ×2 或 ×1）是高频翻车点。面试中就算遇不到这道题，展示你能推导乘法因子来源本身就是加分项。

2. **🟡 1-D DP 模式尚在进行中（6/12）** — Decode Ways 之后是 #139 Word Break、#300 LIS 等。这批题关联性强，动能不能断。建议下周保持每日 1 道 DP 题的节奏。

3. **🟡 前端进度停滞 37/50，已超 2 周无专项内容** — 建议下周强制补上 1-2 个前端主题。候选：Next.js 进阶 API / Server Actions 深化，或 Web Performance 实战（LCP/CLS 优化）。

4. **🟢 系统设计综合是否真正内化？** — 建议做一次无辅助口头 whiteboard：出题"设计通知系统，事件驱动，1B DAU"。如果能自然串出 Kafka 扇出 + DLQ + schema registry + Saga，就是真正掌握了。

*Top priority: Decode Ways II wildcard cases + keep the DP momentum going. Don't let frontend sit at 37 for a third week.*

---

## 🏆 本周亮点 / Win of the Week

**Saturday Deep Dive: Decode Ways 双题全解，把一道题彻底搞透 🔬**

从暴力递归 → 记忆化 Top-Down → Bottom-Up DP → O(1) 空间优化，再到 Hard 变体 LC #639 的 `*` 通配符完整 case 枚举，还有 5 道面试模拟 Q&A——这不是刷题，这是 ownership。

一般人 AC 了就翻篇。你把同一道题从 3 个角度、4 种实现、5 道 Q&A 全部拆透。这才是 Staff 水平的学习方式——不只会做，还要能教，还要能在面试中回答"那如果换成 `*` 通配符呢？"

*Going from brute force to O(1) space to the Hard variant with 5 interview Q&As — that's not just solving a problem, that's owning it. This is what separates candidates who "can code" from those who truly understand.*

---

## 🎯 下周预告 / Next Week Preview

基于当前进度（Day 134 完成，1-D DP 6/12）：

| 预期方向 | 内容 |
|---------|------|
| 算法（Day 135+） | 1-D DP 继续：#139 Word Break · #300 Longest Increasing Subsequence · #416 Partition Equal Subset Sum |
| 系统设计 | Synthesis 综合 |
| 软技能 | Synthesis 综合 |
| Python Craft | Synthesis 综合 |
| 前端 | 建议重新激活：Next.js / Web Performance 主题 |
| AI | News Roundup 或综合 |

**大目标提醒：**
- NeetCode: 104/150，还剩 46 题
- Frontend: 37/50，还剩 13 个主题
- 下周目标：3-4 个活跃学习日，重新找到 Mon-Fri 节奏

*Next up: close out the 1-D DP block, get frontend moving again, aim for 3-4 active days this week.*
