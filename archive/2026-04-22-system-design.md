🏗️ **系统设计 / System Design** — Design a Search Engine

**场景 / Scenario:**
想象你在设计 Google 或 Bing 的核心搜索功能。用户输入查询，你需要在几毫秒内从数十亿个网页中返回最相关的结果。
Imagine you are designing the core search functionality of Google or Bing. A user enters a query, and you need to return the most relevant results from billions of web pages in milliseconds.

**架构图 / Architecture Diagram:**
```text
[User] --> [Load Balancer] --> [Web Servers]
                                     |
                                     v
                            [Query Processor]
                               /           \
                              /             \
                    [Index Cluster]    [Document Store]
                    (Inverted Index)   (HTML/Snippets)
                             |
                      [Ranker / ML]
```

**核心权衡 / Key Tradeoffs:**
1. **Inverted Index (倒排索引):** 为什么不直接搜网页？因为太慢。倒排索引将单词映射到包含该单词的文档列表（就像书后的索引），极大加快了查询速度。/ Why not just search web pages directly? Too slow. An inverted index maps words to a list of documents containing them (like an index at the back of a book), drastically speeding up queries.
2. **Crawling vs Indexing (爬取 vs 索引):** 爬虫（Crawler）异步抓取网页，索引器（Indexer）离线构建索引。查询时只访问索引，不接触爬虫。/ Crawlers fetch pages asynchronously, and Indexers build the index offline. Queries only hit the index, never the crawlers.
3. **Ranking (排名):** 仅找到文档不够，还需要根据相关性（如 PageRank、TF-IDF、机器学习模型）进行排序。/ Finding documents isn't enough; they must be sorted by relevance (e.g., PageRank, TF-IDF, ML models).

**常见误区 / Common Mistakes:**
- ❌ **实时更新索引 (Real-time index updates):** 每次有新网页就更新整个索引。/ Updating the entire index every time a new page is found.
- ✅ **正确做法 (Correct approach):** 使用主索引（只读，定期构建）和辅助/内存索引（处理新文档），查询时合并结果。/ Use a main index (read-only, built periodically) and an auxiliary/in-memory index (for new docs), merging results at query time.

**📚 参考文献 / References:**
- [Elasticsearch Architecture](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html)
- [How Google Search Works](https://www.google.com/search/howsearchworks/)
- [System Design: Search Engine](https://www.geeksforgeeks.org/design-a-search-engine-system-design-interview/)

**🧒 ELI5 (Explain Like I'm 5):**
搜索引擎就像一个超级图书管理员。他不一页一页翻书找答案，而是提前做了一个巨大的“词汇表”，记录了每个词在哪些书的哪一页。你一问，他查词汇表，瞬间就把书找出来了！
A search engine is like a super librarian. Instead of flipping through books page by page to find answers, they made a giant "vocabulary list" beforehand, recording which books and pages contain each word. When you ask, they check the list and find the books instantly!