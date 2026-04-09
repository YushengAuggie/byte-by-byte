🏗️ **系统设计 / System Design**

**想象你在设计... / Imagine you are designing...**
一个键值存储系统（Key-Value Store），比如 Amazon DynamoDB 或 Redis。
A Key-Value Store, like Amazon DynamoDB or Redis.

**架构图 / Architecture Diagram**
```
Client -> [ API Gateway ] -> [ Load Balancer ]
                                |
                   +------------+------------+
                   |            |            |
             [ Node A ]   [ Node B ]   [ Node C ]
             (Data 1-3)   (Data 4-6)   (Data 7-9)
                   |            |            |
                   +---(Gossip Protocol)-----+
```

**核心权衡 / Key Tradeoffs**
- **CAP 定理 (CAP Theorem):** 在分布式系统中，你只能在一致性（Consistency）、可用性（Availability）和分区容错性（Partition Tolerance）中选择两个。大多数键值存储（如 Dynamo）选择 AP（高可用性），通过最终一致性来解决冲突。
- **数据分片 (Data Partitioning):** 使用一致性哈希（Consistent Hashing）将数据均匀分布在多个节点上，并在节点增减时最小化数据迁移。
- **数据复制 (Data Replication):** 将数据复制到多个节点（如 N=3）以保证高可用性和容错性。

**常见误区 / Common Mistakes**
- **单点故障 (Single Point of Failure):** 依赖单一的协调节点。应使用去中心化的架构（如 Gossip 协议）进行集群成员管理。
- **忽略冲突解决 (Ignoring Conflict Resolution):** 在最终一致性模型中，并发写入可能导致冲突。需要使用向量时钟（Vector Clocks）或最后写入胜出（LWW）来解决。

**📚 References**
- [Dynamo: Amazon’s Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [System Design: Key-Value Store](https://bytebytego.com/courses/system-design-interview/design-a-key-value-store)
- [Redis Cluster Specification](https://redis.io/docs/reference/cluster-spec/)

**🧒 ELI5 (Explain Like I'm 5)**
想象你有很多个抽屉（节点）来放玩具（数据）。为了不让一个抽屉太满，你用一个特殊的规则（一致性哈希）决定玩具放哪个抽屉。而且，为了防止某个抽屉坏了，你把每个玩具都复制三份，放在不同的抽屉里。
Imagine you have many drawers (nodes) to store toys (data). To avoid overfilling one drawer, you use a special rule (consistent hashing) to decide where each toy goes. Also, in case a drawer breaks, you make 3 copies of each toy and put them in different drawers.
