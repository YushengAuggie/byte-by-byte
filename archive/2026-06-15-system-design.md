# 🏗️ 系统设计 / System Design — Day 66
## 设计搜索自动补全 / Design a Web Search Autocomplete (Google Suggest)

**⏱️ 阅读时间：约3分钟 / Reading time: ~3 min**

---

### 🌏 想象你在设计...

你在负责 Google 搜索栏的自动补全功能。用户每敲一个字符，系统就要在 **100ms 内** 返回前10条建议。每天有数十亿次请求。这个系统怎么设计？

You're building the autocomplete box for Google Search. Every keystroke must return top-10 suggestions in **<100ms**. Billions of requests per day. How do you design it?

---

### 🏛️ 架构图 / Architecture

```
User Types "sea"
       │
       ▼
┌──────────────────┐
│   Browser Cache  │◄── short-term prefix cache
└──────┬───────────┘
       │ cache miss
       ▼
┌──────────────────┐     ┌─────────────────────┐
│   API Gateway    │────►│  Autocomplete        │
│ (rate limit,     │     │  Service (stateless) │
│  auth, routing)  │     └──────┬──────────────┘
└──────────────────┘            │
                                │ lookup
                    ┌───────────▼───────────┐
                    │   Trie Cache Layer    │
                    │  (in-memory Redis)    │
                    │  prefix → top10 terms │
                    └───────────┬───────────┘
                                │ cache miss
                    ┌───────────▼───────────┐
                    │   Trie DB Cluster     │
                    │  (sharded by prefix)  │
                    └───────────┬───────────┘
                                │ offline build
                    ┌───────────▼───────────┐
                    │   Data Pipeline       │
                    │  (Kafka → Spark)      │
                    │  search logs → freq   │
                    └───────────────────────┘
```

---

### ⚙️ 核心设计决策 / Key Design Decisions

#### 1. 数据结构：Trie vs. Prefix Hash
**Trie（前缀树）** 是直觉上的选择，但纯内存 Trie 存10亿词条代价高。

实际方案：
- **预计算**：离线每小时跑 Spark Job，统计 top-K suggestions per prefix
- **存储**：Redis Hash — `prefix -> [term1:score1, term2:score2, ...]`
- **键空间**：只存长度 ≤ 5 的前缀（覆盖绝大多数真实输入）

**In practice:** Precompute top-K suggestions offline (Spark/MapReduce), store `prefix → top10` in Redis. Don't build a live trie in production.

#### 2. 分片策略 / Sharding
按前缀的第一个字母分片（26个分区），确保每个 shard 负载均衡。
Shard by first character(s) of prefix — ensures balanced load.

#### 3. 更新频率 / Update Frequency
- **实时更新**：新闻热词（"earthquake 2026"）需要在30分钟内出现
- **批量更新**：常规词条每天重建一次

Two-tier update: streaming pipeline for trending terms (< 30 min lag), batch rebuild for stable terms (daily).

#### 4. 个性化 / Personalization
在通用结果之上，叠加用户历史（浏览器本地存储）。不影响主路径延迟。
Layer personal history on top of global suggestions. Keep personal data in the browser to avoid latency.

---

### 🔢 容量估算 / Capacity Estimation

```
QPS: 10B queries/day ÷ 86400s ≈ 115K QPS
     × avg 5 keystrokes/query = 575K autocomplete QPS

Storage: 
  - 5M unique prefixes (len ≤ 5)
  - 10 suggestions × 20 bytes = 200 bytes/prefix
  - Total: ~1 GB → fits in Redis
  
Latency budget:
  - API Gateway: 5ms
  - Redis lookup: 1-2ms
  - Network RTT: 20-50ms
  - Total: < 100ms ✅
```

---

### ⚠️ 别踩这个坑 / Common Mistakes

| ❌ 错误做法 | ✅ 正确做法 |
|------------|------------|
| 实时更新 Trie | 离线批量预计算 top-K |
| 在服务器存个性化数据 | 个性化数据存浏览器本地 |
| 所有前缀等权处理 | 只存 ≤5 字符前缀 |
| 每次都去 DB 查 | Redis 缓存 + 浏览器缓存双层 |
| 存储完整 Trie | 存 prefix→top10 映射 |

---

### 🧒 ELI5

像图书馆索引卡片一样。我们提前把"以 'sea' 开头最常搜索的10个词"写在一张卡片上。你一输入 "sea"，图书管理员(Redis)直接拿出那张卡片，不用临时翻书。

Like index cards in a library. We pre-write the "top 10 things people search starting with 'sea'" on a card. When you type "sea", the librarian (Redis) just pulls out that card instantly.

---

### 📚 References
- 🔗 https://bytebytego.com/courses/system-design-interview/design-a-search-autocomplete-system
- 🔗 https://engineering.linkedin.com/blog/2016/03/instant-typeahead-search
- 🔗 https://www.youtube.com/watch?v=us0qySiUsGU (NeetCode System Design)
