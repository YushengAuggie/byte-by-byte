# 🏗️ 系统设计 / System Design — Design a Key-Value Store

> Day 21 · Phase: Growth · Est. 3 min

---

## 想象你在设计... / Real-World Scenario

想象你在设计 Redis——世界上使用最广泛的键值存储之一。每天有数十亿次请求打到它：缓存数据、存储 session、实现排行榜。你需要设计一个既高性能又高可用的键值存储系统。

*Imagine you're designing Redis — one of the world's most widely used key-value stores. Billions of requests hit it daily: caching data, storing sessions, powering leaderboards. You need to design a high-performance, highly available key-value store.*

---

## 架构图 / Architecture Diagram

```
Client Requests
      │
      ▼
┌─────────────────────────────────────────────┐
│            API / Client Layer                │
│   GET key / SET key value / DEL key / TTL   │
└───────────────────────┬─────────────────────┘
                        │
          ┌─────────────▼──────────────┐
          │     Request Router          │
          │  (Consistent Hashing)       │
          └──────┬──────────┬───────────┘
                 │          │
     ┌───────────▼──┐   ┌───▼────────────┐
     │  Node A       │   │  Node B         │
     │ ┌───────────┐ │   │ ┌───────────┐  │
     │ │MemTable   │ │   │ │MemTable   │  │
     │ │(in-memory)│ │   │ │(in-memory)│  │
     │ └─────┬─────┘ │   │ └─────┬─────┘  │
     │       │ flush │   │       │ flush   │
     │ ┌─────▼─────┐ │   │ ┌─────▼─────┐  │
     │ │  SSTable  │ │   │ │  SSTable  │  │
     │ │ (on disk) │ │   │ │ (on disk) │  │
     │ └───────────┘ │   │ └───────────┘  │
     └───────────────┘   └────────────────┘
                │                │
                └────────────────┘
                        │
              ┌─────────▼──────────┐
              │  Replication Log    │
              │  (Write-Ahead Log)  │
              └────────────────────┘
```

**核心数据结构 / Core Data Structures:**
- **MemTable**: 内存中的有序跳表，写操作先落这里 / In-memory sorted skip-list, writes land here first
- **SSTable**: 磁盘上的不可变有序文件 / Immutable sorted files on disk
- **Write-Ahead Log (WAL)**: 崩溃恢复用 / For crash recovery
- **Bloom Filter**: 快速判断 key 是否可能存在，避免无效磁盘读 / Quickly check if key might exist to avoid unnecessary disk reads

---

## 关键权衡 / Key Tradeoffs

### 为什么这样设计？/ Why design it this way?

**1. LSM Tree vs B-Tree**

| 维度 | LSM Tree | B-Tree |
|------|----------|--------|
| 写性能 | ✅ 顺序写，极快 | 🔄 随机写，较慢 |
| 读性能 | 🔄 需合并多层 | ✅ 直接查找 |
| 空间放大 | 🔄 Compaction 前有冗余 | ✅ 较少冗余 |
| 适用场景 | 写多读少，如日志系统 | 读多写少，如数据库索引 |

> LSM 是 RocksDB、LevelDB 的基础；B-Tree 是 PostgreSQL、MySQL 的基础

**2. 一致性 vs 性能**
- **强一致性** (同步复制): 写操作等所有副本确认 → 延迟高但不丢数据
- **最终一致性** (异步复制): 写操作只等主节点 → 延迟低但可能短暂不一致

**3. 内存 vs 持久化**
- 纯内存方案 (Memcached): 极快但重启丢数据
- 混合方案 (Redis with AOF/RDB): 定期持久化，兼顾性能与持久性

---

## 别踩这个坑 / Common Mistakes

❌ **忘记处理热点 Key (Hot Keys)**
某些 key 被频繁访问（如明星发微博时 user:123 被千万次读取），单节点会成为瓶颈。
解决：本地缓存 + 请求合并 (request coalescing)

❌ **没有 TTL 机制导致内存泄漏**
不过期的 key 会撑爆内存。Redis 用懒删除 + 主动扫描双策略。

❌ **忽视 Compaction 调优**
LSM 的 Compaction 会突发 I/O 竞争，影响正常读写。生产环境要限速 (rate limiting)。

❌ **Consistent Hashing 中节点数量设置错误**
虚拟节点 (virtual nodes) 数量太少会导致负载不均衡，建议 100-200 个虚拟节点/物理节点。

---

## 📚 References

- [Designing Data-Intensive Applications — Chapter 3 (Kleppmann)](https://dataintensive.net/)
- [RocksDB Architecture Overview](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview)
- [Redis Persistence (AOF + RDB)](https://redis.io/docs/management/persistence/)

---

## 🧒 ELI5 (给五岁小孩解释)

键值存储就像一个超级快的字典。你说"帮我记住 `user:123` 的密码是 `abc`"，它就记住了。下次你问"user:123 的密码是什么"，它立刻告诉你。重要的是：这本字典要很快、要记很多东西、还要不怕服务器崩溃。LSM Tree 就像先在便利贴（内存）上写，然后定期整理到笔记本（磁盘）上——写得很快，整理在后台做。

*A key-value store is like a super-fast dictionary. You say "remember that user:123's password is abc" and it does. Later you ask "what's user:123's password?" and it tells you instantly. The trick is making it fast, able to hold tons of data, and crash-proof. LSM Tree is like jotting notes on sticky notes (memory) first, then organizing them into a notebook (disk) later — writes are super fast, cleanup happens in the background.*
