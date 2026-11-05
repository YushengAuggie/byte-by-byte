# Day 148 — System Design Synthesis: 分布式一致性全景对比

> **综合深化 / Expert Synthesis** — Day 148

---

🏗️ **系统设计综合 / System Design Synthesis**

## 主题：分布式状态管理三大范式对比
### Distributed State Management: Consensus vs CRDT vs Event Sourcing

---

### 场景设定 / The Problem Space

想象你在构建一个**全球协作工具**（类似 Notion + Figma 合体）：
- 多个数据中心，每个都要能写入
- 网络分区时系统不能停止工作
- 最终所有节点的数据要一致

Imagine building a **global collaborative tool**: multi-region writes, partition tolerance, eventual consistency. Three architectures compete for this problem — and each makes a radically different bet.

---

### 范式一：强共识 / Strong Consensus (Raft/Paxos)

```
          ┌─────────────┐
          │   Leader    │◄──── All writes go here
          │  (Primary)  │
          └──────┬──────┘
                 │ Replicate (majority quorum)
        ┌────────┼────────┐
        ▼        ▼        ▼
   Follower1  Follower2  Follower3
   (US-East)  (EU-West)  (AP-South)

Write: Leader → 2/3 followers acknowledge → Commit
Read: From leader (linearizable) or any (stale)
```

**适用场景 / When to use:**
- 金融交易、分布式锁（etcd、ZooKeeper）
- 需要严格线性一致性的场景
- Financial transactions, distributed locks, config coordination

**代价 / The cost:**
- 跨大洲写延迟 = 网络 RTT（~100-200ms）
- Leader 成为瓶颈
- Leader failure → 选举暂停（typically 150-300ms）

---

### 范式二：CRDT（无冲突复制数据类型）
### Conflict-free Replicated Data Types

```
   Region A          Region B          Region C
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ Counter=5│      │ Counter=3│      │ Counter=7│
  │ (+2 ops) │      │ (+1 ops) │      │ (+3 ops) │
  └────┬─────┘      └────┬─────┘      └────┬─────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                    Merge: max or union
                    Final: Counter=15 ✅
```

**CRDT 的魔法 / The magic:**
```python
# G-Counter CRDT: each node only increments its own slot
state = {"node_a": 0, "node_b": 0, "node_c": 0}

def increment(node_id):
    state[node_id] += 1

def merge(remote_state):
    # Take max of each node's counter — always safe to merge
    for node, count in remote_state.items():
        state[node] = max(state.get(node, 0), count)

def value():
    return sum(state.values())

# No coordination needed! Any order of merges gives same result.
```

**适用场景:** 协同编辑（Figma、文档光标位置）、购物车、点赞计数、在线状态
**局限:** 复杂数据结构难以建模为 CRDT；某些操作天然不可交换（如"先删后加" vs "先加后删"）

---

### 范式三：事件溯源 + 最终一致性
### Event Sourcing + Eventual Consistency

```
  User Action
      │
      ▼
  Event Log (immutable, append-only)
  ┌────────────────────────────────────────┐
  │ t1: UserCreated{id:123}               │
  │ t2: ItemAdded{id:123, item:"book"}    │
  │ t3: ItemRemoved{id:123, item:"book"}  │
  │ t4: OrderPlaced{id:123, total:29.99}  │
  └────────────────────────────────────────┘
      │
      ▼ Fan-out (async, best-effort)
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Orders   │  │Analytics │  │ Search   │
  │ DB       │  │ DB       │  │ Index    │
  └──────────┘  └──────────┘  └──────────┘
  (may lag     (may lag        (may lag
   100ms)       1s)            500ms)
```

**适用场景:** 审计日志、复杂领域（电商、银行）、需要时间旅行查询
**代价:** 读取需重放事件（慢），schema 演进复杂，eventual consistency 对某些场景不可接受

---

### 三大范式权衡矩阵 / Decision Matrix

| 维度 | 强共识 | CRDT | 事件溯源 |
|------|--------|------|----------|
| **一致性** | 线性 | 最终 | 最终 |
| **写可用性** | 需 Leader | 全部节点 | 全部节点 |
| **写延迟** | 高（RTT） | 低 | 低 |
| **冲突解决** | 无冲突（串行化） | 数学保证 | 业务逻辑 |
| **复杂度** | 中（运维） | 高（设计） | 高（事件设计） |
| **典型系统** | etcd, CockroachDB | Riak, Automerge | Kafka+ES, Axon |

---

### 实战决策树 / Decision Tree

```
需要严格线性一致性？（金融/锁）
  → YES: 强共识 (Raft)

数据是多方并发编辑（协作类）？
  → YES: CRDT

需要完整审计历史/时间旅行查询？
  → YES: Event Sourcing

多写多读，容忍短暂不一致？
  → Leaderless Replication (Cassandra) + read repair
```

---

### 🧒 ELI5

**强共识** = 一个人（Leader）说了算，大家都要等他点头才能继续，慢但不会出错。
**CRDT** = 大家都可以改，但只能"加"不能"减"（或用数学魔法让合并永远安全）。
**事件溯源** = 不记录当前状态，只记录所有发生过的事，随时重播历史。

---

### 📚 References
- https://raft.github.io/ — Raft consensus algorithm visualization
- https://crdt.tech/ — CRDT reference implementations and papers
- https://martinfowler.com/eaaDev/EventSourcing.html — Event Sourcing explained
- https://www.cs.cornell.edu/projects/ladis2009/talks/dean-keynote-ladis2009.pdf — Google's distributed systems lessons
