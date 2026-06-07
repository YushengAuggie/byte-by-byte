📅 **Week in Review — Week 23 (10 min read)**
📊 NeetCode: 50/150 · SysDesign: 49/40 · Behavioral: 49/40 · Frontend: 37/50 · AI: 24/30
🔥 60-day streak!

---

# 🗓️ 本周回顾 / This Week's Journey

本周完成了第 56–59 天（Day 56–59），外加周六深度阅读，横跨「Expert Phase」，每天内容密度极高。

This week covered Days 56–59 (Mon–Thu) plus a Saturday Deep Dive, all in the Expert Phase with high content density across every section.

- **周一 (Day 56)：** A/B 测试平台设计 · 二叉树最大深度 · 快速上手陌生代码库 · 策略模式 · 知识蒸馏
- **周二 (Day 57)：** 地理空间系统设计（Yelp/附近的人）· 二叉树直径 · 快速交付 vs. 做正确的平衡 · 观察者模式 · AI 新闻速递
- **周三 (Day 58)：** 在线代码编辑器设计（Replit）· 平衡二叉树 · 影响工程文化 · 工厂与抽象工厂模式 · RLAIF
- **周四 (Day 59)：** 协同编辑器设计（Google Docs）· Same Tree · 为不可见的工程投资发声 · Decorator 模式 · AI 新闻速递
- **周六深度：** OT 与 CRDT——协同编辑器的底层引擎 (18 分钟深读)

---

# 🧠 系统设计：本周要点 / System Design: Key Takeaways

本周四道设计题，话题迥异但内在联系深刻——从实验平台到地理索引到实时协作，围绕一个共同主线：**如何在规模下保持一致性**。

This week's four design problems span different domains but share a common thread: **maintaining consistency at scale**.

## Top 3 Concepts / 三大核心概念

### 1. 确定性哈希（Deterministic Hashing）——贯穿 A/B 测试
`Hash(userId + experiment_salt) % 100` 确保同一用户永远落入同一个实验桶，同时不同实验用不同 salt 防止桶的相关性。关键洞察：均匀分布 + 无状态 + 极快（<1μs）。

The key: `Hash(userId + experiment_salt) % 100` ensures same user always gets same variant. Different experiments use different salts to prevent cross-correlation. Uniform distribution, stateless, sub-microsecond.

### 2. Geohash + 邻格查询——地理空间检索
将地球表面编码为层级字符串，精度 6 ≈ 1.2km 格子。"附近"查询 = 中心格子 + 8 个邻格 IN 查询，解决了直接经纬度运算无法利用索引的问题。Redis GEORADIUS 底层是 52-bit Geohash，特别适合实时位置（Nearby Friends 场景）。

Geohash encodes the earth into hierarchical strings (precision 6 ≈ 1.2km cells). Nearby query = center cell + 8 neighbors. Redis GEORADIUS uses a 52-bit Geohash internally — ideal for real-time location like Nearby Friends.

### 3. OT vs CRDT——协同编辑的两种路径
**OT（操作变换）**：Google Docs 用的，服务端集中排序变换操作，实现复杂但成熟；**CRDT（无冲突复制数据类型）**：Figma/Linear/Notion 转向，数学上保证收敛，支持离线优先和 P2P，不需要中心化序列化。核心区别：OT 的服务器是"裁判"，CRDT 的数据结构本身是"合同"。

**OT** (Google Docs): server serializes all operations, complex correctness proofs. **CRDT** (Figma, Notion): the data structure mathematically guarantees convergence without central coordination. Key difference: OT's server is the "referee," CRDTs embed the merge rules in the data structure itself.

**三者如何连接：** A/B 测试的「分桶一致性」、Geohash 的「空间一致性」、OT/CRDT 的「操作一致性」——都是在分布式环境下回答同一个问题：**谁的版本是对的？**

---

# 💻 算法：本周模式总结 / Algorithms: Patterns Mastered

本周全力推进 **Trees 模式块**，完成了模板块第 2–5 题（#104, #543, #110, #100），建立了完整的树遍历思维框架。

This week pushed deep into the **Trees pattern block**, completing problems 2–5 (#104, #543, #110, #100) and building a complete tree DFS mental model.

## 模式：后序 DFS 模板变体 / Post-order DFS Template Variations

所有题目共享同一个骨架，关键差异只在**返回值语义**：

All problems share one skeleton; the only variation is **what dfs() returns**:

```python
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(left, right)
```

| 题目 | BASE_CASE | 返回值 | 全局变量 |
|------|-----------|--------|---------|
| #104 Max Depth | 0 | 深度 int | 无 |
| #543 Diameter | 0 | 深度 int | `res`（直径） |
| #110 Balanced | (0, True) | (高度, bool) 元组 | 无 |
| #100 Same Tree | True/False | bool | 无 |

### 关键洞察 / Key Insight per Problem

- **#104 Max Depth：** 最简单的后序 DFS，`max(left, right) + 1`，把空树当 0 处理。
- **#543 Diameter：** DFS 返回值（深度）和答案（直径）是两个不同概念——用 nonlocal 变量在每个节点"路过时"收集直径候选 `left + right`。
- **#110 Balanced Tree：** 返回元组是关键——O(n²) 朴素法 vs O(n) 一次遍历的区别。用哨兵值 `-1` 也是干净的替代方案。
- **#100 Same Tree：** 双树同步 DFS，参数变成两个节点，是下一题（#572 Subtree）的子问题。

**高频坑 / Common Trap：** Diameter 题里，很多人直接让 dfs 返回直径——错了。dfs 必须返回深度（供父节点计算），直径要靠外部变量收集。

---

# 🗣️ 软技能：本周练习重点 / Soft Skills: What to Practice

本周覆盖三个 Staff+ 高频场景，均属于「影响力」与「判断力」类别。

This week covered three high-frequency Staff+ scenarios, all in the "influence and judgment" category.

## 三个场景 / Scenarios Covered

### 1. 快速上手陌生代码库（Day 56）
**框架：三层理解法**——数据流优先（看日志监控，不看代码）→ 测试反向工程（测试是最诚实的文档）→ 关键路径深挖（失败场景优先）。建立「未知清单」批量同步而非持续打扰。

**Framework: 3-layer approach** — data flow first (logs/metrics, not code) → test reverse engineering (tests are the most honest docs) → critical paths (failure scenarios first). Maintain an "unknowns list" and batch your sync rather than interrupting constantly.

**需要练习 / Needs practice：** 能否准确描述「未知清单 + 批量对齐」的具体操作？能否量化你的理解进度（"Day 2 结束前我能描述主数据流"）？

### 2. 快速交付 vs. 做正确（Day 57）
**框架：风险加权决策**——量化快上线的技术风险（P概率 × 影响）→ 量化晚上线的业务损失 → 寻找折中方案（feature flag、降级策略）→ 主动向 stakeholder 说明并定好还债计划。

**Framework: Risk-weighted decision** — quantify risk of shipping fast (probability × impact) → quantify cost of delay → find the middle ground (feature flag, degraded mode) → proactively align stakeholders and commit to a debt repayment plan.

**需要练习 / Needs practice：** 你有没有一个真实案例可以代入这个框架？能否用"P30/P1"这种语言量化风险？

### 3. 为不可见的工程投资发声（Day 59）
**核心技巧：把技术问题翻译成业务语言**——"CI 慢"变成"每季度 390 小时工程损耗"；POC 先行证明可行；提议"一个 sprint 试验"降低感知风险。Staff+ 标志：改变在你停止推动后仍然持续。

**Core skill: translate technical problems into business language** — "CI is slow" → "390 engineer-hours wasted per quarter." POC first to prove feasibility. Propose "one sprint experiment" to lower perceived risk. Staff+ signal: the change persists after you stop pushing.

**需要练习 / Needs practice：** 选一项你做过的「不可见工程工作」，练习用 ROI 数据包装它的故事。

---

# 🎨 Python Craft：本周知识巩固 / Python Craft: Concepts to Lock In

本周完成了「设计模式 Week 3」的后半段，覆盖三个经典 GoF 模式。

This week finished the back half of Design Patterns Week 3, covering three classic GoF patterns.

## 本周三模式速记 / This Week's Three Patterns

### 策略模式（Strategy）
**核心：** 把「怎么做」和「做什么」分开，算法对象可在运行时替换。Python 中可以用 ABC + 子类（经典 OOP）或直接传函数（Protocol，更 Pythonic）。
*When to use: 多种可互换变体，变体数量会增长，或需要对每种变体独立测试。*

### 观察者模式（Observer）
**核心：** 发布者不知道谁在监听，订阅者不知道彼此存在，解耦广播。实战中注意两坑：取消订阅不彻底导致内存泄漏（用 weakref）；Observer 抛异常中断后续订阅者（用 try/except 包裹每个调用）。
*Real-world: Django signals, Python logging handlers, Node.js EventEmitter.*

### 工厂与抽象工厂（Factory & Abstract Factory）
**Factory：** 用字符串 key + 注册表替代散落的 if/elif，新增类型只需 `register()` 一行，调用方无需改动。
**Abstract Factory：** 产品有"家族"时（AWS 全套 vs GCP 全套），一键切换整个家族。
*Rule of thumb: 2-3 种固定实现用 if/else；会扩展时才上 Factory。*

### Decorator 模式（OOP 版，非 @decorator 语法）（Day 59）
**核心：** 动态给对象附加职责，N 种特性任意组合，不需要 2^N 个子类。Logger → TimestampDecorator(Logger) → LevelDecorator(TimestampDecorator(Logger))，每层只加一个职责。
*Python 标准库中的真实例子: `io.BufferedWriter(io.FileIO(...))`。*

**快速自测 / Quick self-check：**
- 策略 vs 观察者：一次用一个 vs 一次广播多个？
- 工厂 vs 抽象工厂：单类型创建 vs 整个产品家族创建？
- Decorator vs 继承：运行时组合 vs 编译时固定？

---

# 🤖 AI：本周知识点 / AI: What Stuck

## 核心概念 / Core Concepts

### 知识蒸馏（Knowledge Distillation）—— Day 56
大模型（Teacher）的输出"软标签"比真实标签包含更多信息——`[猫:0.9, 狗:0.09, 汽车:0.01]` 传递了「猫更像狗，而不像汽车」的相对相似性。蒸馏损失 = α × 软标签 KL 散度（乘以 T²）+ (1-α) × 真实标签交叉熵。温度 T > 1 让分布更平滑，信息量更大。

The Teacher's "soft labels" contain richer information than ground truth — `[cat:0.9, dog:0.09, car:0.01]` encodes relative similarity. Distillation loss = α × KL divergence on soft labels (scaled by T²) + (1-α) × cross-entropy on ground truth. Temperature T > 1 softens the distribution for richer signal.

### RLAIF（Reinforcement Learning from AI Feedback）—— Day 58
用强 AI（Claude/GPT-4）替代人类标注者，生成偏好数据（哪个回答更好），再训练奖励模型，再做 PPO。成本低、速度快、可规模化，但核心风险是「偏差级联」——AI Judge 的偏见会被放大进被训练的模型。Anthropic Constitutional AI 是 RLAIF 的早期实践。

Replace human labelers with a strong AI Judge that generates preference data at scale. Cheaper, faster, more scalable than RLHF — but the key risk is bias cascade: the Judge's biases get amplified into the trained model. Anthropic's Constitutional AI is an early RLAIF implementation.

## AI 新闻（据报道 / 据报道）
- **据报道**，微软 Build 2026 发布了 MAI 模型家族，旗舰 MAI-Thinking-1（35B 参数，256K 上下文），MAI-Code-1-Flash（5B 代码模型），以及企业级 Frontier Tuning 功能。
- **据报道**，GPT-5.5 Instant 已成为 ChatGPT 默认模型，主打 agentic 能力。
- **据报道**，Google Gemini 3.5 Flash 正式 GA，成为 Gemini 应用和 AI Search 默认模型，速度据称是上代旗舰的 4 倍。

本周 AI 新闻的底层主题：**从"谁最强"转向"谁最高效"**——MAI-Code-1-Flash 用 5B 参数深度集成 IDE，Gemini Flash 以 4× 速度媲美旗舰性能。效率竞争已经开始。

*The underlying theme: the race is shifting from "most capable" to "most efficient."*

---

# ⚠️ 需要复习的内容 / What to Review

## 最需要巩固的区域 / Weakest Areas

### 1. OT 的具体变换规则（高优先级）
知道 OT 的概念，但具体的 transform 函数逻辑（insert vs delete、并发顺序不同时如何正确调整 index）在面试中需要能白板推导。建议：手动推导周六深度阅读中的 3 个变换案例。

You understand the OT concept, but the specific `transform(op1, op2)` logic — how insert/delete operations adjust indices under different concurrency orderings — needs to be white-boardable. **Action:** Manually trace through the 3 transformation examples in the Saturday Deep Dive.

### 2. Geohash 边界问题的解法
知道"查询 9 个格子"解决边界，但能否在面试中快速写出代码并解释为什么这样够？建议：手写一次 `nearby_places` 函数并解释 precision 参数的选择逻辑。

You know the "query 9 cells" fix, but can you code it up and explain precision selection under pressure? **Action:** Write `nearby_places()` from scratch once, explain the precision tradeoff.

### 3. 软技能故事的具体量化
三个软技能场景的框架都清晰，但需要把「真实案例」代入模板，准备好数字（时间节省、影响范围、结果指标）。没有具体数字的 STAR 故事说服力弱 50%。

The frameworks are clear, but you need your own real stories with numbers. STAR answers without quantified results are 50% less convincing. **Action:** Pick 2 of this week's 3 questions and draft a full STAR answer with real data.

### 4. 树遍历模板的手速
模板理解了，但 #543 Diameter 的 nonlocal 变量用法和 #110 Balanced 的元组返回要能在 5 分钟内干净写出来，不犹豫。

The template is understood, but the `nonlocal` pattern for Diameter and the tuple-return for Balanced need to be muscle memory. **Action:** Time yourself — write both solutions from scratch, target < 5 min each.

---

# 🏆 本周亮点 / Win of the Week

**连续 60 天！这是一个真实的里程碑。**

第 60 天的连续打卡，不是靠热情，是靠系统。更重要的是：本周从「学了什么」到「理解了模式」——树遍历的四道题，第一次让你看到了模板的力量。当你能看到 #104, #543, #110, #100 共享同一个骨架时，算法学习就从"记题"进化成了"识别模式"。这才是复利开始的地方。

**60-day consecutive streak — a real milestone.**

Day 60 wasn't powered by excitement; it was powered by systems. More importantly: this week, the shift from "learned content" to "recognized patterns" happened. When you can see #104, #543, #110, and #100 all sharing the same DFS skeleton, algorithm learning transforms from "memorizing solutions" to "recognizing patterns." That's where compound learning begins.

---

# 🎯 下周预告 / Next Week Preview

基于当前进度，下周的内容将继续 Trees 模式块（题目 6-10/15），系统设计可能进入更多 Expert Phase 真实场景，Python Craft 将完成 Design Patterns 系列。

Based on current indices:

**算法 / Algorithms (Day 60+)：** 继续 Trees 模式块，预计覆盖 #572 Subtree of Another Tree、#235 LCA of BST 等题——都是本周 Same Tree 的直接延伸，重点是「双指针 DFS」和「BST 特殊性质」的利用。

**系统设计 / System Design：** Expert Phase 继续，可能涉及分布式系统的边缘场景（故障模式、数据一致性保证）。

**Python Craft：** 设计模式系列收尾，或进入新的 Python 内功主题。

**软技能 / Soft Skills：** 继续 Staff+ 级别场景，建议用下周时间把本周三个场景的 STAR 故事写成可以直接说出口的版本。

**AI：** 根据 aiTopicIndex，还剩约 6 个 AI 概念主题——重点关注更前沿的评估（Evaluation）和部署优化方向。

---

*Generated: 2026-06-07 (Week 23) | Days covered: 56–59 + Saturday Deep Dive*
