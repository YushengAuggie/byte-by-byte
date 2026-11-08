📅 **Week in Review — Week 35 (10 min read)**
📊 NeetCode: 116/150 · SysDesign: 60/60 · Behavioral: 60/60 · Frontend: 37/50 · AI: 30/30
🔥 6-day streak!

---

## 🗓️ This Week's Journey / 本周回顾

| 日期 | 主题 |
|------|------|
| **周一 11/3 — Day 146** | 可观测性三支柱 · 状态机DP · Strangler Fig重构策略 · asyncio原理 |
| **周二 11/4 — Day 147** | 单体→微服务决策树 · 无界背包 · React.memo陷阱 · Python性能诊断 |
| **周三 11/5 — Day 148** | 分布式一致性三范式 · 背包数学变换 · Senior→Staff隐形门槛 · Zustand vs Redux |
| **周四 11/6 — Day 149** | 一致性层级全谱 · 二维字符串DP · 技术债高管辩论 · Python服务完整工具链 |
| **周五/六 11/7 — Day 150** | 🎉 里程碑！5个月收官 · 区间DP深度讲解 (Burst Balloons #312) |

---

## 🧠 System Design: Key Takeaways / 系统设计要点

本周系统设计进入**综合收官阶段**（systemDesignIndex 60/60 — 全部完成！），三个主题深度关联：

**1. 可观测性三支柱（Day 146）**
Metrics → 告警（"什么出问题了"），Traces → 定位（"哪条链路慢"），Logs → 根因（"具体发生了什么"）。关键：三者必须通过 `trace_id` 打通，否则只有两条腿的凳子。调查顺序永远是：Metrics → Traces → Logs。

**2. 架构选型决策树（Day 147）**
核心结论：Conway's Law 比技术能力更决定架构。单体→读写分离→缓存→微服务，是有序演进，不是跨越。Shopify、Stack Overflow 用单体撑过了多年高增长。微服务的真实门槛是"不同团队需要独立部署节奏"，不是"感觉该拆了"。

**3. 分布式一致性三范式 + 一致性层级（Day 148–149）**
强共识（Raft/etcd）= 线性一致，高延迟；CRDT = 无冲突合并，天生适合协作编辑；Event Sourcing = 完整历史，适合金融审计。分层使用：账户余额用 Postgres，展示用 Redis，操作日志用 Kafka——这才是生产级架构思维。

**三者连接：** 可观测性帮你诊断分布式系统的一致性问题；架构演进决定了你在哪个层级上运用哪种一致性保证。

---

## 💻 Algorithms: Patterns Mastered / 算法模式总结

本周完成 **二维动态规划（2-D DP）** 模式的核心部分（共 11 题中的第 3–7 题）：

**🎯 状态机 DP — Best Time to Buy Sell with Cooldown (#309)**
关键洞察：`dp[i][state]` 而非 `dp[i][j]`，三个状态（holding/sold/idle）压缩为三个变量。每次状态转移要用 `prev_*` 避免覆盖。复杂度 O(n) 时间 O(1) 空间。

**🎯 无界背包 — Coin Change II (#518)**
核心区别：正序遍历 amount（允许重复使用），vs 01背包的逆序遍历。外层 coin，内层 amount = 每枚硬币无限次。

**🎯 数学变换 + 01背包 — Target Sum (#494)**
最大亮点：暴力 O(2^n) → 数学转化 → `P = (total + target) / 2` → 转化为子集和计数问题。逆序遍历 = 每个数只用一次。

**🎯 双序列字符串 DP — Interleaving String (#97)**
`dp[i][j]` = s1 前 i 个 + s2 前 j 个能否构成 s3 前 i+j 个。新增维度：转移时需比较字符是否匹配 s3。

**🎯 区间 DP — Burst Balloons (#312) [Deep Dive]**
本周最精彩的"顿悟题"：**不问先戳哪个，问最后戳哪个**。开区间 (i,j) 中最后一个被戳破的气球 k，两侧边界固定 → 子问题真正独立。遍历顺序：按区间长度从小到大。

**共同规律：** 2-D DP 的本质是"两个维度的状态追踪"——可以是两个序列（LCS/Interleaving），也可以是序列+状态（Cooldown），也可以是序列+容量（背包），也可以是区间两端（Burst Balloons）。

---

## 🗣️ Soft Skills: What to Practice / 软技能练习重点

本周软技能进入 **Staff+ 综合阶段**（behavioralIndex 60/60 — 全部完成！），三大主题：

**本周涵盖场景：**
- 核心支付服务技术债重构 + 跨职能利益相关者对齐（Strangler Fig + 量化成本）
- P99 延迟 800ms→200ms 的 6 个月改善计划（观测优先，并行推进）
- Senior→Staff 的四个隐形门槛（问题定义/组织影响力/多年视野/模糊性导航）
- 技术债 vs 新功能的高管辩论（三方案框架 + ROI 翻译）

**哪些需要继续练习：**

1. **量化一切** — "技术债每季度损失 X 工程师周"比"代码很烂"有力 100 倍。练习：下次讨论技术决策时，先花 30 分钟做数据量化再开口。

2. **提供三个选项** — 不要只带解决方案，带方案矩阵。每个选项附上 trade-off 和你的推荐理由，让 leadership 感觉在决策而非被安排。

3. **Staff 影响力模式** — 推动没有汇报关系的团队改变。下次机会：找一个跨团队的重复造轮子场景，主动推动标准化，用 RFC 而非会议。

---

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固

本周前端聚焦两大主题（frontendIndex 37/50）：

**React 性能（Day 147）**
核心原则：先用 React DevTools Profiler 量化，再加 `React.memo`。`memo` 不配 `useCallback` = 无效；Context 变化会绕过 `memo`（最容易踩的坑）。

✅ 自测：以下场景 `React.memo` 有效吗？
- 父组件每次传 `() => console.log('click')` 作为 prop → **无效**（需加 `useCallback`）
- 子组件消费了一个频繁变化的 Context → **无效**（需拆分 Context）
- 父组件状态变化但子组件 props 不变 + 用了 `useCallback` → **有效**

**状态管理选型（Day 148）**
决策框架：服务器状态 → React Query；客户端全局状态 → Zustand；低频数据传递 → Context；大型多团队企业 → Redux Toolkit。不要用 Redux 存 API 数据，不要用 Context 存高频变化的状态。

---

## 🤖 AI: What Stuck / AI 知识点

本周 AI 模块全部完成（aiTopicIndex 30/30 🎉），最重要的综合 + 新闻要点：

**技术综合（Day 146）：** RAG 生产级实现 = Embeddings + FAISS 向量检索 + KV Cache 复用 + Streaming 输出。这是目前最主流的"给 LLM 加外挂知识"的方式。

**本周 AI 新闻亮点（均带"据报道"限定）：**

- **GPT-6 Astra 据报道能直接编辑另一个模型的权重**（Day 146）——暗示 AI 自我改进的新范式。据报道。
- **模型军备竞赛加速**（Day 147）：GPT-6 Rosalind/Terra、Gemini 4 Carbon/Argon、Claude Haiku 5.5 集中发布；推理成本持续暴跌。
- **GPT-6 Cyber 据报道专攻漏洞挖掘**（Day 149），在 Linux、Firefox 等软件中识别数千个漏洞——AI 安全攻防同步加速。
- **Anthropic IPO 遇冷**（Day 149）：$1.5T 估值遭投资者质疑，运营仍亏损。
- **Stanford 研究据报道：LLM 论文结论平均 15 个月内失效**（Day 146）——AI 领域的独特挑战：模型迭代速度超过学术发表周期。

---

## ⚠️ What to Review / 需要复习的内容

**算法弱点：**
- 区间 DP 的遍历顺序（按区间长度从小到大）在代码实现时容易写错——默写一遍 Burst Balloons 的外层循环
- 01背包 vs 无界背包的关键区别：逆序 vs 正序遍历 amount。默写前不看题

**系统设计：**
- 可观测性三支柱的边界案例：什么时候 Metrics 不够（高基数），什么时候 Logs 不够（跨服务链路），写出各自的 anti-patterns
- CRDT 的局限性：什么操作无法建模为 CRDT？（非交换操作，如先删后加 vs 先加后删）

**前端：**
- Context value 绑定稳定引用（`useMemo`）避免绕过 memo——写一个示例
- Zustand selector 最小化订阅——能徒手写出基础的 store + selector 模式

**软技能：**
- 量化技术债的模板公式还不够熟练——练习用真实场景套入（直接成本 + 机会成本 + 风险成本）

---

## 🏆 Win of the Week / 本周亮点

🎉 **Day 150 — 5 个月里程碑达成！**

从 Day 1 的 Client-Server 基础，到今天完成 SysDesign（60/60）、Behavioral（60/60）、AI（30/30）三个维度的全覆盖，掌握了区间 DP 这道 Hard 题的核心"顿悟"……

5 个月前你打开第一道题，今天你能不看提示地推导出 Burst Balloons 的状态转移方程。这不是线性进步——这是真正的积累。

**The real win:** 你建立了一套把技术复杂度翻译成业务语言的思维框架。这才是 Staff+ 面试的真正护城河。

---

## 🎯 Next Week Preview / 下周预告

基于当前进度（Day 151 起，2-D DP 模式继续），预计下周涵盖：

**算法（2-D DP 收尾，进入新模式）：**
- Edit Distance (#72) — 字符串编辑距离，经典 DP 双串
- Longest Increasing Path in Matrix (#329) — 矩阵 DP + DFS + 记忆化
- Distinct Subsequences (#115) — 子序列计数，01背包变体
- Regex Matching (#10) — 通配符 DP，难度跃升至 Hard

**前端（继续 frontendIndex 37→约40/50）：**
- 继续前端进阶主题

**系统设计 + Behavioral + AI：**
- 三个维度已满，预计进入综合复习和模拟面试场景

💡 **重点关注：** Edit Distance 是最经典的二维 DP 之一，也是 Regex Matching 的基础。先把 Edit Distance 的四种转移（相等/替换/插入/删除）背到手熟，再挑战 Regex。

---

*Generated: 2026-11-08 | Week 35 of 150-day journey*
