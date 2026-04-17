# 🏗️ 系统设计 / System Design — Day 22
## 设计自动补全 / Typeahead — Design an Autocomplete / Typeahead System

---

### 🌍 真实场景 / Real-World Scenario

想象你在谷歌搜索框里输入 "how to"，瞬间出现 10 条建议。这背后是什么？
*Imagine typing "how to" in Google's search box and instantly seeing 10 suggestions. What's behind it?*

每次用户输入一个字符，系统必须在 **<100ms** 内返回最相关的补全结果。谷歌、YouTube、Amazon、GitHub 都有这个功能——它看似简单，工程上却很复杂。
*Each keystroke must return the most relevant completions in <100ms. Google, YouTube, Amazon, GitHub all have this — it looks simple but is engineering-hard.*

---

### 🏛️ 架构图 / Architecture

```
用户输入 "app"
     │
     ▼
[Client] ──(debounce 50ms)──► [API Gateway]
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                  [Cache Layer]         [Search Service]
                  (Redis, TTL:5min)      │
                                    ┌───┴────────────┐
                                    ▼                ▼
                              [Trie Store]    [ML Ranking]
                              (Prefix Index)  (popularity,
                                              personalization)
                                    │
                                    ▼
                             [Data Pipeline]
                             (Kafka → Spark)
                             counts queries
                             every 10 mins
```

**数据流 / Data Flow:**
1. 用户输入 → 客户端 debounce 50ms（减少请求量）
2. API Gateway → 先查 Redis cache
3. Cache miss → Trie 查找 Top-K 前缀
4. ML 模型 rerank（考虑个性化、地理位置）
5. 日志写入 Kafka → Spark 定期更新 Trie 权重

---

### ⚙️ 核心数据结构 / Core Data Structure: Trie

```
             root
           /  |  \
          a   b   c
         /|    \
        p  r    e
       /    \
      p      o
     /|       \
    l  [end]   w
   /            \
  e               s
  [end,"apple,5"]  [end,"browse,3"]
```

每个节点存储：
- `children: dict`
- `is_end: bool`
- `top_k: list[{word, freq}]` ← **预计算 Top-10，避免遍历**

*Each node stores precomputed Top-10 completions → avoids traversal on query.*

**关键优化：** 每个节点缓存 Top-K，查询 O(prefix_length)，无需 DFS。
*Key optimization: cache Top-K at each node, query is O(prefix_length), no DFS needed.*

---

### ⚖️ 核心权衡 / Key Tradeoffs

| 决策 | 选项 A | 选项 B | 选择 |
|------|--------|--------|------|
| 存储结构 | Trie (prefix-native) | Inverted index (Elastic) | Trie for latency, ES for fuzzy |
| 更新频率 | 实时 (每次搜索) | 批量 (每10分钟) | 批量—实时代价太高 |
| 个性化 | 全局热榜 | 用户历史 | 两者结合 |
| 多语言 | Unicode Trie | 语言分片 | 按语言分片 |

**为什么不实时更新 Trie？**
每次搜索都更新 Trie 需要全局锁，QPS 百万级时会变成瓶颈。批量更新（每10分钟）是工程实际选择。
*Why not real-time Trie updates? Global locks at million QPS become a bottleneck. Batch updates every 10 min is the engineering reality.*

---

### 🚫 别踩这个坑 / Common Mistakes

**❌ 坑1: 忘记 debounce**
每次 keypress 都发请求 → 用户输入 "apple" = 5 个请求。加 debounce 50~100ms，节省 80% 请求。
*Not debouncing = 5 requests for "apple". Add debounce 50-100ms, saves 80% of requests.*

**❌ 坑2: Trie 存完整路径**
只存 top-K 在每个节点，不要在查询时做完整 DFS。
*Store top-K at each node, don't do full DFS at query time.*

**❌ 坑3: 忘记限速**
恶意用户可以爆破搜索建议接口。Rate limit + IP 封锁必须有。
*Malicious users can hammer the suggest endpoint. Rate limiting is non-negotiable.*

**❌ 坑4: 大写/Unicode 不一致**
输入 "Apple" vs "apple" 应该返回一样结果。存储前统一 lowercase + normalize。
*"Apple" and "apple" should return same results. Normalize to lowercase before storing.*

---

### 📐 规模估算 / Scale Numbers

- DAU: 10M 用户
- 平均每次搜索 5 次 keypress → 50M 建议请求/天
- QPS: ~600 req/s（峰值 2000）
- Trie 大小: 英文词典 ~100K 词 → ~50MB（可放内存）
- Cache hit rate: 60%（热词覆盖大量请求）

---

### 📚 深入阅读 / References

1. [System Design Primer — Autocomplete](https://github.com/donnemartin/system-design-primer) — 经典参考
2. [Designing Instagram's Typeahead Search](https://instagram-engineering.com/search-architecture-eeb34a936d3a) — 真实案例
3. [Trie Data Structure — NeetCode](https://neetcode.io/courses/advanced-algorithms/14) — Trie 详解

---

### 🧒 ELI5 (像我5岁一样解释)

想象你有一本超大的电话簿，里面有所有可能的词。每次你写一个字母，电话簿就帮你翻到那一页，显示最热门的词。为了不让你等太久，电话簿提前把每一页最热门的10个词写在页眉上了！
*Imagine a giant phonebook. Each letter you type, the book flips to that page and shows the top 10 popular words it already wrote at the top of the page — no searching needed!*
