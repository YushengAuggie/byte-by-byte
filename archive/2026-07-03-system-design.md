# 🏗️ 系统设计 / System Design — Day 64
**主题 / Topic:** Design an AI Chatbot Platform (ChatGPT-scale)
**难度 / Difficulty:** Expert | **预计阅读 / Read time:** 3 min

---

## 想象你在设计... / Imagine you're designing...

你是 OpenAI 的首席架构师，正在设计支撑 ChatGPT 的后端系统。每天 1 亿次对话请求、流式输出、多模型支持、会话上下文管理，怎么做？

You're the lead architect at OpenAI, designing the backend for ChatGPT. 100M conversations/day, streaming output, multiple models, session context management — how do you build this?

---

## 架构图 / Architecture Diagram

```
                        ┌─────────────────────────────────┐
                        │         Client Apps              │
                        │   (Web / iOS / Android / API)    │
                        └──────────────┬──────────────────┘
                                       │ HTTPS / WebSocket
                        ┌──────────────▼──────────────────┐
                        │         API Gateway              │
                        │  (Rate Limit / Auth / Routing)   │
                        └──────┬───────────────┬──────────┘
                               │               │
               ┌───────────────▼─┐         ┌───▼──────────────┐
               │  Chat Service   │         │  User Service     │
               │  (Stateless)    │         │  (Auth / Profile) │
               └───────┬─────────┘         └──────────────────┘
                       │
          ┌────────────▼──────────────────────────┐
          │            Message Queue               │
          │         (Kafka / SQS / Pub-Sub)        │
          └────────────┬──────────────────────────┘
                       │ async dispatch
          ┌────────────▼──────────────────────────┐
          │        Inference Fleet                 │
          │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
          │  │ Model   │ │ Model   │ │ Model   │  │
          │  │ GPT-4o  │ │  o1/o3  │ │  Mini   │  │
          │  └─────────┘ └─────────┘ └─────────┘  │
          │   (A100/H100 GPU Cluster, vLLM)        │
          └────────────┬──────────────────────────┘
                       │ SSE streaming back
          ┌────────────▼──────────────────────────┐
          │        Storage Layer                   │
          │  ┌──────────────┐ ┌─────────────────┐  │
          │  │ Conversation  │ │  Vector Store   │  │
          │  │  Store (PG)  │ │ (pgvector/Pine) │  │
          │  └──────────────┘ └─────────────────┘  │
          └───────────────────────────────────────┘
```

---

## 核心设计决策 / Key Design Decisions

### 1. 流式输出 / Streaming (Server-Sent Events)
- 用户看到逐词输出，感知延迟从 10s 降到 <1s
- 后端：**vLLM** 批量推理 + KV Cache，逐 token 通过 SSE 推送
- 前端：`EventSource` API 消费，即时渲染
- Use SSE for token-by-token streaming; perceived latency drops from 10s to <1s

### 2. 会话上下文管理 / Context Window Management
- 每次请求需携带完整对话历史（消耗 tokens！）
- 策略：短对话直接传；长对话 → **滑动窗口** 保留最近 N 轮 + **摘要压缩** 远程历史
- Long conversations: sliding window (recent N turns) + summarization for older history

### 3. 推理路由 / Inference Routing
- 简单问题 → GPT-4o mini（便宜快）
- 复杂推理 → o1/o3（贵但准）
- 路由依据：请求复杂度分类器 + 用户 tier
- Route simple queries to cheap fast models; complex reasoning to expensive slow models

### 4. 多租户隔离 / Multi-tenancy
- API 用户 vs. ChatGPT 用户走不同队列
- 用户隔离：会话数据按 `user_id` 分区，GDPR 删除走 soft-delete + 异步清理
- Separate queues for API vs. product traffic; per-user data partitioned for GDPR

---

## 为什么这样设计？/ Why This Design?

| 决策 | 理由 |
|------|------|
| Kafka 解耦 | 推理失败可重试，不影响前端 |
| 无状态 Chat Service | 水平扩展简单 |
| vLLM 批处理 | Continuous batching 提升 GPU 利用率 3-4x |
| PG + pgvector | 统一存储对话 + 语义搜索，减少运维复杂度 |

---

## ⚠️ 别踩这个坑 / Common Mistakes

**坑 1：** 把 LLM 调用做成同步请求 → 超时、连接堆积  
✅ 用消息队列异步化，前端轮询或 WebSocket 接收结果

**坑 2：** 每次请求传全部历史 → token 爆炸，成本失控  
✅ 实现上下文压缩策略（滑动窗口 + 摘要）

**坑 3：** 忽略 GPU 利用率 → 推理成本是最大成本项  
✅ Continuous batching + 模型路由是降本核心

**坑 4：** 单点模型部署 → 一个模型版本更新导致全量中断  
✅ 金丝雀发布 + 流量染色

---

## 📚 References
- [vLLM: Easy, Fast, and Cheap LLM Serving](https://vllm.ai/)
- [How ChatGPT Works (Andrej Karpathy)](https://youtu.be/zjkBMFhNj_g)
- [System Design Interview — ChatGPT-scale](https://github.com/donnemartin/system-design-primer)

## 🧒 ELI5
想象 ChatGPT 是一个巨大的客服中心。你发消息 → 前台排号 → 传到最聪明的客服（GPU）→ 客服边想边回复你（流式输出）→ 聊天记录存起来。简单的问题给初级客服，复杂的给高级客服，这样又快又省钱。

Imagine ChatGPT is a huge call center. You send a message → it gets queued → routed to the smartest agent (GPU) → they answer you word by word (streaming) → chat saved. Simple questions go to junior agents, complex ones to senior — fast and cheap.
