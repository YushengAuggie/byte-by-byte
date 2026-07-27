# 系统设计综合 / System Design Synthesis — Day 101
**Day 61 (Synthesis Mode) · Expert Phase**

---

## 🏗️ 系统设计 / System Design — Expert Synthesis

### 从单点到全局：分布式系统的权衡地图
### From Single Points to Global Scale: The Trade-off Map of Distributed Systems

---

### 想象你在做技术 Review / Imagine You're Doing a Tech Review

你的团队正在设计一个新的后端服务。Tech Lead 问了这个问题：

> "我们用 Kafka 还是 Redis Pub/Sub？要不要加 Consistent Hashing？要不要用 Saga 还是 2PC？"

这些不是孤立的问题——它们背后是一张**权衡地图 (Trade-off Map)**。

Your team is designing a new backend service. The Tech Lead asks:

> "Kafka vs Redis Pub/Sub? Consistent Hashing or not? Saga vs 2PC?"

These aren't isolated questions — they're all part of a **trade-off map**.

---

### 核心权衡矩阵 / Core Trade-off Matrix

```
TOPIC               OPTION A              OPTION B           WHEN TO PICK A
─────────────────────────────────────────────────────────────────────────
消息队列            Kafka                 Redis Pub/Sub      持久化/重放/高吞吐
Message Queue       (persistent,durable)  (ephemeral,fast)   vs 低延迟/简单订阅

分布式事务          2PC (Strong)          Saga (Eventual)    金融强一致 vs
Distributed Txn     (blocking, slow)      (async, complex)   跨微服务最终一致

缓存策略            Write-Through         Write-Behind        读多写少 vs
Cache Strategy      (sync, safe)          (async, faster)     写密集型

一致性哈希          Consistent Hashing    Modulo Hashing      节点增减频繁 vs
Partitioning        (minimal resharding)  (simple, mass       固定分片数
                                           resharding)

数据库选型          PostgreSQL (SQL)       Cassandra (NoSQL)   复杂查询/事务 vs
DB Selection        (ACID, joins)         (AP, wide-column)   写密集/地理分布

API 通信            REST                  gRPC               公开 API vs
API Protocol        (human-readable)      (binary, fast)      内部微服务
```

---

### 系统组合：三种典型架构 / Three Archetypical Architectures

#### 1. 读密集型系统 (Read-Heavy) — e.g. Twitter Feed
```
[Client] → [CDN/Edge Cache]
              ↓
         [API Gateway + Rate Limiter]
              ↓
    [Read Replicas × N] ← hot data
         [Redis Cache Layer]
              ↓
         [Primary DB] ← writes only
```
**关键洞察 / Key Insight:** 90%流量命中缓存，主库只处理写。  
Read replicas + CDN absorb load. Primary DB is write-only.

#### 2. 写密集型系统 (Write-Heavy) — e.g. IoT / Metrics
```
[Devices] → [Kafka / Kinesis] → [Stream Processor]
                                      ↓
                              [Time-Series DB] (InfluxDB)
                                      ↓
                              [Aggregation Layer]
                                      ↓
                              [Dashboard / Alerts]
```
**关键洞察 / Key Insight:** 写操作先缓冲，异步落库。背压 (backpressure) 保护下游。  
Buffer writes with a queue. Protect downstream with backpressure.

#### 3. 事务型系统 (Transaction-Heavy) — e.g. Payment
```
[API] → [Idempotency Check] → [DB Transaction (2PC or Saga)]
              ↓ (duplicate?)
         [Return cached result]
              ↓ (new?)
    [Debit Account → Credit Account → Record Ledger]
         via Saga: each step + compensating transaction
```
**关键洞察 / Key Insight:** Idempotency key 防止重复扣款。Saga 比 2PC 更适合跨服务。  
Idempotency keys prevent duplicate charges. Saga > 2PC across microservices.

---

### 常见 Expert 面试陷阱 / Expert Interview Traps

| 陷阱 Trap | 错误思路 Wrong | 正确思路 Right |
|-----------|--------------|----------------|
| "用 Redis 做持久化" | 默认 Redis 可靠 | Redis 是缓存，不是主库；配合持久化 DB |
| "加更多副本解决写瓶颈" | 副本减少读压力 | 写瓶颈需要分片 (sharding)，不是副本 |
| "Kafka 解决一切消息问题" | Kafka 万能 | 简单通知用 Redis Pub/Sub；Kafka 适合持久化/重放 |
| "微服务就要用 2PC" | 跨服务强一致 | 2PC 阻塞性强，跨服务首选 Saga + 补偿 |

---

### 面试答题框架：5分钟架构对话 / 5-Minute Architecture Framework

```
1. 澄清需求 (1 min): QPS? DAU? 读写比? 强一致还是最终一致?
2. 高层架构 (2 min): 画3层图 (Client → Service → DB)
3. 深入关键组件 (1 min): 面试官感兴趣的那一层
4. 权衡讨论 (1 min): "我选X而不是Y，因为..."
```

---

### 📚 References
- [System Design Primer — Scalability](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications — Kleppmann](https://dataintensive.net/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### 🧒 ELI5
**如果你家有5个孩子喝水：**  
- **读密集 =** 提前多备几瓶水 (缓存)
- **写密集 =** 所有孩子同时倒水，先排队等 (队列)
- **事务型 =** 钱包扣钱和存钱必须同时成功，否则都撤销

**If you have 5 kids at home:**  
- **Read-heavy =** Pre-fill many water bottles (cache)
- **Write-heavy =** Everyone pours at once; line up first (queue)
- **Transactional =** Debit and credit must both succeed, or neither does
