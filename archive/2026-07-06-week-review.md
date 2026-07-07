📅 **Week in Review — Week 28 (10 min read)**
📊 NeetCode: 67/150 · SysDesign: 64/40 · Behavioral: 64/40 · Frontend: 37/50 · AI: 30/30
🔥 坚持精进，复合成长！

---

## 🗓️ 本周回顾 / This Week's Journey

| 日期 / Date | 主题摘要 / Summary |
|------------|-------------------|
| 周一 Jun 30 (Day 78) | AI 聊天平台深度拆解；Word Search II（Trie + DFS 终极 Boss）；连接池实战；AGI 与新兴架构 |
| 周二 Jul 1 (Day 79) | ChatGPT 规模架构（流式+KV Cache）；Heap 新模式 — Kth Largest in Stream；Retry with Backoff；AI 新闻：GPT-5.6 + Fable 5 复出 |
| 周三 Jul 2 (Day 80) | 📚 复习日 — Trie + DFS、连接池与重试的正确分层、AI Chatbot 流式架构 |
| 周四 Jul 3 (Day 81) | AI 聊天平台第三遍巩固；Last Stone Weight（Max-Heap 模拟）；Circuit Breaker 保护下游；AI 监管新动态 |
| 周六 Jul 6 (Day 82+83) | 🔬 Saturday Deep Dive：堆专题（K Closest + 数据流中位数）；专家级综合：多系统共存架构 + 技术债三方博弈 + Rate Limiting 实现 |

---

## 🧠 系统设计：核心要点 / System Design: Key Takeaways

本周系统设计以 **AI 推理系统**为主线，并以一节专家级综合收尾。

**1. 流式输出是 LLM 系统的第一原则 / Streaming is non-negotiable for LLM systems**

- SSE（Server-Sent Events）单向流，CDN 友好，自带断线重连 — 比 WebSocket 更适合 LLM 推理的单向输出场景
- Continuous Batching（vLLM）：GPU 利用率从 30% → 80%+，这是 AI 系统降本的核心杠杆
- Prefix KV Cache：对系统 prompt 的 attention key/value 预计算缓存，节省 ~20% 推理计算量

**2. Session Affinity + 分层存储 / Session Routing + Tiered Storage**

- 用 `conversation_id` 做 Consistent Hashing，而不是 round-robin — 保证同一对话命中同一 GPU 上的 KV Cache
- 分层存储策略：Redis（24h 热数据）→ PostgreSQL（30 天温数据）→ S3（历史冷数据）

**3. 多系统共存的架构原则（Expert Synthesis）/ Multi-System Architecture Principles**

三条跨系统设计的铁律：
- **按一致性需求划分数据边界** — 支付系统（强一致性 ACID）绝不能与聊天/视频（最终一致性 Kafka）共用数据库
- **共享无状态层，隔离有状态层** — API Gateway / Auth / CDN 可以共享；数据库和 Redis 必须隔离 key namespace
- **故障域隔离（Bulkhead）** — 每个系统独立连接池，Chat 流量洪峰不影响 Payment 可用性

**三者的联系**：LLM 推理系统本身就是一个极致的"读路径优化"案例 —— KV Cache、模型路由、SSE 流式，都是在已知 GPU 是唯一瓶颈的前提下，把整条链路的效率压榨到极限。这和 Autocomplete 系统的设计哲学（读多写少、内存优先）是同一类思维。

---

## 💻 算法：模式总结 / Algorithms: Patterns Mastered

本周完整开启了 **Heap / Priority Queue** 模式块（7 题），并用 Saturday Deep Dive 做了系统深挖。

### 堆模式核心模版 / Core Template

```python
import heapq

heap = []
for item in stream:
    heapq.heappush(heap, item)
    if len(heap) > k:
        heapq.heappop(heap)
# heap[0] is the kth largest
```

| 题目 | 变化点 | 关键洞察 |
|------|--------|---------|
| #703 Kth Largest in Stream (Day 79) | 基础模版，min-heap 大小为 k | 堆顶 = 第 k 大的门槛 |
| #1046 Last Stone Weight (Day 81) | Max-heap（取反），每次 pop 2 个 | Python 无 max-heap，全部取反模拟 |
| #973 K Closest Points (Day 83) | Key 是派生指标（距离），非原始值 | skip sqrt — 距离单调，不影响排序 |
| #212 Word Search II (Day 78) | Trie + DFS 终章 | 找到单词后**删除 Trie 叶节点**是关键剪枝优化 |

**Week 28 最重要的算法洞察**：

Word Search II 的核心优化 —— 在 DFS 找到单词后，从 Trie 删除该叶节点（`del node.children[ch]`）。这让 Trie 随着搜索过程越来越小，后续剪枝越来越激进。这是一个"搜索过程中动态优化搜索结构"的经典技巧。

---

## 🗣️ 软技能：重点练习 / Soft Skills: What to Practice

本周软技能聚焦在同一个高频题上：**招聘与团队建设（Hiring & Growing a Team）**，并以周末的复合压力综合场景收尾。

**核心分级框架 / Leveling Framework:**

```
Junior: "我做了 X 次面试"
Senior: "我设计了面试流程，效率提升了 Y%"
Staff:  "我建立了跨团队可复用的招聘框架，并 mentor 了 3 个面试官"
```

**本周提炼的三个关键信号（面试中要体现）:**
1. **系统化，不只是个案** — 说"我建立了结构化 rubric 和 onboarding checklist"，而不是"我帮了某个新人"
2. **量化结果** — Offer 接受率从 40% → 68%、新人 2.5 个月独立上手（vs 行业平均 4-5 个月）
3. **乘数效应思维** — 你的一次投入，让整个团队未来几年都更强

**复合压力场景（Expert Synthesis）的核心框架:**

技术债 + 团队士气 + 业务压力同时来袭时，最强的 Staff 级回答不是"我解决了一个难题"，而是"**我改变了问题被处理的方式**"：
- 量化损失（"上季度浪费了 9 工程师周"）→ 说服 PM 和 CTO
- 建立可持续机制（每个 Sprint 20% 时间还技术债）
- 让进度可见（技术健康仪表盘：部署时间、P99、覆盖率）

**需要继续练习的场景**: 招聘故事需要更具体的数字和结构。建议准备一个完整的 STAR 稿，包含明确的 Situation 规模、Action 的三个具体步骤、以及两个量化 Result。

---

## 🎨 前端（Python Craft）：知识巩固 / Python Craft: Concepts to Lock In

本周 Python Craft 完成了"弹性模式"三件套，是后端工程实战中最高频使用的组合：

**三件套总览 / The Resilience Trio:**

| 模式 | 解决的问题 | 关键参数 |
|------|-----------|---------|
| **Connection Pooling** (Day 78) | TCP 握手重复开销（50-200ms × QPS） | `pool_size`, `max_overflow`, `pool_recycle` + `pool_pre_ping` |
| **Retry with Backoff** (Day 79) | 瞬态失败（网络抖动、429、5xx） | `tenacity`：`wait_exponential` + `retry_if_exception_type` |
| **Circuit Breaker** (Day 81) | 下游雪崩（超时堆积 → 级联崩溃） | 三状态：CLOSED → OPEN → HALF-OPEN |

**正确的分层顺序** (Day 80 复习题的核心洞察)：
```
Retry (外层) 
  └─ Connection Pool (内层)
       └─ 实际请求
```
Retry 包裹 Pool —— 失败时重新从池里借连接，而不是重试拿连接的动作。

**Rate Limiting 实现（Day 83）— 快速自检：**
- Token Bucket：允许突发（burst），O(1) 内存，适合有合法流量峰值的 API
- Sliding Window Log：精确，O(requests) 内存，适合严格 per-user 限制
- 分布式版本：Redis sorted set + pipeline（原子性 + 低延迟）
- 记住：只重试 5xx + 429，**绝不重试 4xx**

---

## 🤖 AI：本周知识点 / AI: What Stuck

本周 AI 内容跨越了两个维度：**架构前沿**（Day 78）和**行业监管新动态**（Day 79, 81, 83）。

**架构前沿 / Architecture Frontier (Day 78 — CONCEPT)**

三个正在重塑 AI 推理的新兴方向：
- **State Space Models (Mamba)**：O(N²) attention → O(N) linear recurrence，长序列场景的计算效率革命
- **Mixture of Experts (MoE)**：GPT-4 据报道是 MoE 架构（8 专家，每次激活 2 个）—— 参数量大、推理计算小
- **Test-Time Compute Scaling**：o1/o3/DeepSeek-R1 的核心思路 —— 难题多给思考时间，而不是只追求更大的模型

*注意：GPT-4 MoE 架构细节系据报道（据报道），非 OpenAI 官方确认。*

**AI 监管加速 / Regulatory Acceleration (Day 79, 81, 83 — NEWS)**

本周最值得工程师关注的趋势 — 据报道：
- GPT-5.6 Sol/Terra/Luna 以"政府审查先行"模式发布，~20 家机构优先访问，标志着前沿模型发布节奏正在制度化（据报道来自 The Next Web 等来源）
- Anthropic Claude Fable 5 因出口管制审查暂停 19 天后复出，新增安全分类器（据报道）
- Illinois 签署 AI 安全措施法；加州、纽约已有类似立法 —— 美国 AI 合规正从联邦缺位走向州级竞赛
- **工程师的实际含义**：前沿 API 访问不再稳定，需要 fallback 模型策略；"release day" ≠ "available day"

---

## ⚠️ 需要复习的内容 / What to Review

**最弱的区域 / Weakest Areas:**

1. **Heap 变体的细节区分** — 三道题看起来相似，但 Key 的含义完全不同：原始值 vs 派生距离 vs 需要返回原始点。建议对比 #703 / #1046 / #973 的代码结构，手写一遍模版变体。

2. **软技能：招聘故事结构化** — 连续三天（Day 78/79/81）都是同一个问题。趁热打铁，现在花 30 分钟准备一个完整 STAR 稿。特别注意 Action 要分 3 个具体步骤，Result 要有 2+ 个量化指标。

3. **Rate Limiting 算法的使用场景** — Token Bucket vs Sliding Window Log vs Sliding Window Counter 的选择逻辑，尤其是"什么时候需要允许 burst"这个判断点，值得再过一遍。

4. **系统设计：一致性边界** — Expert Synthesis 中"支付系统必须隔离"的直觉很重要。下次碰到 multi-system 设计题，第一个问题要是"哪个子系统对一致性要求最强？"

**具体建议 / Specific Next Steps:**
- 在 30 分钟内手写 #973 K Closest Points 的完整解法（含 trace）
- 准备招聘 STAR 故事稿（目标：2 分钟讲完，含 3 个 Action 和 2 个数字 Result）

---

## 🏆 本周亮点 / Win of the Week

**Week 28 的最大亮点：AI 专题知识体系完整收官。**

AI 模块（aiTopicIndex: 30/30）在本周正式画上句号，从最早的 Transformer 工作原理、Tokenization、Embeddings，到 RAG、Vector Databases、MoE，再到 AI Agents、Test-Time Compute、以及本周的 AGI 争论与监管新格局 —— 30 个 AI 话题形成了一条清晰的技术认知链。

加上 Saturday Deep Dive 完整攻克堆专题（K Closest + 数据流中位数双堆），以及 Expert Synthesis 将系统设计、软技能、Python Craft 三条线整合成一个完整的 Staff Engineer 思维框架 ——

**这是整个 byte-by-byte 旅程中内容密度最高的一周。** 🎯

---

## 🎯 下周预告 / Next Week Preview

根据当前进度（Day 83，Expert 阶段），下周将继续 Heap 模式块剩余题目，并开始 Greedy 或 Dynamic Programming 等新算法模式：

- **算法** — Heap 剩余 4 题：#215 Kth Largest in Array、#621 Task Scheduler、#355 Design Twitter、#295 Find Median from Data Stream（双堆经典 Boss 战）
- **系统设计** — Expert 阶段后续深化，可能包括更多分布式系统专题
- **Python Craft** — 新的工程模式块开启（Week 8 预计进入 Testing 或 Observability 主题）
- **软技能** — 新一轮行为问题（可能涵盖"技术决策复盘"或"跨团队对齐"场景）

**特别关注**：#295 Find Median from Data Stream 是 Heap 模式块的终极 Boss，双堆设计是面试高频考点，值得提前预习 NeetCode 视频。

---

*Byte by byte, week by week. 🚀*
