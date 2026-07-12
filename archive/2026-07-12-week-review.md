📅 **Week in Review — Week 29 (10 min read)**
📊 NeetCode: 71/150 · SysDesign: 60/40 · Behavioral: 60/40 · Frontend: 37/50 · AI: 30/30
🔥 Day 88 — Expert Phase，继续前进！

---

## 🗓️ 本周回顾 / This Week's Journey

**一句话总结每天：**

- **Day 84（周一 7/7）** — 系统设计综合：一致性模型全景对比；算法：Task Scheduler（堆+冷却队列）；软技能：技术债×截止日期×团队冲突三角困境；Python：依赖注入（无框架）；AI：OpenAI Jalapeño 芯片 + 联合国 AI 治理 + 开源 LLM 追赶
- **Day 85（周二 7/8）** — 复习日，回顾 Day 81–84：堆模式、断路器、依赖注入、一致性模型
- **Day 86（周三 7/9）** — 系统设计综合：五维决策框架 + 七步面试法；算法：Design Twitter（多路归并堆）；软技能：Staff工程师乘数效应框架；Python：pydantic-settings + 12-Factor配置管理；AI：Grok 4.5、伊利诺伊AI安全法、开源LLM格局
- **Day 87（周四 7/10）** — 系统设计综合：事件驱动 vs 请求-响应深度对比；算法：Find Median from Data Stream（双堆，Hard 收官！）；软技能：Force Multiplier 乘数框架；Python：生产级日志 structlog + Correlation IDs；AI：GPT-Live 全双工语音 + Gemma 4 生态
- **Day 88（周六 7/11）** — Saturday Deep Dive：回溯算法完全指南（Subsets→N-Queens）；系统设计/软技能/AI 均将回溯思维迁移到各自领域；Python：Feature Flags（简单实现到 LaunchDarkly）

---

## 🧠 系统设计：本周关键要点 / System Design: Key Takeaways

**本周是综合模式（Synthesis Mode）——60 个主题全部覆盖完毕，进入跨主题融会贯通。**

**要点一：一致性模型横向对比（Day 84）**

生产环境常见的五种系统的一致性模型各不相同：PostgreSQL 主库是强一致，副本是最终一致（延迟~ms）；Redis Cluster 同一 slot 内强一致，跨 slot 无保证；Kafka 是 at-least-once；Elasticsearch 近实时（约1秒延迟）；DynamoDB 默认最终一致、强一致需额外开销（2x RCU）。**最危险的 bug 不是单系统出错，而是在跨越一致性边界时假设了不存在的保证。**

Staff Engineer 应对框架：CLASSIFY（数据一致性等级）→ SCOPE（哪些操作需要强一致）→ TRADEOFF（强一致的延迟/吞吐/可用性代价）→ MONITOR（如何检测不一致）。

**要点二：五维决策框架（Day 86）**

面对任何系统设计题，五个维度决定技术选型：读写比（Read/Write Ratio）、一致性要求（Consistency）、规模量级（Scale）、延迟SLA、失败模式。面试七步法：澄清需求(2min) → 估算规模(2min) → 高层设计(5min) → 数据模型(3min) → 深入细节(8min) → 扩展优化(3min) → 权衡总结(2min)。

**要点三：事件驱动 vs 请求-响应（Day 87）**

决策框架：用户需要立即知道结果 → 同步；操作是副作用而非核心 → 异步；需要扇出给多个下游 → 事件驱动；需要削峰 → 消息队列。真实系统是两种架构共存：前端请求走同步低延迟路径，副作用（审计日志、分析、通知、缓存失效）走 Kafka 异步路径。

**连接三个主题：** 一致性选型 → 决定架构模式（强一致必须同步）→ 影响事件驱动的适用边界。

---

## 💻 算法：模式总结 / Algorithms: Patterns Mastered

**本周完成了「堆/优先队列」7题全块，并开启了「回溯」块（9题）。**

**堆模式收官（7/7）：**

| 题目 | 技巧 | 关键点 |
|------|------|--------|
| #621 Task Scheduler（Day 84） | max-heap + wait deque | 冷却时间 = 时间轴上的"等待队列"；贪心选最高频任务最小化 idle |
| #355 Design Twitter（Day 86） | 多路归并 + min-heap | heap 存 (时间戳, tweetId, userId, 指针)，跨多个有序列表合并取 top-10 |
| **#295 Find Median（Day 87）** | **双堆平衡** | left max-heap + right min-heap；维护不变量：两堆大小差 ≤ 1，left最大值 ≤ right最小值 |

**最重要的洞察：** 堆问题的复杂度随"维护的堆数量"递增——单堆追踪top-k，双堆维护中位数，多堆合并多路数据流。#295 是这个模式的 Hard 收官，体现了"两个平衡的数据结构 + 精确的不变量"的设计思维。

**回溯块开启（1/9，Day 88）：**

通用模板：`选择 → 递归 → 撤销`。从 Subsets 起步——每个决策树节点都是合法答案，`start` 参数防重复。

---

## 🗣️ 软技能：练习重点 / Soft Skills: What to Practice

**本周三个高价值综合场景：**

**场景1：三角困境（Day 84）** — 同时面对硬 deadline + 技术债 + 团队分歧时，关键不是"选哪个技术方案"，而是建立可信的决策过程：量化风险（spike两天）→ 用 Pre-mortem 把争论转化为数据 → 带 checkpoint 的有时间边界的决定 → 1-pager 向上对齐（透明度，而非转移决策）。

**场景2：Staff 乘数效应框架（Day 86）** — 四种乘数：技术方向、人员赋能、流程改善、跨团队协调。面试时用 STAR+S 框架，加第五步 Systemic Impact：这个解决方案现在如何**持续**产生价值？信号词升级：把"我做了" → "我推动了/赋能了/建立了"；结果要包括"其他团队后来也..."。

**场景3：优雅回溯（Day 88）** — 面对重大路线调整时，框架化为"信息积累后的理性决策"：快速 POC 验证优化是否可行 → 记录6周学到了什么 → 修订方案纳入新约束 → 对 stakeholder 说"我们找到了更好的路径，现在转向能节省后面3个月"。

**哪个最需要练习：** 场景2 的 STAR+S 格式——大多数人的故事停在 Result，很少延伸到 Systemic Impact。准备2-3个有"组织级别扩散"的故事。

---

## 🎨 前端 / Python Craft：巩固重点

**本周 Python Craft 聚焦在生产工程实践：**

- **依赖注入（Day 84）** — 三种无框架 DI 模式：构造函数注入（最常用）、手写容器（中型项目）、函数式DI（FastAPI 风格）。Python Protocol 让接口定义不需要继承。核心价值：可测试性（swap real DB for fake）。
- **pydantic-settings（Day 86）** — 12-Factor 第三条：配置存在环境变量中。pydantic-settings 提供类型验证+自动强制转换，`@lru_cache` 实现单例。关键规则：`.env` 文件绝不提交 Git。
- **structlog + Correlation ID（Day 87）** — 结构化日志 = 可查询 + 可聚合；Correlation ID 用 `ContextVar` 实现线程/异步安全，在 middleware 层注入，跨服务追踪的基础设施。
- **Feature Flags（Day 88）** — 四个层次：dict（最简）→ 环境变量 → hash-based 百分比 rollout → LaunchDarkly。hash 保证同一用户每次落到同一 bucket（不会闪烁）。生产注意：定期清理旧 flag，避免 flag debt。

**快速自查：** 在 FastAPI 项目中，如何注入一个 fake 数据库用于单元测试？（提示：构造函数注入 + Depends override）

---

## 🤖 AI：关键要点 / AI: What Stuck

**本周最重要的技术洞察：AI 系统的分层架构**

Day 87 GPT-Live 的架构揭示了一个现代 AI 产品的设计范式：
- **轻量对话层（GPT-Live-1）** — 管理对话流程，低延迟响应，全双工实时交互
- **重量推理层（GPT-5.5）** — 处理复杂任务，后台运行不阻塞对话

这与微服务的前端/后端分离高度类似——**把高频低延迟路径和低频高计算路径分开**。这个模式对构建 AI 产品的工程师极其有参考价值。

其次，Day 88 总结了"回溯思维在 AI 中的映射"：
- Beam Search = 宽度优先的路径探索
- Tree of Thoughts = 显式决策树 + 剪枝
- AlphaCode = 大量采样 + 测试过滤（Sample → Test → Filter）

**"据报道" 提醒（新闻类内容）：** 本周 AI 新闻中的具体数字——OpenAI Jalapeño 芯片性能数据、Gemma 4 的 4 亿次下载量、MiniMax M3 的 1M token 上下文——均为据报道数据，应以实际发布文档为准。

---

## ⚠️ 需要复习 / What to Review

**最薄弱区域：**

1. **Find Median from Data Stream（#295）** — 双堆的三步 invariant 维护逻辑（先push到left → 检查大小关系 → 重平衡大小）容易在压力下写错。**建议**：不看答案，徒手默写一遍，跑通 trace。

2. **一致性模型横向对比** — 能随口说出 Redis Cluster、DynamoDB、Elasticsearch 各自的一致性模型和失败场景吗？**建议**：用卡片背诵对比矩阵，练习系统设计中"我会选 X 而非 Y，因为..."的口头表达。

3. **STAR+S 扩展** — 口头练习时注意把故事讲到 Systemic Impact，而不是停在 Result。

---

## 🏆 本周亮点 / Win of the Week

**完成了「堆/优先队列」7题全块！**

从 #703（基础 min-heap）到 #295（双堆 Hard），走完了堆模式的完整进化路径。Find Median from Data Stream 是经典 Hard 题，双堆 invariant 的设计是真正考察结构化思维的题目——不是套公式，而是从"如何维护中位数"反推出"需要两个对称的数据结构"。完整走过一个 7 题 pattern block，印证了 NeetCode 路线图"模式学习"的价值。

---

## 🎯 下周预告 / Next Week Preview

**算法（NeetCode: 71/150）：**
- 继续回溯块（当前 1/9）：Combination Sum → Permutations → Subsets II → N-Queens
- 回溯是面试高频考点，所有变体都可以用一套模板推导

**系统设计（Synthesis Mode 持续）：**
- 继续 Expert Synthesis：跨主题深度融合，准备 Staff-level 面试的复合型问题

**软技能：**
- 继续 Synthesis Mode：练习把已有 STAR 故事升级到 STAR+S 格式，重点打磨 Systemic Impact 部分

**Python Craft（#32/40+）：**
- 下一批实践模式待揭晓，本周的 Feature Flags、structlog、pydantic-settings 三件套是生产后端的核心工具链

**提醒：** 回溯是本周开启的新 block，需要高质量时间投入。建议每道题先画决策树，再写代码。
