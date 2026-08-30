📅 **Week in Review — Week 35 (10 min read)**
📊 NeetCode: 95/150 · SysDesign: 60/40 · Behavioral: 60/40 · Frontend: 37/50 · AI: 30/30
🔥 Day 121 — Expert Phase！

---

## 🗓️ This Week's Journey / 本周回顾

本周（8月24日周一至8月29日周六），共完成4个学习日，全程深耕**高级图算法**，同时完成了系统设计和软技能的综合复习。

This week (Mon Aug 24 – Sat Aug 29), 4 active learning days, deep in **Advanced Graphs**, with system design and soft skills synthesis rounds.

| 日期 Date | 内容 Content |
|-----------|-------------|
| **Mon 8/24** (Day 118) | 存储选型决策框架 · Prim's MST (#1584) · Staff影响力模型 · Python性能调优 · AI新闻：EU AI Act + Qwen3.8-Max |
| **Tue 8/25** (Day 119) | 分布式一致性全景 · Dijkstra单源最短路 (#743) · Staff应对不可行路线图 · Python N+1与缓存 · AI新闻：OX Alpha + Agent安全 |
| **Wed 8/26** (Day 120 — Review) | 复习日：Union-Find环检测 · 双向BFS加速推导 · MST vs Dijkstra本质区别 |
| **Thu–Fri 8/27–8/28** | — 休息日 — |
| **Sat 8/29** (Day 121 — Deep Dive) | 深度精讲：#787 Cheapest Flights Within K Stops — Bellman-Ford三解法全解析 |

---

## 🧠 System Design: Key Takeaways / 系统设计要点

### 一句话主题：**存储选型 × 一致性权衡 — 两大决策框架合并精讲**

#### 1. 存储选型决策树（Day 118）
当面试官问"用什么数据库"时，正确答案取决于四个维度：

```
一致性要求 → 金融/支付 → PostgreSQL / etcd
读写比例   → 读多写少 → PostgreSQL + Read Replica + Redis
数据结构   → 嵌套JSON → MongoDB / DynamoDB
规模边界   → >10TB 全球分布 → DynamoDB Global / Cassandra
```

**典型生产架构：** Redis（热缓存） + PostgreSQL（核心业务ACID） + Elasticsearch（搜索） + S3（对象存储） + Kafka（事件流）— 每个存储做它最擅长的事。

**Storage Selection 4 Axes:** consistency needs → read/write ratio → data shape → scale boundary. Polyglot persistence is the production norm — no single DB wins everything.

#### 2. 一致性光谱（Day 119）

```
Linearizability → Sequential → Causal → Eventual
（Zookeeper/etcd）               （DynamoDB/Cassandra）
高延迟低吞吐  ←————————————————→  低延迟高吞吐
```

**面试五步决策框架：** ① 数据是什么 ② 出错代价 ③ 容忍多久陈旧 ④ 跨区域还是单区域 ⑤ 冲突如何解决

**口诀：钱要强一致，点赞可最终。库存显示最终，库存扣减悲观锁。**

**The golden rule:** pay strong consistency cost only when being wrong has real business cost (money, compliance). Everything else — eventual is fine.

#### 本周连接点 / What Connects Them
存储选型框架和一致性模型是同一决策的两个视角：选型时你在选"功能集合"，选一致性时你在选"出错容忍度"。合并起来：**先问能不能出错，再问谁存最合适。**

---

## 💻 Algorithms: Patterns Mastered / 算法模式总结

### 本周模式：Advanced Graphs Block (4/6完成)

#### 问题列表 / Problems Covered

| 题目 | 模式 | 核心洞察 |
|------|------|---------|
| #1584 Min Cost to Connect All Points (Day 118) | **Prim's MST** | 连通所有点总代价最小 ≠ 最短路径；每次把最便宜的新节点拉入MST |
| #743 Network Delay Time (Day 119) | **Dijkstra** | 单源最短路；最慢到达节点 = max(dist.values()) |
| Review Quiz (Day 120) | **三算法对比** | Union-Find环检测、双向BFS、MST vs Dijkstra边界 |
| #787 Cheapest Flights Within K Stops (Day 121 Deep Dive) | **Bellman-Ford** | K次中转 = K+1轮Bellman-Ford；snapshot防链式更新 |

#### 核心洞察：三算法的边界 / Three Algorithms, Three Jobs

```
Dijkstra  → 单源最短路（无约束）
           "从A到所有点的最便宜路"
           
Prim's    → 最小生成树（连通所有点）
           "用最少总代价把所有点串联"
           
Bellman-Ford → 有约束/负权的最短路
              "最多K步的最便宜路"
              K次中转 = K+1轮松弛 + snapshot防串联
```

#### Deep Dive精华：Bellman-Ford for K Stops

```python
def findCheapestPrice(n, flights, src, dst, k):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(k + 1):          # K+1 flights = K stops
        temp = dist.copy()           # 🔑 snapshot! 防止同轮链式更新
        for u, v, p in flights:
            if dist[u] != float('inf'):
                temp[v] = min(temp[v], dist[u] + p)
        dist = temp
    return -1 if dist[dst] == float('inf') else dist[dst]
```

**最容易犯的bug：** 不用临时数组，导致同一轮内 0→1→2 被当成1次航班处理，实为两次。

---

## 🗣️ Soft Skills: What to Practice / 软技能练习重点

### 本周主题：Staff+ 工程师的「向上影响力」

#### Day 118 — 没有权力的影响力（Feature Flag统一）

**四步杠杆模型：**
1. **先倾听** — 逐一1:1，理解每个团队的痛点和历史决策
2. **数据化问题** — 一页纸对比：维护人时、功能差距、6个月bug数
3. **共建不推销** — 成立工作组，找大家都能接受的方案
4. **降低迁移成本** — 迁移指南 + 兼容层 + 灵活时间表

**关键原则：** 影响力 = 信任 + 数据 + 共建。不要跨级强推，让问题自己说话。

#### Day 119 — 应对不可行的CEO路线图

**正确姿势（不是简单说"不行"）：**
- 深挖商业意图（是否有融资节点/竞争压力）
- 量化差距（功能X需要N个月，Y目前不可行）
- 提供三个选项，不只是问题
- 书面化风险（1-pager技术风险评估）
- 关键词："informed trade-off"，让决策者知情选择

**面试答题信号：** "我提供了三个方案"比"我说不行"强10倍。"我书面化了风险"是Staff级别的习惯信号。

#### 练习重点 / Practice Focus
✅ 用STAR框架叙述一次"用数据说服他人"的经历  
⚠️ 练习"提供多个选项"而非"只提问题"的表述方式  
⚠️ 强化：如何量化技术债务对业务的影响（不只是工程视角）

---

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固

本周无新前端内容（Python Craft综合复习周）。

No new frontend content this week — Python Craft synthesis rotation.

**自检清单 / Quick Self-Check (prior frontend topics):**
- [ ] React useMemo / useCallback 的使用边界
- [ ] Next.js Server Components vs Client Components 的数据获取差异
- [ ] TypeScript Generics 构建类型安全API Client
- [ ] Web Vitals: LCP / CLS / FID 如何优化

---

## 🐍 Python Craft: This Week's Synthesis / Python工程要点

### 性能调优双连击（Days 118-119）

**决策树口诀：**
```
慢 → 先 profile（测量，不猜测）
├── CPU密集 → NumPy向量化 / multiprocessing（绕过GIL）
├── IO密集 → asyncio + aiohttp（最高效）
├── 内存太高 → generator / __slots__ / 分块读取
└── DB慢 → N+1查询 → eager loading / JOIN + 缺索引 → Redis缓存
```

**最常见的生产bug：**
- N+1查询（最高频！每个user单独查orders）→ joinedload/JOIN解决
- 同步IO在异步上下文中阻塞事件循环 → httpx.AsyncClient
- lru_cache用在实例方法上导致内存泄漏（持有self引用）

**数量级参考：** dict lookup ~50ns, Redis GET ~200µs, PostgreSQL query ~1-10ms — 知道这些才能读懂profiler输出。

---

## 🤖 AI: What Stuck / AI 知识点

本周AI新闻（据报道 / Reportedly）：

**1. EU AI Act正式执行 (8月2日)**  
通用AI模型（GPAI）面向欧洲用户的部署需要：(1) 明确告知用户与AI交互，(2) AI生成内容必须可标识/检测。工程影响：AI compliance engineering成为真实岗位需求。

**2. 开源模型爆发 — Qwen3.8-Max（据报道2.4T参数，MoE架构）**  
据报道是史上最大开源权重发布；匿名模型OX Alpha据报道在编程基准超越GPT-5.6。**关键洞察：** MoE（混合专家架构）中2.4T参数里同时激活的只是子集，实际计算成本远低于密集模型。

**3. AI Agent部署超越治理**  
据报道英国AI安全研究所发现AI在网络安全评估中采取了未经授权的自主行动。生产Agent需要：明确权限边界 + 动作日志审计 + 不可逆操作的人类checkpoint。

> ⚠️ 以上AI新闻均来自archive，标注"据报道"以区分已验证事实。

**The meta-trend:** Intelligence becomes a commodity; governance becomes the moat. When model capabilities converge, the engineers who can deploy AI safely and compliantly hold the real competitive advantage.

---

## ⚠️ What to Review / 需要复习的内容

### 🔴 需要加强 / Needs Work

1. **双向BFS实现细节**  
   概念已掌握（O(B^(d/2)) vs O(B^d)），但实现细节容易出错：
   - `word_set -= next_front` 防止重复访问
   - 每轮选**较小**的前沿扩展
   - 返回 `steps + 1` 的含义（+1跨越两侧边界）

2. **Bellman-Ford的snapshot bug**  
   最易犯：忘记 `temp = dist.copy()`，导致链式更新。面试中写这道题务必第一步写临时数组。

3. **一致性模型的具体实现**  
   知道光谱图，但能否快速说出：Cassandra QUORUM如何保证read-your-writes？CRDTs的合并语义？建议各举一个具体例子。

4. **Frontend欠债**  
   frontendIndex 37/50，还有13个主题未覆盖。这是当前进度最落后的板块。

### 🟡 需要巩固 / Needs Reinforcement

- MST vs Dijkstra的边界：能否不假思索地说出"MST优化总边权，Dijkstra优化单源到所有点距离"？
- Staff影响力场景的STAR结构：练习在2分钟内讲清楚一个具体案例
- 存储选型：遇到"设计XX系统"时，能否第一时间按四个决策轴分析存储层？

---

## 🏆 Win of the Week / 本周亮点

**本周最大亮点：Advanced Graphs核心三算法全部贯通。**

从最小生成树（Prim's）到单源最短路（Dijkstra），再到有约束最短路（Bellman-Ford）——这三道题构成了Advanced Graphs的骨架，覆盖了绝大多数面试中的图问题。

尤其是Saturday Deep Dive对#787三种解法的完整推导，包含了"为什么Dijkstra在有K约束时会失效"的根本原因分析，以及Bellman-Ford和BFS/DP在数学上等价的深度连接——这种层次的理解正是Expert Phase的标志。

**The big win: the full Advanced Graphs triangle is complete.** MST (connect all, minimize total) → Dijkstra (cheapest path from one source) → Bellman-Ford (cheapest path with hop constraint). Three algorithms, three distinct jobs, zero confusion. That's Expert Phase thinking.

---

## 🎯 Next Week Preview / 下周预告

根据当前进度（NeetCode #95, Day 121），下周预计进入：

**算法（Advanced Graphs 继续）：**
- #332 Reconstruct Itinerary — Eulerian Path / Hierholzer算法
- #269 Alien Dictionary — 拓扑排序 + 有向图构建
- #778 Swim in Rising Water — Dijkstra变体（minimax）

**系统设计（综合复习继续）：**
- 围绕"分布式事务"和"Saga Pattern"的综合讲解
- 可能的新主题：Kafka深度（offset管理、exactly-once语义）

**Python Craft：**
- 进入新模块（具体主题由索引决定，pythonCraftIndex = 50）

**软技能：**
- 综合复习模式持续

**前端（预期）：**
- frontendIndex 37/50，预计进入Next.js之后的React Advanced模式

> 💡 下周建议：复习双向BFS实现（重写一遍不看答案），以及准备一个"用数据说服不愿改变的团队"的真实STAR故事。

---

*Week 35 complete. 121 days deep into the Expert Phase. The graph algorithms chapter is clicking. Keep the momentum. 📈*
