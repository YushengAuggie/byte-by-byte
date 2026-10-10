# 🗣️ 软技能 / Soft Skills — Day 137 (Synthesis)
## 新鲜题目：当你的技术决策被事后证明是错的
## Fresh Scenario: When Your Technical Decision Is Proven Wrong in Hindsight

> **综合模式 / Synthesis Mode** — 超越了 60 道标准题，深入一个 Senior/Staff 工程师真正会遇到的场景。

---

### 🎯 面试题 / Interview Question

> *"Tell me about a time when you made a technical decision with confidence, and later discovered it was the wrong call. How did you handle it — with your team, with stakeholders, and within yourself?"*
>
> "说一个你曾经满怀信心做了技术决策，后来发现是错的。你怎么处理的——跟团队、跟 stakeholder，以及跟自己？"

这道题超越了「我犯了个错」，考察的是**自我意识、透明度、以及在不确定性下的工程判断力**。

---

### ⭐ STAR 拆解 / STAR Breakdown

**Situation（情境）**

我们在设计一个高并发的用户会话服务时，我力排众议选了 PostgreSQL + 应用层 sharding，而不是团队里有人建议的 Cassandra。理由是：我们的团队熟悉 Postgres，运维成本低，初期流量预测不需要 Cassandra 的写吞吐。

**Task（任务）**

我是技术 owner，需要对这个选型负责，并带着团队执行。

**Action（行动）**

上线三个月后，流量是预测的 5 倍（一个大客户签约带来的），分片 key 设计出现 hot spot，几个分片的负载是其他的 10 倍。我做了三件事：

1. **快速承认 / Acknowledge fast**：在下周的架构评审会上，我明确说「这个 hot spot 问题是我当初 sharding key 设计的失误，我来主导修复」。不甩锅给「需求变化」。

2. **带方案，不带问题 / Come with solutions**：同时提出了三个修复路径（re-shard, consistent hashing, 迁移到 Cassandra 的最小路径），并附上每个方案的风险和工时评估，让团队选。

3. **复盘机制化 / Blameless postmortem**：写了一份 postmortem，重点不是「谁的错」，而是「我们的决策框架哪里有盲点」——我们当时没有做流量 sensitivity analysis，没有问「如果 5x 呢？」。把这个加进了架构决策 checklist。

**Result（结果）**

团队最终选了 consistent hashing 方案，两个 sprint 完成迁移，没有客户感知。更重要的是，那份 postmortem 成了团队的「决策框架文档」，后来被其他团队引用。

---

### ❌ 不好的回答 vs ✅ 好的回答

**❌ 坏答案：**
> "我选了一个技术方案，后来需求变了，所以需要调整。这很正常，我们处理了。"

（回避责任，把问题归因于外部，没有展示反思）

**✅ 好答案（关键词）：**
- 「我当时的判断是 X，但我没有考虑到 Y」（具体，自我归因）
- 「我第一时间告诉了团队」（透明）
- 「我带着方案，而不是带着问题」（主动）
- 「我们把这个变成了流程改进」（系统化）

---

### 🌟 Senior/Staff 视角 / Senior & Staff Tips

在 Staff+ 层级，面试官最想看到的是：

1. **Calibration（校准感）**：你知道自己的判断在哪些情况下可能错。这比「我从不出错」更值钱。

2. **速度 vs 完美 / Velocity over perfectionism**：承认错误要快，比「等问题更大再说」代价低 10 倍。

3. **学习系统化 / Institutionalized learning**：个人的错误变成团队的 checklist，才是 Staff 级别的影响力。

4. **没有防御心 / No defensiveness**：接受反馈的方式，是面试官对你未来接受反馈方式的最好预测。

---

### 🔑 关键要点 / Key Takeaways

- 承认错误不是软弱，是高自我意识的信号
- 带方案来：「我错了，但这是下一步」比「我错了」好 10 倍
- 把个人错误转化为团队流程改进，是 Staff 级工程师的区别点
- 面试官看的是你「怎么」承认，而不只是「是否」承认

---

### 📚 参考资料 / References

- [Blameless Postmortems — Google SRE Book](https://sre.google/sre-book/postmortem-culture/)
- [The Staff Engineer's Path — Tanya Reilly, O'Reilly](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/)
- [Architectural Decision Records (ADR) — GitHub](https://adr.github.io/)

### 🧒 ELI5

就像你在乐高积木比赛里选了一种搭法，结果发现不稳。聪明的做法是：先告诉大家「这里不稳是我选错了」，再说「我有三种加固方法，我们选哪个？」，最后写下来「下次搭之前先测一下稳不稳」。这样比悄悄把积木推倒重搭，别人都不知道发生了什么，要好得多。
