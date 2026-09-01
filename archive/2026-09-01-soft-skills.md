# 🗣️ 软技能 / Soft Skills — Day 123 (Expert Synthesis)

> **合成模式** — 所有 60 个行为面试问题已完成。今日：高级场景合成。

---

## 场景：你的团队和平台团队对基础设施方向存在根本性分歧
## Scenario: Your Team vs. Platform Team — Fundamental Infrastructure Disagreement

---

### 为什么这道题重要 / Why It Matters

这是 Senior/Staff 工程师最难的真实场景之一：
- 你有强烈的技术判断
- 对方是有权力的内部平台团队
- 公开对抗会损害关系，但沉默会害了产品

This is one of the hardest real scenarios for Senior/Staff engineers:
- You have strong technical judgment
- The other party is a powerful internal platform team
- Open confrontation damages relationships; silence damages the product

---

### STAR 框架拆解 / STAR Breakdown

**Situation:**
"我们的服务需要 < 50ms P99 延迟，但平台团队要求所有新服务迁移到他们基于 gRPC + 服务网格的新标准框架。初步测试显示这给我们增加了 30-40ms 延迟开销。"

**Task:**
推动平台团队为我们的场景提供例外方案，同时保持合作关系，并让 VP 不必介入。

**Action (4 个具体步骤):**

1. **量化，不要情绪化** — 带数据去对话，而不是"感觉慢"
   - 做 benchmark，记录 P50/P95/P99
   - 展示对用户 SLO 的具体影响

2. **理解对方的约束** — 平台团队有自己的 KPI
   - "你们为什么要做这个迁移？" → 通常是可观察性/安全/维护成本
   - 找到双方真正的需求，而不只是立场

3. **提出双赢方案** — 不是"我们不迁移"，而是"我们这样迁移"
   - 提议：保留直接 HTTP 内部调用 + 只在边界层加服务网格
   - 承诺：我们来实现可观察性适配，满足他们的 KPI

4. **升级有策略** — 如果僵局出现，找共同的 sponsor，不要 email chain 撕

**Result:**
"最终我们采用了 sidecar 模式：服务网格在边界层保证安全和可观察性，内部核心路径保留直连。P99 延迟降回 45ms，满足 SLO，平台团队的可观察性需求也得到满足。"

---

### ❌ 坏回答 vs ✅ 好回答

❌ **"我们坚持了自己的方案，因为我们是对的"**
→ 显示缺乏协作能力；忽略了组织健康

❌ **"我们妥协了，接受了新框架"**
→ 显示缺乏判断力；不敢捍卫工程决策

✅ **"我们用数据证明影响，理解对方约束，提出第三方案，让双方都能交付目标"**
→ 这才是 Staff 级别的系统思维

---

### Senior vs Staff 级别的区别

| 层级 | 行为 |
|---|---|
| **Senior** | 解决问题，做出妥协 |
| **Staff** | 设计流程，让未来类似冲突不再出现 |
| **Principal** | 影响平台策略，使标准本身更有弹性 |

Staff 级补充：面试时加一句："这次之后，我推动平台团队在 RFC 流程中加入性能影响评估步骤，避免下次重演。"

---

### 关键 Takeaways

1. **立场 ≠ 利益**：冲突往往来自立场对立，找到背后利益往往有第三条路
2. **数据是无声的盟友**：不是你 vs 他们，是"数据 vs 假设"
3. **保留关系，打赢打法**：今天赢了但关系坏了，下个项目你就输了

---

### 🧒 ELI5

两个部门抢一个资源，都觉得自己对。聪明的做法不是谁声音更大，而是问"你为什么需要这个？"然后找一个两个人都能要到自己真正想要的东西的方法。

---

### 📚 References
- https://www.principlesofchaos.org/ (building resilient systems that handle disagreement)
- https://hbr.org/2004/10/getting-to-yes-negotiating-agreement-without-giving-in
- https://staffeng.com/guides/staff-archetypes (Staff archetypes and influence patterns)
