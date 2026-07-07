# 🏗️ 系统设计综合 / System Design Synthesis — Day 84

> **综合模式 / Synthesis Mode** — All 60 curated topics covered. Today: Cross-topic synthesis at Expert level.

---

## 🧩 综合主题：一致性模型的全景对比
### **Consistency Models Across Distributed Systems — A Deep Comparative Study**

---

## 中文部分

### 想象你是一个新任 Staff Engineer

你刚加入一家公司，发现他们在不同系统中混用了以下技术：
- **Redis Cluster** — 缓存层
- **PostgreSQL with read replicas** — 主数据库
- **Kafka** — 事件流
- **Elasticsearch** — 搜索索引
- **DynamoDB** — 用户会话

你的老板问："这几个系统的一致性模型各是什么？会不会出问题？"

这是一个典型的 Staff-level 问题，要求你**跨系统横向对比**，而不是只会讲单个系统。

---

### 一致性模型对比矩阵

```
系统                | 一致性模型          | 读己写 | 单调读 | 适用场景
--------------------|---------------------|--------|--------|------------------
PostgreSQL Primary  | Strong              | ✅     | ✅     | 金融交易、订单
PostgreSQL Replica  | Eventual (lag ~ms)  | ❌     | ✅     | 报表、搜索
Redis (standalone)  | Strong              | ✅     | ✅     | 分布式锁、计数器
Redis Cluster       | Eventual (partns)   | ❌*    | ❌*    | 缓存（容忍失效）
Kafka               | At-least-once       | N/A    | N/A    | 事件日志
Elasticsearch       | Near-real-time (1s) | ❌     | ✅     | 搜索、分析
DynamoDB (default)  | Eventual            | ❌     | ✅     | 高吞吐读写
DynamoDB (strong)   | Strong (2x RCU)     | ✅     | ✅     | 强一致要求
```

*Redis Cluster：同一 key slot 内强一致；跨 slot 无事务保证

---

### 最容易踩的坑：读后写不一致

```python
# 场景：用户更新头像后立刻读取
async def update_avatar(user_id: str, avatar_url: str):
    # 写入 Primary
    await db.execute(
        "UPDATE users SET avatar=? WHERE id=?",
        avatar_url, user_id
    )
    
    # ❌ 立即读 Replica — 可能看到旧数据（replication lag）
    user = await db_replica.fetch("SELECT * FROM users WHERE id=?", user_id)
    return user.avatar  # 可能返回旧头像！

    # ✅ 正确：写后读 Primary，或用 read-your-writes session token
    user = await db_primary.fetch("SELECT * FROM users WHERE id=?", user_id)
    return user.avatar
```

---

### 分布式系统一致性的三个关键问题

**Q1: 什么时候选 Eventual Consistency？**
- 用户的朋友圈点赞数 ± 几个无所谓
- 搜索索引延迟 1-2 秒可接受
- 缓存失效后会 fallback 到 DB
- **关键词**：高吞吐、高可用比一致性更重要

**Q2: 什么时候必须 Strong Consistency？**
- 金融余额、库存扣减（超卖是灾难）
- 权限/认证检查（旧数据 = 安全漏洞）
- 分布式锁（多个节点同时持锁 = bug）
- **关键词**：correctness > availability

**Q3: 如何在不改架构的情况下提升一致性？**
```
策略 1: Sticky sessions — 同一用户总路由到同一副本
策略 2: Version vectors — 每次写附带版本号，读时校验
策略 3: Write-through cache — 写 DB 同时更新 cache
策略 4: CQRS — 命令走 Primary，查询走 Replica + 明确 SLA
```

---

### Staff Engineer 的思维框架

面试时遇到一致性问题，用这个框架：

```
1. CLASSIFY: 这个数据的一致性需求是什么等级？
   → 金融/库存 = Strong
   → 社交/内容 = Eventual OK
   → 搜索/缓存 = Eventual + TTL

2. SCOPE: 哪些操作需要强一致，哪些不需要？
   → 写操作 + 读己写 = Strong
   → 后台统计 = Eventual

3. TRADEOFF: 强一致的代价是什么？
   → 更高延迟 (2PC, quorum reads)
   → 更低吞吐 (DynamoDB strong read = 2x 费用)
   → 可用性降低 (CAP theorem: CP tradeoff)

4. MONITOR: 如何检测不一致？
   → Replication lag metrics
   → Read-after-write test probes
   → Data reconciliation jobs
```

---

### 真实事故案例

**GitHub 2012**: MySQL 主从延迟导致代码仓库数据短暂不一致，用户在 push 后刷新看到旧 commit。
**解法**: 引入 "read your writes" session 保证，写操作后一段时间内强制走 Primary。

**Amazon DynamoDB**: 默认 eventually consistent 读导致订单系统超卖。
**解法**: 高价值操作改用 `ConsistentRead=True`，接受 2x RCU 成本。

---

## English Summary

**The Core Question**: Across your stack, which systems give you strong consistency, which are eventual, and **what are the failure modes at the boundary?**

**Key Insight**: Most production incidents at scale don't come from a single system failing — they come from **assuming consistency across systems that have different guarantees**. The user updates their profile (strong, via Primary), then reads from Elasticsearch (eventual, 1s lag) and sees stale data.

**Interview Signal**: When a Staff-level candidate talks about consistency, they should:
1. Know the model of each system in their stack
2. Identify the "boundary" where consistency guarantees differ
3. Have concrete mitigation strategies (sticky read, version checks, CQRS)
4. Cite real operational experience, not just theory

---

## 📚 References
- [Jepsen: Distributed Systems Safety Analysis](https://jepsen.io/analyses)
- [AWS DynamoDB Strong Consistency Docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)
- [PostgreSQL Replication Docs](https://www.postgresql.org/docs/current/warm-standby.html)
- [Martin Kleppmann — Designing Data-Intensive Applications](https://dataintensive.net/)

## 🧒 ELI5
Imagine 3 kids copying notes in class. The "strong" kid copies instantly and perfectly. The "eventual" kid copies eventually but might miss a word for a few seconds. The "at-least-once" kid makes sure they write everything down but might write the same thing twice. Your job as Staff Engineer is to know which kid is copying which notes — and never accidentally trust the "eventual" kid for your math test answers.
