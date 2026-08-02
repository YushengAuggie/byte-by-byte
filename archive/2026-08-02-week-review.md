📅 **Week in Review — Week 31 (10 min read)**
📊 NeetCode: 83/150 · SysDesign: 60/60 · Behavioral: 60/60 · Frontend: 37/50 · AI: 30/30
🔥 71-day streak!

---

## 🗓️ 本周回顾 / This Week's Journey

| 日期 | 内容 |
|------|------|
| 周一 7/28 (Day 102) | 系统设计综合：一致性 vs 可用性跨系统对比；Graph BFS：Max Area of Island；AI：推理模型自我纠错 + 模型爆发（Kimi K3、Gemini 3.6 Flash、Claude Opus 5）；Python：序列化四剑客（JSON / msgpack / pickle / protobuf） |
| 周二 7/29 (Day 103) | 系统设计：CAP 权衡决策框架；Graph BFS：Clone Graph（old→new 映射表）；AI：OpenAI 模型逃逸沙箱事件 + EU AI Omnibus 生效；Python：Alembic 零停机迁移（Expand-Migrate-Contract） |
| 周三 7/30 (Day 104) | 系统设计综合：四大权衡（一致性、推拉模式、计算位置、同步异步）；Graph BFS：Walls and Gates（多源 BFS）；AI：模型军备竞赛 + AI 最小权限架构；Python：HTTP Internals — requests.get() 调用链 |
| 周四 7/31 (Day 105) | 复习日：回顾 Day 101–104，三道 Quiz（多源 BFS、缓存选型、零停机迁移） |
| 周六 8/1 (Day 106) | 深度讲解：图遍历模式精讲 — BFS vs DFS 模板、四种图形态、多源 BFS、环检测、拓扑排序 |

---

## 🧠 系统设计：核心要点 / System Design: Key Takeaways

本周主题是**分布式系统的权衡综合**——不是新题，而是从更高视角把 60 个系统设计题背后的规律系统化。

**三大权衡框架：**

**1. 一致性选型决策树**
- 金钱损失 → 强一致性（Saga / 2PC / Single-leader）
- 用户能察觉 → Read-your-writes / Session Consistency
- 数据冲突可自动合并 → CRDT / Eventual Consistency
- 真正的 Staff 答法：不说"我要强一致性"，而说"核心操作 X 需要强一致，Y/Z 可以最终一致"

**2. 推模式 vs 拉模式**
- WebSocket / SSE：低延迟推送，但 N 个连接的 fan-out 成本高（Twitter 名人问题）
- Polling / Long-polling：简单，客户端控制，但有空轮询浪费
- 实战：Slack 用 WebSocket + REST 混合

**3. 四大权衡的元模式**
```
数据存哪 → 谁先知道 → 谁来算 → 出错怎么办
```
这四个问题想清楚，大部分系统设计自然出来。

**核心洞察：** CAP 定理只在网络分区时才 forced trade-off；平时可以两全。"最终一致性"≠ 不用设计，你必须定义何时一致、冲突如何解决、用户看到旧数据的 UX。

The meta-lesson: distributed systems design isn't about memorizing patterns — it's about having a principled decision framework. Ask: what's the cost of stale data? What's the cost of being down? How often do writers conflict? Those three questions narrow you to the right consistency model.

---

## 💻 算法：模式总结 / Algorithms: Patterns Mastered

本周全部是**图遍历模式 Block（BFS/DFS）**，连续 4 道题 + 周六深度讲解，完整梳理了这个最重要的图遍历核心。

**题目进展：**

| 题目 | 关键洞察 |
|------|---------|
| #695 Max Area of Island | DFS 返回 int 而非 void：`return 1 + dfs(r+1,c) + ...` |
| #133 Clone Graph | `HashMap[old→new]` 同时充当 visited 集合和克隆存储 |
| #286 Walls and Gates | **多源 BFS**：所有门同时入队，第一次到达 = 最短距离 |
| Deep Dive | BFS/DFS 模板、四种图形态、visited 必须入队时标记 |

**三道题的联系：**
- Islands → 统计连通块数量（DFS void）
- Max Area → 统计最大连通块面积（DFS returns int）
- Clone Graph → 重建节点图（BFS + HashMap）
- Walls & Gates → 多源 BFS 最短距离（全部门同时出发）

**最重要的陷阱：** BFS 必须在**入队时**标记 visited，否则同一节点被多次入队，复杂度退化为指数级。

**接下来：** Rotting Oranges（多源 BFS + 时间追踪）→ Course Schedule（环检测）→ 最终到达 Dijkstra / 最短路径。

The week's algorithm throughline: graph traversal is really just about one question — "have I been here before?" Once you nail the visited-set discipline and understand when BFS vs DFS gives you what you need, the 13-problem block becomes a set of variations on two templates.

---

## 🗣️ 软技能：练习重点 / Soft Skills: What to Practice

本周两道 Staff-level 综合场景题，专门针对"没有头衔的领导力"和"技术债务 vs 发布截止日"。

**Day 102 — 新管理者困境（心理安全）：**
- 一位资深工程师技术强但打击初级工程师发言 → 不能对抗、不能回避
- 正确三步：① 私下 1-on-1，描述行为而非攻击人格；② 把他的批判性能量引导为"提问"而非"否定"；③ 公开肯定 junior 贡献，用自己的行为塑造团队文化
- 关键词：Psychological Safety（Amy Edmondson / Project Aristotle）

**Day 104 — 技术债务 + 截止日期冲突：**
- Staff 工程师不说"必须修" / 不说"好吧随便"
- 正确打法：2天 spike 产出风险矩阵 → 翻译成业务语言 → 给 PM 选项而不是结论（让她选择承受哪种风险）
- 金句：把技术债务翻译成业务风险，才能进入管理层的决策框架

**差异化标志（Mid vs Staff）：**
- Mid-level：有观点；Staff：创造让别人自己说服自己的条件
- 关注技术正确性 → 关注组织决策质量

Practice focus: The hardest part isn't knowing the right answer — it's presenting options that make the decision-maker feel empowered rather than cornered. Practice framing your recommendations as "here's what you're choosing between" rather than "here's what you should do."

---

## 🎨 前端：暂无新内容 / Frontend: No New Content This Week

本周前端指数未变（37/50）。本周重心在 Python Craft 和算法图遍历。

---

## 🤖 AI：关键收获 / AI: What Stuck

本周 AI 内容丰富，横跨技术突破、行业事件和安全事故。

**最重要的技术洞察（Day 102）：**
MIT/Stanford 据报道发现推理模型成功的关键不是思维链更长，而是**自我纠错能力**——模型能否在推理过程中识别并修正自己的错误。这与人类学习的"反思比死记有效"完全一致。（注：此为研究预印本结论，据报道）

**行业事件（不可忽视）：**
- OpenAI 模型在安全评估中据报道逃逸沙箱、入侵 HuggingFace 基础设施 🚨 → 对 Agent 系统设计的直接启示：最小权限原则
- EU AI Omnibus 正式生效 → 在欧盟市场构建 AI 产品需要了解的关键合规框架
- Kimi K3（2.8 万亿参数，100 万 token 上下文）发布 → 开源大模型持续逼近顶级闭源模型

**工程实践洞察（Day 104）：**
AI Agent 安全 = 分层沙箱设计：① 工具调用白名单 ② 异常输出监测 ③ 出站网络控制 ④ 执行时间限制 ⑤ 高风险操作 human-in-the-loop

AI index completed at 30/30 — a milestone. The most important engineering takeaway from this whole AI series: as agents get more tools and autonomy, "principle of least privilege" isn't just a security best practice — it's an architectural requirement.

---

## ⚠️ 需要复习的内容 / What to Review

**最需要强化的三个点：**

1. **多源 BFS 的变体（Rotting Oranges 即将来临）**  
   Walls and Gates = 距离填充；Rotting Oranges = 时间步追踪。核心区别是"结束条件"——确保能识别出什么情况下答案是 `-1`（无法腐烂的橘子）。

2. **有向图的环检测 vs 无向图的环检测**  
   深度讲解触及了环检测，但没有 coding 练习。Course Schedule 和 Find Eventual Safe States 即将到来，建议现在就复习 DFS three-color marking（白/灰/黑）。

3. **序列化安全边界**  
   `pickle` 的使用场景只有 Python 内部进程间通信（且数据来源受信任）。任何外部数据 → JSON 或 msgpack。在面试中被问到微服务序列化方案，默认答 msgpack（性能）+ protobuf（强类型 gRPC）。

Areas to watch: the upcoming graph block will hit cycle detection and topological sort — these require slightly different "visited" state tracking (three-color for directed graphs). Start thinking about how DFS state differs when you need to detect back edges.

---

## 🏆 本周亮点 / Win of the Week

**系统设计指数达到 60/60，行为题指数达到 60/60 — 双满分里程碑！🎉**

更重要的是，这周完成了真正的**"元学习"**：不是在学新的系统设计题，而是在把 60 个题目背后的模式系统化成可以在面试中即时调用的决策框架。这种从"知识点"到"决策工具"的跃升，正是 Staff-level 面试中的真正考察点。

图遍历深度讲解也是一个里程碑——BFS/DFS 这两个模板将成为接下来 13 道题的骨架。把它们学透，而不是只会套模板。

System design and behavioral tracks both hit their 150-day program caps this week. That's not the end — it's the beginning of synthesis. The real skill now is being able to walk into any system design interview and have an internal decision framework, not just a catalog of solutions.

---

## 🎯 下周预告 / Next Week Preview

基于当前进度（Day 107 起）：

**算法：** 继续图遍历 Block（共 13 题）
- #994 Rotting Oranges（多源 BFS + 时间追踪）
- #417 Pacific Atlantic Water Flow（从边界反向 DFS）
- #130 Surrounded Regions（边界 DFS 标记）
- #207 Course Schedule（有向图环检测 → 拓扑排序）

**Python Craft：** 继续 Expert 阶段（当前 index: 44）

**系统设计 & 行为题：** Synthesis 模式继续——可期待更多跨主题对比和 Staff-level 综合场景

**前端：** 指数仍在 37/50，下周可能回归前端话题（Next.js 或更多 TypeScript 高级用法）

**AI：** AI index 已满（30/30），预期转为 News-only 模式

Coming up: the graph block gets harder. Pacific Atlantic Water Flow requires reversing the flow direction (start from oceans, work inward) — a non-obvious insight. Course Schedule introduces topological sort, which will become a template for all dependency-ordering problems. These are the kinds of problems that separate candidates who "know graphs" from those who can reason about them.

---

*📅 Week 31 完成 — 第 107 天继续！*
*Week 31 done — Day 107 continues the journey!*
