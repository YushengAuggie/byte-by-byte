# 🏗️ 系统设计 / System Design — Day 61
## Design an AI Chatbot Platform (ChatGPT-scale)
**Difficulty:** Expert | **Read time:** ~3 min

---

## 想象你在设计...
你是 OpenAI 的首席工程师。ChatGPT 突然爆红，用户从零增长到一亿。你需要设计一个支撑大规模 AI 对话的平台。每秒处理数万请求，每次请求都要调用一个巨大的语言模型——如何不崩？

You're OpenAI's principal engineer. ChatGPT goes viral overnight. You need a platform that handles hundreds of millions of users, each having multi-turn conversations with a giant language model. How do you architect this?

---

## 📐 架构图 / Architecture Diagram

```
        用户 / Users
            │
            ▼
    ┌──────────────────┐
    │   API Gateway    │  ← 认证、限流、路由
    │  (Rate Limit /   │    Auth, rate limiting, routing
    │   Auth / TLS)    │
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │  Chat Service    │  ← 会话管理、流式响应
    │  (Stateless)     │    Session mgmt, streaming
    └────────┬─────────┘
             │
     ┌───────┴──────────┐
     │                  │
┌────▼─────┐   ┌────────▼────────┐
│  Context │   │  Inference      │
│  Store   │   │  Cluster        │
│ (Redis)  │   │  (A100/H100     │
│          │   │   GPUs)         │
└────┬─────┘   └────────┬────────┘
     │                  │
┌────▼──────────────────▼────────┐
│        Message Queue           │  ← 解耦推理请求
│        (Kafka)                 │    Decouple inference requests
└────────────────┬───────────────┘
                 │
        ┌────────▼────────┐
        │  Batch Scheduler │  ← 连续批处理
        │  (Continuous     │    Continuous batching
        │   Batching)      │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │   Model Store   │  ← 权重分布式存储
        │   (HDFS/NFS)    │    Distributed weight storage
        └─────────────────┘
```

---

## 🔑 关键权衡 / Key Tradeoffs

### 1. 流式 vs 批量 / Streaming vs Batching
- **流式 (SSE/WebSocket):** 用户体验好，首 token 快；但连接资源消耗大
- **连续批处理:** 把多个用户请求合并一次 GPU forward pass，吞吐量提升 10x
- **选择:** 对外用流式，对内用连续批处理

*Streaming (SSE/WebSocket): great UX, fast first token — but resource-heavy. Continuous batching: merge multiple user requests into one GPU forward pass = 10x throughput. Use streaming externally, continuous batching internally.*

### 2. 上下文存储 / Context Storage
- 对话历史不能放在服务器内存（无状态横向扩展）
- 用 Redis 存 session → context，TTL 24h 节省成本
- KV Cache offloading: 把 attention KV cache 从 GPU 换到 CPU/SSD 减少显存压力

*Conversation history can't live in server RAM (you need stateless horizontal scaling). Store sessions in Redis with 24h TTL. Offload KV caches to CPU/SSD to reduce GPU memory pressure.*

### 3. 模型并行 / Model Parallelism
- 单张 A100 (80GB) 放不下 GPT-4 级别模型
- **张量并行 (Tensor Parallelism):** 把权重矩阵切分到多张 GPU
- **流水线并行 (Pipeline Parallelism):** 不同层跑在不同 GPU 组上
- 生产中通常 TP×PP 组合

*A single A100 (80GB) can't hold a GPT-4-class model. Tensor parallelism splits weight matrices across GPUs. Pipeline parallelism puts different layers on different GPU groups. Production uses both (TP × PP).*

### 4. 多租户隔离 / Multi-tenant Isolation
- 不同 tier（免费/Plus/API）用不同优先级队列
- 免费用户请求在高峰期可被降级（graceful degradation）

*Different tiers (free/Plus/API) use different priority queues. Free user requests can be deprioritized during peak load.*

---

## 🚫 别踩这个坑 / Common Mistakes

1. **用 HTTP 长轮询而不是 SSE** — SSE 更简单，断线自动重连，不需要 WebSocket 的复杂握手
2. **不限制上下文长度** — 无限上下文 = 显存爆炸，必须有截断策略（sliding window 或 summarization）
3. **忽略 time-to-first-token (TTFT)** — 用户感知的延迟，不是总生成时间，要单独优化
4. **单点 GPU 集群** — GPU 比 CPU 贵 100x，故障成本极高，必须做热备 + 快速重路由

*Don't use HTTP long-polling instead of SSE. Don't allow unbounded context (it blows GPU memory). Track TTFT separately from total latency. Never have a single GPU cluster without hot standby.*

---

## 📚 References
- [vLLM: Efficient Memory Management for LLM Serving](https://vllm.ai/)
- [How ChatGPT Actually Works (High Scalability)](http://highscalability.com/blog/2023/2/3/system-design-chatgpt.html)
- [OpenAI Triton & GPU Kernel Optimization](https://openai.com/research/triton)

## 🧒 ELI5
想象一个超级繁忙的餐厅，厨房只有几个特别贵的大厨（GPU）。侍者（Chat Service）把所有订单（请求）汇总，让大厨一次做多道菜（批处理），这样比一道一道做快多了。Redis 是记事本，记住每桌客人之前点了什么（对话历史）。

*Imagine a super-busy restaurant where the kitchen has a few very expensive master chefs (GPUs). Waiters collect all orders and let chefs cook multiple dishes at once (batching) — much faster than one at a time. Redis is the notepad that remembers what each table ordered before (conversation history).*
