# 🏗️ 系统设计 / System Design — Day 77
## 设计 AI 聊天平台（ChatGPT 量级）/ Design an AI Chatbot Platform (ChatGPT-scale)

> ⏱️ 阅读时间约 3 分钟 / ~3 min read

---

### 🎬 场景导入 / Real-World Scenario

想象你在 OpenAI 的基础设施团队。产品刚刚宣布 ChatGPT 对所有人免费开放——你的系统需要在**几分钟内**从 100 万用户扩展到 1 亿用户。每个请求都是长连接 streaming，每个 token 都要实时推送。

Imagine you're on OpenAI's infra team. ChatGPT just went free for everyone — your system needs to scale from 1M to 100M users in minutes. Every request is a long-lived streaming connection, every token pushed in real time.

---

### 🏛️ ASCII 架构图 / Architecture

```
User Browser / App
        │  WebSocket / SSE
        ▼
┌─────────────────────────────────┐
│         API Gateway             │  ← Auth, Rate Limiting, Routing
│   (Kong / NGINX / Envoy)        │
└──────────┬──────────────────────┘
           │
    ┌──────▼──────┐
    │  Chat API   │  ← FastAPI/Go service
    │  Service    │    Stateless, auto-scaled
    └──────┬──────┘
           │ enqueue
    ┌──────▼──────────────┐
    │   Inference Queue   │  ← Kafka / SQS (priority lanes)
    └──────┬──────────────┘
           │ pull
    ┌──────▼──────────────────────────┐
    │     Inference Cluster           │
    │  ┌─────────┐  ┌─────────┐       │
    │  │ vLLM    │  │ vLLM    │  ...  │  ← A100/H100 GPU pods
    │  │ node 1  │  │ node 2  │       │
    │  └─────────┘  └─────────┘       │
    └──────┬──────────────────────────┘
           │ SSE token stream
    ┌──────▼──────┐
    │  Streaming  │  ← Server-Sent Events relay
    │  Service    │    per-user connection manager
    └──────┬──────┘
           │
    ┌──────▼──────┐    ┌──────────────┐
    │  History DB │    │  Vector DB   │
    │  (Postgres) │    │  (pgvector)  │  ← RAG / memory
    └─────────────┘    └──────────────┘
```

---

### ⚖️ 核心权衡 / Key Tradeoffs

**为什么用队列而不是直接调 GPU？/ Why queue instead of direct GPU call?**
- 直接调用：延迟低，但 GPU 过载时请求直接失败
- 队列：增加~50ms 延迟，但提供背压（backpressure）保护，允许优先级调度（付费用户 > 免费用户）
- Direct: lower latency but fails under load; Queue: ~50ms overhead but enables priority scheduling

**流式输出 SSE vs WebSocket？/ SSE vs WebSocket?**
- ChatGPT 用 SSE：单向、HTTP 友好、CDN 可缓存心跳、浏览器原生支持
- WebSocket 适合双向实时（游戏、协作编辑）；纯 LLM 流式输出 SSE 足够
- ChatGPT uses SSE: unidirectional, HTTP-friendly, no upgrade handshake

**KV Cache 共享 / Shared KV Cache:**
- vLLM 的 PagedAttention 允许多请求共享 prompt prefix 的 KV cache，显著提升 throughput
- vLLM's PagedAttention shares prompt prefix KV cache across requests — critical for system prompts

---

### 🚫 别踩这个坑 / Common Mistakes

1. **把对话历史塞进 context 而不截断** — 超出 context window，直接 crash。正确做法：滑动窗口 + 向量摘要
   Don't stuff all history into context — sliding window + vector summary for old turns

2. **单点 GPU 节点不做健康检查** — GPU OOM 是常态，必须有自动剔除 + 重新路由
   GPU OOM is routine — must auto-remove unhealthy nodes and reroute inflight requests

3. **忽略 cold start** — 推理服务启动加载模型要 30-60s，必须预热（keep warm instances）
   Model loading takes 30-60s — keep warm instances, don't scale to zero for LLM

4. **Rate limiting 只在 API Gateway 做** — 绕过 Gateway 的内部流量会打穿 GPU
   Rate limit at GPU cluster level too, not just the gateway

---

### 📚 References

- [How ChatGPT is built — OpenAI engineering blog](https://openai.com/research/chatgpt)
- [vLLM: Easy, Fast, and Cheap LLM Serving](https://vllm.readthedocs.io/)
- [Server-Sent Events vs WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

---

### 🧒 ELI5

把它想成一家超级繁忙的餐厅：API Gateway 是前台收银，Kafka 队列是点单系统，GPU 集群是厨房（很贵，每个厨师一秒钟能出几道菜），SSE 是服务员一道一道把菜端出来的过程。餐厅的关键不是厨师有多快，是**怎么让厨师一直在干活不空等**。

Think of it as a restaurant: the gateway is the cashier, the queue is the order system, GPUs are the (very expensive) chefs, and SSE is the waiter delivering dishes one by one. The key isn't chef speed — it's keeping chefs busy with zero idle time.
