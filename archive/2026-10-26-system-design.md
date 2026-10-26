🏗️ **系统设计 / System Design**
*Day 142 · Expert Synthesis — Production AI 系统架构全景*

---

## 场景 / Scenario

想象你是一家 AI 公司的 Staff Engineer。你已经学完了全部 60 个系统设计话题，现在把它们**全部串起来**——设计一个生产级 AI API 平台，支持 100K RPS、RAG、流式输出、多租户限速。

You've covered all 60 system design topics. Now stitch them together: design a production AI API platform (100K RPS, streaming, RAG, multi-tenant rate limiting).

---

## 完整架构 / Full Architecture

```
[Client / SDK]
      │
      ▼
[CDN + WAF]          ← Day 64: cache static, filter bots
      │
      ▼
[Global Load Balancer] ← Day 4: geo-aware Anycast routing
      │
      ▼
[API Gateway]         ← Day 16: auth, routing, rate limit
      │  (token bucket per tenant — Day 17)
      ├──────────┬──────────┐
      ▼          ▼          ▼
[Chat Svc] [Embed Svc] [Admin API]
      │          │
      ▼          ▼
[Kafka Queue] [Vector DB]   ← Day 13, Day 18: RAG retrieval
      │        (pgvector/Pinecone, HNSW index)
      ▼
[LLM Inference Workers]     ← Day 73: vLLM, continuous batching
      │  (KV Cache shared prefix, speculative decoding)
      ▼
[Response Cache — Redis]    ← Day 6: semantic dedup TTL=1h
      │
      ▼
[Monitoring + Tracing]      ← Day 42, Day 68: Datadog + Jaeger
```

---

## 关键权衡 / Key Tradeoffs

**推理层 (Day 73):**
- **连续批处理** — vLLM 不等一批跑完就插新请求，吞吐 10-20×↑
- **Speculative Decoding** — 小模型打草稿，大模型验证，延迟↓30%
- **KV Cache** — 相同前缀的请求共享 attention 计算

**RAG 管道 (Day 16, 18):**
```
Query → Embedding (并行) → HNSW Vector Search (~10ms)
                               ↓ Top-K Chunks
              Augmented Prompt → LLM → Stream (SSE)
```
权衡: ANN 牺牲 0.1% 精度换 100× 速度。精确 KNN 在 >1M 向量时不可接受。

**多租户限速 (Day 17):**
- Free: 10 RPM · Pro: 1K RPM · Enterprise: custom
- 超限返回 `429 + Retry-After`
- 每个模型独立配额（GPT-4 不能挤占 GPT-3.5）

---

## 60 个话题的核心教训 / Top Lessons

| 话题 | 教训 |
|------|------|
| Caching (D6) | AI 用语义缓存 > 精确缓存 |
| Message Queue (D13) | 长推理走异步，避免 HTTP timeout |
| Rate Limit (D17) | 按 token 数限速比按请求数更准 |
| Consistent Hashing (D11) | GPU 节点横向扩展时不重建 KV cache |
| Feature Flags (D53) | 新模型灰度 1%→10%→100% |
| Distributed Tracing (D68) | trace_id 串联 RAG + 推理全链路 |

---

## 别踩这个坑 / Common Mistakes

❌ 同步串行：embedding → vector search → LLM  
✅ 并行：embedding 和向量搜索同时跑，结果 merge 后再 LLM

❌ 无限 context window 当免费 buffer  
✅ RAG 截断 + 动态 context 管理，token 是钱

❌ 单 Redis 节点做推理缓存  
✅ Redis Cluster + L1 本地缓存 + graceful degradation

---

## 📚 References

- https://vllm.ai/blog/2023-06-20-vllm — vLLM continuous batching
- https://www.pinecone.io/learn/series/vector-databases-in-production/ — Vector DB in prod
- https://platform.openai.com/docs/guides/rate-limits — Rate limiting patterns

## 🧒 ELI5

把它想象成一家高级餐厅：API Gateway = 前台（验身份、分桌），Rate Limiter = 每桌限点几道菜，Kafka = 厨房订单队列，LLM Worker = 厨师，Vector DB = 菜谱知识库（RAG = 查完菜谱再做菜），Cache = 热门菜提前备好。高峰期不乱，靠的是每一层都做对。
