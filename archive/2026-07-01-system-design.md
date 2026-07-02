# 🏗️ 系统设计 / System Design — Day 79
## 设计 AI 聊天机器人平台（ChatGPT 规模）/ Design an AI Chatbot Platform (ChatGPT-scale)
**预计阅读时间 / Est. read time: 3 min**

---

## 🌍 真实场景 / Real-World Scenario

想象你在 2023 年加入 OpenAI 工程团队。ChatGPT 刚刚走红，DAU 从零飙升到 1000 万，而你们只有几周时间来处理这个规模问题。

Imagine joining OpenAI's engineering team in 2023. ChatGPT just went viral—DAU jumped from zero to 10M in weeks, and you have a few weeks to handle the scale.

**核心挑战 / Core Challenges:**
- 请求是流式的（SSE/WebSocket），不是普通 REST
- 每个请求耗时 10-60 秒（LLM 推理很慢）
- 用户期望对话历史持久化
- 模型推理成本极高（GPU 资源昂贵）

---

## 🏛️ 架构图 / Architecture Diagram

```
用户 / User
     │ HTTPS (SSE stream)
     ▼
┌─────────────────────────────────────────────┐
│            API Gateway / Load Balancer       │
│         (rate limiting, auth, routing)       │
└────────┬──────────────────────────┬──────────┘
         │                          │
    ┌────▼─────┐              ┌─────▼──────┐
    │ Chat API │              │ Auth Svc    │
    │ Service  │              │ (JWT/OAuth) │
    └────┬─────┘              └────────────┘
         │
    ┌────▼──────────────────────────────────┐
    │            Message Queue              │
    │          (Kafka / SQS)                │
    └────┬──────────────────────────────────┘
         │ fan-out
    ┌────▼──────────────────────────────────┐
    │         Inference Workers             │
    │  ┌──────────┐  ┌──────────┐           │
    │  │ GPU Pod 1│  │ GPU Pod 2│  ...      │
    │  │ (A100×8) │  │ (A100×8) │           │
    │  └──────────┘  └──────────┘           │
    └────┬──────────────────────────────────┘
         │
    ┌────▼────────────────────────────────────┐
    │  Storage Layer                          │
    │  ┌──────────────┐  ┌──────────────────┐ │
    │  │ PostgreSQL   │  │  Redis Cache     │ │
    │  │ (conv history│  │  (session state, │ │
    │  │  user data)  │  │   rate limits)   │ │
    │  └──────────────┘  └──────────────────┘ │
    └─────────────────────────────────────────┘
         │
    ┌────▼────────────┐
    │  KV Cache Store │
    │  (GPU-side,     │
    │   prompt cache) │
    └─────────────────┘
```

---

## ⚖️ 关键权衡 / Key Tradeoffs

### 1. 流式响应 vs 批量响应 / Streaming vs Batch
**为什么选流式？** 用户感知延迟从 30s 降到"首 token" ~500ms，体验天壤之别。
技术上用 **Server-Sent Events (SSE)** 或 WebSocket；SSE 更简单且天然支持单向流。

### 2. KV Cache — GPU 内存的黄金
LLM 推理时，同一对话的前缀（prompt）每次都重新计算太浪费。
**KV Cache** 在 GPU 内存里缓存这些 attention key/value 张量，命中时推理速度提升 3-10×。
代价：GPU 内存昂贵，需要 LRU 驱逐策略。

### 3. 会话路由 / Session Affinity
为了命中 KV Cache，同一对话的请求要尽量路由到同一 GPU Pod。
用 `conversation_id` 做 consistent hashing，不是纯 round-robin。

### 4. 背压 / Backpressure
GPU 推理是瓶颈。当队列积压，要优雅降级：
- 返回 503 + Retry-After（不要让用户一直等）
- 对免费用户限流，优先保障付费用户

---

## 🚫 别踩这个坑 / Common Mistakes

| 错误 ❌ | 正确 ✅ |
|--------|--------|
| 用普通 HTTP 请求等全部生成完再返回 | 用 SSE 流式推送 token |
| 每次都从头重算 prompt | 用 KV Cache 缓存前缀 |
| 所有对话请求 round-robin 分发 | 用 conversation_id 做 sticky routing |
| 忽略 GPU OOM | 设置 max_context_length 硬限制 |
| 对话历史存 GPU 内存 | 历史存 DB，推理时按需加载 |

---

## 📐 规模估算 / Back-of-Envelope

- 1000 万 DAU，每人每天 10 条消息 → **1 亿请求/天** ≈ **1160 req/s**
- 每请求平均 20s 推理 → 需要 ~23,200 并发 GPU "slots"
- A100 8-GPU pod 可处理 ~16 并发请求
- 需要约 **1450 个 A100 Pod** → 这就是为什么 OpenAI 的 GPU 账单以亿美元计

---

## 📚 参考资料 / References
- [OpenAI: How We Scale ChatGPT](https://openai.com/research/scaling-language-models)
- [ByteDance: How to Serve LLMs Efficiently](https://arxiv.org/abs/2309.06180) — vLLM 论文，KV cache 管理
- [AWS: Streaming Responses with API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-websocket.html)

## 🧒 ELI5
就像一个超级忙的老师在课堂上同时给 1000 个学生解答问题。
老师不是等到全部想完才开口，而是边想边说（streaming）。
还有个小秘诀：老师记住了每个学生之前问过什么（KV cache），这样不用从头理解对话，更快！
It's like a super-busy teacher answering 1000 students simultaneously—speaking while still thinking (streaming), and remembering each student's conversation history (KV cache) so they don't start from scratch each time.
