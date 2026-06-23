# 🏗️ 系统设计 / System Design — Day 60

**设计一个 AI 对话平台 (ChatGPT 规模)**
**Design an AI Chatbot Platform (ChatGPT-scale)**

---

## 🌐 真实场景 / Real-World Scenario

想象你在设计一个每天处理 **1 亿次对话**的 AI 聊天平台。
每个请求都要调用巨大的 LLM（比如 GPT-4o）、保持对话历史、支持流式输出（streaming），还要保证低延迟 + 高可用。
这不是普通的 CRUD 系统——推理的成本是 I/O 的 1000 倍。

Imagine building an AI chat platform handling **100M conversations per day**.
Each request calls a massive LLM, maintains conversation history, supports streaming output, all while meeting low-latency and high-availability SLAs.
This is not a normal CRUD system — inference costs 1000x more than I/O.

---

## 📐 架构图 / Architecture Diagram

```
User (Browser/App)
        │  WebSocket / SSE
        ▼
  ┌─────────────┐
  │  API Gateway │  (rate limit, auth, routing)
  └──────┬──────┘
         │
  ┌──────▼──────────────────┐
  │    Conversation Service  │  (session mgmt, context assembly)
  └──────┬──────────────────┘
         │ context + prompt
  ┌──────▼──────────────────┐
  │    LLM Inference Router  │  (load balance across model replicas)
  └──────┬──────────────────┘
         │ GPU workers
  ┌──────▼──────────────────────────────────┐
  │  Model Serving Cluster                  │
  │  ┌────────────┐  ┌────────────┐         │
  │  │  vLLM pod  │  │  vLLM pod  │  ...    │
  │  │  (A100)    │  │  (H100)    │         │
  │  └────────────┘  └────────────┘         │
  └─────────────────────────────────────────┘
         │ tokens (streaming)
  ┌──────▼──────┐      ┌──────────────┐
  │ Stream Relay │      │   Storage    │
  │  (SSE push)  │      │ - Redis: ctx │
  └─────────────┘      │ - S3: history│
                        │ - Postgres: │
                        │   user data  │
                        └──────────────┘
```

---

## ⚖️ 核心权衡 / Key Tradeoffs

### 1. 为什么用 vLLM + Continuous Batching？
传统服务一次处理一个请求，GPU 大部分时间在等待。
vLLM 用 **PagedAttention** + continuous batching，把等待时间"填满"，GPU 利用率从 30% 提升到 80%+。

vLLM with **PagedAttention** + continuous batching fills GPU idle time. Without it, one slow streaming response blocks the entire GPU.

### 2. 流式输出：SSE vs WebSocket
- **SSE (Server-Sent Events):** 单向、HTTP/1.1 兼容、自动重连。适合 token 流。
- **WebSocket:** 双向、更复杂。聊天场景用 SSE 更简单。

Use SSE for token streaming — simpler than WebSocket for unidirectional token flow.

### 3. 对话上下文管理
- 短期上下文 → **Redis** (TTL 30 min)
- 长期历史 → **S3** (压缩存储)
- 上下文窗口有限 → 超长历史需要 **摘要压缩** (recursive summarization)

Context window is finite. Long conversations require summarization to fit within token limits.

### 4. 模型路由 / Model Routing
- 简单问题 → 小模型 (GPT-4o-mini, Haiku) — 便宜 10x
- 复杂推理 → 大模型 (GPT-4o, Sonnet)
- 路由决策基于 intent classification（用小模型分类）

Route cheap questions to small models. 80% of traffic often qualifies.

---

## ❌ 别踩这个坑 / Common Mistakes

**坑 1: 对每个 token 都写数据库**
→ 把 token 流缓存在内存，对话结束后一次性写入。

**坑 2: 不限制并发请求数**
→ GPU 内存是有限的。没有背压控制，会导致 OOM crash。用队列 + 请求限速。

**坑 3: 上下文放全部历史**
→ 100 轮对话 = context 爆炸 = 推理慢且贵。必须截断或摘要。

**坑 4: 没有 prompt 注入防护**
→ 用户可以通过 prompt 绕过系统指令。需要 input/output guardrails。

---

## 📚 References

- https://vllm.ai/ — vLLM project, PagedAttention paper
- https://platform.openai.com/docs/guides/streaming — OpenAI streaming guide
- https://www.youtube.com/watch?v=80bIUggRJf4 — Andrej Karpathy on LLM serving

## 🧒 ELI5

把 AI 聊天平台想成一家饭店：用户点菜（输入问题），厨师（GPU）做菜（推理），服务员一道一道上菜（流式输出）。
vLLM 就像让厨师同时帮多张桌子备菜，而不是只等一桌做完。

It's like a restaurant: customers order (input), chefs cook (GPU inference), waiters serve dish by dish (streaming tokens). vLLM lets chefs prep multiple tables at once instead of one at a time.
