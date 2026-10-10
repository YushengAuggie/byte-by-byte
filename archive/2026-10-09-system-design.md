# 🏗️ 系统设计 / System Design — Day 137 (Synthesis)
## LLM 应用后端架构全景：把 60 个系统设计主题整合在一起
## Building an LLM Application Backend: Tying All 60 Topics Together

> **综合模式 / Synthesis Mode** — 回顾过去 60 个主题，看它们如何在一个真实的 AI 产品后端中协同工作。

---

### 🎬 真实场景 / Real-World Scenario

想象你在设计一个 **AI 编程助手**（类似 Cursor 或 GitHub Copilot Chat）的后端。用户在 IDE 里问问题，你的系统要在 200ms 内返回代码建议。这个系统需要用到过去 60 天学过的几乎每一个模块。

*Imagine you're designing the backend for an AI coding assistant (like Cursor or GitHub Copilot). Users ask questions in their IDE; your system must return code suggestions within 200ms. This system touches almost every topic from the past 60 days.*

---

### 🏛️ 架构全图 / Architecture Overview

```
User IDE Plugin
      │  (WebSocket / SSE)
      ▼
[API Gateway + Auth]        ← Rate Limiter (Token Bucket, per user/org)
      │
      ▼
[LLM Orchestrator Service]  ← Message Queue for async jobs
      │           │
      ▼           ▼
[Context Builder]    [Cache Layer - Redis]
  (RAG pipeline)       (semantic cache: same question → skip LLM)
      │
      ▼
[Vector DB]          ← User's codebase indexed as embeddings
(Pinecone/pgvector)
      │
      ▼
[LLM API Pool]       ← Load Balancer + circuit breaker per provider
(OpenAI / Anthropic)
      │
      ▼
[Response Streamer]  ← Chunked SSE back to IDE
      │
      ▼
[Observability Stack]
(Distributed Tracing + Structured Logs + Metrics)
```

---

### 🔑 关键权衡 / Key Tradeoffs

**延迟 vs 成本 / Latency vs Cost**
- **语义缓存 / Semantic cache**：LLM 调用 $0.01/请求，缓存命中 $0.0001。对相似（非完全相同）的问题使用向量相似度检索缓存结果。覆盖率 ~30-40%，能显著降低成本。
- **流式响应 / Streaming**：不等待完整结果，SSE 流式推送 token，TTFB（首字节时间）从 2s 降到 200ms。

**可用性 / Availability**
- **Circuit breaker per LLM provider**：如果 OpenAI 超时率 > 5%，自动切换到 Anthropic fallback。
- **Multi-region active-active**：用户在哪个区域，就从哪个区域的向量 DB 检索，减少跨洋延迟。

**一致性 / Consistency**
- 用户的代码库索引是**最终一致**的 — 文件保存后异步更新向量 DB。对于编程助手来说，几秒的滞后是可接受的（用 Eventual Consistency）。

---

### 🚫 别踩这个坑 / Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| 每次请求都调 LLM，不缓存 | 先查语义缓存 → 再调 LLM |
| 同步等待 LLM 完整响应 | SSE/WebSocket 流式返回 |
| 单一 LLM Provider，无 fallback | Circuit breaker + 多 Provider |
| 不限速，被滥用爆成本 | Token bucket per user，org-level burst |
| 全量代码库塞进 prompt | RAG：只检索最相关的 top-k chunks |

---

### 🧩 模块映射 / Module Map

这个系统用到了过去 60 天的哪些主题？

- **API Gateway + Rate Limiter** → Day 16, 17, 18, 67
- **Load Balancing** → Day 4
- **Caching (Redis, Semantic Cache)** → Day 6, 21
- **Message Queue** → Day 13
- **Vector DB (RAG)** → Day 18's AI section
- **Distributed Tracing** → Day 68
- **Circuit Breaker** → Day 81's Python Craft
- **CDN (serving static IDE plugin assets)** → Day 64
- **Multi-region Active-Active** → Day 54

> 这就是为什么系统设计没有"孤立"的主题。真实系统永远是这些模块的组合。
> 
> *This is why system design has no "isolated" topics. Real systems are always combinations of these building blocks.*

---

### 📚 参考资料 / References

- [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832)
- [Building LLM Applications for Production – Chip Huyen](https://huyenchip.com/2023/04/11/llm-engineering.html)
- [How Cursor Works (Architecture Deep Dive)](https://www.cursor.com/blog/how-cursor-works)

### 🧒 ELI5

想象你在点外卖。你（用户）先查缓存（"上次点的是什么？"），找到就直接下单（缓存命中）。找不到就去菜单（LLM），但菜单太大，就先问服务员推荐（RAG 检索相关代码）。厨房（LLM）做好了一道道端上来（流式返回），不用等所有菜做完。

*Think of it like ordering food — check your saved favorites first (cache), if not found search the menu with a waiter's help (RAG), and food arrives dish by dish as it's ready (streaming).*
