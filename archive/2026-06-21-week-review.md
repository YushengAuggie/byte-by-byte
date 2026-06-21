📅 **Week in Review — Week 25（约10分钟阅读 / ~10 min read）**
📊 NeetCode: 59/150 · SysDesign: 58/40 · Behavioral: 58/40 · Frontend: 37/50 · AI: 29/30
🔥 7-day streak！

---

## 🗓️ 本周回顾 / This Week's Journey

*Days 66–71（2026年6月15日–20日）*

本周处于 **Expert 阶段**，五个内容日 + 一个复习日 + 周六深潜。每天密度都不低。

- **周一 Day 66**：自动补全系统设计 · Count Good Nodes（树DFS+路径状态）· 利益相关者管理 · 状态机 · AI生产监控三件套
- **周二 Day 67**：限流即服务 · Validate BST（双边界DFS）· 个人贡献vs团队赋能 · Repository 模式 · AI新闻（SpaceX算力问题/Anthropic政府叫停/马斯克诉讼再败）
- **周三 Day 68**：分布式追踪系统（Jaeger/Zipkin）· Kth Smallest in BST（中序遍历）· 季度OKR目标设定 · Python描述符协议 · 开源vs闭源LLM格局
- **周四 Day 69**：密钥管理系统（Vault）· 从前序+中序重建二叉树 · 为初级工程师发声 · 元类（Metaclass/ORM实战）· AI新闻（Shazeer加入OpenAI/Fable风波/Claude Design更新）
- **周五 Day 70**：复习日——回顾 Days 66–69 全部内容，Quick Quiz三道
- **周六 Day 71**：周六深潜——二叉树最大路径和（Hard，15分钟完整解析）

---

## 🧠 系统设计：本周要点 / System Design: Key Takeaways

本周啃了四道 Expert 级别的"基础设施类"系统设计题，有清晰的主线：

### 核心主题：可观测性 × 安全 × 流量控制

**1. 自动补全（Autocomplete）**
预计算是核心：不要在线维护 Trie，而是离线 Spark Job 算好 `prefix → top10` 存进 Redis。只存 ≤5 字符前缀，节省 99% 存储。两层缓存（浏览器 + Redis）保证 100ms SLA。

**2. 限流即服务（Rate Limiter as a Service）**
五种算法要会对比（令牌桶/漏桶/固定窗口/滑动日志/滑动计数器）——生产推荐**滑动窗口计数器 + Redis Pipeline 原子操作**。多维度限流（用户/IP/API Key）按最严维度拒绝。Redis 挂了要有 fail-open 降级。

**3. 分布式追踪（Jaeger/Zipkin）**
三大可观测性支柱：Logs（什么发生了）/ Metrics（发生了多少）/ Traces（为什么发生）。Span 的两个关键字段：`trace_id`（链路）+ `parent_span_id`（因果）。Tail-based 采样是生产首选——总保留 error trace 和 P99 慢 trace。

**4. 密钥管理（Vault）**
杀手级功能是 **Dynamic Secrets**：按需生成 DB 凭证，TTL 后自动吊销。不要用 Root Token。不要忘记开 Audit Log（不可变存储）。Vault 本身也要 HA（Raft 共识）。

### 三者的连接点
这四道题本质上都是**分布式系统的防御性基础设施**：Autocomplete 防延迟，Rate Limiter 防滥用，Tracing 防故障盲点，Vault 防凭证泄露。面试中被问到"你们团队如何保证系统可靠性"——这四个系统就是答案的骨架。

The four problems this week are all **defensive distributed infrastructure**: Autocomplete fights latency, Rate Limiter fights abuse, Tracing fights blind spots, Vault fights credential leaks. Together they form the backbone of a reliable production system.

---

## 💻 算法：模式总结 / Algorithms: Patterns Mastered

本周全部是**树遍历（Trees Block）**，Day 66–71 覆盖了第 10–15 题，完成了整个 Trees 模块！

### 本周四道核心题

| 题目 | 核心模式 | 关键洞察 |
|------|----------|----------|
| #1448 Count Good Nodes | 自顶向下传状态 | 路径最大值随递归下传，不是向上聚合 |
| #98 Validate BST | 双边界约束 | 不是比父子，而是比整个子树的合法范围 |
| #230 Kth Smallest in BST | 中序遍历 | BST 中序 = 天然升序，迭代版本可早退 |
| #105 Construct BT from Pre+Inorder | 重建树 | 前序首元素 = 根；中序找根位置切左右子树 |
| #124 Max Path Sum（深潜）| 局部+全局双视角 | 返回值=向上贡献（单支）；拱形=只更新全局max |

### 树 DFS 模板变体小结

```
基础模板：后序（left → right → 当前）
  → 求深度、路径和等聚合型问题

变体1：自顶向下传状态（top-down）
  → Count Good Nodes（路径最大值）
  → Validate BST（合法范围 min/max）

变体2：中序（left → 当前 → right）
  → BST 相关（Kth Smallest、验证有序性）

变体3：重建树（从数组而非树出发）
  → Construct from Preorder+Inorder
  → Serialize/Deserialize（下一块预习）

变体4：双角色（返回值 ≠ 局部最优）
  → Max Path Sum（最经典 Hard 模式）
```

**规律 / Pattern rule:** 需要路径上的累积信息 → 往下传参数。需要子树的聚合结果 → 从下往上返回。返回值无法涵盖"拱形"路径时 → 全局变量记录最优。

---

## 🗣️ 软技能：练习重点 / Soft Skills: What to Practice

本周四道行为题全部是 **Staff 级别**领导力场景，刚好构成一个完整的"影响力框架"：

| 场景 | 核心技能 | 一句话总结 |
|------|----------|-----------|
| 对项目方向提出反对 | 数据驱动说服 | 先私下对齐，再用量化数据公开提方案 |
| 个人贡献 vs 团队赋能 | 杠杆效应判断 | 20h onboarding → 400h 未来团队产能 |
| 季度目标设定与沟通 | OKR 自上而下+自下而上 | 说清"不做什么"和"做什么"同样重要 |
| 为初级工程师发声 | 技术验证 + 赋能 | 先自己验证想法，再用事实替好想法撑腰 |

### 哪道题需要多练？
**个人贡献 vs 团队赋能**这道题最难量化——面试时容易说成"我帮了他"而没有体现 Staff 视角。

练习重点：说出**具体的拆分决策**（什么由我做、什么教别人做）+ **量化杠杆**（多少小时投入换来多少产能）+ **系统改变**（不只是这次救场，而是改变了团队 review 文化）。

The hardest to articulate is **individual vs. team enablement** — easy to sound like "I helped someone" without the Staff-level framing. Practice: specific split decisions + quantified leverage + systemic culture change.

---

## 🐍 Python Craft：本周知识点 / Python Craft: Concepts to Lock In

本周 Python Craft 进入了高阶地带——从设计模式走向 Python 语言机制本身：

| 主题 | 核心概念 | 记忆锚点 |
|------|----------|---------|
| 状态机（State Machine）| 转换表作为单一事实来源 | `TRANSITIONS = {PENDING: {PAID, CANCELED}, ...}` |
| Repository 模式 | 业务逻辑 ↔ 数据源解耦 | `InMemoryUserRepository` 让测试不用真实DB |
| 描述符协议（Descriptor）| `__get__/__set__` 控制属性访问 | `@property` 是内置描述符；多类复用时写自定义描述符 |
| 元类（Metaclass）| 类的工厂，拦截类创建 | Django Model 字段自动注册的底层原理 |

### 速查自测
1. `@property` 和自定义描述符的选择依据？ → **一个类用 @property；多个类复用 → 自定义描述符**
2. 元类的 `__new__` 什么时候执行？ → **类被定义时**（不是实例化时）
3. Repository Pattern 最大的好处是什么？ → **业务逻辑可以用 InMemory 实现做单元测试，零依赖真实DB**
4. `State Machine` 比 if/elif 强在哪？ → **转换表是单一真实来源，非法转换立即报错**

---

## 🤖 AI：本周核心知识点 / AI: What Stuck

本周三个 AI 主题 + 两天新闻，信息量很大：

### 核心主题回顾

**AI in Production（Day 66）**
Guardrails（运行时护栏）+ Monitoring（可观测性）+ Cost Optimization（成本优化）。
成本优化四板斧：模型路由（简单问题用小模型）+ 语义缓存 + Prompt 缓存 + 上下文压缩。

**开源 vs 闭源 LLM（Day 68）**
决策框架：敏感数据 → 开源本地部署；最强推理 → 闭源；深度定制 → 开源微调；中文场景 → Qwen/DeepSeek。
据报道，模型路由策略可降低平均每次查询成本 37-46%。

**AI 新闻亮点（Days 67/69）**（据报道）

- **据报道** SpaceX Colossus 因站点间距超10英里+老旧网络基础设施，导致分布式训练延迟，转而将算力出租给 Anthropic 和 Google
- **据报道** 美国政府叫停 Anthropic 最新模型（Fable 5）发布，AI 监管正从"讨论框架"走向"实际干预"
- Noam Shazeer（Transformer 原作者之一、前 Gemini 联合负责人）**据报道**已加入 OpenAI
- Elon Musk 对 OpenAI 的诉讼**据报道**再次败诉

> ⚠️ 以上新闻条目均为 AI 新闻日内容，据报道标注。

### 最重要的一个洞察
**算力 ≠ AI 能力。** SpaceX 有世界顶级硬件，却因网络工程问题无法自用。AI 的瓶颈往往在**系统工程**，而不在参数量。这对后端工程师来说是个好消息——你的能力比你想的更稀缺。

**Compute ≠ AI capability.** SpaceX had world-class hardware but hit networking engineering limits. AI bottlenecks are often systems engineering, not parameter counts — good news for backend engineers.

---

## ⚠️ 需要复习的内容 / What to Review

### 最薄弱的区域

**1. 算法 — Max Path Sum 的双角色模型**
周六深潜内容信息密度最高。要确保能**无注释**写出完整解法：
- `max_sum = float('-inf')`（不是 0！）
- `left_gain = max(dfs(left), 0)`（截断负增益）
- 返回值 = 单支向上贡献；arch_path = 更新全局 max

**2. 系统设计 — Vault 的 Seal/Unseal 机制**
这个概念涉及 Shamir Key Shares，考点在于：Vault 重启为什么要重新解封？Auto-unseal（KMS）vs 手动解封的权衡是什么？

**3. Python Craft — 描述符查找优先级**
Data Descriptor（有 `__get__` + `__set__`）> Instance `__dict__` > Non-data Descriptor（只有 `__get__`）。这个优先级顺序容易忘，但面试偶尔会被问到。

**4. 软技能 — 季度 OKR 模板**
这类题需要随时能说出完整结构：向上对齐（QBR）→ 自下而上收集 → 草案（含 KR）→ 共识对齐（明确不做什么）→ 双周进度更新。能说出完整流程才算掌握。

---

## 🏆 本周亮点 / Win of the Week

**完成了完整的 Trees 模块！**

从 Day 57 开始的树遍历 Block 在本周正式收尾。15 道题覆盖了树 DFS 的全部四种变体：后序聚合、自顶向下传状态、中序 BST、双角色返回值。这是 NeetCode 150 最重要的板块之一，完整打完是实实在在的里程碑。

周六深潜的 Binary Tree Maximum Path Sum 是整个 Trees 板块的压轴题——Hard 难度，15 分钟完整解析，五道面试 Q&A。能把这道题讲清楚，Trees 板块就真正掌握了。

**The Trees block is complete!** 15 problems, all four DFS variants fully covered. Binary Tree Maximum Path Sum — the Hard capstone — was tackled with full depth in Saturday's deep dive. If you can explain this problem cold in an interview, the entire Trees block is yours.

---

## 🎯 下周预告 / Next Week Preview

根据当前进度，下周进入新的板块：

**算法（NeetCode 59/150）：**
Heaps / Priority Queue 模块开始——Find Median from Data Stream、Task Scheduler、Merge K Sorted Lists 等。

**系统设计（Index 58）：**
继续 Expert 阶段，即将进入更多实战系统设计变体。

**Python Craft（Index 21）：**
设计模式系列继续。可能进入 Python 并发或高级模式。

**AI（Index 29/30）：**
AI 主题即将完结本阶段，下周会是一个重要的收尾主题。

准备好迎接堆（Heap）的世界了吗？这是面试里第二常见的数据结构，也是很多"top K"类问题的标准武器。

*Get ready for Heaps — the second most common data structure in interviews, and the standard weapon for "top K" problems.*

---

*本 Week in Review 基于 2026-06-15 至 2026-06-20 归档内容生成。*
*Generated from archived content: June 15–20, 2026.*
