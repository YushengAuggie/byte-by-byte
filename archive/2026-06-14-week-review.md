📅 **Week in Review — Week 24 (10 min read)**
📊 NeetCode: 54/150 · SysDesign: 53/40 · Behavioral: 53/40 · Python: 16 · AI: 26/30
🔥 65-day streak!

---

## 🗓️ 本周回顾 / This Week's Journey

本周是第 61–65 天（Expert Phase），覆盖五个内容满满的交易日，以 Saturday Deep Dive 收尾。

*Week 61–65 (Expert Phase) — five packed days plus a Saturday Deep Dive.*

| 日期 / Date | 主题亮点 / Highlights |
|---|---|
| 周一 6/9 (Day 61) | 直播系统 · Subtree of Another Tree · Singleton 模式 · AI 编程助手生产化警示 |
| 周二 6/10 (Day 62) | 股票撮合引擎 · LCA of BST · AI 编程助手底层架构 · Command 模式 |
| 周三 6/11 (Day 63) | 分布式锁服务 · BFS 层序遍历 · 可逆/不可逆决策框架 · Builder 模式 |
| 周四 6/12 (Day 64) | CDN 从零设计 · Binary Tree Right Side View · Structured Output & JSON Mode · Adapter 模式 |
| 周六 6/13 (Day 65) | Review Day — Mini-quiz 涵盖 Day 61–64 核心知识点 + 深度回顾 |

---

## 🏗️ 系统设计要点 / System Design: Key Takeaways

**本周系统设计的暗线：极端可靠性系统的共同基因。**

*This week's hidden theme: what makes extreme-reliability systems tick.*

### 🎥 设计 Twitch 直播系统 (Day 61)
主播用 **RTMP 推流 → Transcoding 集群（多码率 HLS 分片）→ CDN 边缘节点 → 观众 ABR 拉流**。核心权衡：延迟 vs 稳定性（LL-HLS 降至 1-2s 但实现复杂）；聊天系统 fan-out 需要 pubsub + 限速采样，而非 1:1 推送。

*Streamer → RTMP → transcoding → CDN → viewer ABR pull. LL-HLS reduces latency to 1-2s but adds complexity. Chat fan-out requires pubsub + rate-limiting, not 1:1 push.*

### 📈 设计股票撮合引擎 (Day 62)
**核心反直觉：单线程比多线程更快。** 每个股票品种一个单线程引擎，零锁竞争。订单簿 = MaxHeap(买) + MinHeap(卖)；持久化靠 WAL + Event Sourcing；延迟目标 < 1ms。Fencing token 防止 GC 暂停导致的过期持有者写脏数据。NYSE 和 NASDAQ 实际架构就是这样。

*Counterintuitive: single-threaded matching engine is faster because zero lock contention. Order book = MaxHeap(bids) + MinHeap(asks). WAL + event sourcing for persistence. Sub-millisecond target.*

### 🔐 设计分布式锁服务 (Day 63)
Zookeeper 用 ephemeral sequential 节点 + watch 前驱（避免羊群效应）；etcd 用 lease TTL + compare-and-swap Txn。**最重要的设计点：Fencing Token**——单调递增令牌，防止 GC 暂停/网络抖动导致的过期持有者写脏。用 Redis SETNX 做生产级分布式锁是危险的。

*Zookeeper: ephemeral sequential nodes + watch predecessor (avoids herd effect). etcd: lease TTL + CAS transaction. Critical: fencing tokens prevent stale lock holders from corrupting data.*

### 🌐 设计 CDN (Day 64)
Pull（按需填充）vs Push（提前预热）策略；DNS/Anycast 就近路由；静态资源用内容哈希命名 + 长 TTL；动态内容 bypass CDN 或短 TTL。常见陷阱：忘记 `Vary: Accept-Encoding`、缓存含用户数据的 API 响应、Origin 单点导致雪崩回源。

*Pull vs Push caching; DNS/Anycast routing; content-hash naming for long TTL on statics. Top traps: missing Vary header, caching user-specific API responses, single-origin SPOF.*

**🔗 系统间连接 / What Connects Them:**
直播、撮合引擎、分布式锁、CDN——四个系统都依赖**同一套可靠性工具箱**：WAL/Event Sourcing（可回放性）、TTL/Lease（防死锁）、CDN/分片（就近+解耦）、fencing token（防止脑裂）。这是 Expert Phase 的核心主题：**设计模式在极端规模下的复用**。

*All four systems share the same reliability toolkit: WAL/event-sourcing (replayability), TTL/lease (deadlock prevention), sharding by key (contention avoidance), and fencing tokens (split-brain protection). Expert Phase theme: reliability patterns at scale.*

---

## 💻 算法模式总结 / Algorithms: Patterns Mastered

**本周完成树遍历 Block 第 6–9 题，DFS 与 BFS 双工具箱均已就位。**

*Completed tree traversal problems 6–9 of 15. Both DFS and BFS toolkits are now online.*

### 🌳 DFS 模式 — 子程序复用 (Day 61: Subtree of Another Tree)
关键洞察：把 **Same Tree 作为子程序**，外层 DFS 遍历每个节点，内层 isSameTree 检查是否匹配。时间 O(m×n)。进阶：序列化树 → 字符串匹配可降到 O(m+n)。

*Key insight: Same Tree as subroutine. Outer DFS traverses every node; inner isSameTree checks for match. O(m×n). Optimization: serialize to string → O(m+n).*

### 🌲 BST 导航模式 (Day 62: LCA of BST)
利用 BST 有序性：两节点都在左 → 往左；都在右 → 往右；分叉点 → 即为 LCA。**时间从 O(n) 降到 O(h)**。迭代版本空间 O(1)，优于递归版本。普通二叉树的 LCA（#236）需要双侧递归，O(n)。

*BST ordering enables guided navigation: O(h) instead of O(n). Iterative version preferred (O(1) space). Generic tree LCA requires O(n) both-sides recursion.*

### 📶 BFS 层序遍历 (Day 63: Level Order Traversal)
**核心技巧：每轮循环开始记录 `n = len(queue)`，只处理这 n 个节点**。一次 while 循环迭代 = 一层。这个 BFS 骨架是后续层级类题目的通用模板。

*Core trick: snapshot `n = len(queue)` at loop start, process exactly n nodes. One while-loop iteration = one level. This BFS skeleton is the template for all level-based problems.*

### 👁️ BFS 变体 — 右视图 (Day 64: Right Side View)
在层序遍历骨架上，每层只记录最后一个节点（`i == level_size - 1`）。DFS 变体：先遍历右子树 + `depth == len(result)` 自动只记录最右节点，更优雅但反直觉。

*Layer traversal skeleton with one change: record only the last node per level. DFS variant: visit right first + depth check — more elegant but counterintuitive.*

| 题目 | 模式 | 关键洞察 |
|---|---|---|
| #572 Subtree | DFS 嵌套调用 | Same Tree 作为子程序 |
| #235 LCA of BST | BST 性质导航 | 分叉点 = LCA，O(h) |
| #102 Level Order | BFS 队列 | len(queue) 快照分层 |
| #199 Right Side View | BFS 变体 | 每层最后一个 |

---

## 🗣️ 软技能练习重点 / Soft Skills: What to Practice

**本周软技能主题：Senior/Staff 工程师在「困难情境」下的领导力模型。**

*This week's theme: Leadership models for difficult situations at the Senior/Staff level.*

### 📋 涵盖场景 / Scenarios Covered:

**Day 61 — 队友持续 miss deadline**
核心框架：私聊优先 → 根因分析（意愿 vs 能力 vs 流程）→ 支持而非监控 → 中间检查点。Staff 级别加分：把个人问题转化为流程改进（估时规范、Definition of Ready）。

*Private conversation first → root cause (will vs skill vs process) → support not surveillance → intermediate checkpoints. Staff upgrade: convert individual issue to systemic improvement.*

**Day 62 — 主导事故响应**
框架：Triage → Communicate → **Mitigate first（先缓解，再根因）** → Root Cause → Fix → Blameless Postmortem。面试时记得给数字（QPS 影响、恢复时长）和说出 "blameless postmortem" 这个词。

*Framework: Triage → Communicate → Mitigate first → Root Cause → Blameless Postmortem. Include numbers and say "blameless postmortem" explicitly.*

**Day 63 — 信息不全时做决策（可逆 vs 不可逆）**
Bezos 的"单向门 vs 双向门"框架：可逆决策 → 快速行动 + 安全网；不可逆决策 → 慢慢来 + 多评审。**大多数决策是可逆的**——用单向门的标准处理双向门是团队速度杀手。

*Bezos's one-way vs two-way door: reversible = move fast with safety nets; irreversible = slow down. Most decisions are reversible — treating them as irreversible kills team velocity.*

**Day 64 — 长期项目动力下滑**
解耦外部依赖（mock server + contract testing）→ 大 milestone 拆小锚点 → 主动带方案上报风险 → 庆祝小胜利维持士气。"动力 = 进展感"是核心心理学原理。

*Decouple dependencies (mock server) → split milestones into 2-week anchors → proactive risk reporting with solutions → celebrate small wins. "Momentum = sense of progress."*

**⚠️ 最需要练习的场景 / Most Needs Practice:**
事故响应回答容易流于"找到 bug 修好了"。练习用完整 STAR（含数字 + blameless postmortem）来讲，以及明确说出"先 mitigate 再 investigate"的原则。

*Incident response answers tend to devolve into "found the bug and fixed it." Practice the full STAR with numbers + postmortem, and explicitly stating "mitigate before investigate."*

---

## 🐍 Python Craft: Design Patterns Week 4 — 模式总结

**本周完成设计模式 Week 4，四个模式都有深度实战代码。**

*Completed Design Patterns Week 4. All four patterns covered with production-grade code examples.*

| 模式 / Pattern | 核心用途 | Python 特别提示 |
|---|---|---|
| **Singleton** (Day 61) | 全局唯一实例（连接池、配置） | module-level var 更 Pythonic；注意线程安全的双重检查锁 |
| **Command** (Day 62) | 操作封装 → Undo/Redo/Queue | Task Queue 场景下序列化 Command 是 Celery 的基础 |
| **Builder** (Day 63) | 多可选参数的分步构造 | Python 优先用 `@dataclass + kwargs`；Builder 用于需要校验/链式 DSL 时 |
| **Adapter** (Day 64) | 第三方接口转统一接口 | 适配器只做接口转换，业务逻辑留给调用方；保持无状态 |

**模式间的联系：** Command + Adapter 是构建"可插拔、可扩展"系统的基础组合——Command 让操作可排队可撤销，Adapter 让不同数据源统一接口。这正是事件驱动架构的核心思想。

*Command + Adapter are the foundation of pluggable, extensible systems — Command makes operations queueable and undoable; Adapter unifies disparate interfaces. This is the core of event-driven architecture.*

---

## 🤖 AI 要点 / AI: What Stuck

**本周 AI 内容聚焦两个主题：AI Coding Assistants 的技术内核 + Structured Output 最佳实践。**

### 🤖 AI 编程助手架构 (Day 62)
四层架构：Editor Plugin → **Context Engine**（FIM + RAG + LSP）→ LLM Inference → Output Rendering。关键技术：**Fill-in-the-Middle (FIM)** 训练让模型能填 prefix/suffix 之间的空白；Context Engine 用 Jaccard 相似度（不需要 embedding！）做代码片段检索；Cursor 等进阶工具用 ReAct 模式实现 agent 级别的多文件编辑。

*Four layers: Editor Plugin → Context Engine (FIM + RAG + LSP) → LLM Inference → Output. FIM training enables prefix+suffix → middle completion. Jaccard similarity (no embeddings needed) for snippet retrieval.*

### 📊 Structured Output & JSON Mode (Day 64)
核心原理：**约束解码 (Constrained Decoding)**——JSON Schema → 状态机 → 每步只能选合法 token。JSON Mode 只保证合法 JSON 语法，Structured Outputs 保证字段名/类型/结构完全匹配 Schema。最佳实践：Schema-First 开发、处理 refusal、复杂推理用两阶段生成。据报道 Anthropic 于 2026 年初正式 GA 结构化输出功能。

*Constrained Decoding compiles JSON Schema to a state machine. JSON Mode ≠ Structured Outputs — only the latter guarantees schema conformance. Schema-first development is the right approach.*

### 📰 AI 新闻速递 (Day 61, Day 63)
- 据报道 Anthropic 80% 生产代码由 Claude 编写；Snap 裁员 1000 人称 AI 生成 65%+ 代码（据报道）；Nvidia 发布 Cosmos 3 物理 AI 基础模型（据报道）
- 据报道 Anthropic 发布 Claude Fable 5（专为药物发现设计）；微软 Build 2026 发布 MAI-Thinking-1（稀疏 MoE，~350 亿激活参数）；Nvidia Nemotron 3 Ultra（据报道 5500 亿参数 MoE，1M token 上下文）（据报道）
- 趋势：MoE + 长上下文 + 低比特训练（4-bit NVFP4/QAT）正成为标配

*Key trend: MoE + long context + low-bit training (4-bit NVFP4/QAT) becoming standard. AI coding contribution rates at major companies signal a structural shift in software development.*

---

## ⚠️ 需要复习的内容 / What to Review

**1. 分布式锁的 Fencing Token（两次提到，仍需加深）**
Kleppmann 的论点常在面试中被追问："分布式锁能 100% 保证安全吗？" 答案是否——GC 暂停可以让持有者在锁过期后仍继续写。Fencing token（单调递增令牌 + 被保护资源校验）才是真正安全的做法。建议：实际手写一个 etcd lease + fencing token 的伪代码流程。

*Can a distributed lock guarantee 100% safety? No — GC pauses can cause stale holders to write after expiry. Fencing tokens are the real answer. Practice: write pseudocode for etcd lease + fencing token flow.*

**2. 算法：DFS 右子树优先 + depth 判断的 Right Side View 解法**
BFS 解法直观，但 DFS 解法（先右后左 + `depth == len(result)`）更优雅且空间复杂度更好（O(h) vs O(w)）。建议从零手写 DFS 版本，不要依赖 BFS 版本的记忆。

*The DFS variant for Right Side View (visit right first + depth check) is more elegant and space-efficient. Practice writing it from scratch without relying on the BFS version.*

**3. 软技能：事故响应回答的数字化**
回答事故响应时，"影响了一些用户，我们在几小时内修复了"远不如"影响了 15% 的支付请求，我们在 47 分钟内恢复了 SLA"。建议：准备 2-3 个真实事故的 STAR 故事，每个都有具体数字。

*"Impacted some users, fixed in a few hours" is weak. "Impacted 15% of payment requests, restored SLA in 47 minutes" is strong. Prepare 2-3 real incident stories with specific metrics.*

---

## 🏆 本周亮点 / Win of the Week

**本周最大的亮点：算法模式的质变。**

从 Day 61 到 Day 64，树遍历从"用 Same Tree 作为子程序"（组合模式），到"利用 BST 性质做有目的的导航"（O(h) vs O(n)），到"BFS 与 DFS 双工具箱互补"——这是一次清晰的认知升级，不再是记题解，而是在**感受算法工具箱里每个工具的边界和选择时机**。Day 62 股票撮合引擎"单线程反而更快"也是本周最反直觉、最值得炫耀的洞察。

*The algorithmic leap this week: from "memorize solutions" to "feel the boundary and choice moment of each tool." The counterintuitive insight that single-threaded matching engines outperform multi-threaded ones is this week's most interview-worthy takeaway.*

本周亮点也体现在 Python Craft 的系统性收尾——四个设计模式形成了一个完整的 Week 4，Command + Adapter 的组合更是看到了模式之间的协同关系。

*Python Craft Week 4 is complete — and seeing how Command + Adapter combine to build event-driven architectures shows the patterns are starting to compose.*

---

## 🎯 下周预告 / Next Week Preview

根据当前进度（Day 65，Expert Phase），下周（Day 66–71）预计内容：

*Based on current state (Day 65, Expert Phase), next week (Day 66–71) is expected to cover:*

**系统设计 (SysDesign Index: 53)：** 继续 Expert Phase 后期题目，可能包括更多分布式系统深度题（如 CRDT、一致性协议等）

**算法 (NeetCode Index: 54)：** 继续树遍历 Block（#10–15 题），进入 BST 验证、Kth Smallest、BST 序列化等题目，或开始新 Pattern Block

**Python Craft：** 设计模式 Week 5 或新主题（性能优化、测试模式等）

**AI：** 继续交替新闻速递和概念深度讲解

🏁 **65 天了。Expert Phase 的最后冲刺正在进行中。** 坚持住！

*65 days in. The Expert Phase final sprint is underway. Keep going!*
