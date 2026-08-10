# 🏗️ 系统设计综合 / System Design Synthesis — Day 111

## 分布式一致性协议全景对比
## Distributed Consensus: Raft vs ZAB vs Paxos — When to Pick What

你已经学了 Raft (etcd)、ZooKeeper (ZAB)、以及多个依赖一致性的系统。今天来综合对比。
You've studied Raft (etcd), ZooKeeper (ZAB), and systems built on them. Today: a synthesis.

---

### 问题的本质 / The Core Problem

**多节点如何就一个值达成一致，即使有节点宕机？**
How do multiple nodes agree on a single value even when some crash?

所有共识算法都解决这个问题，但设计权衡各不相同。
All consensus algorithms solve this — with very different tradeoffs.

---

### 三协议对比 / Protocol Comparison

```
                Raft             ZAB (ZooKeeper)    Paxos
Leader?         Strong leader    Primary            Varies
Reads on        Leader only      Any follower       Any
  followers?    (linearizable)   (may be stale)     
Writes          Leader only      Primary only       Leader only
Use case        etcd, Consul     ZooKeeper          Spanner, Chubby
Complexity      Simpler ✅       Moderate           Very complex ❌
```

---

### 关键洞察 / Key Insights

**Raft vs ZAB 最大区别：**
- **Raft:** follower 不直接服务读取 → 强一致性，每次读都走 leader
- **ZAB:** follower 可服务读取，但可能读到旧数据（eventual reads）→ 高吞吐

**何时选哪个？**
| 需求 | 选择 |
|------|------|
| 强一致元数据存储 (Kubernetes) | Raft → etcd |
| 配置管理 + 分布式协调 (Kafka) | ZAB → ZooKeeper |
| 超大规模全球分布 (Google) | Paxos → Spanner |

---

### 你学过的系统用了什么共识？ / Systems You've Studied

| 系统 | 共识层 |
|------|--------|
| Kubernetes | etcd (Raft) |
| Kafka (旧) | ZooKeeper; 新版迁移至 KRaft |
| Google Spanner | Multi-Paxos |
| TiDB | Raft (multi-region) |
| Consul | Raft |

---

### 别踩这个坑 / Common Pitfalls

❌ 把 etcd 当数据库用 → etcd 只存小 key-value 元数据，建议总数据 < 8 GB
❌ ZooKeeper 节点数设偶数 → 必须奇数（需要 majority quorum = N/2+1）
❌ 忽略 leader 切换窗口的 stale read → 用 linearizable reads 或 watch 机制解决
❌ 把共识协议当成性能优化 → 共识本质是牺牲性能换安全性

---

### 📚 参考 / References
- https://raft.github.io/
- https://zookeeper.apache.org/doc/current/zookeeperInternals.html
- https://www.cs.cornell.edu/courses/cs6452/2012sp/papers/paxos-simple-web.pdf

### 🧒 ELI5
想象班级选班长：Raft 要求每次投票全班 >50% 同意才算数（严格但慢）；ZAB 让班长先宣布决定然后大家记下来（快但可能同学还没更新）；Paxos 是数学最严格的版本，但最难理解，Google 才用得起。
