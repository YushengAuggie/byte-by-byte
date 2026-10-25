📅 **Week in Review — Week 33 (8 min read)**
📊 NeetCode: 109/150 · SysDesign: 60/40 · Behavioral: 60/40 · Frontend: 37/50 · AI: 30/30
🔥 Day 141 — Expert Phase

---

## 🗓️ 本周回顾 / This Week's Journey

本周是一个专注周——平日静默，周六以一道经典 Hard 题作为收尾。Edit Distance 是二维 DP 的起点，也是从「一维到二维」的重要思维跨越。

This was a focused week — quiet Mon–Fri, capped by a Saturday deep dive into a classic Hard problem. Edit Distance marks the start of the 2-D DP block and the key mental shift from 1-D to 2-D state space.

| 日期 Date | Day | 内容摘要 Summary |
|---|---|---|
| 周一–周五 Mon–Fri Oct 19–23 | — | 无发送 / No content sent this week |
| 周六 Sat Oct 24 | 141 | 🔬 Saturday Deep Dive: Edit Distance (LeetCode #72) — 二维DP深度精讲 |

---

## 🧠 系统设计要点 / System Design: Key Takeaways

本周无系统设计专题发送。

No system design content this week — the focus was entirely on the algorithms deep dive.

**Carry-forward from Expert phase synthesis:**
系统设计 60 题已全部覆盖（超出原计划 40 题），进入综合运用阶段。核心能力：从需求出发设计架构，识别权衡点，主动提出优化方向。

All 60 system design topics covered (20 beyond the original 40). Core skill now: start from requirements, identify trade-offs, proactively propose optimizations.

---

## 💻 算法模式总结 / Algorithms: Patterns Mastered

### 🎯 本周焦点：二维动态规划 / Focus: 2-D Dynamic Programming

**Edit Distance (LeetCode #72) — Levenshtein Distance**

**核心子问题定义：**
```
dp[i][j] = 将 word1 前 i 个字符变成 word2 前 j 个字符的最少操作数
```

**状态转移：**
- 字符相同：`dp[i][j] = dp[i-1][j-1]`（对角线，零代价）
- 字符不同：`dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])` → replace / delete / insert

**三个方向 = 三种操作：**
- 对角（↖）= replace
- 上方（↑）= delete from word1
- 左方（←）= insert into word1

**空间优化路径：** O(m×n) → O(n)，只保留当前行 + prev 变量记录对角值

**关键洞察：** Insert 和 Delete 是对称的——从 word1 插入 = 从 word2 删除，两者互为镜像。

---

**Key Insight (English):**
Edit Distance is the gateway to 2-D DP. The recurrence has three neighbors instead of one — that's the only new complexity. Once you visualize the table and know which direction = which operation, the rest follows.

**Real-world connections covered:**
- Git diff (Myers algorithm, a variant)
- Spell checkers (dictionary lookup within edit distance ≤ 2)
- DNA sequence alignment (Needleman-Wunsch)
- Elasticsearch fuzzy search (`fuzziness` param = edit distance threshold)
- Mobile autocorrect (edit distance + keyboard-proximity weights)

**Interview follow-ups to nail:**
1. Space optimization: O(m×n) → O(n)
2. Reconstruct the actual edit sequence (backtrack through DP table)
3. LCS connection: `editDist = m + n - 2 * LCS` (insert/delete only)
4. Weighted edit distance (different costs per operation)
5. When NOT to use edit distance (Jaro-Winkler for names, phonetic for audio)

---

## 🗣️ 软技能练习重点 / Soft Skills: What to Practice

本周无行为面试专题发送。

No behavioral content this week.

**Carry-forward reminder:** 本阶段行为面试已覆盖 60 道题（超出计划 40 题）。建议每周口头练习 2–3 个 STAR 故事，保持流利度。

Behavioral at 60/40 coverage. Keep 2–3 STAR stories fresh with spoken practice weekly — fluency degrades without rehearsal.

---

## 🎨 前端巩固 / Frontend: Concepts to Lock In

本周无前端专题发送。

No frontend content this week.

**Quick self-check on recent topics (Days 130–136 coverage):**
- [ ] 1-D DP: Climbing Stairs, House Robber, Coin Change patterns
- [ ] Python Craft synthesis: generators, serialization, database migrations
- [ ] Caching patterns: `lru_cache`, Redis, memoization strategies

Frontend: 37/50 — 13 topics remaining.

---

## 🤖 AI 知识点 / AI: What Stuck

本周无 AI 专题发送。

No AI content this week.

**Carry-forward:** AI 30/30 完成。全部话题已覆盖，包括：Transformers、RLHF、RAG、Vector DB、Agents、MoE、Multimodal、Quantization、Evaluation、AI Safety 等。建议定期回顾 AI 新闻综述，保持对领域动态的敏感度。

AI 30/30 complete. Periodically revisit AI News Roundup entries to stay current on the field.

---

## ⚠️ 需要复习的内容 / What to Review

**重点复习建议 / Priority Review List:**

1. **二维 DP 心智模型** — Edit Distance 的 DP 表格可视化需要成为直觉，不需要反推。目标：闭眼能画出转移方程。
   *2-D DP mental model* — The table visualization for Edit Distance needs to be intuitive. Goal: write the recurrence without looking.

2. **空间优化推导** — 从 O(m×n) 到 O(n) 的压缩过程，能向面试官清晰解释"为什么只需要两行"。
   *Space optimization* — Be able to explain why only two rows are needed, not just code it.

3. **1-D DP 全模式复盘** — 本周周末是进入 2-D DP 的转折点。建议快速过一遍：Climb Stairs / House Robber / LIS / Word Break / Coin Change / Max Product Subarray 的核心转移方程。
   *1-D DP pattern sweep* — Before going deeper into 2-D, do a quick 15-min mental review of all 1-D recurrences.

4. **平日连续性** — 本周平日无内容发送，打破了连续节奏。下周回到正轨。
   *Weekday cadence* — No Mon–Fri content this week. Get back on daily rhythm next week.

---

## 🏆 本周亮点 / Win of the Week

**Edit Distance 完整掌握 — 从理论到工业应用**

这道题不只是 LeetCode Hard，它是二维 DP 的「母题」，也是每天都在跑的工业代码（git diff、Elasticsearch、拼写检查背后都是它）。本周把三种实现（递归+记忆化、二维迭代、空间优化）、五个面试追问、五个实际应用全部系统梳理，是技术深度的标志性时刻。

This isn't just a LeetCode Hard — it's the archetypal 2-D DP problem powering tools used daily in production. Mastering all three implementations, five follow-up questions, and five real-world applications in one deep dive is a genuine milestone in technical depth.

**记忆口诀：**
> 两串对比找距离，dp 表格填满你
> 字符相同取对角，字符不同三选一
> 删插替换各 +1，右下角就是答案

---

## 🎯 下周预告 / Next Week Preview

**2-D DP 全面展开 — 从 Edit Distance 到 Unique Paths**

进入二维 DP 的核心题目块：

| 预计 Day | 算法 Algorithm | 主题 Topic |
|---|---|---|
| Day 142 | Unique Paths (#62) | 网格 DP — 路径计数 |
| Day 143 | Unique Paths II (#63) | 带障碍的网格 DP |
| Day 144 | Jump Game (#55) | Greedy vs DP |
| Day 145 | Jump Game II (#45) | 最少跳跃次数 |
| Day 146 | Review Day 145 | 综合复习 |

**2-D DP connecting theme:** 所有这些问题都遵循同一逻辑——定义 `dp[i][j]` 代表某个子问题，找到它与左方/上方/对角的关系，初始化边界，填表。掌握 Edit Distance 后，这些题都是变体。

*All 2-D DP problems follow the same logic: define `dp[i][j]` as a subproblem, find its relation to neighbors, initialize boundaries, fill the table. Master Edit Distance, and these are all variations.*

**目标：** 下周回归平日节奏，5天正常内容 + 周六深潜。

---

*📬 byte-by-byte · Week 33 · Week in Review*
*🗓️ Oct 19–25, 2026 · Day 141 complete · Expert Phase*
