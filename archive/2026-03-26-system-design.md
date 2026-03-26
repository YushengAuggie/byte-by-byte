# 🏗️ 系统设计 Day 10 / System Design Day 10
**Topic: Consistent Hashing (一致性哈希)**
*预计阅读时间 / Estimated reading time: 3 minutes*

---

## 场景 / Scenario

想象你在设计一个分布式缓存系统（比如 Redis 集群），有 10 台缓存服务器存储着数百万用户的数据。

*Imagine you're designing a distributed cache (like a Redis cluster) with 10 servers storing millions of users' data.*

一天，服务器 #3 宕机了。用系统的普通哈希 `key % 10`，你要重新分配 **90% 的数据**！

*One day, server #3 goes down. With simple modulo hashing `key % 10`, you'd need to reassign **90% of your data**!*

**一致性哈希只需要重新分配 ~1/N 的数据。这就是它的魔力。**

*Consistent hashing only reassigns ~1/N of data. That's the magic.*

---

## 架构图 / Architecture Diagram

```
                    哈希环 / Hash Ring (0 to 360°)
                         0°
                         │
              Server A   │   Server B
              (90°)      │   (180°)
                    ┌────┴────┐
              ──────┤  RING   ├──────
                    └────┬────┘
              Server D   │   Server C
              (315°)     │   (270°)
                         │
                        360°

  Key "user:123" hashes to 210° → goes to Server C (next clockwise)
  Key "user:456" hashes to 95°  → goes to Server B (next clockwise)

  Virtual Nodes (虚拟节点):
  ┌─────────────────────────────────────────┐
  │  Physical: A  B  C  D                   │
  │  Virtual:  A1 B1 C1 D1 A2 B2 C2 D2 ... │
  │  (150 virtual nodes per physical node)  │
  └─────────────────────────────────────────┘
```

**数据流 / Data Flow:**
1. 计算 key 的哈希值，映射到环上某个角度 → *Hash key to a position on the ring*
2. 顺时针找到第一个服务器节点 → *Find next server clockwise*
3. 读写该服务器 → *Read/write from that server*
4. 服务器宕机：只有它的数据转移到下一个节点 → *On failure: only its data migrates to the next node*

---

## 关键权衡 / Key Tradeoffs

**为什么这样设计？/ Why this design?**

| 普通哈希 / Simple Hash | 一致性哈希 / Consistent Hash |
|---|---|
| `key % N` 简单但脆弱 | 环形映射，容错强 |
| 增减节点 → 大规模重分配 | 增减节点 → 仅影响 ~1/N 数据 |
| 热点不均匀难处理 | 虚拟节点解决负载均衡 |

**虚拟节点的作用 / Virtual Nodes:**
每个物理节点在环上有多个虚拟位置（通常 100-200 个），解决数据分布不均的问题。*Each physical node has many virtual positions on the ring, solving uneven data distribution.*

**CAP 定理视角 / CAP Perspective:**
一致性哈希帮助在分区容错（P）下提升可用性（A），但一致性（C）需要额外机制（如 quorum reads）保证。

---

## 别踩这个坑 / Common Mistakes

❌ **虚拟节点数量太少** — 数据分布会很不均匀，导致热点
*Too few virtual nodes → uneven distribution → hot spots*

❌ **不考虑节点权重** — 新服务器内存更大，应承担更多虚拟节点
*Ignoring node weights → underutilizing powerful servers*

❌ **哈希函数选错** — 用差的哈希函数（如 MD5）导致聚集
*Bad hash function → clustering → poor distribution*

✅ 用 MurmurHash 或 FNV1a，配合 150-200 个虚拟节点，是生产环境的黄金配置。
*Use MurmurHash or FNV1a with 150-200 virtual nodes in production.*

---

## 实际使用 / Real-World Usage

- **Amazon DynamoDB** — 内部分区路由
- **Apache Cassandra** — token-based consistent hashing
- **Memcached / Twemproxy** — 客户端一致性哈希
- **Nginx upstream hash** — `hash $request_uri consistent`

---

## 📚 References

1. [Consistent Hashing — Tom White's original paper explanation](https://www.toptal.com/big-data/consistent-hashing)
2. [Amazon DynamoDB's use of consistent hashing](https://aws.amazon.com/blogs/database/amazon-dynamodb-under-the-hood-how-we-built-a-hyper-scale-database/)
3. [Cassandra's consistent hashing implementation](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)

---

## 🧒 ELI5 (解释给5岁小孩听)

想象一圈小朋友站成一个圆，每人负责一段颜色。玩具来了，看看玩具是什么颜色，顺时针找到对应颜色的小朋友，就给他。少了一个小朋友，只有他那段颜色的玩具要重新分，其他小朋友不受影响！

*Imagine kids standing in a circle, each responsible for a color range. A toy arrives — find the next kid clockwise with that color. If one kid leaves, only their toys need reassigning. Everyone else stays put!*
