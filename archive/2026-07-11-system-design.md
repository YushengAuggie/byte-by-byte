# 🏗️ 系统设计 / System Design — Day 88 · Expert Synthesis

**主题 / Topic:** Saturday Deep Dive Week — 回溯与系统设计的交叉点

---

## 综合视角 / Synthesis Perspective

今天是 Saturday Deep Dive，重点在回溯算法。系统设计综合思考：

**回溯思维在系统设计中的映射 / Backtracking Thinking in System Design:**

系统设计本质上也是回溯：你提出一个方案，发现某个约束被违反（延迟太高、成本太贵、扩展性不够），然后"回退"到上一个决策节点，选择另一条路。

**具体类比 / Concrete Analogies:**

1. **数据库选型** — 选了 SQL → 遇到 schema 变化频繁的问题 → 回退 → 换 NoSQL
2. **缓存策略** — Write-through 发现写延迟不可接受 → 回退 → Write-behind
3. **服务拆分** — 过度微服务化发现运维复杂度爆炸 → 回退 → 合并为模块化单体
4. **API 设计** — REST → 发现实时推送需求 → 回退 → 加 WebSocket 层

**剪枝的系统设计等价物 / Pruning in System Design:**
- "This violates the latency SLA" → prune the branch
- "This exceeds our ops team capacity" → prune
- "CAP theorem: you can't have both strong consistency AND high availability here" → prune

The difference: in coding, backtracking is explicit. In system design, it's called "iterating on the design."

*Today's Saturday deep dive covers: backtracking algorithms — Subsets through N-Queens.*
