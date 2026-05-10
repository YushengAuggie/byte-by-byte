📅 **Week in Review — Week 9 (10 min read)**
📊 NeetCode: 34/150 · SysDesign: 33/40 · Behavioral: 33/40 · Frontend: 33/50 · AI: 16/30
🔥 39-day streak!

---

## 🗓️ 本周旅程 / This Week's Journey

本周是 Mastery 阶段的第二周（Day 35–39），系统设计冲进复杂现实场景，算法继续深挖二分搜索模式，周六迎来一次深度精讲。

*This was Week 2 of the Mastery Phase (Days 35–39) — system design tackled real-world complex platforms, algorithms continued the binary search deep-dive, and Saturday brought an extended hard-problem breakdown.*

| 日期 | 亮点 |
|------|------|
| **Fri 5/5** | 复习日(Day 35) — 回顾 YouTube/Google Maps/Uber/Google Drive + Binary Search 变体系列 |
| **Mon 5/6** | 电商平台设计·Find Min in Rotated Array·设置技术方向·Memoization Triangle·多模态AI |
| **Tue 5/7** | Ticketmaster 票务·Search in Rotated Array·过度设计的教训·Virtualization·AI新闻(Moonshot/Spotify/xAI) |
| **Wed 5/8** | 支付系统(Stripe)·Time Based KV Store·系统设计权衡·Code Splitting·扩散模型 |
| **Thu 5/9** | 🔬 周六深度精讲：Median of Two Sorted Arrays (LeetCode #4 Hard) — 分布式缓存(Redis) |

---

## 🧠 系统设计：本周要点 / System Design: Key Takeaways

### 1. 现实系统的"三角困局" — 库存 / 锁 / 一致性

本周三道设计题（电商、票务、支付）其实在反复考同一个核心：**高并发写入时如何保证数据一致性而不牺牲性能**。

- **电商（E-Commerce）**：库存超卖是经典难题。Redis `DECR` 原子操作 + 悲观锁（秒杀时 `SELECT FOR UPDATE`）+ 15 分钟订单 TTL 自动释放库存，三层防护缺一不可。
- **票务（Ticketmaster）**：更极端——10万人抢同一张座位。加了**虚拟等候室（Virtual Waiting Room）**，用 Kafka/SQS 削峰，先拿号再进场；座位锁是两阶段：Redis `SETNX` 软锁（10分钟）+ DB `SELECT FOR UPDATE` 硬提交。
- **支付（Stripe）**：最不能出错的系统。核心是**幂等键**（避免重复扣款）+ **双重记账账本**（Double-Entry Ledger）+ **状态机**（PENDING→PAID→SETTLED）。金额永远存整数（分），不用 float。

*These three design problems — e-commerce, ticketing, and payments — all circle back to the same triangle: high-concurrency writes, data consistency, and performance. The layered approach (Redis for speed + DB for truth) is the recurring pattern across all three.*

**连接点 / The Thread:** Redis 做速度缓冲，DB 是最终真相（Source of Truth）。两者分工明确，缺少任何一层都会导致系统崩溃或数据错误。

---

## 💻 算法：模式总结 / Algorithms: Patterns Mastered

### 二分搜索模式 — 4/7 → 7/7 基本完成

本周把整个**二分搜索 Block**（NeetCode 中的连续7道题）基本扫完：

| # | 题目 | 变体模式 | 关键技巧 |
|---|------|---------|---------|
| 4 | #153 Find Min in Rotated | 旋转数组找最小值 | 比 `arr[right]`，用 `right = mid` |
| 5 | #33 Search in Rotated | 旋转数组找target | 先判断哪半有序，再判断目标在哪半 |
| 6 | #981 Time Based KV Store | 找最右满足条件的值 | `result = value; left = mid + 1` 保留候选 |
| 7 | #4 Median of Two Sorted | 分割两数组找中位数 | 搜分割位置而非具体值（Hard深讲） |

**核心规律 / The Pattern:** 所有二分题的本质都是"每次排除一半搜索空间"。变体只是改变了"条件"：找值、找边界、找旋转点、找分割位置……模板不变，条件换换。

*All binary search variants share the same skeleton. The only difference is what condition drives the left/right decision. Once you internalize "which half to eliminate," every variant falls into place.*

---

## 🗣️ 软技能：本周练习重点 / Soft Skills: What to Practice

本周三道 Behavioral 题，级别都偏 Staff：

1. **设置技术方向（Technical Direction）**：Staff 工程师不只是"提出了好想法"，而是数据驱动诊断 → RFC 建立共识 → 处理异议（PoC 证明）→ 量化结果。关键词：跨团队影响力 + multi-quarter 视角。

2. **过度设计（Over-engineering）**：YAGNI 原则。最容易翻车的地方：为假设的未来用户量优化。强回答结构：具体技术细节 + 业务代价（延期/复杂度）+ 根因分析（"我的假设是…实际是…"）+ 改变后的决策框架。

3. **系统设计权衡（Trade-offs）**：PAST 框架（Problem → Alternatives → Selection → Trade-offs）。先问约束，再提方案。主动说出"我选 X 意味着放弃 Y"比等面试官追问更加分。

**最需要练习的 / Most Needs Practice:** 过度设计这题需要一个具体的真实案例，且要能量化业务代价（延期了几周、维护成本如何）。如果还没有现成案例，现在就开始构思一个。

*The over-engineering question is the trickiest — it requires a concrete story with measurable business cost, not just a philosophical lesson. Prepare a real example now.*

---

## 🎨 前端：本周巩固 / Frontend: Concepts to Lock In

本周三个前端主题组成了一个**性能优化三件套**：

**1. React Memoization Triangle（React.memo + useMemo + useCallback）**
- `React.memo` 只做 shallow compare，object/function prop 每次都是新引用 → memo 失效
- `useMemo` 稳定 value 引用，`useCallback` 稳定 function 引用
- **自测：** 什么时候 `React.memo` 不起作用？（答：prop 是 inline object/function 时）

**2. Virtualization（react-window / TanStack Virtual）**
- 核心：只渲染视口内节点，用 spacer 占位撑高度
- 最常见 bug：忘记把 `style` prop 传给每个 Row，导致所有行堆在 top:0
- **自测：** 1万条记录，行高固定，用哪个库？变高行呢？

**3. Code Splitting & Lazy Loading（React.lazy + Suspense）**
- 路由级别拆分收益最大；`lazy()` 必须在模块顶层定义，不能在组件内部
- `Suspense` 必须包裹 `lazy()` 组件，fallback 是加载期间显示的内容
- **自测：** `dynamic(() => import('./C'), { ssr: false })` 中 `ssr: false` 有什么作用？

*These three form a mental model: don't render what you don't see (virtualization), don't load what you don't use (code splitting), and don't re-render what didn't change (memoization). Three angles on the same goal: ship less, compute less, render less.*

---

## 🤖 AI：本周知识点 / AI: What Stuck

**Multimodal AI（多模态AI）**
核心思路：把不同模态（图片、音频、文字）都转换成向量，在同一个嵌入空间里对齐。CLIP 用对比学习做图文对齐；GPT-4o 是原生多模态（不是插件），延迟更低。实际使用注意：图片上的幻觉比文字更严重，特别是小字和数字。

**Diffusion Models（扩散模型）**
两阶段：前向加噪（固定，不学习）→ 反向去噪（神经网络学习每步去掉多少噪声）。Stable Diffusion 的关键优化是**潜在扩散（Latent Diffusion）**——先用 VAE 压缩到 64×64，计算量减少 64 倍。文字引导靠 Classifier-Free Guidance：`guidance_scale` 越大越贴近描述，但多样性降低。

**AI News（据报道）**
- 据报道 Moonshot AI（Kimi）完成 20 亿美元融资，估值 200 亿美元
- 据报道 Spotify 押注 AI 个人化音频，扩展 AI DJ 到多语言
- 据报道 xAI 正转型为 neocloud，向外部客户出租 GPU 算力

**最重要的一个 takeaway / Most Important Takeaway:** 扩散模型的"先破坏再重建"思路——这个反直觉的训练范式（学习加噪的逆过程）是理解生成式AI的关键心智模型。它适用于图片、视频、音频、甚至蛋白质结构预测。

*The "destroy to create" mental model of diffusion is the most transferable insight this week — it's the core paradigm behind image/video/audio generation. Once you understand it, the various architectures (DALL-E, Sora, Stable Diffusion) make intuitive sense.*

---

## ⚠️ 需要复习的内容 / What to Review

**优先级高 / High Priority:**

1. **系统设计 — 支付系统状态机**：能默写出完整状态转移链（`PENDING → PROCESSING → AUTHORIZED → CAPTURED → SETTLED`，以及各种失败和退款分支）吗？实际面试中画这个状态机会很加分。

2. **算法 — LeetCode #4 Hard**：Median of Two Sorted Arrays 的二分分割逻辑非常容易遗忘。边界条件（L1/L2 = -∞，R1/R2 = +∞）是容易出错的地方。至少再做一遍。

3. **前端 — 实战练习**：三个 memoization hook 的使用时机（React.memo / useMemo / useCallback）需要真正手写一个有性能问题的组件再优化，而不只是理解概念。

**次优先级 / Medium Priority:**

4. 票务系统的**两阶段锁**（Redis 软锁 + DB 硬锁）和过期处理逻辑。
5. 软技能：准备一个过度设计的真实故事（含量化代价）。

---

## 🏆 本周亮点 / Win of the Week

**🔬 周六深度精讲 — LeetCode #4 Median of Two Sorted Arrays**

这道 Hard 题是整个 NeetCode 150 里公认最难的二分之一。完整精讲了从 O(m+n) 暴力解法到 O(log(min(m,n))) 最优解的完整思路演变——核心洞见是"搜索分割位置，而不是搜索具体值"。这是一个彻底的心智模型转变，掌握了它才算真正理解二分搜索的上限。

能完整读完这道题的精讲，本身就是一个值得庆祝的里程碑 🎉

*Finishing the full deep-dive on LeetCode #4 is legitimately impressive — this problem trips up even experienced engineers. The key insight (search for the partition, not the value) represents a fundamental upgrade in how you think about binary search. That's a real milestone.*

---

## 🎯 下周预告 / Next Week Preview

基于当前进度（Day 39，即将进入 Day 40+），下周将继续 Mastery 阶段：

**系统设计（SysDesign: 33→36+）**
- 预计进入：Design a Social Media Feed（Twitter/Instagram）、Design a Live Streaming System、Design a Distributed Message Queue

**算法（NeetCode: 34→37+）**
- 进入新模块：**Linked List**（NeetCode Block）
- 从 Reverse Linked List 开始，逐步到 LRU Cache

**前端（Frontend: 33→36+）**
- 预计主题：JavaScript 引擎工作原理、Web Security（XSS/CSRF）、Service Workers & PWA

**AI（AI: 16→18+）**
- 将进入：Fine-tuning in Practice 或 AI Infrastructure

**🔥 当前连击：39天！** 继续保持！

*Next week dives deeper into large-scale distributed systems design and starts the Linked List algorithm block. The 40-day milestone is right around the corner — keep the streak alive!*
