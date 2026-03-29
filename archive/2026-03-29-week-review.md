# 📅 **Week in Review — Week 3 (10 min read)**
📊 Day 13/150 · NeetCode: 13/150 · SysDesign: 12/40 · Behavioral: 12/40 · Frontend: 12/50 · AI: 5/30
🔥 13-day streak!

---

## 🗓️ 本周回顾 / This Week's Journey

本周是第 3 周（第 8–13 天），阶段从 Foundation 迈入 Growth，难度明显上台阶。

*Week 3 covered Days 8–13, bridging Foundation → Growth phase with a noticeable difficulty step-up.*

| 日期 / Date | 亮点 / Highlight |
|---|---|
| **Mon 3/23 · Day 8** | 数据库索引 B-Tree + N+1 查询；CSS Animations & Transitions；模糊需求处理 |
| **Tue 3/24 · Day 9** | 数据库复制 & 分片（Replication / Sharding）；算法切换双指针模式（#125 Valid Palindrome）；AI 大新闻：Agentic AI、百万 Token 上下文 |
| **Wed 3/25 · Day 10** | 📝 复习日：回顾 Day 6-9 全部内容，巩固薄弱点 |
| **Thu 3/26 · Day 11** | 一致性哈希（Consistent Hashing）+ 虚拟节点；双指针 #167 Two Sum II；React useEffect；主动发现问题的 behavioral |
| **Fri 3/27 · Day 12** | CAP 定理 & 最终一致性（Growth Phase 正式开始）；3Sum（双指针 3/5）；React useRef；RLHF 深度讲解；优先级排序 behavioral |
| **Sat 3/28 · Day 13** | 🔬 深挖：消息队列 & 事件驱动架构（15 min read，含 Kafka 实战代码）|

---

## 🧠 系统设计要点 / System Design: Key Takeaways

本周系统设计从"单机"向"分布式"跃进，三个核心概念构成一套完整的分布式基础：

*This week's system design made the leap from single-machine to distributed, forming a complete distributed foundation:*

**1. 数据库索引 → 复制 → 分片 / Indexing → Replication → Sharding**
- 索引解决**单机查询速度**（B-Tree O(log N) vs 全表扫 O(N)）
- 复制解决**读扩展 + 高可用**（多副本分担读流量）
- 分片解决**写扩展 + 存储规模**（每个 shard 只负责一部分数据）
- 三者是递进关系：先索引，再复制，实在撑不住再分片

**2. 一致性哈希 / Consistent Hashing**
- 普通哈希 `key % N`：增减节点触发 90% 数据重分配 ❌
- 一致性哈希：增减节点只影响 ~1/N 数据 ✅
- 核心武器：**虚拟节点**（每个物理节点 150-200 个虚拟位置），解决负载不均
- 真实应用：DynamoDB、Cassandra、Memcached

**3. CAP 定理 / CAP Theorem**
- 分布式系统三选二：Consistency（一致）、Availability（可用）、Partition Tolerance（分区容错）
- 网络分区不可避免，实际是 CP vs AP 的取舍
- **CP**：金融、支付、计数器（HBase、ZooKeeper）
- **AP + 最终一致性**：社交 feed、购物车、点赞（Cassandra、DynamoDB）
- 面试技巧：先问业务对一致性的要求，再决定选型

**本周连接点 / The thread connecting them all:**
索引 → 复制 → 分片 → 一致性哈希 → CAP，是任何大规模数据库系统设计的完整脉络。消息队列（Day 13）则是在此基础上，解耦服务间的依赖，进一步提升系统韧性。

---

## 💻 算法模式 / Algorithms: Patterns Mastered

本周完成双指针模式 5 题中的 3 题（进度 3/5）：

*Completed 3 of 5 Two Pointers problems this week:*

| 题目 | 核心变化 | 关键洞察 |
|---|---|---|
| **#125 Valid Palindrome** | 跳过非字母数字 | 双指针"对比"而非求和；Space O(1) 优于 O(n) |
| **#167 Two Sum II** | 有序数组求和 | 排序后才能确定性地收缩：sum < target → left++，sum > target → right-- |
| **#15 3Sum** | 三数之和为零 | 外层固定一个数，内层双指针；排序后跳过重复解 |

**模式识别信号 / When to reach for Two Pointers:**
> ✅ 有序数组 · ✅ 找配对/三元组 · ✅ 回文检测 · ✅ 原地操作 · ✅ 要求 O(1) 空间

**下两题预告 / Coming next:**
- `#11 Container With Most Water` — 移动较短边指针，最大化面积
- `#42 Trapping Rain Water` — 最复杂变体，维护左右最大高度

---

## 🗣️ 软技能练习 / Soft Skills: What to Practice

本周覆盖了 5 个核心行为面试主题（Day 8–12），全部 Senior/Staff 级别：

*5 behavioral interview topics covered, all targeting Senior/Staff level:*

| 主题 | STAR 核心动作 | 需要强化的点 |
|---|---|---|
| **模糊需求** | 写假设文档、区分可逆/不可逆决策 | 结果要量化（"避免了 1.5 周返工"） |
| **向上推回** | 先跑负载测试量化风险，再提替代方案 | 带数据 + 替代方案是关键；不要空手说"不行" |
| **主动发现问题** | 复现 bug → 量化风险 → 独立推进修复 | 系统性主动（建立监控体系）比偶发性主动更有说服力 |
| **优先级排序** | Impact × Urgency 矩阵；把技术连接到业务目标 | 明确说出"选 A 意味着 B 推迟到 X，风险是 Y" |
| **处理交付坏消息** | 提前同步，给选项，聚焦解决方案 | 不要等到最后一刻才上报风险 |

**综合练习建议 / Practice focus:**
用 STAR 框架为每个主题准备 1-2 个真实故事，重点量化结果。"主动发现问题"和"优先级排序"是最容易被考到但准备不足的两个主题。

---

## 🎨 前端巩固 / Frontend: Concepts to Lock In

本周 React Hooks 三件套全部覆盖：

*All three core React Hooks covered this week:*

**useState → useEffect → useRef — 递进关系：**

```
useState: 需要 UI 更新时存状态（触发重渲染）
useEffect: 需要同步副作用（数据获取、订阅、DOM 操作）
useRef: 需要持久值但不想触发重渲染（DOM 引用、timer ID）
```

**高频考点 / High-frequency interview traps:**

1. `useState` 批量更新：`setCount(count+1)` 三次 → count 只 +1；用 `prev => prev + 1` 才能累加 ✅
2. `useEffect` 清理：return 里关闭 WebSocket/清除 timer，否则内存泄漏 ✅
3. CSS `transition` vs `animation`：transition 需要触发（hover/JS），animation 自动运行 ✅
4. 动画性能：优先 `transform` + `opacity`（GPU），避免 `width/height/margin`（触发 reflow）✅

**自查问题 / Quick self-check:**
- `useEffect` 的依赖数组为空 `[]` 和不传有什么区别？
- `useRef` 的值改变了，组件会重渲染吗？
- CSS `display: none` 可以加 transition 吗？

---

## 🤖 AI 知识点 / AI: What Stuck

本周 AI 内容从"行业动态"到"技术机制"都有覆盖：

*AI content ranged from industry trends to technical mechanisms:*

**最重要的技术概念 / Most important technical concept:**

**RLHF — ChatGPT 是怎么学会"有用"的：**
1. **SFT（监督微调）**：在人类示范答案上微调基础模型，学格式和风格
2. **奖励模型（RM）训练**：收集人类对多个回答的排序偏好，训练打分器
3. **PPO 强化学习**：模型生成 → RM 打分 → 更新策略（同时用 KL 散度约束偏移）

**正在替代 PPO 的新方法**：DPO（Direct Preference Optimization）— 更简单，无需显式奖励模型。

**本周行业信号 / Industry signals:**
- Agentic AI 从"生成文本"→"自主完成任务"，GPT-5.4 已实现原生电脑操作（GUI）
- 76% 企业未准备好支持 AI Agent → 未来 1-3 年最值钱的技能：**设计与 AI Agent 协作的系统架构**（清晰 API、幂等操作、可审计工作流）
- 上下文窗口突破 100 万 token，某些场景 long-context 比构建向量数据库更简单准确

---

## ⚠️ 需要复习的内容 / What to Review

**优先级排序（从弱到强）：**

| 🔴 最需要复习 | 具体建议 |
|---|---|
| **CAP 定理 + PACELC** | 能否在 3 句话内解释 CP vs AP 的区别，并各举一个真实系统？DynamoDB 如何在同一系统里提供可调一致性？ |
| **一致性哈希虚拟节点** | 为什么虚拟节点数少了会有热点？能在白板上画出完整的哈希环 + 节点故障时的数据迁移吗？ |
| **3Sum 去重逻辑** | 能手写完整解法吗？排序后如何跳过重复的 `nums[i]`、`nums[left]`、`nums[right]`？ |

| 🟡 值得巩固 | 具体建议 |
|---|---|
| **消息队列：Kafka vs RabbitMQ** | 什么时候选 Kafka（高吞吐、回放），什么时候选 RabbitMQ（复杂路由、短生命周期消息）？ |
| **useEffect 依赖数组** | 写 3 个不同 useEffect 示例，分别对应"mount once"、"每次 render"、"deps 变化时" |
| **STAR 故事量化** | 为"主动发现问题"和"优先级排序"各准备一个有具体数字的故事 |

---

## 🏆 本周亮点 / Win of the Week

**成功跨越 Foundation → Growth 阶段！**

第 11 天开始 Growth Phase，内容难度明显上升（一致性哈希、CAP、3Sum、RLHF），但节奏保持稳定。最值得庆祝的是：Saturday Deep Dive（消息队列 & 事件驱动架构）内容深度和代码质量都达到了 senior 面试的实战水准——从 Kafka producer/consumer 配置，到幂等性设计，到死信队列，一篇顶得上市面上很多付费课程的一章。

🔥 13 天，从未间断。系统设计的脉络正在形成：网络 → HTTP → 负载均衡 → 缓存 → 数据库（索引→复制→分片→一致性哈希→CAP）→ 消息队列。这不是孤立的知识点，这是在构建一张完整的系统设计地图。

*Bridged Foundation → Growth phase without breaking stride. The Saturday Deep Dive on message queues hit senior-interview depth. More importantly, a coherent system design map is forming — 13 days, zero breaks.*

---

## 🎯 下周预告 / Next Week Preview

基于当前进度（SysDesign: 12/40 · Algorithms: 13/150 · Behavioral: 12/40 · Frontend: 12/50 · AI: 5/30）：

| 模块 | 下周内容 |
|---|---|
| 🏗️ **系统设计** | #13 CDN & 边缘计算 · #14 速率限制（Rate Limiting）· #15 SQL vs NoSQL 深度对比 |
| 💻 **算法** | 双指针收官：#11 Container With Most Water · #42 Trapping Rain Water · 开始滑动窗口模式 |
| 🗣️ **软技能** | 持续 Growth Phase：从影响力、跨团队协作到最终 behavioral |
| 🎨 **前端** | React Context · 自定义 Hook · 性能优化（useMemo/useCallback 实战） |
| 🤖 **AI** | AI News Roundup · 更多 AI 概念深挖 |

**本周学到的，下周就会用到**：CAP 定理 → 在设计 CDN/速率限制时你需要选择 CP 还是 AP；消息队列 → 在任何通知系统设计中都会出现；双指针 → Container With Most Water 是下周双指针收官题，比 3Sum 还更直接地考查"移动哪个指针"的决策逻辑。

加油，下周见！💪
