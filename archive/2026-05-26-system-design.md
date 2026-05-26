# 🏗️ 系统设计 / System Design — Day 42
**Topic:** Design a Distributed File System (HDFS/GFS)
**Date:** 2026-05-26 | **Phase:** Expert

---

## 🏗️ 系统设计 / System Design — 分布式文件系统 (HDFS/GFS)
**⏱️ 预计阅读时间 / Estimated reading time: 3 min**

---

### 场景导入 / Scenario

想象你在 Google 负责存储互联网上所有网页的爬虫数据——每天新增 PB 级数据，数千台机器并发写入，任何单台机器随时可能宕机。你怎么设计这个系统？

Imagine you're at Google storing petabytes of web crawl data — terabytes added daily, thousands of machines writing concurrently, any single machine can fail at any time. How do you design this?

这就是 **GFS（Google File System）**要解决的问题，也是 Hadoop HDFS 的原型。

---

### 架构图 / Architecture

```
Clients
  │
  ├──► Master Node (NameNode)
  │      - Namespace tree (file → chunk IDs)
  │      - Chunk location map (in-memory!)
  │      - No data I/O — metadata only
  │
  └──► Chunk Servers (DataNodes)  ×N
         - Store 64MB chunks
         - 3x replication by default
         - Heartbeat to master

Write Flow:
  Client ──► Master: "Where do I write /foo/bar?"
  Master ──► Client: "Primary=CS1, replicas=CS2,CS3"
  Client ──► CS1 (pipeline): CS1→CS2→CS3 (chain replication)
  CS1 ──► Master: "Chunk committed"

Read Flow:
  Client ──► Master: "Where is chunk 42?"
  Master ──► Client: "CS2, CS5, CS7" (closest replica)
  Client ──────────► CS2 directly (bypasses master!)
```

---

### 关键设计决策 / Key Design Decisions

**1. 大文件优先（64MB chunk size）**
- 减少 master 元数据量（1PB 数据 ≈ 只需几十万 chunk 记录）
- 减少网络往返（一次 metadata 查询读取更多数据）
- ❗ 代价：小文件效率差（1KB 文件占用 64MB chunk）

**2. Master 只存元数据，不存数据**
- 所有数据直接在 client ↔ chunkserver 之间流动
- Master 成为控制平面，不是数据瓶颈
- Master 挂了 → 读写停止，但数据不丢失

**3. 三副本 + 机架感知（Rack-Aware Replication）**
```
Rack A: CS1 (primary), CS2 (replica 1)
Rack B: CS3 (replica 2)
```
- 同机架故障（断电、网络交换机）时仍有 Rack B 副本

**4. 追加写优化（Append-Only Workload）**
- GFS 的设计假设：文件一旦写入很少修改
- 支持 `record append`（原子追加），不支持随机写
- 适合 MapReduce、日志处理、大数据批处理

---

### 为什么这样设计？/ Why This Design?

| 选择 | 原因 |
|------|------|
| 中心化 Master | 简化一致性，避免分布式锁复杂度 |
| 大 chunk size | Google 的 workload 就是大文件顺序读 |
| Append-only | 简化并发控制，牺牲通用性换可靠性 |
| 心跳检测故障 | Chunkserver 每 N 秒向 master 心跳，超时自动踢出 |

---

### 别踩这个坑 / Common Mistakes

❌ **"HDFS 适合小文件"** — 错！HDFS 对小文件极不友好。1 亿个小文件 = 1 亿条 NameNode 内存记录，直接打爆 NameNode。

✅ 小文件场景改用 HBase、S3（object storage）或先合并再存 HDFS。

❌ **"Master 单点 → 系统不可用"** — 现代 HDFS 有 HA NameNode（active/standby + shared journal），不再是单点。

❌ **面试忘说 consistency model** — GFS 是 relaxed consistency（宽松一致性）。并发追加可能有重复/填充字节，应用层需处理。

---

### 📚 References
- [Google File System Paper (2003)](https://research.google/pubs/pub51/)
- [HDFS Architecture Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [Designing Data-Intensive Applications — Chapter 3 (Kleppmann)](https://dataintensive.net/)

### 🧒 ELI5
想象一个超级大图书馆。图书馆有一个"目录员"（Master/NameNode），他只记"哪本书放在哪个书架"，但不实际搬书。书架工人（ChunkServer）负责存放真正的书页。每本书被复印成3份放在不同书架，这样就算一个书架着火了，书还在。
