📅 **Week in Review — Week 16 (10 min read)**
📊 NeetCode: 23/150 · SysDesign: 22/40 · Behavioral: 22/40 · Frontend: 22/50 · AI: 11/30
🔥 26-day streak!

## 🗓️ This Week's Journey / 本周回顾
- **Monday (Day 22):** Unique ID Generators, Sliding Window Maximum, Process Improvement, TS Basics, Prompt Engineering. / 唯一 ID 生成器，滑动窗口最大值，流程改进，TS 基础，提示工程。
- **Tuesday (Day 23):** Web Crawlers, Valid Parentheses, Designing for Scale, TS with React, AI News. / 网络爬虫，有效括号，为扩展性设计，React+TS，AI 新闻。
- **Wednesday (Day 24):** Notification Systems, Min Stack, Conflict Resolution, TS Utility Types, Chain of Thought. / 通知系统，最小栈，冲突解决，TS 工具类型，思维链。
- **Thursday (Day 25):** Review Day — Consolidating the week's learnings. / 复习日 — 巩固本周所学。
- **Friday (Day 26):** Autocomplete Systems, Evaluate RPN, Handling Tough Feedback, TS Generics Deep Dive, AI Agents. / 自动补全系统，逆波兰表达式求值，应对严厉反馈，TS 泛型深度解析，AI 智能体。
- **Saturday (Deep Dive):** Designing a News Feed (Push vs Pull models). / 深度解析：设计信息流（推/拉模式）。

## 🧠 System Design: Key Takeaways / 系统设计要点
1. **Distributed Coordination (分布式协调):** From Snowflake IDs (no coordination) to Web Crawlers (Bloom filters for deduplication), avoiding centralized bottlenecks is key. / 从 Snowflake ID（无需协调）到网络爬虫（使用 Bloom Filter 去重），避免中心化瓶颈是关键。
2. **Asynchronous Processing (异步处理):** Notification systems rely heavily on message queues (Kafka/SQS) to decouple producers from consumers and ensure high availability. / 通知系统严重依赖消息队列（Kafka/SQS）来解耦生产者和消费者，确保高可用性。
3. **Data Structures at Scale (规模化数据结构):** Autocomplete relies on Tries with precomputed Top-K results at each node to guarantee <100ms latency. / 自动补全依赖 Trie 树，并在每个节点预计算 Top-K 结果以保证 <100ms 的延迟。

## 💻 Algorithms: Patterns Mastered / 算法模式总结
- **Sliding Window Finale (滑动窗口收官):** Mastered Monotonic Deque for Sliding Window Maximum (#239) — maintaining a decreasing queue of indices. / 掌握了用于滑动窗口最大值的单调队列——维护递减的索引队列。
- **Stack Pattern (栈模式):** Transitioned to Stacks. Solved Valid Parentheses (#20) for matching, Min Stack (#155) by augmenting elements with `min_so_far`, and Evaluate RPN (#150) for operand evaluation. / 转向栈模式。解决了有效括号（匹配）、最小栈（携带辅助信息）和逆波兰表达式求值（操作数计算）。
- **Key Insight (核心洞察):** Stacks are perfect for "lazy evaluation" — deferring processing until you have enough information (like matching a closing bracket or evaluating an operator). / 栈非常适合“延迟处理”——直到有足够信息（如匹配右括号或计算运算符）才进行处理。

## 🗣️ Soft Skills: What to Practice / 软技能练习重点
- **Scenarios Covered:** Process improvement, designing for scale, conflict resolution, and receiving tough feedback. / 涵盖场景：流程改进，扩展性设计，冲突解决，接受严厉反馈。
- **What Needs Practice:** Transitioning from "I built this" to "I influenced the team to build this." Emphasize data-driven decisions, gathering buy-in (RFCs/ADRs), and showing a growth mindset when facing criticism. / 需要练习：从“我做了这个”转变为“我影响团队做了这个”。强调数据驱动决策、获得团队认可（RFC/ADR）以及在面对批评时展现成长型思维。

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固
- **TypeScript Mastery:** Moved from basic Types/Interfaces to using Generics for reusable logic. / 从基础的 Types/Interfaces 进阶到使用泛型实现逻辑复用。
- **React Integration:** Properly typing Props, Events (`React.ChangeEvent`), and Refs (`useRef<HTMLInputElement>(null)`). / 正确为 Props、事件和 Refs 添加类型。
- **Advanced TS:** Leveraged Utility Types (`Partial`, `Pick`, `Omit`) to keep code DRY, and Type Guards (`is` keyword) for safe union type narrowing. Built a type-safe API client using Generics. / 利用工具类型保持代码 DRY，使用类型守卫安全缩小联合类型。使用泛型构建了类型安全的 API 客户端。

## 🤖 AI: What Stuck / AI 知识点
- **Prompt Engineering & CoT:** "Let's think step by step" forces the LLM to break down complex problems, improving reasoning accuracy. / “让我们一步一步思考”强迫大语言模型拆解复杂问题，提高推理准确率。
- **AI Agents (ReAct):** Agents combine Reasoning and Acting (Goal → Think → Act → Observe). They use tools to interact with the external world. / 智能体结合了推理与行动。它们使用工具与外部世界交互。
- **Industry News:** 据报道，联合国强调人类必须处于 AI 决策中心；美国多州推进 AI 立法（要求披露聊天机器人身份）；PwC 报告指出领先公司正利用 AI 重塑工作流而非仅仅添加工具。 / According to reports, the UN emphasizes humans must remain central to AI decisions; US states are advancing AI legislation; PwC reports leading companies are reinventing workflows with AI.

## ⚠️ What to Review / 需要复习的内容
- **Stack Pop Order:** In Evaluate RPN, remember that `a - b` means popping `b` first, then `a`. / 在逆波兰表达式求值中，记住 `a - b` 意味着先弹出 `b`，再弹出 `a`。
- **System Design Tradeoffs:** Review when to use pull vs. push models in News Feeds, especially handling the "Celebrity Problem". / 复习在信息流中何时使用拉模式 vs 推模式，特别是处理“明星问题”。

## 🏆 Win of the Week / 本周亮点
- Successfully transitioned from Sliding Window to Stack patterns, and built a fully type-safe API client in TypeScript! / 成功从滑动窗口模式过渡到栈模式，并在 TypeScript 中构建了完全类型安全的 API 客户端！

## 🎯 Next Week Preview / 下周预告
- **Algorithms:** Continuing the Stack pattern block (Generate Parentheses, Daily Temperatures). / 继续栈模式（生成括号，每日温度）。
- **System Design:** More distributed system components and data-heavy architectures. / 更多分布式系统组件和重数据架构。
- **Frontend:** Deepening React patterns and performance optimization. / 深化 React 模式和性能优化。