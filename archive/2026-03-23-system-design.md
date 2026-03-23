🏗️ **系统设计 Day 8（3 min read）/ System Design Day 8**
**主题 / Topic：Database Indexing & Query Optimization（数据库索引与查询优化）**

想象你在设计一个电商网站：用户在搜索框里输入“airpods”，页面要在 100ms 内返回结果。数据在持续增长，表里有千万级商品。如果没有索引，你的数据库就像“每次找一本书都从图书馆第一排开始一页页翻”。

Imagine you’re building an e-commerce search page: user types “airpods” and expects results in ~100ms. Your products table grows to tens of millions of rows. Without indexes, the database is basically “flip through every page of the library every time.”

---

## 1) 直觉 / Intuition
**索引（Index）= 额外维护的一份“按某种顺序排好”的目录**，让数据库能更快定位行。

An **index** is an extra data structure (a “sorted directory”) that helps the DB find rows faster.

- 没索引：通常是 **全表扫描 / full table scan**（O(n) 级别的行访问）
- 有合适索引：可以 **走索引 / index seek**（更少的页读取，常见是 B+Tree 的 logN）

但索引不是免费的：
- 写入变慢（INSERT/UPDATE/DELETE 需要维护索引）
- 占用存储（索引页 + 指针）
- 选错索引会“看起来有索引但依然慢”

---

## 2) 典型架构位置 / Where this fits (ASCII)
```
[App/API]
   |
   v
[Query Builder/ORM]
   |
   v
[DB]
   |
   +--> [Index (B+Tree)]  --> (fast seek + range scan)
   |
   +--> [Table Heap/Clustered Data] --> (row fetch)
```

**关键点 / Key idea:** 很多查询慢，不是 CPU 慢，而是 **磁盘/页读取多**。索引能显著减少需要读取的页数。

---

## 3) 核心概念速记 / Core concepts
### A. B+Tree 索引（最常见）/ B+Tree index (common default)
- 适合等值查询、范围查询（`WHERE x = ?` / `WHERE x BETWEEN a AND b`）
- 叶子节点按顺序链接，范围扫描很快

### B. 覆盖索引 / Covering index
如果查询需要的列都在索引里，DB 不用回表取数据：
- MySQL/InnoDB：少一次“回表”
- Postgres：index-only scan（需要可见性信息满足条件）

If all selected columns are in the index, the DB can answer from the index alone.

### C. 组合索引的“最左前缀”/ Composite index & leftmost prefix
索引 `(a, b, c)`：
- 能用：`a`、`a,b`、`a,b,c`
- 通常不能用：只按 `b` 过滤（除非有其他技巧/统计恰好能用）

Composite index `(a,b,c)` works best when your WHERE/GROUP/ORDER starts from `a`.

### D. 选择性 / Selectivity
**选择性越高（越“能区分行”）越值得建索引。**
- `gender` 这种只有 2-3 个值的列，单列索引可能收益很小
- `user_id` 这种高基数列，非常适合索引

Higher selectivity → better index payoff.

### E. EXPLAIN / Query Plan
优化不是“猜”，是 **看执行计划**：
- 是否走了 index scan/seek
- 估算行数是否离谱（统计信息过期）
- 是否发生了排序/回表/大量 hash join

Don’t guess—use `EXPLAIN` to see the plan.

---

## 4) 为什么这样设计？/ Why this design? (Tradeoffs)
- **读多写少的系统**：多建索引通常划算（搜索、feed、报表）
- **写多读少的系统**：索引要克制（日志写入、事件流落库）

Tradeoff: indexes speed reads but slow writes and consume storage.

### 你常见会遇到的取舍 / Practical tradeoffs
1) **索引数量 vs 写入吞吐**
   - 每多一个索引，写入要多维护一次结构

2) **覆盖索引 vs 索引体积**
   - 把更多列放入索引可减少回表，但索引更大、缓存命中率可能下降

3) **单列索引 vs 组合索引**
   - 组合索引更贴近真实查询，但更难设计（依赖查询模式稳定）

---

## 5) 常见坑 / Don’t fall into this trap
1) **在低选择性列上建单列索引**（收益很小，写入还变慢）
2) **组合索引顺序错了**：`(created_at, user_id)` vs `(user_id, created_at)` 区别巨大
3) **SELECT ***：取太多列导致无法 index-only/covering，回表成本暴涨
4) **统计信息不准**：数据分布变化后，优化器选错计划（记得 ANALYZE / 维护统计）
5) **把“加索引”当唯一手段**：有时正确做法是改查询、加物化视图、分区、或引入搜索引擎

---

## 📚 深入学习 / Learn More
- Engineering blog（真实案例）: https://aws.amazon.com/blogs/database/understanding-amazon-rds-performance-insights/  
- YouTube（讲解清晰）: https://www.youtube.com/@ByteByteGo  
- 权威参考 / Authoritative: *Designing Data-Intensive Applications*（Chapter: Indexing / Storage & Retrieval）

## 🧒 ELI5
索引就像书后面的“索引页”，你不用从第一页开始翻，就能直接找到你要的内容。

An index is like the index pages at the back of a book—you jump straight to what you need instead of reading every page.