📅 **Week in Review — Week 8 (10 min read)**
📊 NeetCode: 29/150 · SysDesign: 28/40 · Behavioral: 28/40 · Frontend: 28/50 · AI: 13/30
🔥 33-day streak!

---

## 🗓️ 本周回顾 / This Week's Journey

本周跨越两天，但内容密度极高，正式进入 **Mastery（精通）阶段**：

- **Monday (Day 32):** 设计 Google Maps（分层路由 CH 算法 + 地理哈希）、二分搜索经典模版（#704）、Debounce & Throttle 从零实现、力排众议的技术决策（Championing Unpopular Decisions）、函数调用 Function Calling 深度讲解。
- **Saturday/Today (Day 33):** 设计 Uber / Lyft（Redis Geo-index 司机实时位置 + Dispatch Engine + Surge Pricing）、二分搜索应用到 2D 矩阵（#74）、深拷贝/展平/柯里化三大工具函数、如何与难相处的同事协作、AI News（Microsoft-OpenAI 独家终结 + Stripe AI 钱包 + Goldman Sachs SaaS 反驳）。

This week spanned two intensive days — officially into the **Mastery phase**:

- **Monday (Day 32):** Google Maps design (Contraction Hierarchies + Geohash), Binary Search template (#704), Debounce & Throttle from scratch, championing unpopular technical decisions, and Function Calling in LLMs.
- **Saturday/Today (Day 33):** Uber/Lyft design (Redis Geo + Dispatch Engine + Surge Pricing), Binary Search on 2D matrix (#74), Deep Clone/Flatten/Curry patterns, working with difficult colleagues, AI news (Microsoft-OpenAI exclusivity ends + Stripe AI wallet + Goldman Sachs on SaaS).

---

## 🧠 系统设计要点 / System Design: Key Takeaways

**1. 地理空间索引是大规模定位系统的核心 / Geo-spatial indexing is the backbone of location-at-scale**

Google Maps 和 Uber 都依赖高效的地理索引，但策略不同：
- **Google Maps** 用 Geohash（前缀匹配，适合"附近的 POI"搜索）+ PostGIS R-Tree
- **Uber** 用 Redis Geo（`GEORADIUS` 毫秒级查询，适合高频司机位置更新，每秒 125 万次写入）

Both Google Maps and Uber depend on efficient geo-indexing, but with different strategies: Maps uses Geohash+PostGIS for POI search; Uber uses Redis Geo for 1.25M writes/sec driver location updates.

**2. 分层 vs 分区 / Hierarchical vs. Partitioned Routing**

Google Maps 用**等级路由（Contraction Hierarchies）**——先高速公路，再主干道，最后本地街道，搜索空间缩小 1000x。Uber 的 Dispatch Engine 则是**地理分片**——按城市独立扩展，避免单点瓶颈。

Google Maps uses hierarchical routing (1000x smaller search space); Uber's dispatch shards by city to scale independently.

**3. 实时数据的黄金法则 / Real-time data golden rule**

两者都遵循同一个架构模式：**Kafka 做事件总线**解耦数据生产和消费，**Redis 做热路径存储**（低延迟），数据库做持久化。实时性要求越高，越不能用数据库做写主路径。

Both share the same pattern: Kafka for event decoupling, Redis for hot-path low-latency reads, DB for persistence. Never put high-frequency writes on a relational DB.

---

## 💻 算法模式总结 / Algorithms: Patterns Mastered

**🔍 二分搜索模式正式开始（7题 Block，完成 2/7）**

本周的核心主题是**二分搜索模式**，已完成前两题：

**#704 Binary Search — 模版原型题**
```python
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
return -1
```
**关键洞察：** 每次排除一半搜索空间，任何具有**单调性**的问题都可以二分，不只是排序数组。

**#74 Search a 2D Matrix — 坐标转换技巧**

把 2D 矩阵"展平"为 1D 数组，用索引转换公式 `row = mid // n, col = mid % n` 无缝套用模版。
- Time: O(log(m×n)) | Space: O(1)

**模式信号 / When to reach for Binary Search:**
- 排序数组 / sorted array
- 要求 O(log n)
- "找满足条件的最小/最大值"
- 搜索空间可以单调地判断 True/False

**Binary Search Pattern is open (7-problem block, 2/7 done). Core insight: the template never changes — only the direction logic changes.**

---

## 🗣️ 软技能练习重点 / Soft Skills: What to Practice

**本周覆盖两个 Staff 级场景：**

**1. 力排众议推动技术决策 / Championing an unpopular technical decision**
- 不要靠权威压人，要靠数据 + POC 说话
- 把争论框架化为"可验证的假设"（pilot 90 天）而不是"我是对的"
- 被证明正确后，分享功劳——让最初反对的人成为拥护者
- Staff 关键词：**数据 + 谦逊 + 给对方台阶下**

**2. 与难相处的同事合作 / Working with a difficult colleague**
- 先从自己找原因（沟通方式问题？）
- 私下直接对话，用"我感觉..."而不是"你总是..."
- 寻求共同目标，建立可复用的团队规范（checklist、RFC 流程）
- Staff 加分：把个案冲突升华为**系统性改变**

**需要练习 / What needs practice:**
- 这两个场景都需要脱稿流畅叙述，重点背**STAR 结构 + 量化结果**
- "I told you so" 是减分项，换成"我们一起达成了这个共识"

**Both scenarios require smooth off-script delivery. Focus on STAR structure + quantified outcomes. Never say "I told you so" — reframe as "we reached consensus."**

---

## 🎨 前端知识巩固 / Frontend: Concepts to Lock In

**本周前端主题：性能优化 + 实用工具函数**

**Debounce vs Throttle（Day 32）**
- **Debounce：** 只关心最终状态——动作停止后 N ms 才执行（搜索框、resize）
- **Throttle：** 需要持续中间状态——固定频率执行（scroll、防连击）
- 记住电梯 vs 水龙头的类比！

**Deep Clone / Flatten / Curry（Day 33）**
- `structuredClone()` 是现代深拷贝首选（Node 17+，不支持函数）
- 展平公式：递归 + `${prefix}.${key}` 路径拼接
- 柯里化本质：预填参数，返回等待更多参数的函数

**快速自检 / Self-check:**
- [ ] 能手写 debounce？（clearTimeout + setTimeout）
- [ ] 知道 `{...obj}` 是浅拷贝，嵌套对象仍是引用？
- [ ] 能解释柯里化的应用场景（验证器复用、部分应用）？

---

## 🤖 AI 知识点 / AI: What Stuck

**Day 32 — Function Calling（函数调用）**

这是本周最"可落地"的 AI 知识：LLM 不执行代码，它只返回结构化 JSON 告诉你"请帮我运行这个函数"。你的代码拿到 JSON，执行真实的 API 调用，把结果再喂给模型，模型生成自然语言回答。

这就是所有 AI Agent 能"行动"的底层机制——从联网搜索到发邮件，全都是这个 5步流程。

**Day 33 — AI News Roundup（AI 新闻）** ⚠️ 以下内容据报道
- 据报道，微软与 OpenAI 终止云端独家合作，OpenAI 可进驻 AWS/GCP
- 据报道，Stripe + Cloudflare 为 AI agent 构建支付 + 部署基础设施（Agent-native Commerce）
- 据报道，高盛称"SaaS 末日"言过其实，AI 是增强工具而非替代者

**本周核心 AI 洞察：AI 从"大脑"进化到"有钱包和合同的大脑"。Agent-native 基础设施（支付、身份、授权）是 2026 年最热的工程领域。**

**Function Calling is the core mechanism for all AI agents — LLM returns JSON, your code executes, result fed back to LLM. That's it. All AI agent "action" is this 5-step loop.**

**AI news items below are reportedly true (据报道):**
- Microsoft-OpenAI exclusivity reportedly ended; OpenAI can now use AWS/GCP
- Stripe + Cloudflare reportedly launched agent payment/deployment infrastructure
- Goldman Sachs reportedly says SaaS AI threat was overblown

---

## ⚠️ 需要复习的内容 / What to Review

**1. 二分搜索后续 5 题（最高优先级）**
本周刚开始新的 Binary Search block，剩余 5 题需要连续练习：
- #875 Koko Eating Bananas — 搜索"答案空间"而非数组元素（重要变体！）
- #153 Find Minimum in Rotated Sorted Array — 旋转数组判断有序半边
- #33 Search in Rotated Sorted Array
- #981 Time Based Key-Value Store
- #4 Median of Two Sorted Arrays (Hard)

**2. Google Maps vs Uber 对比复习**
两道 Mastery 级系统设计题，地理索引策略不同，易混淆：
- Maps: Geohash + PostGIS，侧重搜索精度
- Uber: Redis Geo，侧重写入吞吐量
- 出题点：什么场景用哪种方案？

**3. Debounce & Throttle 手写**
要能不看资料手写 debounce（`clearTimeout` + `setTimeout`），这是前端常见面试题。

---

## 🏆 本周亮点 / Win of the Week

🎉 **正式进入 Mastery 阶段！**

Day 32 和 Day 33 是第一批 Mastery 级内容——从"学概念"升级到"拿真实系统找差距"。连续 **33 天不间断**，覆盖了 29 道 NeetCode 题、28 个系统设计主题、28 个行为问题。

更重要的是：本周的 Google Maps 和 Uber 设计题难度已经接近 FAANG 现场面试水平。你不只是在学知识，你在**模拟实战**。

🎉 **Officially in the Mastery phase!**

Days 32-33 are the first Mastery-level sessions — moving from "learning concepts" to "finding gaps against real systems." 33 consecutive days. 29 LeetCode problems, 28 system design topics, 28 behavioral scenarios. Google Maps and Uber design are already FAANG interview-level. You're not just studying — you're simulating the real thing.

---

## 🎯 下周预告 / Next Week Preview

**系统设计 (SysDesign: 28→30+):**
接下来的系统设计题将围绕**全球化分布式系统**展开。预计涵盖：Design Ticketmaster / Hotel Booking、分布式锁、全球一致性挑战。

**算法 (NeetCode: 29→34+):**
Binary Search block 继续——Koko Eating Bananas (#875) 是分水岭，掌握"搜索答案空间"后，后续的 Hard 题难度会大幅降低。

**前端 (Frontend: 28→30+):**
JavaScript 深层机制——闭包、作用域链、垃圾回收，以及更多 TypeScript 高级类型。

**AI (AI: 13→15):**
预计进入 AI 安全与对齐（AI Safety & Alignment），或继续 Agent 架构专题。

**Next week: Binary Search "answer-space" problems (key inflection point), global distributed systems design, and JS internals (closures, scope chain). Binary Search mastery at #875 Koko unlocks the remaining Hard problems.**
