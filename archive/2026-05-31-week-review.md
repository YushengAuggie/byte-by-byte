📅 **Week in Review — Week 12 (10 min read)**
📊 NeetCode: 46/150 · SysDesign: 45/40 · Behavioral: 45/40 · Frontend: 37/50 · AI: 22/30
🔥 54-day streak!

---

## 🗓️ This Week's Journey / 本周回顾

**周一 Mon 5/26 (Day 51):** 分布式文件系统 HDFS/GFS + LRU Cache（链表大招）+ 服务下线迁移 + WSGI/ASGI + AI 新闻（政府/军事 AI 军备竞赛）
**周二 Tue 5/27 (Day 52):** 时序数据库 InfluxDB/TSM + 合并 K 个链表（堆登场）+ 架构分歧解决 + concurrent.futures + AI 评估体系
**周三 Wed 5/28 (Day 53):** Feature Flag 系统 LaunchDarkly + 链表 K 组翻转（模式压轴！）+ 从重大失误中复盘 + Producer-Consumer + AI 新闻（Agentic AI、AI 安全、合成数据法律问题）
**周四 Thu 5/29 (Day 54):** 多区域 Active-Active 系统 + 翻转二叉树（树模式启航）+ 绩效不佳高级工程师反馈 + GIL 深度剖析 + 合成数据
**周五 Fri 5/30 (Day 55):** 复习日 — Day 51–54 Quiz + Saturday Deep Dive：合并 K 个链表完整精讲（18 min）

---

## 🧠 System Design: Key Takeaways / 系统设计要点

### 三大高级系统 + 一个 Meta 主题

**1. 分布式存储的"控制/数据分离"原则**
HDFS/GFS 的精髓：NameNode 只存元数据（文件→chunk 映射），所有实际数据在 Client ↔ ChunkServer 之间直接流动，Master 永远不是数据瓶颈。时序数据库的列式存储 + TSM Tree 同理——写入路径与查询路径天然分离，append-only 设计让时间有序性成为性能优势而非负担。

**2. Feature Flag 的本质是运行时配置 + 渐进发布**
SDK 本地缓存全量规则（评估 <1ms），SSE 推送增量更新。`hash(userId + flagKey) % 100` 而非 `random()`——保证同一用户在多次请求间看到一致的实验结果。Tag cardinality 爆炸是最常踩的坑。

**3. Active-Active = 写冲突是必须回答的问题**
本周最复杂的系统设计。关键不是架构图，是数据分区策略：按 user_id 路由到固定区域写（消除冲突）vs. LWW（简单但可能丢数据）vs. CRDT（自动合并，适合计数器）。面试时不说 consistency model 会直接失分。

**连接点：** 这三个系统都体现了同一个设计哲学——**把复杂性限制在有界范围内**（NameNode 只管元数据、Flag 评估只在本地、写操作路由到固定区域）。

---

**1. "Control plane / Data plane separation" — the HDFS/GFS principle**
NameNode holds only metadata; actual data flows directly between Client and ChunkServers. Time-series TSM Tree follows the same pattern — append-only writes naturally leverage time ordering as a performance asset.

**2. Feature flags = runtime config + progressive rollout**
Local SDK cache for <1ms evaluation, SSE for incremental updates. `hash(userId + flagKey) % 100` ensures consistent experiment bucketing across requests. Tag cardinality explosion is the most common production pitfall.

**3. Active-Active forces you to answer: "how do we handle write conflicts?"**
The architecture diagram is table stakes. The real interview is the data partition strategy: route writes by user_id to a fixed region (eliminates conflicts), LWW (simple, risks data loss), CRDT (auto-merge, good for counters). Failing to mention consistency model = automatic point deduction.

---

## 💻 Algorithms: Patterns Mastered / 算法模式总结

### ✅ 链表技巧模式 — 完结！(11/11)

本周完成了链表模块的最后三题，也是最难的三题：

| 题目 | 核心技巧 | 关键洞察 |
|---|---|---|
| #146 LRU Cache | 双向链表 + HashMap | O(1) 全靠"知道前驱节点"→ 必须双向 |
| #23 Merge K Lists | 最小堆 | 每次只关心 K 个队头，堆大小恒为 K |
| #25 Reverse K-Group | 递归/迭代 + 探路指针 | Hard 题 = #206 反转 + #141 快指针探路，组合而已 |

**周末 Deep Dive：Merge K Sorted Lists（18 min）**
暴力 → 顺序合并 → 最小堆 → 分治，四种解法从 O(N log N) 到 O(N log K)。最重要的实现细节：heap 存 `(val, index, node)` 三元组，`index` 做 tie-breaker（ListNode 不可直接比较）。

### 🌳 树遍历模式 — 刚启动！
Day 54 第一题 #226 Invert Binary Tree 开了新模式。核心模板已建立：
```python
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```
几乎所有树题都是这个框架，`COMBINE` 的定义决定一切。

---

### ✅ Linked List Pattern — Complete! (11/11)

The week finished the last and hardest three linked list problems. Key insight crystallized: **Hard linked list problems are compositions of Easy techniques** — K-Group Reversal is literally #206 Reverse + fast pointer scouting. Merge K Lists is #21 Merge Two × heap abstraction.

### 🌳 Tree Traversal Pattern — Just Started!
Day 54 kicked off with #226 Invert Binary Tree — the template-setter for the next 15 problems. `COMBINE` semantics vary (swap children / add depths / track global max) but the recursive skeleton never changes.

---

## 🗣️ Soft Skills: What to Practice / 软技能练习重点

本周覆盖了三个高频 Senior/Staff 场景，难度递进：

**1. 服务下线迁移（Day 51）**
关键词：Strangler Fig Pattern、渐进式关闭（freeze → warning → throttle → shutdown）、instrumentation 发现未知依赖。练习时要能说出"发现了 2 个团队的 legacy batch job 还在调用"这种细节——面试官会追问"你怎么发现的"。

**2. 架构分歧解决（Day 52）**
模板：倾听 → 找合理之处 → 数据+场景论证 → 折中方案 → 写下 ADR。加分项：提出 proof of concept 代替口头争辩。⚠️ 最容易犯的错：直接进入"我来说服你"模式，跳过"倾听"步骤。

**3. 重大失误复盘（Day 53）**
区分三个层次——普通工程师修了 bug，Senior 改善了团队流程，Staff 改变了组织的工作方式。必须量化：47 分钟 incident、15% 基础设施成本节省。**No numbers = not credible.**

**4. 绩效不佳高级工程师反馈（Day 54）**
最难的软技能题。记住 SBI 模型（Situation / Behavior / Impact），先诊断问题类型（能力 / 动力 / 外部阻碍），解法完全不同。

**🎯 最需要练习的：** 题目 #2 和 #4——很多人在这两题上不是没有内容，而是讲成了"我说服了对方/我批评了对方"的单方叙事，缺少合作感。

---

**Three high-frequency Senior/Staff scenarios, escalating difficulty:**

1. **Service deprecation**: The "strangler fig" and phased shutdown pattern. Practice saying *how you discovered unknown callers* — interviewers always probe this.
2. **Architecture conflict**: The formula is listen → find merit → data-backed tradeoff analysis → compromise → ADR. The failure mode: skipping the "listen" step.
3. **Recovering from a major mistake**: Quantify everything. 47-minute incident, 15% infra cost savings. No numbers = not credible. Staff-level = you changed the org's process, not just your own behavior.
4. **Feedback to underperforming senior engineers**: Diagnose first (skill gap? motivation? blocked?). Use SBI model. The failure mode: delivering a verdict before understanding the cause.

---

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固

本周没有专属 Frontend 内容（Day 46+ 切换为 Python Craft 模块），但进度显示 **frontendIndex: 37/50**，上周已覆盖：Next.js App Router / Data Fetching / API Routes / Middleware & Auth。

**快速自检（Next.js 重点）：**
- [ ] Server Component vs Client Component — 各自什么时候用？
- [ ] `use cache` / `noStore()` — 默认缓存行为是什么？
- [ ] Server Actions vs API Routes — 表单场景选哪个？
- [ ] Middleware 的执行顺序和 `matcher` 配置

*下周 Frontend 模块（frontendIndex 38+）预计涵盖 Next.js 优化/部署相关内容。*

---

*No new Frontend content this week (switched to Python Craft module at Day 46+). Quick self-check on last week's Next.js content: Server vs Client Components, caching behavior, Server Actions vs API Routes, middleware matcher config.*

---

## 🤖 AI: What Stuck / AI 知识点

本周三条 AI 新闻 + 两个概念深讲：

**概念：AI 评估体系（Day 52）**
三层框架：基准测试（能力基线）→ 离线评估（LLM-as-Judge + 自动指标）→ 生产监控（真实用户反馈）。关键：基准污染问题——MMLU 已经被"背"熟，Humanity's Last Exam（最优模型仅 ~45%）是目前最可信的公开基准。

**概念：合成数据（Day 54）**
模型蒸馏（Teacher→Student）+ 自我蒸馏（生成→验证→过滤→再训练）是 o1/o3 背后的关键。核心前提：需要可靠的**验证器**。模型崩溃（Model Collapse）是主要风险——连续在自己生成的数据上训练导致输出同质化。

**新闻亮点（含"据报道"标注）：**
- 据报道，白宫申请 90 亿美元为情报机构购买 Nvidia Grace Blackwell 芯片（算力 = 国力）
- 据报道，Anthropic Claude 和 GPT-5.5 通过英国 AI 安全研究所的 32 步网络攻击模拟，前沿攻击能力据报道每 4 个月翻一番
- Microsoft Agent 365 + "computer use" 标志着 Agentic AI 的企业化落地，但微软研究员同时警告多步骤工作流仍不可靠

**🎯 最重要的一条：** 合成数据 + 自动验证器的组合是近两年 AI 能力跃升的核心机制。理解这个，才能真正理解为什么 reasoning models（o1/o3/Gemini 2 thinking）如此强大。

---

**Two concept deep-dives this week:**

**AI Evaluation (Day 52):** Three-layer framework: benchmarks → offline eval (LLM-as-Judge) → production monitoring. Key: benchmark contamination is real — MMLU is memorized. Humanity's Last Exam (~45% for best models) is the current gold standard for uncheatable difficulty.

**Synthetic Data (Day 54):** Model distillation + self-play (generate → verify → filter → retrain) is the engine behind o1/o3's capabilities. The critical requirement: a reliable verifier. Model collapse is the main risk — generational quality degradation when training only on self-generated data.

**News highlights (reported claims):** 据报道 $9B White House chip request for spy agencies; 据报道 frontier models passed 32-step cyberattack simulations; Microsoft's Agent 365 marks enterprise agentic AI deployment (with their own researchers cautioning multi-step workflows remain unreliable).

---

## ⚠️ What to Review / 需要复习的内容

**最弱的几个点 / Weakest areas:**

1. **Active-Active 系统中的写冲突处理** — 能说出 LWW / Vector Clock / CRDT / Transaction Routing 的名字，但面试时能否快速判断"这个场景该用哪种"？多练判断题。

2. **LRU Cache 实现细节** — dummy head/tail 的指针操作容易写乱。建议徒手写一遍 `_remove` 和 `_insert_front`，不要看答案。特别注意：put 时如果 key 已存在，先 remove 再 insert，然后才检查 capacity。

3. **时序数据库的 Tag Cardinality 问题** — 知道规则（Tags 要低基数），但面试中能否主动提出并解释为什么？倒排索引 + 高基数 = 无限膨胀，这个因果链要能脱口而出。

4. **软技能 #4：绩效反馈** — 练习说清楚"诊断阶段"。在 STAR 的 Action 部分，很多人直接跳到"我怎么给反馈"，但真正的 Senior 会先花 1-2 周观察和了解背景。

5. **树遍历模式刚开始** — #226 Invert Binary Tree 是第一题，`COMBINE` 语义简单（swap）。下周的 #104 Maximum Depth、#543 Diameter 会要求 `COMBINE` 返回数值，需要建立直觉。

---

**Five specific gaps to address:**

1. **Active-Active write conflict selection** — Can you quickly pick LWW vs CRDT vs transaction routing for a given scenario? Practice decision-tree reasoning, not just listing options.
2. **LRU Cache implementation** — Write `_remove` and `_insert_front` from scratch, no reference. Pay attention to: existing key → remove first, then insert, *then* check capacity overflow order.
3. **TSDB tag cardinality** — The cause chain: inverted index + high-cardinality tags = unbounded index growth. This should be a reflex, not a recalled fact.
4. **Soft skill #4 — underperformer feedback** — Most people skip the diagnosis phase. Before any feedback, 1-2 weeks of observation + 1:1 context-gathering should be explicit in your STAR answer.
5. **Tree traversal pattern just started** — Build intuition for `COMBINE` return value semantics before next week's harder problems.

---

## 🏆 Win of the Week / 本周亮点

**链表模式 11/11 完成！**

这是整个 NeetCode 150 中公认最容易出 Bug 的模式之一。从第一天的 Reverse Linked List 到本周的 LRU Cache、Merge K Lists、K-Group Reversal——11 题走下来，快慢指针、双向链表 + 哈希表、堆辅助、分治，把链表的所有核心武器都走了一遍。

更重要的是建立了一个**元认知**：Hard 链表题不是全新的问题，是 Easy/Medium 技巧的组合。这个认知在面试中价值连城——看到一道 Hard 题，第一反应不是"我不会"，而是"这是哪几个我会的东西拼起来的？"

---

**The Linked List pattern is done — all 11 problems.**

More than the problems themselves, the meta-skill crystallized this week: Hard linked list problems are compositions of techniques you already know. K-Group Reversal = #206 Reverse + fast pointer scouting. Merge K Lists = two-way merge × heap abstraction. This reframe — "what known pieces is this made of?" — is worth more in an interview room than any single algorithm.

---

## 🎯 Next Week Preview / 下周预告

**Based on current indices / 基于当前进度：**

📊 **Day 56-61 (Week 13)** — Expert Phase 继续

- **算法：** 树遍历模式（Tree Traversal）深入 — 预计覆盖 #104 Maximum Depth、#543 Diameter of Binary Tree、#110 Balanced Binary Tree、#100 Same Tree、#572 Subtree
- **系统设计：** systemDesignIndex: 45，下周题目预计进入 Expert 阶段后期，可能涵盖 CDN 设计、分布式锁、或 Streaming 系统
- **Python Craft：** pythonCraftIndex: 8，下一个主题预计是 asyncio 深入（gather / Semaphore / TaskGroup / 实战模式）
- **AI：** aiTopicIndex: 22，下一个概念主题预计是 MoE 深度、Inference 优化续集，或新一轮 AI 新闻

**重点关注：** 树遍历模式的 `COMBINE` 语义随难度变化——从简单的 swap/depth int 到需要维护全局变量的路径最大值（#124 Hard）。建议每道题做完后在脑子里默背一遍模板，看 COMBINE 变化了什么。

---

**Week 13 preview:**

- **Algorithms:** Tree Traversal deep dive — #104 Max Depth, #543 Diameter, #110 Balanced Tree, #100 Same Tree, #572 Subtree. Watch `COMBINE` semantics evolve from simple swaps to global-variable tracking.
- **System Design:** Expert phase continues — likely CDN, distributed lock, or streaming system territory.
- **Python Craft:** Next up: asyncio deep dive (gather, Semaphore, TaskGroup, production patterns).
- **AI:** aiTopicIndex at 22 — next concept topic likely MoE deep-dive or inference optimization sequel.

**Focus:** The tree traversal template stays constant; `COMBINE` is the variable. After each problem, mentally replay: "what did COMBINE return, and why?" That's the muscle to build this week.
