📅 **Week in Review — Week 3 (10 min read)**
📊 Day 17/150 · NeetCode: 16/150 · SysDesign: 15/40 · Behavioral: 15/40 · Frontend: 15/50 · AI: 7/30
🔥 5-day streak!

## 🗓️ This Week's Journey / 本周回顾
- **Tue 3/31 (Day 14):** 微服务 vs 单体架构 (Microservices vs Monolith), Trapping Rain Water, 跨团队项目领导力, React Custom Hooks, LoRA & QLoRA.
- **Wed 4/1 (Day 15):** 📝 阶段复习日 (Review Day 15) — 巩固一致性哈希、CAP定理、双指针与 React Hooks.
- **Thu 4/2 (Day 16):** API Gateway & Service Mesh, 股票买卖 (Sliding Window 起步), 技术债处理, React Context, RAG.
- **Fri 4/3 (Day 17):** Rate Limiting & Throttling, 无重复字符的最长子串, 快速学习新技术, React Composition, AI News.
- **Sat 4/4 (Deep Dive):** 🔬 深度解析：Rate Limiting & Throttling (四大限流算法与 Redis 分布式实现).

## 🧠 System Design: Key Takeaways / 系统设计要点
**1. 微服务架构演进 (Microservices vs Monolith)**
单体架构适合早期快速开发，微服务适合团队和流量规模化后的独立扩展。不要过早微服务化，避免陷入"分布式单体"的陷阱。
**2. 流量治理 (API Gateway & Service Mesh)**
API Gateway 负责"南北流量"（外部入口的认证、限流、路由），Service Mesh 负责"东西流量"（内部服务间的 mTLS、熔断、可观测性）。两者结合构成完整的微服务网络抽象。
**3. 流量保护 (Rate Limiting & Throttling)**
四大算法：Fixed Window（有边界突破缺陷）、Sliding Window Log（精确但耗内存）、Sliding Window Counter（工程最常用折中）、Token Bucket（支持突发流量，生产最常用）。
**连接点 / What connects them:** 当系统从单体拆分为微服务时，直接暴露内部服务会引发混乱，因此引入 API Gateway 统一入口；而为了防止外部恶意流量或突发流量击垮网关和后端，必须在网关层实现 Rate Limiting。

## 💻 Algorithms: Patterns Mastered / 算法模式总结
**1. Two Pointers (双指针收官)**
- *Trapping Rain Water (#42)*: 核心洞察是每个位置的积水由左右两侧最高柱子的最小值决定。双指针从两端向中间逼近，哪侧的 max 较小就结算哪侧。
**2. Sliding Window (滑动窗口开启)**
- *Best Time to Buy and Sell Stock (#121)*: 最简滑动窗口，只需追踪历史最小值（买入点），不断用当前值（卖出点）更新最大利润。
- *Longest Substring Without Repeating Characters (#3)*: 窗口内维护一个字符集合（Set/Map）。右指针不断扩张，一旦遇到重复字符，左指针持续收缩直到重复字符被移出窗口。
**Key Insight:** 双指针通常用于"夹逼"寻找最优解，而滑动窗口用于在连续子数组/子串中维护一个特定约束（如无重复字符），右指针探索，左指针维护合法性。

## 🗣️ Soft Skills: What to Practice / 软技能练习重点
- **跨团队项目 (Cross-team initiatives):** 重点在于对齐目标（North-star metric）、可视化依赖、建立沟通节奏和前置风险。
- **处理技术债 (Handling technical debt):** 永远先用数据量化痛苦（如 incident 耗时），提出渐进式重构方案（Strangler Fig 模式），并争取 20% 的 sprint capacity。
- **快速学习新技术 (Adaptability):** 展示系统性学习策略（Mental model → 最小可用知识 → 实战），强调 trade-off（快速上手解决问题而非盲目追求精通）。
**Needs Practice:** 量化技术债的影响。在面试中，很容易泛泛而谈"代码很乱"，需要练习用具体的工时浪费或事故频率来构建商业 case。

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固
- **Custom Hooks:** 提取可复用的状态与副作用逻辑（如 `useJsonFetch`），注意使用 `AbortController` 清理请求。
- **React Context:** 解决 Prop Drilling 的利器，适合"读多写少"的全局状态（如主题、用户信息）。避免把频繁变化的值放入 Context 以防全量重渲染。
- **React Composition:** 使用 `children` props 封装容器，使用 Render Props 注入数据，使用 HOC 封装横切关注点（如权限校验）。
**Quick self-check:** 你的 Custom Hook 是否正确处理了组件卸载时的竞态条件？你的 Context Provider 是否被过度使用导致性能瓶颈？

## 🤖 AI: What Stuck / AI 知识点
- **LoRA & QLoRA:** 高效微调技术。LoRA 冻结原模型，只训练低秩适配器矩阵；QLoRA 进一步量化基座模型，极大降低显存需求。
- **RAG (Retrieval Augmented Generation):** 解决 LLM 幻觉和知识滞后的核心架构。先在向量数据库中检索相关文档片段，再将其作为上下文喂给 LLM 生成答案。
- **AI News:** 据报道，OpenAI 收购了科技脱口秀 TBPN 进军媒体；据报道，Google 为 Gemini API 增加了 Flex 推理分层以控制成本；据报道，TurboQuant 技术可将大模型推理内存压缩 6 倍；据报道，Noah Labs 的 Vox 获 FDA 认定，可用 5 秒语音筛查心衰。

## ⚠️ What to Review / 需要复习的内容
- **Sliding Window 的收缩逻辑:** 熟练掌握 `while` 循环内部左指针的移动条件，以及如何用 HashMap 优化跳跃。
- **Token Bucket 算法实现:** 深刻理解令牌桶为什么能应对突发流量（Burst），并在白板上写出基于时间戳的懒加载补充令牌逻辑。

## 🏆 Win of the Week / 本周亮点
成功攻克了经典的 Hard 题 Trapping Rain Water，并顺利从双指针模式过渡到滑动窗口模式。同时，在 Saturday Deep Dive 中彻底吃透了 Rate Limiting 的底层算法和 Redis 生产级实现。

## 🎯 Next Week Preview / 下周预告
- **SysDesign:** 深入分布式系统的更多组件，如 CDN、消息队列进阶与一致性协议。
- **Algorithms:** 继续深耕 Sliding Window 模式，挑战更复杂的频率统计与窗口约束（如 Minimum Window Substring）。
- **Frontend:** 探索 React 性能优化（useMemo/useCallback）与高级状态管理。