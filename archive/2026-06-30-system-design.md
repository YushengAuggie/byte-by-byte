# 🏗️ 系统设计 / System Design — Day 78
**Topic:** Design an AI Chatbot Platform (ChatGPT-scale)
**Difficulty:** Expert | **Phase:** Expert

---

## 想象你在设计... / Imagine you're designing...

你是 OpenAI 的首席架构师。需要设计一个能同时支持 **1000 万**并发用户的 AI 对话平台。每个请求都需要调用一个巨大的 LLM，延迟敏感，成本巨高，故障不可接受。

You're the lead architect at OpenAI. Design a platform that serves **10 million** concurrent users, each streaming responses from a massive LLM — latency-sensitive, extremely expensive, zero tolerance for failures.

---

## 核心挑战 / Core Challenges

1. **LLM 推理极慢** — GPT-4 级别模型，首 token 延迟 500ms-2s
2. **流式输出** — 用户要看到逐字"打字"效果，不是等全部完成
3. **有状态会话** — 每轮对话需要历史 context
4. **成本爆炸** — 每 1M tokens 约 $10-30，乘以 1000 万用户
5. **GPU 是瓶颈** — A100/H100 极贵，利用率必须最大化

---

## 架构图 / Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTS                              │
│         Web / iOS / Android / API / Plugins                 │
└────────────────────────┬────────────────────────────────────┘
                         │ WebSocket / SSE (streaming)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY LAYER                        │
│   Auth (JWT/OAuth) │ Rate Limiting │ Abuse Detection        │
│              (Kong / Nginx + Lua)                           │
└──────────┬──────────────────────────────┬───────────────────┘
           │                              │
           ▼                              ▼
┌─────────────────────┐       ┌─────────────────────────────┐
│   CONVERSATION SVC  │       │    SESSION STORE             │
│  - History mgmt     │◄─────►│  Redis Cluster              │
│  - Context window   │       │  (last N turns, TTL 24h)    │
│  - Token counting   │       └─────────────────────────────┘
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                   INFERENCE ROUTER                          │
│   - Model selection (GPT-4o / GPT-4 / GPT-3.5 by cost)     │
│   - Load balancing across GPU pods                          │
│   - Priority queuing (paid > free)                          │
└──────────┬──────────────────────────┬───────────────────────┘
           │                          │
           ▼                          ▼
┌─────────────────────┐   ┌─────────────────────────────────┐
│  GPU CLUSTER A      │   │  GPU CLUSTER B                  │
│  (A100/H100 pods)   │   │  (Spot instances for overflow)  │
│  vLLM / TensorRT    │   │  vLLM + dynamic batching        │
│  KV-Cache enabled   │   │                                 │
└──────────┬──────────┘   └──────────────────────────────────┘
           │
           ▼ SSE stream
┌─────────────────────────────────────────────────────────────┐
│               STREAMING PROXY                               │
│   - Chunked transfer (token by token)                       │
│   - Connection multiplexing                                 │
│   - Backpressure handling                                   │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│               STORAGE LAYER                                 │
│  PostgreSQL (conversations) │ S3 (attachments/files)        │
│  ElasticSearch (search)     │ ClickHouse (analytics)        │
└─────────────────────────────────────────────────────────────┘
```

---

## 关键设计决策 / Key Design Decisions

### 1. 流式传输用 SSE，不用 WebSocket
- **SSE (Server-Sent Events)** = 单向流，更简单，CDN 友好
- WebSocket 是双向的，但 LLM 推理只需要服务端→客户端方向
- SSE 天然支持断线重连 (`Last-Event-ID`)

### 2. vLLM + Continuous Batching
- 传统推理：一个请求用完 GPU 才处理下一个 → 利用率低
- **Continuous batching**：把多个请求的 prefill/decode 阶段交织执行
- 效果：GPU 利用率从 30% → 80%+，吞吐量提升 3-10x

### 3. KV Cache 复用
- 系统 prompt ("You are a helpful assistant") 对所有用户相同
- **Prefix caching**：预计算并缓存这部分的 KV cache
- 节省 ~20% 推理计算量

### 4. 分层会话存储
```
热数据 (最近 24h) → Redis (内存，<1ms)
温数据 (最近 30d) → PostgreSQL (SSD，<10ms)  
冷数据 (历史)   → S3 (对象存储，按需加载)
```

### 5. 成本控制：模型分级路由
```python
def route_model(user_tier, message_complexity):
    if user_tier == "free":
        return "gpt-3.5-turbo"   # $0.002/1K tokens
    elif is_simple_query(message_complexity):
        return "gpt-4o-mini"     # $0.015/1K tokens  
    else:
        return "gpt-4o"          # $0.03/1K tokens
```

---

## 为什么这样设计 / Why This Design

| 决策 | 原因 |
|------|------|
| Inference Router 独立 | 模型升级不影响上游；可做 A/B 测试 |
| Redis 存 session | 低延迟读取历史，避免每次查 DB |
| 优先队列 | 付费用户等待时间 < 2s；免费用户可接受 5-10s |
| Spot instances | LLM 推理是无状态的，被抢占只影响当前请求 |

---

## 别踩这个坑 / Common Mistakes

❌ **坑1：把整个对话历史每次都发给 LLM**
- 100 轮对话 × 200 tokens = 20K tokens/请求
- Context window 满了就崩，成本也爆了
- ✅ 正确：摘要旧轮次，只保留最近 10-20 轮

❌ **坑2：同步等待 LLM 完成再返回**
- GPT-4 生成 500 字需要 10-30 秒
- 用户会以为卡死了
- ✅ 正确：SSE 流式推送，第一个 token < 1s 到达

❌ **坑3：没有限流，被 prompt injection 攻击**
- 攻击者发超长 prompt，把所有 GPU 资源耗尽
- ✅ 正确：输入 token 上限 + 每用户 RPM/TPM 限流

❌ **坑4：忽略 GPU 内存碎片**
- 不同长度请求的 KV cache 大小不同，导致显存碎片
- ✅ 正确：vLLM 的 PagedAttention 像操作系统管理物理内存一样管理显存

---

## 📚 References

- 🔗 [vLLM: Easy, Fast, and Cheap LLM Serving](https://vllm.ai/)
- 🔗 [How ChatGPT Works — Architecture Deep Dive](https://newsletter.pragmaticengineer.com/p/chatgpt-infrastructure)
- 🔗 [OpenAI's Infrastructure at Scale](https://openai.com/research/scaling-kubernetes-to-7500-nodes)

---

## 🧒 ELI5

想象你是个超忙的厨师，同时要给一万个客人做饭。每道菜（LLM 推理）需要 30 秒。

- **分批下锅（Continuous Batching）**：不等一道菜全熟，多道菜轮流用炉灶
- **菜单分级（Model Routing）**：简单的要沙拉用小厨师做，复杂的大餐才用大厨
- **提前备料（KV Cache）**：每个菜都用的酱汁提前熬好，不用每次现做
- **边做边上（SSE Streaming）**：前菜做好先端上来，不用等整套菜都好

这样 1 万个客人才不会都在等！
