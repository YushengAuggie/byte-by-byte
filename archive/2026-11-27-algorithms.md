# 💻 算法 / Algorithms — Day 159
**题目 / Problem:** #55 Jump Game (Medium) — Greedy
**模式位置 / Pattern:** 🧩 贪心模式 (2/8) — building on the template from Day 158

---

## 🧩 贪心模式 (2/8) — 延续昨天的模版

> 昨天 #53 Maximum Subarray 用了贪心思路（局部最优 → 全局最优）。
> 今天 Jump Game 是同一模式的**经典变种**：维护一个"能到达的最远位置"。

**关键区别 vs 昨天：**
- Maximum Subarray：维护"当前子数组和"，负了就重置
- Jump Game：维护"最远可达 index"，扫描时不断更新

---

## 🔗 链接
- LeetCode: https://leetcode.com/problems/jump-game/ 🟡 Medium
- NeetCode: https://neetcode.io/problems/jump-game

---

## 现实类比 / Real-World Analogy

想象你在过一条河，河上有很多石头。每块石头上写了一个数字，表示"**从这块石头最多能跳多远**"。

```
[2, 3, 1, 1, 4]
 0  1  2  3  4  ← index
```

站在 index 0（数字 2）→ 最远能跳到 index 2
站在 index 1（数字 3）→ 最远能跳到 index 4
只要 index 4（终点）在你的"最远可达"范围内，你就能过河。

---

## 问题描述

给定整数数组 `nums`，`nums[i]` 表示在位置 `i` 最多可以跳的步数。
初始在 `nums[0]`，判断是否能到达最后一个下标。

```
Input: nums = [2,3,1,1,4] → Output: True
Input: nums = [3,2,1,0,4] → Output: False  (永远到不了 index 4)
```

---

## 映射到贪心模版

```python
# 通用贪心模版：维护局部最优量，遍历更新
# 这里的"局部最优量" = 当前能到达的最远 index

def canJump(nums: list[int]) -> bool:
    max_reach = 0  # 当前能到达的最远位置
    
    for i in range(len(nums)):
        if i > max_reach:
            # 当前位置已经超出可达范围，死路
            return False
        # 贪心：从 i 出发，最远能到哪？
        max_reach = max(max_reach, i + nums[i])
    
    return True
```

**执行轨迹 / Trace** (`nums = [2,3,1,1,4]`):
```
i=0: max_reach = max(0, 0+2) = 2
i=1: max_reach = max(2, 1+3) = 4
i=2: max_reach = max(4, 2+1) = 4
i=3: max_reach = max(4, 3+1) = 4
i=4: max_reach = max(4, 4+4) = 8  → 返回 True ✅
```

**失败案例** (`nums = [3,2,1,0,4]`):
```
i=0: max_reach = 3
i=1: max_reach = 3
i=2: max_reach = 3
i=3: max_reach = max(3, 3+0) = 3
i=4: i(4) > max_reach(3) → 返回 False ✅
```

---

## 为什么贪心正确？/ Proof of Correctness

**贪心的难点不是写代码，是证明策略正确。**

直觉：如果我们能到达位置 `i`，就一定能到达 `0..i` 之间任意位置（因为可以"停短一点"）。
因此，`max_reach` 是所有可达位置中最优的选择——不需要枚举所有路径。

反证法：假设贪心失败（认为不可达），但真实可达。那么必然存在某个位置 j < max_reach 能跳得更远——但我们已经用 max 取了所有位置的最远值，矛盾。✅

---

## 复杂度 / Complexity
- **时间：O(n)** — 一次遍历
- **空间：O(1)** — 只用一个变量

vs 暴力 DFS/BFS：O(n²)，贪心完胜

---

## 举一反三 / Pattern Connections

| 题目 | 贪心量 | 关系 |
|------|--------|------|
| #53 Maximum Subarray (Day 158) | 当前子数组和 | 同系列，负了重置 |
| **#55 Jump Game (今天)** | **最远可达 index** | **维护单个最优量** |
| #45 Jump Game II (明天) | 最少跳数 | 加一层 BFS 层计数 |
| #134 Gas Station (Day 162) | 累积油量 | 类似"可达性"贪心 |

**Jump Game II 预告：** 同样的 max_reach 思路，但要数"跳了几次"——变成 BFS level 计数。

---

## 📚 References
- https://leetcode.com/problems/jump-game/editorial/
- https://neetcode.io/solutions/jump-game
- https://en.wikipedia.org/wiki/Greedy_algorithm

## 🧒 ELI5
你在玩一个跳格子游戏，每个格子写着"最多跳几步"。你不需要想最优路线，只需要记住**你目前最远能跳到哪**。每走到一格，就更新这个最远距离。如果走着走着发现自己的位置已经超过了最远距离，就说明你"卡住了"，到不了终点。
