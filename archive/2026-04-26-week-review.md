📅 **Week in Review — Week 7 (10 min read)**
📊 NeetCode: 27/150 · SysDesign: 26/40 · Behavioral: 26/40 · Frontend: 26/50 · AI: 12/30
🔥 31-day streak!

## 🗓️ This Week's Journey / 本周回顾
- **Monday (Day 27):** 设计新闻流 (News Feed)、括号生成 (Generate Parentheses)、闭包 (Closures)、建立信任 (Building Trust)、AI 动态。
- **Tuesday (Day 28):** 设计聊天系统 (Chat System)、每日温度 (Daily Temperatures)、异步控制流 (Promises)、自研与外购 (Build vs Buy)、MCP 协议。
- **Wednesday (Day 29):** 设计搜索引擎 (Search Engine)、车队 (Car Fleet)、事件循环 (Event Loop)、应对组织变革 (Navigating Org Change)、AI 动态。
- **Thursday (Day 30):** 综合复习日 (Review Day)。
- **Friday (Day 31):** 设计视频流媒体 (YouTube/Netflix)、直方图最大矩形 (Largest Rectangle in Histogram)、原型与 this (Prototypes & this)、衡量项目成功 (Measuring Success)、AI 动态。
- **Saturday (Deep Dive):** 深度解析 Google Maps 架构 (Design Google Maps)。

## 🧠 System Design: Key Takeaways / 系统设计要点
1. **Fan-out 策略 (Fan-out Strategies):** 在新闻流和聊天系统中，写时扇出 (Fan-out on write) 适合普通用户和中小群组，而读时扇出 (Fan-out on read) 适合大V。
2. **异步与解耦 (Async & Decoupling):** 视频转码 (YouTube) 和消息推送 (Chat) 都极度依赖消息队列 (Kafka) 来解耦 CPU 密集型或高并发任务。
3. **空间与时间索引 (Spatial & Time Indexing):** 搜索引擎依赖倒排索引 (Inverted Index)，而 Google Maps 依赖四叉树/Geohash 进行空间索引。

1. **Fan-out Strategies:** In News Feeds and Chat Systems, fan-out on write is ideal for normal users/small groups, while fan-out on read is better for celebrities.
2. **Async & Decoupling:** Video transcoding (YouTube) and message pushing (Chat) heavily rely on message queues (Kafka) to decouple CPU-heavy or high-concurrency tasks.
3. **Spatial & Time Indexing:** Search engines rely on Inverted Indexes, while Google Maps relies on Quadtrees/Geohashes for spatial indexing.

## 💻 Algorithms: Patterns Mastered / 算法模式总结
**单调栈模式 (Monotonic Stack Pattern):**
- **#739 Daily Temperatures:** 使用单调递减栈寻找下一个更大元素。
- **#853 Car Fleet:** 结合排序与单调栈，通过到达时间判断追及关系。
- **#84 Largest Rectangle in Histogram:** 使用单调递增栈，在弹出元素时利用左右边界计算最大面积（该模式的最难点）。

**Monotonic Stack Pattern:**
- **#739 Daily Temperatures:** Monotonic decreasing stack to find the next greater element.
- **#853 Car Fleet:** Sorting + stack to simulate catch-up scenarios based on arrival time.
- **#84 Largest Rectangle in Histogram:** Monotonic increasing stack to calculate max area using left/right boundaries upon popping (the hardest variation).

## 🗣️ Soft Skills: What to Practice / 软技能练习重点
- **建立信任 (Building Trust):** 在新团队中，信任来自可预测性、透明度和稳定交付，而非单纯的人际关系。
- **Build vs Buy:** 评估总拥有成本 (TCO) 和核心竞争力。不要在非核心的通用基础设施上浪费工程资源。
- **衡量成功 (Measuring Success):** 成功不仅是技术上线，还包括用户影响和业务价值。需要建立分层的指标框架。

- **Building Trust:** In a new team, trust comes from predictability, transparency, and delivery, not just being nice.
- **Build vs Buy:** Evaluate TCO and core differentiators. Don't waste engineering cycles on commodity infrastructure.
- **Measuring Success:** Success is not just shipping code; it's user impact and business value. Build a multi-layered metrics framework.

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固
- **闭包 (Closures):** 函数及其捕获的词法作用域。注意在循环中捕获变量时的陷阱。
- **异步控制流 (Async Control Flow):** `Promise.all` 用于并行请求，避免不必要的串行 `await` 阻塞。
- **事件循环 (Event Loop):** 区分微任务 (Microtasks, 如 Promise) 和宏任务 (Macrotasks, 如 setTimeout)，以及它们在渲染前后的执行顺序。
- **原型与 this (Prototypes & this):** 掌握 `this` 的四种绑定规则，理解箭头函数如何继承外层词法作用域的 `this`。

- **Closures:** Functions + captured lexical scope. Watch out for variable capture traps in loops.
- **Async Control Flow:** Use `Promise.all` for parallel requests to avoid sequential `await` blocking.
- **Event Loop:** Differentiate between Microtasks (Promises) and Macrotasks (setTimeout), and their execution order relative to rendering.
- **Prototypes & this:** Master the 4 rules of `this` binding and how arrow functions inherit lexical `this`.

## 🤖 AI: What Stuck / AI 知识点
- **MCP (Model Context Protocol):** AI 工具的“USB 标准”，允许大模型以统一、标准化的方式连接外部工具和数据源。
- **AI 动态 (News):** 据报道，Google 发布了分离训练和推理的第八代 TPU (8t/8i)，并强制工程师使用内部 AI 编程代理。同时据报道，Anthropic 的 Claude Mythos 帮助 Mozilla 发现了 271 个 Firefox 漏洞。

- **MCP (Model Context Protocol):** The "USB standard" for AI tools, allowing LLMs to connect to external tools and data sources in a unified, standardized way.
- **AI News:** Reportedly, Google released 8th-gen TPUs (8t/8i) separating training and inference, and mandated internal AI coding agents. Also reportedly, Anthropic's Claude Mythos helped Mozilla find 271 Firefox bugs.

## ⚠️ What to Review / 需要复习的内容
- **单调栈的边界处理 (Monotonic Stack Boundaries):** 特别是 Largest Rectangle in Histogram 中的 `extend-left` 技巧，需要反复手写加深肌肉记忆。
- **事件循环的执行顺序 (Event Loop Execution Order):** 容易在复杂的异步嵌套中判断失误，需多做代码输出推演。

- **Monotonic Stack Boundaries:** Especially the `extend-left` trick in Largest Rectangle in Histogram. Needs repeated practice for muscle memory.
- **Event Loop Execution Order:** Easy to misjudge in complex async nesting. Needs more code output tracing practice.

## 🏆 Win of the Week / 本周亮点
成功攻克了单调栈模式中最难的 #84 Largest Rectangle in Histogram，并完成了对 Google Maps 架构的深度解析！
Successfully conquered the hardest monotonic stack problem (#84 Largest Rectangle in Histogram) and completed a deep dive into Google Maps architecture!

## 🎯 Next Week Preview / 下周预告
- **Algorithms:** 二分查找 (Binary Search) 模式。
- **System Design:** 分布式事务与共识算法 (Distributed Transactions & Consensus)。
- **Frontend:** React 性能优化与底层原理。
