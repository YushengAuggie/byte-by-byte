# Day 63 — 系统设计 / System Design

🏗️ **系统设计 / System Design** · Day 63 · Expert Phase

---

## 设计分布式锁服务 / Design a Distributed Lock Service (Zookeeper/etcd)

---

### 真实场景 / Real-World Scenario

想象你有 100 个 worker 进程，都想执行同一个定时任务（比如每天凌晨清理数据），但只能有一个执行。或者多个服务实例要更新同一份配置，必须串行化。你需要一把**跨机器的锁**——单机的 `threading.Lock` 帮不了你。

*Imagine 100 worker processes all wanting to run the same cron job, but only one should. Single-machine locks are useless across a fleet — you need a lock that lives outside any one process.*

---

### 核心需求 / Core Requirements

- **互斥 / Mutual exclusion** — 任意时刻只有一个持有者
- **防死锁 / No deadlock** — 持有者崩溃后锁能自动释放(TTL / ephemeral node)
- **容错 / Fault tolerance** — 协调服务本身不能是单点
- **可重入 / 公平性**(可选) — fencing token 防止过期持有者写脏数据

---

### 架构图 / Architecture

```
   Client A      Client B      Client C
      │             │             │
      └──── acquire("/lock/job") ──┘
                    │
        ┌───────────▼────────────┐
        │   Coordination Quorum   │   ← Raft/ZAB consensus
        │  ┌────┐ ┌────┐ ┌────┐  │
        │  │ L  │ │ F  │ │ F  │  │   Leader + Followers
        │  └────┘ └────┘ └────┘  │
        └─────────────────────────┘
   Ephemeral znode / lease key with TTL
```

---

### 两种实现思路 / Two Approaches

**Zookeeper (ephemeral sequential nodes):**
每个客户端在 `/lock` 下创建一个 ephemeral sequential 节点(`lock-0001`, `lock-0002`...)。**序号最小的获得锁**。其他客户端 watch 前一个节点——避免羊群效应(herd effect)。客户端断开 → session 超时 → ephemeral 节点自动删除 → 锁释放。

**etcd (lease + key):**
客户端先申请一个有 TTL 的 lease，再用 `Txn` 原子地 "if key not exist, put key with lease"。持有者周期性 `KeepAlive` 续租；崩溃则 lease 过期，key 自动删除。

*Zookeeper uses ephemeral sequential znodes + watch-the-predecessor to avoid the thundering herd. etcd uses a lease with TTL + a compare-and-swap transaction, with periodic keepalive.*

---

### 关键权衡 / Key Tradeoffs

- **TTL 太短** → 持有者还在干活但锁被抢走;**太长** → 崩溃后等很久才释放。需要 keepalive 自动续租。
- **Fencing token**:Martin Kleppmann 的经典论点 — GC 暂停或网络延迟会让"持有者"以为自己还拿着锁。给每次 acquire 返回单调递增的 token,被保护的资源拒绝旧 token 的写入。**没有 fencing token 的分布式锁是不安全的。**

---

### 别踩这个坑 / Common Mistakes

- ❌ 用单个 Redis `SETNX` 当生产级锁(无共识 → 主从切换会丢锁)。要用 Redlock,且仍有争议。
- ❌ 忘记 fencing token,以为锁就 100% 安全。
- ❌ 业务逻辑耗时 > TTL,锁中途失效自己却不知道。

---

### 📚 References
- [etcd: Distributed locks](https://etcd.io/docs/latest/dev-guide/api_concurrency_reference_v3/)
- [ZooKeeper Recipes: Locks](https://zookeeper.apache.org/doc/current/recipes.html#sc_recipes_Locks)
- [Kleppmann: How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)

🧒 **ELI5:** 一群小朋友想玩同一个秋千。他们排队拿号码牌,号码最小的先玩。玩的人要是中途跑掉了,他的号码牌自动消失,下一个就能玩。
