📅 **Week in Review — Week 25 (10 min read)**
📊 NeetCode: 61/150 · SysDesign: 60/40 · Behavioral: 60/40 · Frontend: 37/50 · AI: 30/30
🔥 Keep the streak alive!

---

## 🗓️ 本周回顾 / This Week's Journey

**周一 Day 73（6/22）** — 系统设计：LLM 推理服务系统；算法：序列化/反序列化二叉树（Trees 收官第 15 题）；软技能：On-Call 陌生系统；Python Craft：CPython 垃圾回收；AI 新闻：AI agent 框架安全漏洞、Self-Harness 自进化框架、挪威 AI 教育分级政策

**周二 Day 74（6/23）** — 系统设计：设计 AI 聊天平台（ChatGPT 规模）；算法：实现 Trie（前缀树模式开篇）；软技能：招聘与团队成长（Staff 级别）；Python Craft：Python 导入系统；AI：AGI 争论与新兴架构（Mamba、MoE、Test-Time Compute）

**周三 Day 75（6/24）** — 复习日：回顾 ChatGPT 平台架构（Sticky Session + KV Cache）、二叉树序列化 BFS 原理、Python 循环引用与分代 GC

**周四 Day 61（6/25）** — 系统设计：AI 聊天平台深度补充（SSE vs WebSocket、多租户隔离）

**周五 Day 62（6/26）** — 系统设计：AI 聊天平台第三视角；算法：前缀树模式 2/3 — 通配符搜索（`.` 匹配任意字符，DFS 回溯）

**周六 Day 76（6/27）** — 深度专题：前缀树通配符搜索全解（理论 + 实现 + 面试追问 + 生产应用）

---

*Mon Day 73 (6/22): LLM Inference Serving + Tree Serialization (Trees 15/15) + On-Call ownership + CPython GC + AI framework security news*
*Tue Day 74 (6/23): AI Chatbot Platform + Trie intro (1/3) + Hiring/growing teams + Python import system + AGI/emerging architectures*
*Wed Day 75 (6/24): Review day — session affinity, BFS serialization, generational GC*
*Thu Day 61 (6/25): AI Chatbot Platform — SSE deep dive + multi-tenant queues*
*Fri Day 62 (6/26): AI Chatbot Platform (third take) + Wildcard Trie (2/3) — DFS backtracking*
*Sat Day 76 (6/27): Deep Dive — Design Add and Search Words (Trie + wildcard, interview simulation)*

---

## 🧠 系统设计要点 / System Design: Key Takeaways

本周系统设计完全聚焦在 **AI 基础设施**这一主题，三个话题层层递进：

**1. LLM 推理服务（Day 73）— GPU 利用率的艺术**

传统 static batching 让 GPU 等最慢的请求，利用率仅 ~30%。**Continuous Batching（vLLM）** 允许请求随时进出队列，GPU 利用率提升至 80%+。**PagedAttention** 把 KV Cache 像操作系统管理内存一样分页管理，解决长上下文的显存碎片问题。关键区分：Prefill 阶段（处理 prompt）是计算密集型；Decode 阶段（生成 token）是内存带宽密集型——两者应分开优化，即 Prefill-Decode Disaggregation。

**2. AI 聊天平台（Days 73-75, 61, 62）— 五次讲同一题，每次都有新角度**

核心架构决策链：
- 流式用 **SSE**（单向，HTTP/2 兼容），不用 WebSocket
- 对话上下文用 **Redis TTL**（短期），长历史压缩存 S3
- 模型并行：**张量并行**（低延迟单请求）+ **流水线并行**（高吞吐批量）组合使用
- 多租户：不同 tier 走不同**优先级队列**，免费用户高峰期可降级
- **Session Affinity**：同会话路由到同 GPU 节点，减少 KV Cache miss

**3. 三者之间的连接**：推理服务是 AI 平台的底层引擎；AI 平台是面向用户的产品层；两者共同依赖 GPU 资源池的精细化调度。

---

*This week's system design was entirely AI infrastructure — three interconnected topics. LLM inference serving: continuous batching + PagedAttention = 3x better GPU utilization. AI chatbot platform: SSE over WebSocket, Redis for context, tensor × pipeline parallelism, priority queues for multi-tenancy, session affinity to reduce KV cache misses. Connection: inference serving is the engine beneath the chatbot platform.*

---

## 💻 算法模式总结 / Algorithms: Patterns Mastered

### 🌳 Trees 模式（第 13-15 题）— 本周完结

本周以 **序列化/反序列化二叉树（#297）** 结束了整个 Trees 模式块（共 15 题）。

**BFS 序列化的关键洞察**：null 节点也要作为占位符入队，否则无法区分左/右子节点缺失。`"1,2,3,N,N,4,5"` 中的两个 `N` 是 node 2 的左右子节点，位置信息不能丢失。反序列化时按 `(父节点 → 左子 → 右子)` 的顺序消费 token，队列保证层序同步。

15 题 Trees 全景回顾：
```
翻转 → 最大深度 → 直径 → 平衡 → 同构 → 子树 → 层序 → 右视图
→ 路径和 → 好节点 → BST验证 → BST第K小 → 前/中序建树 → 最大路径和 → 序列化
```
每题都是一个 DFS 模板的变体，核心变化是"返回值语义"越来越复杂。

### 🔡 Tries 模式（第 1-2 题）— 新模式开始

**Day 73/61（#208 Implement Trie）**：共享前缀 → O(L) 查询，无论字典多大。
**Day 76（#211 Wildcard Search）**：`.` 通配符 = 在 Trie 上做 DFS + 回溯，遇到通配符尝试所有子节点。最坏情况 O(N)（全通配符遍历整棵树）。

下周终局：**#212 Word Search II（Hard）** = Trie + 2D Grid DFS，用前缀剪枝避免无效路径。

---

*Trees block complete (15/15): serialization's key insight = null placeholders preserve positional info. Trie block started (2/3): wildcard `.` converts O(L) lookup to DFS backtracking. Coming up: #212 Word Search II — Trie meets 2D grid, prefix pruning eliminates dead paths early.*

---

## 🗣️ 软技能练习重点 / Soft Skills: What to Practice

本周覆盖两个高频 Staff+ 场景：

**On-Call 陌生系统（Day 73）**：面试官考的不是技术能力，是**系统性准备**的心态。三步框架：① 接手前两周主动建 context（读代码、看历史 incident、理解 top 5 告警类型）；② 每个告警必须对应 runbook，没有 runbook 不接手；③ 明确升级标准——知道何时叫人是专业，不是失败。Staff 加分：把自己做的 runbook 模板推广到 org，推动"服务转移 checklist"制度化。

**招聘与团队成长（Day 74）**：最高杠杆的工作。关键区别：参与招聘 vs **定义招聘标准**。Staff 期望：建 rubric 让主观判断可量化；做 shadow/reverse-shadow 传递面试文化；把经验制度化而非个人独享。量化影响很重要——"pass-rate variance 降低 40%" 比 "面了很多人" 更有说服力。

**需要刻意练习**：两个场景都要准备具体的 STAR 故事，量化结果是关键。On-Call 场景可以结合生产事故经历；招聘场景可以结合改进过的面试流程或设计过的 rubric。

---

*On-call foreign systems: proactive context-building before the first page + runbook-per-alert + clear escalation criteria. Hiring: define the bar (rubric), calibrate others (shadow program), institutionalize learnings. Both need quantified STAR stories ready to go.*

---

## 🎨 前端知识巩固 / Frontend: Concepts to Lock In

本周无新前端内容（前端 index 维持在 37/50）。

上次覆盖的主题（Days 61-65 期间）包括：Virtualization、Code Splitting、Web Vitals（LCP/FID/CLS）— 如果还没复习，这周是好时机。

自查题：
- `LCP > 2.5s` 最常见的两个原因是什么？如何优化？
- `React.lazy` + `Suspense` 实现路由级 code splitting 的完整写法？
- 虚拟列表（windowing）的核心原理 — 为什么只渲染可视区域够用？

---

*No new frontend content this week (index at 37/50). Good week to revisit Web Vitals, code splitting, and virtualization. Self-check: LCP causes + fixes, React.lazy syntax, windowing principle.*

---

## 🤖 AI 知识点 / AI: What Stuck

**AI 框架安全漏洞（Day 73 新闻）**：LangGraph、Langflow、LangChain-core 同时曝出高危漏洞，Langflow 约 7,000 台服务器遭在野攻击。漏洞本质是老问题（SQL 注入、路径遍历、不安全反序列化），不是 AI 特有风险。**据报道**受影响版本和修复版本已公开，如果生产环境在用这些框架，应尽快检查并升级。工程师关键认知：这些框架持有 API 密钥和数据库凭证，攻破一个等于暴露所有下游系统。

**AGI 与新兴架构（Day 74）**：最值得记住的是三条技术趋势——① **Mamba/SSM**：线性时间序列处理，O(n) vs Transformer 的 O(n²)，长上下文高效；② **Test-Time Compute**（OpenAI o3、DeepSeek R1 路线）：推理时多花算力生成思维链，不依赖更大的预训练模型；③ **MoE 细粒度化**：每 token 激活更少比例的专家，实现大容量模型 + 小推理成本。

---

*AI framework CVEs: old vulnerabilities (SQLi, path traversal) in new frameworks — upgrade immediately if using LangFlow/LangGraph/LangChain in prod. ("据报道" applies to specific CVSS scores cited.) AGI section: Mamba (linear-time attention alternative), Test-Time Compute (reasoning via inference-time budget, not model size), fine-grained MoE (sparse activation = big capacity, low cost) — these three architectural shifts are worth tracking.*

---

## ⚠️ 需要复习的内容 / What to Review

**最需要强化的区域：**

1. **二叉树完整 15 题串联**：Trees 模式刚收官，趁热打铁快速复习 #124（最大路径和）和 #297（序列化），这两题返回值语义最复杂，是面试高频出现的"Hard 题压轴"。

2. **Trie 模式第 3 题准备**：下周 #212 Word Search II（Hard）是 Trie 模式的终局。提前思考：如何把 Trie 剪枝嵌入 2D 网格 DFS？什么时候从 Trie 删除已找到的词（避免重复）？

3. **AI 聊天平台多视角融合**：同一题讲了三次（Days 60、61、62），核心区别要能区分清楚：连续批处理（推理层）vs 会话亲和性（路由层）vs 上下文截断（应用层）。

4. **Python GC 面试题**：循环引用 + 分代 GC 是 Python 面试必考题，`gc.collect()`、`weakref`、`tracemalloc` 三个工具的使用场景要能流利回答。

---

*Priority review: Trees Hard problems (#124, #297) while fresh; prep #212 Word Search II (Trie + grid DFS — think about pruning strategy); clarify AI chatbot architecture layers (batching ≠ routing ≠ context management); Python GC triad (refcount + generational + weakref) for interviews.*

---

## 🏆 本周亮点 / Win of the Week

**Trees 模式 15/15 完结！**

从第 1 题（翻转二叉树）到第 15 题（序列化/反序列化），完整走完了 NeetCode Trees 模式的全部 15 道题。这不只是数字上的里程碑——Trees 是二叉搜索树、图、Trie、堆等所有后续数据结构的基础。掌握了"DFS 返回值语义的演变"这一核心模式，后续的 Graph DFS 和 Trie DFS 都是这个模式的自然延伸。

同时，本周的深度专题（Saturday Deep Dive）质量很高——包含完整实现、迭代版本、面试追问 5 题、生产应用 4 个场景，是迄今为止最完整的一次深度专题。

---

*Trees pattern complete: 15/15. The core insight — DFS return value semantics evolve from simple (depth) to complex (path sum + global max) — carries directly into graphs and Trie DFS. Saturday Deep Dive quality this week: full implementation, iterative alternative, 5-question interview simulation, 4 production applications.*

---

## 🎯 下周预告 / Next Week Preview

基于当前进度（Day 76，Expert 阶段，6/28 星期日）：

**算法（Trie 模式终局）**
- `#212 Word Search II`（Hard）— Trie + 2D Grid DFS，本 block 最难题
- 进入下一模式：**Heap / Priority Queue**（#703, #1046, #703...）

**系统设计**（第 61 题之后）
- 新话题暂不透露，但 Expert 阶段会继续涉及分布式系统深水区

**Python Craft**
- index 23 — 预计继续 Python 内部机制或高级设计模式话题

**软技能**
- 继续 Staff/Principal 级别领导力场景

**一个问题提前想**：`#212 Word Search II` 用 Trie 的关键剪枝：当一条路径走到 Trie 中某个叶节点（`is_end=True` 且无子节点），找到单词后应该从 Trie 中删掉这个节点，避免重复记录同一个词。这个"边找边剪"的 Trie 变种是本题的核心技巧。

---

*Next week: #212 Word Search II (Trie block finale — hardest problem, Trie + grid backtracking), then Heap/Priority Queue block starts. System design continues Expert-tier distributed systems. Pre-think: in #212, delete found words from Trie to avoid duplicates — the "prune-while-searching" trick is the key insight.*

---

*byte-by-byte · Week 25 · Day 76 · Generated 2026-06-28*
