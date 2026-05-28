# 🏗️ 系统设计 / System Design — Design a Time-Series Database (InfluxDB)
*Day 52 · Expert Phase · ~3 min read*

---

## 场景 / Scenario

想象你在设计 Datadog 或 Prometheus 的存储后端。每秒要写入数百万条指标数据：CPU 使用率、请求延迟、错误率……这些数据都有一个关键特征：**时间是主键**。你会如何设计？

*Imagine building the storage backend for Datadog or Prometheus. You're ingesting millions of metric data points per second: CPU usage, request latency, error rates. These all share one key property: **time is the primary key**. How would you design this?*

---

## 架构图 / Architecture

```
                    ┌─────────────────────────────────────┐
  Producers          │         Ingestion Layer              │
  ─────────          │  ┌─────────┐    ┌──────────────┐    │
  App Metrics ──────►│  │  HTTP   │    │   WAL        │    │
  Server Stats──────►│  │  API    │───►│ (Write-Ahead │    │
  IoT Sensors ──────►│  │         │    │    Log)      │    │
                     │  └─────────┘    └──────┬───────┘    │
                     └────────────────────────┼────────────┘
                                              │ batch flush
                     ┌────────────────────────▼────────────┐
                     │         Storage Engine               │
                     │                                      │
                     │  ┌──────────────────────────────┐   │
                     │  │ In-Memory Write Buffer        │   │
                     │  │ (TSM Tree hot data ~1h)       │   │
                     │  └──────────────┬───────────────┘   │
                     │                 │ compaction         │
                     │  ┌──────────────▼───────────────┐   │
                     │  │ Columnar Storage (TSM Files)  │   │
                     │  │ time│cpu│mem│req_rate│...     │   │
                     │  │ ────┼───┼───┼────────┼───     │   │
                     │  │ t1  │80 │60 │ 1200   │        │   │
                     │  │ t2  │82 │61 │ 1250   │        │   │
                     │  └──────────────────────────────┘   │
                     │                                      │
                     │  ┌──────────────────────────────┐   │
                     │  │ Tag Index (inverted index)    │   │
                     │  │ host=web-01 → [t1,t2,t3...]   │   │
                     │  │ region=us-west → [...]        │   │
                     │  └──────────────────────────────┘   │
                     └────────────────────┬────────────────┘
                                          │
                     ┌────────────────────▼────────────────┐
                     │      Retention & Downsampling        │
                     │  raw: 7d → 1m avg: 30d → 1h avg: 1y │
                     └─────────────────────────────────────┘
```

---

## 核心设计决策 / Key Design Decisions

### 1. 列式存储 (Columnar Storage)
**为什么？** 时序查询几乎总是范围查询（"过去1小时的CPU"），列式存储让你只读需要的列。压缩率也更高 — 相邻时间点的值变化小，Delta + Gorilla 编码可压缩 90%+。

*Why columnar? Time-series queries are almost always range scans ("last hour of CPU"). Columnar lets you read only the columns you need. Compression is also far better — adjacent values change minimally, and Delta + Gorilla encoding achieves 90%+ compression.*

### 2. TSM Tree (Time-Structured Merge Tree)
类似 LSM Tree，但针对时序优化：
- **Write Buffer** → 写入内存，定期 flush 到磁盘
- **Compaction** → 合并小文件，有序，利于范围扫描
- **Append-only** → 时间天然有序，无需像 B-Tree 那样随机写

*Similar to LSM Tree but time-optimized. Writes go to memory buffer, flush to disk periodically. Compaction merges small files. Append-only nature aligns with time's natural ordering.*

### 3. 倒排索引 (Inverted Index for Tags)
```
tag_index["host=web-01"] → [series_1, series_5, series_12]
tag_index["region=us-west"] → [series_1, series_3]
```
允许高效过滤：`SELECT cpu WHERE host='web-01' AND region='us-west'`

### 4. 数据保留策略 (Retention + Downsampling)
```
Raw data (1s resolution) → keep 7 days
1-minute averages        → keep 30 days  
1-hour averages          → keep 1 year
Delete oldest            → automatic TTL
```
这是时序数据库的"超能力" — 自动降精度。

---

## 常见错误 / Common Mistakes

❌ **用关系型数据库存时序数据**
每秒百万写入 → 行锁、B-Tree 写放大、索引膨胀。PostgreSQL 可以用 TimescaleDB 扩展，但裸 Postgres 扛不住。

❌ **Tag cardinality 爆炸**
把 user_id 或 trace_id 作为 tag → 倒排索引无限膨胀。Tags 应该是**低基数**的（host、region、env），高基数数据放 fields。

❌ **忽略时钟漂移**
分布式系统中，不同节点的时间戳可能乱序到达。需要处理 **out-of-order writes**（InfluxDB 有 max-allowed-past-time 配置）。

---

## 📚 参考资料 / References

- [InfluxDB TSM Engine Architecture](https://docs.influxdata.com/influxdb/v1/concepts/storage_engine/) — official deep dive
- [Gorilla: A Fast, Scalable, In-Memory Time Series Database (Meta)](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf) — Facebook's TSDB paper
- [TimescaleDB Architecture](https://docs.timescale.com/about/latest/timescaledb-editions/) — Postgres-based TSDB

---

## 🧒 ELI5

时序数据库就像一本**每秒自动记日记**的笔记本。普通数据库像一本可以随意翻改的书，时序数据库像一卷纸带 — 只往前走，不往回改，查的时候按时间切一段就行。而且它会自动帮你把昨天的记录"压缩摘要"，省空间。

*A time-series database is like a notebook that auto-journals every second. Regular databases are like books you can edit anywhere. A TSDB is like a paper tape — always moves forward, never edits old entries, and it automatically "summarizes" old data to save space.*
