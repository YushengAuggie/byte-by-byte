# 🏗️ 系统设计 / System Design — Day 39

**主题 / Topic:** 分布式共识 — Raft 与 Paxos / Distributed Consensus (Raft/Paxos)
**难度 / Difficulty:** Expert | **阶段 / Phase:** Mastery

---

## 想象你在设计...

你在构建一个分布式数据库集群（想想 etcd、CockroachDB 或 Kafka）。你需要让 5 台机器就"谁是 leader"、"写操作按什么顺序执行"达成一致意见。

**如果没有共识算法，**任何一台机器宕机都可能导致脑裂（split-brain）——两个节点都认为自己是 leader，各自接受写入，数据永久分叉。

**Imagine you're designing a distributed database cluster** (like etcd, CockroachDB, or Kafka's KRaft). You need 5 machines to agree on "who is the leader" and "in what order writes happen." Without consensus, any machine failure risks split-brain — two nodes both think they're leader, data forks forever.

---

## ASCII 架构 / Architecture

```
       Client
         │  Write Request
         ▼
    ┌─────────┐
    │ Leader  │  ← elected by majority vote
    │ Node 1  │
    └────┬────┘
         │ AppendEntries RPC (log replication)
    ┌────┼─────────┐
    ▼    ▼         ▼
 Node2  Node3    Node4   Node5
 (F)    (F)      (F)     (F)

F = Follower

Quorum = ⌊N/2⌋ + 1 = 3 out of 5 must acknowledge
before leader commits an entry.

Leader Election:
  Follower timeout → Candidate → RequestVote RPC
  Gets majority → becomes Leader → heartbeat starts
```

---

## 核心概念 / Core Concepts

### Raft — 为可读性而设计 / Designed for Understandability

Raft 把共识问题分解成三个相对独立的子问题：
1. **Leader 选举** — 随机超时，先超时先投票
2. **日志复制** — Leader 把日志条目发给所有 Follower，得到多数 ACK 后提交
3. **安全性** — 已提交的日志条目永不丢失（只有拥有最新日志的节点才能成为 Leader）

Raft splits consensus into three relatively independent sub-problems:
1. **Leader Election** — randomized timeouts, first to time out requests votes
2. **Log Replication** — leader appends, waits for majority ACK, then commits
3. **Safety** — committed entries are never lost (only node with most up-to-date log can win election)

**Raft 核心保证 / Core Guarantee:**
```
Term N 中已提交的日志条目，在 Term N+1 的新 Leader 中一定存在。
An entry committed in Term N is guaranteed to exist in any leader elected in Term N+1.
```

### Paxos — 更通用但更难理解 / More General but Harder

```
Phase 1a: Proposer sends Prepare(n) to majority
Phase 1b: Acceptors respond with Promise (if n > any seen)
Phase 2a: Proposer sends Accept(n, value) with highest seen value
Phase 2b: Acceptors accept if n >= promised; Learners learn when majority accepts
```

Multi-Paxos 优化：选出稳定 Leader 后跳过 Phase 1，性能接近 Raft。
Multi-Paxos optimization: skip Phase 1 after stable leader elected — performance close to Raft.

---

## 关键权衡 / Key Tradeoffs

| 维度 | Raft | Paxos (Multi) |
|------|------|---------------|
| 可理解性 | ✅ 高 | ❌ 低 |
| 工程实现 | ✅ 直观 | ❌ 复杂 |
| 灵活性 | 🔶 固定模型 | ✅ 更通用 |
| 性能 | 相当 | 相当 |
| 实际使用 | etcd, Consul, TiKV | Chubby (Google), Zookeeper (ZAB ≈ Paxos) |

**CAP 下的位置：** 共识算法实现 CP — 有网络分区时宁可拒绝请求，也不接受可能不一致的写入。

---

## 为什么这样设计？

**为什么需要 Quorum（多数派）？**
- 5 节点集群可容忍 2 个节点宕机
- 任何两个多数派集合至少有 1 个共同节点 → 保证信息传递
- `N=2f+1` 节点可容忍 `f` 个故障

**Why Quorum?** Any two majority sets share at least 1 node, guaranteeing information propagation. N=2f+1 nodes tolerate f failures.

**为什么随机化选举超时？**
防止所有 Follower 同时成为 Candidate 造成票数分裂（split vote）。

**Why randomized election timeouts?** Prevents all followers from simultaneously becoming candidates (split vote → no winner → livelock).

---

## 别踩这个坑 / Common Mistakes

❌ **认为 Raft/Paxos 解决了一切** — 它们只解决单值或日志顺序共识，不解决拜占庭故障（节点可能发恶意消息）。拜占庭容错需要 PBFT 或 BFT 变种。

❌ **忘记 Leader 选举期间的不可用性** — 典型 Raft 实现选举超时 150-300ms，选出新 Leader 需要 1-2 轮 RTT。在此期间请求被拒绝。

❌ **混淆"已提交"与"已应用"** — 日志条目被多数派确认叫"committed"，被状态机执行叫"applied"。读从 Leader 读是强一致，从 Follower 读可能读到"committed but not applied"。

❌ **Assuming Raft/Paxos handles everything** — they handle ordering/consensus, NOT Byzantine faults (malicious nodes). Byzantine fault tolerance needs PBFT.

---

## 真实系统 / Real Systems

- **etcd** — Kubernetes 的 backing store，使用 Raft，是学习 Raft 的最佳代码库
- **CockroachDB / TiKV** — Raft group per range/region
- **Apache Kafka KRaft** — 2.8+ 用 Raft 替代 ZooKeeper
- **Google Spanner** — Paxos groups，结合 TrueTime 实现外部一致性

---

## 📚 参考资料 / References

1. [The Raft Consensus Algorithm (raft.github.io)](https://raft.github.io/) — 原论文 + 可视化动画
2. [In Search of an Understandable Consensus Algorithm (Ongaro & Ousterhout, 2014)](https://raft.github.io/raft.pdf) — Raft 原论文
3. [Paxos Made Simple — Leslie Lamport (2001)](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
4. [etcd Raft implementation](https://github.com/etcd-io/raft) — 生产级实现

---

## 🧒 ELI5

想象一个 5 人委员会做决定。Raft 的规则是：一个人举手说"我来主持会议"，只要有 3 人（多数）说"好"，他就成为主持人。主持人提议每件事，只要 3 人点头，这件事就正式通过。如果主持人突然消失，大家等一段随机时间，第一个说"我来"并获得 3 票的人成为新主持人。

Imagine a 5-person committee making decisions. The rule: one person raises their hand "I'll chair the meeting" — if 3+ people say "OK," they're the chair. Chair proposes everything, and items only pass with 3+ nods. If the chair disappears, everyone waits a random time, and the first person who asks and gets 3 votes becomes the new chair.
