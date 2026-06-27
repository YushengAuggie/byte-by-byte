# 🏗️ 系统设计 / System Design — Day 61

## 设计 AI 聊天平台（ChatGPT 规模）
## Design an AI Chatbot Platform (ChatGPT-scale)

**⏱️ 预计阅读时间 / Estimated read time: 3 min**

---

### 🎯 真实场景 / Real-World Scenario

想象你在 OpenAI 工作，需要设计一个每天处理 **1 亿次**对话请求的 AI 聊天系统。用户发一条消息，几秒内就收到流式回复——背后究竟发生了什么？

*Imagine you're at OpenAI, designing a system handling **100 million** conversation requests per day. A user sends a message and gets a streamed response within seconds — what's happening under the hood?*

---

### 🏛️ 架构图 / Architecture Diagram

```
User Browser / Mobile App
        │  WebSocket / SSE
        ▼
┌───────────────────────────────────────────────────────┐
│                   API Gateway                         │
│   (Auth, Rate Limiting, Session Routing)              │
└──────────────────┬────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────┐     ┌──────────────────┐
│  Chat Service│     │  Streaming Proxy  │
│  (FastAPI)   │     │  (SSE/WebSocket)  │
└──────┬───────┘     └────────┬─────────┘
       │                      │
       ▼                      ▼
┌──────────────┐     ┌────────────────────┐
│ Context Svc  │     │  LLM Inference     │
│ (Redis TTL)  │     │  Cluster           │
│              │     │  (vLLM / TGI)      │
└──────┬───────┘     │  ┌───┐ ┌───┐ ┌───┐│
       │             │  │GPU│ │GPU│ │GPU││
       ▼             │  └───┘ └───┘ └───┘│
┌──────────────┐     └────────────────────┘
│  Conversation│              │
│  DB          │     ┌────────▼─────────┐
│  (Postgres)  │     │  Model Registry   │
└──────────────┘     │  (S3 + weights)   │
                     └───────────────────┘
```

---

### ⚖️ 核心权衡 / Key Tradeoffs

**为什么用 SSE（Server-Sent Events）而非 WebSocket？**
- SSE 是单向流 → 服务端推送 token 更简单
- WebSocket 需要双向通信 → 聊天场景不必要
- SSE 天然支持 HTTP/2 多路复用

*Why SSE over WebSocket? SSE is one-directional — perfect for streaming tokens. WebSocket adds bidirectional complexity you don't need here. SSE also works seamlessly with HTTP/2 multiplexing.*

**为什么用 Redis 存对话上下文？**
- LLM 是无状态的：每次都要传完整 history
- 用户平均对话 10-20 轮，token 预算有限
- Redis TTL = 30min 自动过期，不堆垃圾

*Why Redis for conversation context? LLMs are stateless — you must send the full history every request. Redis with TTL handles the limited context window budget and auto-expires stale sessions.*

**推理集群如何扩容？**
- vLLM 的 PagedAttention：GPU KV Cache 利用率 +3x
- 请求路由按 session affinity（同 session → 同 GPU 节点，减少 KV cache miss）

*How do you scale inference? vLLM's PagedAttention gives 3x better GPU memory utilization. Route by session affinity — same session to same GPU node minimizes KV cache misses.*

---

### ❌ 常见误区 / Common Mistakes

**坑 1：对话 Context 没有截断策略**
- LLM 有最大 context window（如 128K tokens）
- 超限直接报错，要实现 sliding window 或 summary 压缩

*Trap 1: No context truncation strategy. LLMs have max context windows. You need a sliding window or summary compression before you hit the limit.*

**坑 2：没有请求排队导致 GPU OOM**
- 并发大量推理请求 → GPU 内存爆炸
- 正确做法：inference queue + backpressure

*Trap 2: No request queuing leads to GPU OOM. Concurrent requests overwhelm GPU memory. Add an inference queue with backpressure.*

**坑 3：每次都重新加载模型权重**
- 权重一次加载，常驻 GPU
- 用 Model Registry（S3）管理版本，热更新

*Trap 3: Reloading model weights per request. Weights should be loaded once, resident on GPU. Use a Model Registry for version management with hot-reload.*

---

### 📚 参考资料 / References

1. [vLLM: PagedAttention for Efficient LLM Serving](https://vllm.ai/)
2. [OpenAI API Streaming Docs](https://platform.openai.com/docs/api-reference/streaming)
3. [Designing ML Systems — Chip Huyen](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)

---

### 🧒 ELI5

就像一个超级快的打字员：
你问问题 → 助手边想边打 → 你实时看到每个字出现。
背后有很多电脑（GPU）轮流帮忙打字，
还有一个"记忆本"记住你们聊过什么。

*Like a super-fast typist: you ask a question → the assistant types while thinking → you see each word appear in real time. Behind the scenes, many computers (GPUs) take turns "typing," and a "memory notebook" (Redis) remembers your conversation history.*
