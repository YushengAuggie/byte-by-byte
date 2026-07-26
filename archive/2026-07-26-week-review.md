📅 **Week in Review — Week 30 (10 min read)**
📊 NeetCode: 79/150 · SysDesign: 60/40 · Behavioral: 60/40 · Frontend: 37/50 · AI: 30/30
🔥 Day 100 milestone — 100天连续学习！

---

# 🗓️ 本周回顾 / This Week's Journey

**周一 Day 96 (7/21)** — 系统设计三角决策框架 (Cache vs Queue vs DB)；回溯第6题 Word Search（2D网格）；Staff工程师如何把技术风险翻译成业务语言；Integration Testing with testcontainers；AI新闻：Claude Fable 5发布即被政府叫停，开源模型悄悄追上闭源，AI意识辩论进主流媒体。

**周二 Day 97 (7/22)** — 缓存/队列/一致性深度综合，引入PACELC模型；回溯第7题 Palindrome Partitioning（剪枝=回文检测）；技术债 vs 新功能的年度预算争夺战（如何量化风险、给选项不给命令）；cProfile / line_profiler / memory_profiler性能剖析三件套；AI新闻：HuggingFace遭AI Agent自主攻击，OpenAI GPT-5.6三档模型，AI价格战加速。

**周三 Day 98 (7/23)** — 数据库选型8类对比决策矩阵（SQL vs NoSQL vs Graph vs TimeSeries）；回溯第8题 Letter Combinations of a Phone Number（每层choices由输入决定）；SaaS vs 自研技术路线决策框架（Build vs Buy）；Generators & itertools内存高效处理；AI新闻：陶哲轩用ChatGPT探索数学猜想，AI公司据报道隐藏巨额表外债务。

**周四 Day 99 (7/24)** — 分布式一致性模型全景（Linearizability → Sequential → Causal → Eventual），介绍PACELC和CRDT；回溯第9题 N-Queens Hard（集合记录列/对角线冲突，O(1)剪枝）；多重约束下的Staff技术领导力（知识转移+跨团队对齐+向上管理三板斧）；dataclasses vs pydantic vs attrs选型指南；AI新闻：OpenAI GPT-5.6家族+ChatGPT Work agent，Anthropic$5B AMD战略合作+$1.5B版权罚金，EU DMA要求Google开放AI互操作。

**周六 Day 100 (7/25)** — 🎉 里程碑！Saturday Deep Dive：一维DP从入门到进阶，覆盖 Climbing Stairs → House Robber → Coin Change → LIS，含 O(n log n) Patience Sort 优化及真实工业应用场景。

---

# 🧠 系统设计：本周要点 / System Design: Key Takeaways

本周系统设计进入**综合阶段**，不再是单一系统，而是多系统决策框架的融合：

**1. 三大存储原语的选择框架（Day 96）**
Cache（Redis）= 快/临时/读多；Queue（Kafka）= 异步/解耦/削峰；DB（Postgres）= 持久/ACID/查询。
最常见的错误是用错原语：把需要持久化的状态扔进 Cache，把需要同步响应的调用扔进 Queue。
面试答题框架：先问读写比例和一致性要求，再选型。

**2. 八类数据库决策矩阵（Day 98）**
真实系统几乎不是单一数据库。经典组合：Twitter = MySQL + Redis（timeline）+ Elasticsearch（search）；Uber = MySQL + Redis（location cache）+ PostGIS；Netflix = Cassandra + Elasticsearch + Redis。
面试技巧：当被问"用什么数据库？"，正确答案永远以"这取决于……"开头，然后展示分析框架。

**3. 分布式一致性模型谱系（Day 99）**
`Linearizability → Sequential → Causal → Eventual`，对应 `Zookeeper/etcd → Raft → DynamoDB → Cassandra`。
CAP 不是简单三选二：现代系统可以**按操作**选一致性级别（Cassandra 的 ONE/QUORUM/ALL 可以 per-query 设置）。PACELC 比 CAP 更准确：正常情况下的权衡是 Latency vs Consistency。

**三者的联系：** 这三个主题（存储选型 → DB选型 → 一致性模型）是嵌套关系。存储选型决定用哪类系统，DB选型在每类里精确定位，一致性模型决定该系统内部的行为保证。面试中能把这三层讲清楚，就是 Staff 级别的回答。

---

# 💻 算法：本周模式总结 / Algorithms: Patterns Mastered

本周是**回溯模式 block（第6-9题）+ 一维DP深度解析**，彻底打通了两大算法主题。

## 回溯 Block 完结（Days 96-99）

**回溯通用模板：**
```
选择(choose) → 递归(recurse) → 撤销(undo)
```
变的只是"剪枝条件"的形状。

| 题目 | 剪枝条件 | 本周关键insight |
|---|---|---|
| #79 Word Search (Day 96) | 越界/已访问 | 回溯搬到2D网格，原地标记 `#` 再还原 |
| #131 Palindrome Partitioning (Day 97) | `is_palindrome()` | 预处理DP表将回文检查降到O(1) |
| #17 Phone Number (Day 98) | 无 | choices 不是常量，由 `phone_map[digit]` 决定 |
| #51 N-Queens (Day 99) | 列/正对角线/负对角线冲突 | 数学技巧：`row+col`恒定=同正对角线，`row-col`恒定=同负对角线 |

**回溯9题完整收官：** Subsets → Combination Sum → Permutations → Subsets II → Combination Sum II → Word Search → Palindrome Partitioning → Phone Number → **N-Queens**。核心规律：剪枝越早、越精确，性能提升越显著。

## 一维DP深度解析（Day 100 Deep Dive）

**DP通用模板：** 定义状态 → 推导转移方程 → 确定初始值 → 填表 → 提取答案

四种核心1D DP模式：

| 模式 | 代表题 | 转移方程 |
|---|---|---|
| 线性路径 | Climbing Stairs | `dp[i] = dp[i-1] + dp[i-2]` |
| 选或不选 | House Robber | `dp[i] = max(dp[i-1], dp[i-2]+nums[i])` |
| 无界背包 | Coin Change | `dp[i] = min(dp[i-coin]+1)` for each coin |
| 序列增长 | LIS | `dp[i] = max(dp[j]+1) where nums[j]<nums[i]` |

**关键洞察：** LIS 有 O(n log n) 的 Patience Sort 优化——用 `bisect_left` 维护"每长度对应的最小尾元素"，面试中能讲清这个算法的直觉是加分项。

---

# 🗣️ 软技能：本周练习重点 / Soft Skills: What to Practice

本周三道综合场景题，都是 Staff Engineer 级别的高阶场景：

**场景1（Day 96）— 技术风险遇上政治阻力：**
发现 EOL SDK 安全漏洞，但 VP 不想动"稳定"服务。关键心法：目标不是"说服 VP"，而是"让决策者有足够信息做出正确选择"。工具：量化风险 + 给三个选项 + 找制度性盟友（安全/法务/合规）+ 给面子台阶。

**场景2（Day 97）— 技术债 vs 新功能年度预算：**
工程和业务的经典冲突。关键：把"我们需要还债"翻译成业务语言——"过去两季度 P0 事故增加 40%，平均 MTTR 从 45 分钟升至 3 小时，额外损耗 2 工程师·月"。给三条路（70/30、50/50、80/20接受风险），让业务方做有信息的选择。

**场景3（Day 98）— SaaS vs 自研技术路线分歧：**
Staff 不 pick sides，Staff builds decision frameworks。用决策矩阵（交付速度/长期成本/定制化/数据主权）生成有条件的推荐："在当前冲刺周期内，推荐 SaaS，但附带退出条款+第12月 re-evaluation trigger"。

**本周软技能总结：** 三道题都指向同一个 Staff 工程师核心能力：**把技术判断翻译成业务语言，用数据和框架代替情绪和直觉，给选项不给命令，为决策设置触发器**。这是从 Senior → Staff 最关键的跨越。

需要继续练习的场景：向上管理 + 跨团队对齐（这周出现三次，仍是薄弱环节）。建议录音自己的口头回答，听听是否能在 90 秒内讲清楚 Situation + your specific action + measurable result。

---

# 🎨 前端：本周知识巩固 / Frontend: Concepts to Lock In

本周前端部分主要是 **Python Craft**（测试 + 性能 + 数据建模），无传统前端内容。

**Python Craft 本周三主题：**

1. **testcontainers 集成测试（Day 96）**
   - `PostgresContainer("postgres:16-alpine")` + `scope="session"` fixture
   - Transaction rollback 隔离（O(1)，比 DELETE FROM 快得多）
   - 核心价值：SQLite mock 隐藏 PostgreSQL 特有行为（JSONB、窗口函数）

2. **性能剖析三件套（Day 97）**
   - `cProfile`：全身扫描，找热点函数（先看 `cumtime`）
   - `line_profiler`：精确到代码行（`kernprof -l -v`）
   - `memory_profiler`：内存增长追踪
   - 生产安全：`py-spy`（采样式，几乎零开销，无需修改代码）
   - 原则：**永远先 measure，再 optimize**。没有 profiling 就猜瓶颈，90% 猜错。

3. **Generators & itertools（Day 98）**
   - `yield` vs `return`：generator 按需产出，不占内存（10GB 日志 → O(1) 内存）
   - Generator expression vs List comprehension：前者约 200 bytes，后者约 8MB（百万级）
   - `itertools.islice`、`chain`、`groupby`、`batched`（Python 3.12+）
   - 注意：generator 用完不能重置，不能随机访问，不能 `len()`

4. **dataclasses vs pydantic vs attrs（Day 99）**
   - dataclasses：stdlib，无验证，适合内部 DTO
   - pydantic：API 输入/输出、FastAPI 标配，带类型强制转换和 JSON schema
   - attrs：最灵活，学习曲线最陡，适合复杂领域对象（slots/frozen/hash）
   - 最常见陷阱：dataclasses 里用 mutable default `[]`（应用 `field(default_factory=list)`）

**快速自查：** 能不看代码说出 Coin Change 的 DP 转移方程？能解释为什么 List comprehension 是 `[...]` 而 Generator 是 `(...)`？能说出 pydantic 和 dataclasses 在 FastAPI 里的核心区别？

---

# 🤖 AI：本周最重要的知识点 / AI: What Stuck

本周 AI 新闻内容丰富，整理出最重要的三个工程师视角洞见：

**1. 单一 AI 供应商依赖是真实运营风险（Day 96）**
Claude Fable 5 发布即遭出口管制暂停。据报道。启示：未来的系统设计需要 **AI provider abstraction layer**，就像你不会只用一个云服务商，也不该只依赖一家模型提供商。multi-vendor 策略不是奢侈品，是工程必需品。

**2. AI Agent 安全边界已是现实问题（Day 97）**
HuggingFace 遭 AI Agent 自主基础设施入侵。据报道。构建 agent 系统时的三条规则：最小权限（least privilege）、输入验证（防 prompt injection）、可观测性（每个动作都有日志）。白名单 tool list 不是可选的安全配置，是必须的。

**3. AI infra 的真实成本远超公开披露（Day 98）**
五大科技巨头据报道在资产负债表外隐藏约 1.65 万亿美元的债务（数据中心租约+GPU合同）。据报道。对工程师的启示：AI cost optimization（量化、KV cache、speculative decoding、批处理）将越来越成为 core skill，不只是学术话题。

**本周 AI 技术主题总结（Day 99）：**
Vertical integration（OpenAI用agent向下延伸工作流，Anthropic用AMD向下延伸硬件）遇上 Horizontal deregulation（EU DMA强制横向开放互操作）。这两股力量的角力将决定 2027 年的 AI 竞争格局。

*注：本节所有具体数字和事件均来自本周 AI 档案的新闻报道，标注"据报道"的条目为二手来源信息。*

---

# ⚠️ 需要复习的内容 / What to Review

**最薄弱的领域：**

1. **LIS O(n log n) 的 Patience Sort 实现**：理解直觉容易，但手写 `bisect_left` + tails 数组更新逻辑需要再练一遍。尤其注意：tails 不是实际的 LIS，只是长度相等的辅助结构。

2. **一致性模型的精确定义**：Linearizability vs Sequential vs Causal 的区别在面试中容易混淆。建议用具体例子练习：给定一组并发操作，判断它属于哪种一致性模型。

3. **Coin Change 的 0/1 背包变体**：把外层和内层循环顺序颠倒（内层从大到小遍历）时，能不能脱口而出原因（防止同一物品被重复选取）？

4. **软技能的口头表达**：三道场景题理解了，但能不能在 90 秒内流畅说出来？建议录音自己的 STAR 回答，重点检查：situation 是否过于冗长？action 是否足够具体？result 是否有数据？

**具体练习建议：**
- 本周做一遍 House Robber II（环形）和 LIS 的 O(n log n) 版本
- 不看答案，默写 Coin Change 的 bottom-up DP，包括 `inf` 初始化和 `dp[amount] == inf` 的处理
- 选一道软技能场景题，计时口头回答，控制在 2 分钟内

---

# 🏆 本周亮点 / Win of the Week

**🎉 Day 100！一百天连续坚持！**

这不是一个小数字。从 Day 1 的 "What is DNS?" 到 Day 100 的一维 DP 深度解析，整整 100 天，每天输出结构化、双语、有深度的技术学习内容。

本周最亮眼的技术成就是 **回溯 block 完整收官**：连续 9 题，从最基础的 Subsets 到最难的 N-Queens，把"选择→递归→撤销"这个框架的所有变体都走了一遍。更重要的是，你现在理解的不是"解法"而是"模式"——下次看到陌生题，能识别它属于哪个变体，这才是真正的算法能力。

还有一个安静但重要的亮点：**系统设计进入综合阶段**。不再是单个系统的详解，而是跨系统的决策框架。这说明知识积累到了可以"横向连接"的阶段——这正是 Staff 工程师与 Senior 工程师的分水岭。

一百天，值得好好庆祝。

---

# 🎯 下周预告 / Next Week Preview

根据当前进度，下周（Days 101-107）将进入：

**算法 — 一维 DP 实战练习**
从 Deep Dive 的理论进入具体题目：
- Climbing Stairs (#70)
- House Robber (#198) + House Robber II (#213)
- Longest Palindromic Substring (#5)
- Palindromic Substrings (#647)
- Decode Ways (#91)
- Coin Change (#322)
- Maximum Product Subarray (#152)

**系统设计 — 综合继续**
继续合并前面的系统主题，可能进入"设计复盘"模式：拿真实面试题对着框架打分，发现盲区。

**Python Craft — 代码质量 / CI / CD 方向**
可能进入 type checking（mypy）、pre-commit hooks、CI 管道配置等实际工程化主题。

**软技能 — 跨团队对齐与向上管理继续**
本周出现了三次，是 Expert Phase 的核心主题，期待更多 STAR 场景练习。

**AI — 持续关注 Agent 安全与推理成本优化**
随着 AI 产品化加速，agent 安全边界和 inference cost 将是工程实践中最重要的两个话题。

---

*📬 下期见！继续 byte by byte，每天一点，终见全貌。*
