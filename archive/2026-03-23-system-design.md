# 🏗️ 系统设计 Day 8 / System Design Day 8
**主题 / Topic:** 数据库索引与查询优化 / Database Indexing & Query Optimization
**分类 / Category:** Fundamentals · Beginner · Foundation Phase

---

## 🌍 真实场景 / Real-World Scenario

想象你在设计 Twitter 的搜索功能。用户搜索某条推文，数据库里有 **5 亿条记录**——如果没有索引，数据库必须逐行扫描，花几分钟才能返回结果。有了索引，查询可以在 **几毫秒内** 完成。

*Imagine you're designing Twitter's search feature. Users search for tweets, and there are 500 million records in the database — without indexing, the database must scan row-by-row, taking minutes. With indexes, queries return in milliseconds.*

---

## 🏛️ 架构图 / ASCII Architecture Diagram

```
User Query: "SELECT * FROM tweets WHERE user_id = 42 AND created_at > '2026-01-01'"

WITHOUT INDEX:                     WITH INDEX:
┌─────────────────────┐           ┌─────────────────────┐
│   Full Table Scan   │           │   B-Tree Index      │
│   Row 1: user_id=1  │           │   (user_id, date)   │
│   Row 2: user_id=15 │           │        Root         │
│   Row 3: user_id=42 │           │       /    \        │
│   ...               │           │    Node    Node     │
│   Row 500M: ???     │           │   /  \    /  \      │
│   ❌ 500M reads     │           │  L1  L2  L3  L4     │
└─────────────────────┘           │  ✅ ~log(N) reads   │
                                  └─────────────────────┘

Index Storage:
┌──────────┬──────────┬─────────────────┐
│ user_id  │   date   │  row_pointer →  │
│    42    │ 2026-01  │  page 1042, r3  │
│    42    │ 2026-02  │  page 2891, r7  │
└──────────┴──────────┴─────────────────┘
```

---

## ⚖️ 关键权衡 / Key Tradeoffs (为什么这样设计？)

### 索引加速读，但拖慢写 / Indexes Speed Reads, Slow Writes

| 指标 / Metric | 无索引 Without Index | 有索引 With Index |
|---|---|---|
| SELECT 查询 | O(N) 全表扫描 | O(log N) B-Tree 遍历 |
| INSERT / UPDATE | 快 ⚡ | 慢（需维护索引）|
| 存储空间 Storage | 小 | 更大（索引占空间）|

**为什么用 B-Tree？** B-Tree 保持数据有序，支持范围查询（`BETWEEN`, `>`），适合绝大多数业务场景。  
*Why B-Tree? It keeps data sorted, supports range queries (`BETWEEN`, `>`), fitting most business use cases.*

**复合索引的列顺序很重要 / Column order in composite indexes matters:**
```sql
-- Index on (user_id, created_at)
-- ✅ Can use: WHERE user_id = 42 AND created_at > '2026-01-01'
-- ✅ Can use: WHERE user_id = 42
-- ❌ Cannot use: WHERE created_at > '2026-01-01' (alone)
-- 最左前缀原则 / Leftmost prefix rule!
```

---

## ⚠️ 常见错误 / Common Mistakes (别踩这个坑)

1. **过度索引 Over-indexing** — 给每列都加索引？写操作会变得极慢。生产中见过 INSERT 耗时 10 秒的案例。  
   *Adding an index to every column? Writes become painfully slow.*

2. **索引列上做函数运算 Function on indexed column** — `WHERE YEAR(created_at) = 2026` 无法使用索引！改用 `WHERE created_at BETWEEN '2026-01-01' AND '2026-12-31'`。  
   *`WHERE YEAR(created_at) = 2026` can't use the index! Use range instead.*

3. **忽视 EXPLAIN / Ignoring EXPLAIN** — 不跑 `EXPLAIN SELECT ...` 怎么知道是否用到了索引？  
   *Never running `EXPLAIN SELECT ...` — how do you even know if the index is used?*

4. **N+1 查询问题 / N+1 Query Problem** — 循环里查询数据库，100 次查询 vs 1 次 JOIN。  
   *Querying inside a loop: 100 queries vs 1 JOIN.*

---

## 📚 References

- [PostgreSQL Index Documentation](https://www.postgresql.org/docs/current/indexes.html)
- [Use The Index, Luke — Free SQL Indexing Guide](https://use-the-index-luke.com/)
- [MySQL EXPLAIN Output Format](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)

## 🧒 ELI5 (小朋友也能懂)

索引就像书的**目录**。没有目录，你要找"索引"这个词，就得从第1页翻到最后。有了目录，直接翻到第 283 页。数据库索引做的是同样的事情——不用"翻遍所有数据"，直接跳到你要找的地方。

*An index is like a book's table of contents. Without it, you'd flip through every page to find "indexing." With a table of contents, you jump right to page 283. Database indexes do the same thing — skip straight to what you need.*
