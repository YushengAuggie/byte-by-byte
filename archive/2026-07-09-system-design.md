# 系统设计综合 / System Design Synthesis — Day 86

## 🏗️ 系统设计 / System Design — 专家级综合：设计原则的统一视角

### 综合主题：当你面对"设计任何系统"时，头脑中应该有的框架

*Expert Synthesis: The unified mental model for "design any system"*

---

### 想象你在面试中被问到：设计一个实时协作 AI 编辑器

这道题综合了我们过去学过的几乎所有主题：实时协作（Google Docs）+ AI 推理服务 + 分布式缓存 + CDN + 监控系统。

*Imagine you're asked in an interview: "Design a real-time collaborative AI editor." This single question synthesizes nearly every topic we've covered.*

---

### 📐 高维框架：五个维度，任何系统都适用

```
          READ HEAVY          WRITE HEAVY
          ────────────────────────────────
高一致性  │  Google Search     │  Bank Transfer
          │  CDN + Cache       │  2PC / Saga Pattern
低一致性  │  Social Feed       │  Real-time Collab
          │  Eventual + CRDT   │  OT / WebSocket
```

**维度 1 — 读写比** (Read/Write Ratio)
- 读多写少 → CDN、缓存、读副本 (replicas)
- 写多读少 → 异步队列、批写入、LSM Tree (Cassandra)
- 平衡 → 主从复制 + 缓存层

**维度 2 — 一致性要求** (Consistency Requirement)
- 强一致性 → Raft/Paxos、2PC、单主写
- 最终一致性 → Gossip 协议、CRDT、版本向量
- 经验法则：**写钱用强一致性，写帖子用最终一致性**

**维度 3 — 规模量级** (Scale)
- < 1M DAU：单体 + 垂直扩展先行
- 1M~100M DAU：水平扩展 + 分片 + 缓存
- > 100M DAU：多区域 Active-Active + 全球负载均衡

**维度 4 — 延迟 SLA** (Latency SLA)
- p99 < 10ms → 内存数据库 (Redis)、连接池、预计算
- p99 < 100ms → 合理缓存 + 索引优化
- p99 < 1s → 异步处理可接受

**维度 5 — 失败模式** (Failure Mode)
- 关键路径 → 熔断器 + 重试 + 降级
- 数据持久 → WAL + 多副本 + 跨区域备份
- 幂等设计 → 所有写操作带唯一 ID

---

### 🔗 各系统的核心取舍回顾

| 系统 | 核心挑战 | 关键决策 |
|------|----------|----------|
| URL Shortener | 读多写少，全球分布 | 一致性哈希 + CDN |
| Chat (WhatsApp) | 实时推送，在线状态 | WebSocket + Presence Service |
| YouTube | 视频转码，CDN 分发 | Async pipeline + Edge cache |
| Rate Limiter | 分布式计数，低延迟 | Redis + Token Bucket |
| Notification | 多渠道，可靠投递 | Message Queue + Retry |
| Search Autocomplete | 低延迟，前缀匹配 | Trie in Redis + 预热 |
| Distributed Cache | 驱逐策略，一致性 | Consistent Hashing + LRU |
| LLM Serving | 显存瓶颈，长尾延迟 | KV Cache + Continuous Batching |

---

### 🎯 面试答题的七步法

**当你拿到任何系统设计题：**

```
1. 澄清需求 (2 min)
   └─ QPS / DAU / 数据量 / SLA / 地理分布

2. 估算规模 (2 min)
   └─ 存储量 = QPS × 数据大小 × 保留时间
   └─ 带宽 = QPS × 请求大小

3. 高层设计 (5 min)
   └─ Client → LB → API Gateway → Service → DB/Cache

4. 数据模型 (3 min)
   └─ SQL vs NoSQL 选择依据
   └─ 关键表结构 / 索引设计

5. 深入细节 (8 min)
   └─ 针对面试官关注点展开（通常是最难的那个）

6. 扩展与优化 (3 min)
   └─ 瓶颈在哪？如何水平扩展？

7. 权衡总结 (2 min)
   └─ "我选择 X 而不是 Y，因为在当前场景下..."
```

---

### ⚠️ 高频陷阱（综合版）

1. **过早优化** — 不问规模就上分布式，面试官扣分
2. **忽略 CAP 取舍** — 说"强一致+高可用+分区容忍"三者全选，不现实
3. **数据库选错** — 关系型数据用 MongoDB，图数据用 PostgreSQL，都是减分项
4. **单点故障** — 设计中没有 LB、没有副本，面试官会追问
5. **不说数字** — "会很慢"不如"p99 > 500ms 时触发报警"

---

### 📚 References

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications (DDIA)](https://dataintensive.net/)
- [The Architecture of Open Source Applications](https://aosabook.org)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### 🧒 ELI5

设计系统就像搭乐高。你要先问：要搭多大？能倒塌吗？谁会来玩？
然后选对积木块（数据库、缓存、队列），按顺序搭起来，最后检查每块会不会掉。

*Designing systems is like building with LEGO. First ask: how big? Can it fall? Who will use it? Then pick the right pieces (database, cache, queue), stack them in order, and check which pieces might fall.*
