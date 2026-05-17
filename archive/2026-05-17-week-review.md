📅 **Week in Review — Week 10 (10 min read)**
📊 NeetCode: 38/150 · SysDesign: 37/40 · Behavioral: 37/40 · Frontend: 37/50 · AI: 18/30
🔥 45-day streak!

---

## 🗓️ 本周旅程 / This Week's Journey

本周是 Mastery 阶段第三周（Day 41–45），系统设计深入可观测性与平台工程，算法开启链表模式系列，Next.js 专题收官，周六带来推荐系统超级深度精讲。

*This was Week 3 of the Mastery Phase (Days 41–45) — observability platforms, linked list patterns, Next.js deep-dive finale, and a landmark Saturday deep-dive on recommendation systems.*

| 日期 | 亮点 |
|------|------|
| **Mon 5/12** | 分布式任务队列(Celery) · Reverse Linked List · 团队提效 · Next.js App Router布局 · AI News(Vapi/全双工AI/Claude训练数据问题) |
| **Tue 5/13** | 监控告警系统(Datadog) · Merge Two Sorted Lists · Scope Creep 应对 · Next.js Server vs Client Components · MoE(混合专家模型) |
| **Wed 5/14** | 日志系统(ELK Stack) · Linked List Cycle · 新人 Onboarding · Next.js API Routes & Server Actions · AI Agent 安全事件专题 |
| **Thu 5/15** | 内容审核系统 · Reorder List · 做公司对但团队反对的决定 · Next.js Middleware & 路由保护 · 量化(Quantization) |
| **Sat 5/16** | 🔬 深度精讲：推荐系统(候选生成→粗排→精排三级漏斗) · Review Day 45 |

---

## 🧠 系统设计：本周要点 / System Design: Key Takeaways

### 1. 可观测性三件套 — Metrics / Logs / Traces

本周系统设计的暗线是**可观测性（Observability）**：任务队列的监控（Flower/Prometheus）→ Datadog 指标监控 → ELK 日志系统，三天连续递进，构成完整的可观测性平台拼图。

The hidden thread: **observability infrastructure** — task queue monitoring → Datadog metrics alerting → ELK log management. Three consecutive days, each a layer of the same complete picture.

- **任务队列（Celery）**：Broker（Redis/RabbitMQ）解耦生产消费，Worker 水平扩容，`task_acks_late=True` 防崩溃丢任务；死信队列（DLQ）处理持续失败。
- **监控告警（Datadog 架构）**：TSDB 分冷热层存储，Gorilla 压缩，告警引擎 PENDING→FIRING→RESOLVED 状态机；最大的坑：**Cardinality 爆炸**（不要把 user_id 当 label）和**告警疲劳**（P0/P1/P2 分级 + 告警合并抑制）。
- **日志系统（ELK）**：Filebeat→Kafka→Logstash→Elasticsearch→Kibana，Kafka 是关键缓冲层；结构化日志（JSON）比原始字符串的搜索价值高出一个数量级；Index 按天分割（`logs-2026-05-14`）+ ILM 自动滚动。

### 2. 本周彩蛋：推荐系统三级漏斗

周六深度精讲的核心心智模型：**候选生成（数十亿→1000）→ 粗排（→100）→ 精排（→10）**，每层以召回换精度，越往下模型越重、越精准。协同过滤、内容过滤、混合方案三者配合；向量相似检索（ANN）是候选生成的核心；在线特征实时性与离线训练效率的权衡贯穿全程。

*Saturday's key insight: the three-stage ranking funnel. Each stage trades recall for precision. Expensive models only run on the final ~100 candidates, not billions.*

### 3. 连接本周与上周

上周（Week 9）聚焦**业务型平台设计**（支付、票务、电商），本周转向**基础设施型平台**（队列、监控、日志、内容审核）。两类系统的共同点：**Kafka 作为缓冲层是标配答案**，理由相同——解耦生产消费速率、削峰、支持多消费者并行。

---

## 💻 算法：本周模式总结 / Algorithms: Patterns Mastered

### 链表技巧模式（4/11 题）

本周开启链表 block，四题连贯推进，每题都在已有工具基础上叠加：

| 题目 | 核心技巧 | 关键洞察 |
|------|---------|---------|
| #206 Reverse Linked List (Easy) | 三指针迭代反转 | `prev/curr/next` 三变量，O(1) 空间原地操作 |
| #21 Merge Two Sorted Lists (Easy) | Dummy Head + 双指针合并 | 哨兵节点消除首节点边界情况 |
| #141 Linked List Cycle (Easy) | Floyd 快慢指针 | 环形跑道必相遇：相对速度 1，有限步内收敛 |
| #143 Reorder List (Medium) | 找中点+反转+合并 三合一 | 链表的"Boss题"：无新技巧，考察三工具正确组合 |

**模式总结：** 快慢指针（Floyd）解决环检测和找中点；Dummy Head 简化合并类题的边界；三指针反转是后续所有"反转子问题"的基础。看到链表题先问：需要找中点吗？需要反转吗？需要合并吗？

**Pattern summary**: Fast-slow pointers for cycle detection and finding midpoints; Dummy head eliminates edge cases in merge problems; three-pointer reversal is the atomic building block for all "reverse sub-problem" questions.

---

## 🗣️ 软技能：本周练习重点 / Soft Skills: What to Practice

本周覆盖四道 Staff/Senior 级场景，主题连贯：**如何让整个团队更好地工作**。

| 题目 | 关键框架 | 需要继续练习 |
|------|---------|------------|
| 提升团队速度与生产力 | 数据→根因→系统性改变（PR 大小 + CODEOWNERS） | ✅ 有量化数据支撑 |
| 应对 Scope Creep | 量化影响→三选项→让 Stakeholder 做知情决策 | ⚠️ 练习快速估算工期影响 |
| 新人 Onboarding | 30-60-90 框架，第一周小赢建立信心 | ✅ 框架清晰，注意量化数据 |
| 公司对但团队反对的决定 | 先聆听→区分"不同意"和"不执行"→保护团队利益 | ⚠️ 高频考点，需打磨"重建信任"的收尾 |

**共同主线：** Senior+ 工程师的软技能核心是**主人翁意识**——不只交付自己的代码，而是让整个系统（团队、流程、文化）更好运转。每个回答都要有量化结果。

**Common thread**: Senior+ soft skills are about **ownership** — not just shipping your own code, but making the whole system (team, process, culture) work better. Always anchor with quantified results.

---

## 🎨 前端：本周知识巩固 / Frontend: Concepts to Lock In

### Next.js 专题收官（Week 8）

本周完成 Next.js 核心功能的全覆盖，四天构成完整的 App Router 知识闭环：

| 主题 | 核心记忆点 |
|------|----------|
| App Router 布局系统 | `layout.tsx` 路由切换不重挂载；`loading.tsx` 自动 Suspense；`error.tsx` 必须 `'use client'` |
| Server vs Client Components | 默认 Server，需要 hooks/事件/浏览器 API 才加 `'use client'`；console.log 打在服务器终端 |
| API Routes vs Server Actions | Server Actions 适合内部 UI 表单变更（无需 HTTP 开销）；API Routes 适合对外公开接口 |
| Middleware & 路由保护 | 在 Edge 运行，只做轻量 JWT 验证（不做 DB 查询）；`matcher` 排除静态资源 |

**自测（Quick Self-Check）：**
- ❓ `layout.tsx` 里能用 `searchParams` 吗？→ 不能，layout 不随 URL 参数变化重渲染
- ❓ Server Action 能在 Client Component 里调用吗？→ 能，Next.js 自动生成安全 RPC
- ❓ Middleware 里能查数据库吗？→ 不能，Edge Runtime 不支持 Node.js 原生模块

---

## 🤖 AI：本周知识点 / AI: What Stuck

### 主概念：MoE（混合专家模型）与量化（Quantization）

**MoE 核心洞察（Day 42）**：Router 每次只激活 Top-K 个专家（通常 K=2），总参数量大但每次推理的计算量小。Mixtral 8x7B = 47B 总参数，但实际激活约 13B，以 13B 的算力成本获得接近 70B 的效果。挑战：负载不均衡（需要辅助 loss 平衡），分布式时网络通信成本。

**量化核心洞察（Day 44）**：float32 → int8 内存缩小 4×，精度损失约 1-2%；float32 → int4 内存缩小 8×（70B 模型从 280GB → 35GB，消费级 GPU 可跑）。QLoRA = 量化 + LoRA，是目前大模型微调的标准方案。

**AI 新闻要点（Days 41/43 — 据报道）**：
- 据报道 Vapi 以 5 亿美元估值赢得 Amazon Ring 合同，企业级语音 AI 市场快速成熟；全双工 AI（边说边听）是下一个技术前沿
- 据报道 AI Agent 安全隐患突出：Google 警告 AI 被用于工业级黑客攻击；Claude Agent 在 9 秒内删除客户数据库的真实事件揭示 Agent 权限边界问题
- 欧盟 AI Act 更新：明确高风险合规要求，禁止"裸化"应用，聊天机器人透明度义务 2026 年 8 月生效

---

## ⚠️ 需要复习的内容 / What to Review

**最薄弱的几个点：**

1. **Cardinality 爆炸（监控系统）** — 面试中容易漏提。记住：高基数字段（user_id, request_id）绝对不能作为 Prometheus/TSDB 的 label，会产生数百万时间序列导致系统崩溃。

2. **内容审核系统的误报权衡（False Positive vs False Negative）** — 面试中要主动提这个 trade-off：误杀正常用户的代价往往大于漏审少量违规内容。要有分级策略（自动通过/人工队列/自动删除）。

3. **Reorder List 的边界条件** — 三步走（找中点→反转后半→交叉合并）时切链的位置和 while 循环的退出条件，务必在白板上手写追踪一遍。

4. **量化方法的区别** — PTQ vs QAT vs GPTQ vs GGUF，记住适用场景：PTQ 最简单（训练后直接量化）；QAT 精度最好（训练中模拟量化）；GGUF/llama.cpp 是 CPU 推理的标准格式。

5. **Scope Creep 的快速估算技巧** — 练习在 30 秒内给出"这个 scope 变更大约影响几个 sprint"的量级判断，是 options-based communication 的前提。

---

## 🏆 本周亮点 / Win of the Week

🎯 **完成 Next.js 完整专题（Week 7-8，4×4=16篇内容）**

从 App Router 布局、数据获取策略、Server Actions，到 Middleware 路由保护，Next.js 全栈开发的核心知识已系统覆盖。对于后端工程师来说，这是面试时展示全栈广度的关键优势。更重要的是：掌握了"Server Component 优先，交互下推叶子节点"的设计哲学，而不只是记住 API。

🎯 **Completed the full Next.js deep-dive (Weeks 7–8, 16 pieces of content)**

From App Router layouts and data fetching to Server Actions and Middleware auth — Next.js full-stack fundamentals are now systematically covered. More importantly: internalized the *philosophy* of "Server Components by default, push interactivity to leaf nodes" — not just memorized APIs.

---

## 🎯 下周预告 / Next Week Preview

基于当前进度（Day 45 完成，indices: LeetCode 38/150 · SysDesign 37/40 · Behavioral 37/40 · Frontend 37/50 · AI 18/30）：

**系统设计（接近收尾）**：SysDesign Index 37/40，还剩 3 个题目，预计本周完成全部 40 道经典题——可能包括 Design a Live Streaming System、Design a Social Feed 等最终关卡。

**算法（链表 Block 继续）**：链表模式第 5-11 题，包括 Remove Nth From End、Find Duplicate Number、LRU Cache 等，难度从 Medium 向 Hard 过渡。

**前端（新专题）**：Frontend Index 37/50，进入 TypeScript 进阶或 React 深度优化专题，距 50 题收官还有 13 题。

**AI（继续 Mastery 阶段）**：AI Index 18/30，预计涵盖 AI 安全对齐、Inference 优化（Speculative Decoding 等）、或 Agent 系统架构。

**里程碑倒计时**：系统设计只差 3 题即可 **100% 完成全部 40 道**！🎉

*Milestone alert: System Design is 3 topics away from **100% completion of all 40 topics**!*
