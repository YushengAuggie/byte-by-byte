📅 **Week in Review — Week 15 (10 min read)**
📊 NeetCode: 19/150 · SysDesign: 18/40 · Behavioral: 18/40 · Frontend: 18/50 · AI: 8/30
🔥 21-day streak!

## 🗓️ This Week's Journey / 本周回顾
- **Monday (Day 18):** Rate Limiters, Longest Repeating Character Replacement, Outage Management, Error Boundaries, Vector DBs.
- **Tuesday (Day 19):** URL Shortener, Permutation in String, Quality Assurance, React Server Components, AI News.
- **Wednesday (Day 20):** Review Day (URL Shortener, Sliding Window, RAG).
- **Friday (Day 21):** Key-Value Store, Minimum Window Substring, Saying No, React Forms, Prompt Engineering.
- **Saturday (Deep Dive):** Sliding Window Maximum (Monotonic Queue).

## 🧠 System Design: Key Takeaways / 系统设计要点
1. **限流器 (Rate Limiter):** 保护系统免受突发流量冲击，常放在 API 网关，使用 Redis 存储令牌桶或滑动窗口。 / Protects systems from burst traffic, usually at the API Gateway using Redis.
2. **短链接服务 (URL Shortener):** 核心是自增 ID 转 Base62 编码，配合 302 重定向和缓存。 / Core is auto-increment ID to Base62 encoding, with 302 redirects and caching.
3. **键值存储 (Key-Value Store):** 权衡 CAP 定理，使用一致性哈希分片，以及 LSM Tree 提供极高的写入性能。 / Balancing CAP theorem, using consistent hashing for partitioning, and LSM Trees for high write performance.
**连接点 (Connection):** 它们都需要高可用性和低延迟，Redis 在限流和短链缓存中扮演关键角色，而键值存储本身就是 Redis 的底层原理。 / They all require high availability and low latency; Redis plays a key role in rate limiting and URL shortening caches, while the Key-Value store design explains Redis itself.

## 💻 Algorithms: Patterns Mastered / 算法模式总结
**滑动窗口模式 (Sliding Window Pattern):**
- **#424 Longest Repeating Character Replacement:** 窗口有效性由“最多字符数 + 允许替换数”决定。 / Validity determined by max frequency char + allowed replacements.
- **#567 Permutation in String:** 固定大小窗口，通过频次匹配判断。 / Fixed-size window, checking character frequencies.
- **#76 Minimum Window Substring:** 满足条件时贪心收缩，寻找最短有效窗口。 / Greedily shrinking when valid to find the shortest window.
- **#239 Sliding Window Maximum:** 使用单调队列 (Monotonic Queue) 保持 O(N) 时间复杂度。 / Using a Monotonic Queue to maintain O(N) time complexity.
**核心洞察 (Key Insight):** 右指针负责探索，左指针负责维护约束。根据求最长还是最短，决定是在不满足条件时收缩，还是在满足条件时收缩。 / Right pointer explores, left pointer maintains constraints. Shrink when invalid for "longest", shrink when valid for "shortest".

## 🗣️ Soft Skills: What to Practice / 软技能练习重点
- **生产环境故障 (Production Outages):** 强调先止血 (Mitigation over Investigation) 和无指责复盘 (Blameless Culture)。 / Emphasize mitigation first and blameless post-mortems.
- **保证系统质量 (Ensuring Quality):** 展现系统性思维，通过自动化 (CI/CD) 和文化建设 (Shift-Left) 提升质量。 / Show systems thinking via automation and shift-left culture.
- **拒绝受欢迎的想法 (Saying No to Popular Ideas):** 用数据说话，理解业务压力，并提供务实的替代方案。 / Use data, acknowledge business pressure, and offer pragmatic alternatives.
**需要练习 (Needs Practice):** 如何在面试中自然地表达“替代方案”而不显得生硬。 / How to naturally express "alternative solutions" in interviews without sounding rigid.

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固
- **Error Boundaries & Suspense:** 声明式地处理局部崩溃和异步加载状态。 / Declaratively handle local crashes and async loading states.
- **React Server Components (RSC):** 服务端组件不发送 JS 到浏览器，直接发送渲染好的 UI，大幅减小 Bundle Size。 / Server components send rendered UI, not JS, reducing bundle size.
- **React Forms (受控 vs 非受控):** 需要实时响应用户输入用受控组件，只关心最终提交值用非受控组件。 / Use controlled for real-time input response, uncontrolled for final submit values.
**自测 (Quick Self-Check):** 如果一个组件只需要在提交时获取输入框的值，应该用 `useState` 还是 `useRef`？（答案：`useRef`）。 / If a component only needs the input value on submit, use `useState` or `useRef`? (Answer: `useRef`).

## 🤖 AI: What Stuck / AI 知识点
- **向量数据库 (Vector Databases):** 专为语义搜索设计，存储高维向量并计算相似度。 / Designed for semantic search, storing high-dimensional vectors and computing similarity.
- **Prompt Engineering:** 超越基础提问，使用 Few-Shot、思维链 (Chain-of-Thought) 和结构化输出引导模型。 / Beyond basic prompts: using Few-Shot, Chain-of-Thought, and structured outputs to steer models.
- **AI 资讯 (AI News):** 据报道，科技巨头正在激烈争夺 AI 基础设施人才，Anthropic 签下数十亿美元的算力大单，端侧 AI 正在普及。 / According to reports, tech giants are fiercely competing for AI infrastructure talent, Anthropic signed a multi-billion dollar compute deal, and Edge AI is becoming widespread.
**最重要收获 (Most Important Takeaway):** Prompt engineering 是一门工程化引导概率分布的技术，而不是“哄” AI。 / Prompt engineering is engineering the probability distribution, not "sweet-talking" AI.

## ⚠️ What to Review / 需要复习的内容
- **单调队列 (Monotonic Queue):** 逻辑较绕，需要重新手写一遍 #239 的代码。 / The logic is tricky; need to rewrite the code for #239 from scratch.
- **LSM Tree vs B-Tree:** 键值存储的底层数据结构差异，容易在面试中被深挖。 / The underlying data structure differences in Key-Value stores, often probed deeply in interviews.

## 🏆 Win of the Week / 本周亮点
完成了滑动窗口模式的所有高难度变体（包括两道 Hard 题），并保持了 21 天的连续学习记录！ / Mastered all difficult variants of the Sliding Window pattern (including two Hard problems) and maintained a 21-day streak!

## 🎯 Next Week Preview / 下周预告
- 算法将进入新的模式。 / Algorithms will enter a new pattern.
- 系统设计将继续深入分布式系统组件。 / System Design will dive deeper into distributed system components.