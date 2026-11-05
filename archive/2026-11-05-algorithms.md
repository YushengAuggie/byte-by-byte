# Day 148 — Algorithms: #494 Target Sum (Medium) — 2-D DP

> 🧩 **二维动态规划 (5/11)** — building on the template from earlier in this block

---

💻 **算法 / Algorithms**

🔗 [LeetCode #494 Target Sum](https://leetcode.com/problems/target-sum/) 🟡 Medium
📹 [NeetCode Video](https://neetcode.io/problems/target-sum)

---

## 🧩 二维DP模式回顾 (5/11) — Pattern Context

**本块已学:** Unique Paths → LCS → Stock Cooldown → Coin Change II → **Target Sum (今天)**
**接下来:** Interleaving String → Edit Distance → Longest Increasing Path → Distinct Subsequences → Burst Balloons → Regex Matching

今天这题**表面是回溯，实质是背包**。关键在识别转化。

---

## 真实类比 / Real-World Analogy

想象你有一台**旧式弹球机**，有 N 个钉子，每个钉子让球向左（-1）或向右（+1）偏移。
球从顶部落下，你能控制每个钉子的方向，目标是让最终偏移量等于 target。问有多少种路线？

Imagine a pinball machine with N pegs. Each peg deflects the ball left (subtract) or right (add). How many paths lead to the target score?

---

## 问题描述

```
nums = [1, 1, 1, 1, 1], target = 3
Add '+' or '-' before each number.

+1+1+1+1-1 = 3  ✓
+1+1+1-1+1 = 3  ✓
+1+1-1+1+1 = 3  ✓
+1-1+1+1+1 = 3  ✓
-1+1+1+1+1 = 3  ✓

Answer: 5
```

---

## 暴力解 → 数学转化 → 2D DP

### 暴力: O(2^n) DFS — 太慢
```python
def findTargetSumWays_brute(nums, target):
    def dfs(i, curr_sum):
        if i == len(nums):
            return 1 if curr_sum == target else 0
        return dfs(i+1, curr_sum + nums[i]) + dfs(i+1, curr_sum - nums[i])
    return dfs(0, 0)
```

### 关键洞察 / Mathematical Transform

设所有加号的数字之和为 P，减号的数字之和为 Q。
- P + Q = total_sum
- P - Q = target
- 因此 **P = (total_sum + target) / 2**

问题转化为：**从 nums 中选出若干数字，使其和恰好等于 P = (total_sum + target) / 2**
这正是 Coin Change II 的变体！

```
total_sum = 5, target = 3
P = (5 + 3) / 2 = 4

How many subsets of [1,1,1,1,1] sum to 4?
[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1] → 5 ways ✓
```

---

## 2D DP 解法 — 映射到模版

```python
def findTargetSumWays(nums: list[int], target: int) -> int:
    total = sum(nums)
    
    # Edge cases: no valid partition exists
    if (total + target) % 2 != 0:
        return 0
    if abs(target) > total:
        return 0
    
    # subset_sum = (total + target) // 2
    # Count subsets of nums that sum to subset_sum
    subset_sum = (total + target) // 2
    n = len(nums)
    
    # dp[i][j] = number of ways to pick from nums[0..i-1] summing to j
    # Maps to 2D DP template: dp[n+1][subset_sum+1]
    dp = [[0] * (subset_sum + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # base: 0 items, sum 0 → 1 way (pick nothing)
    
    for i in range(1, n + 1):
        num = nums[i - 1]
        for j in range(subset_sum + 1):
            # Don't take nums[i-1]
            dp[i][j] = dp[i-1][j]
            # Take nums[i-1] (if feasible)
            if j >= num:
                dp[i][j] += dp[i-1][j - num]
    
    return dp[n][subset_sum]

# Trace: nums=[1,1,1,1,1], target=3, subset_sum=4
#
# dp table (rows=items 0-5, cols=sum 0-4):
#
#      0  1  2  3  4
#  0:  1  0  0  0  0   (no items)
#  1:  1  1  0  0  0   (consider num=1)
#  2:  1  2  1  0  0   (consider num=1)
#  3:  1  3  3  1  0   (consider num=1)
#  4:  1  4  6  4  1   (consider num=1)
#  5:  1  5 10 10  5   (consider num=1)
#
# dp[5][4] = 5 ✅
```

---

## 空间优化 — 1D 滚动数组

```python
def findTargetSumWays_optimized(nums: list[int], target: int) -> int:
    total = sum(nums)
    if (total + target) % 2 != 0 or abs(target) > total:
        return 0
    
    s = (total + target) // 2
    dp = [0] * (s + 1)
    dp[0] = 1
    
    for num in nums:
        # Traverse RIGHT to LEFT to avoid using same item twice
        for j in range(s, num - 1, -1):
            dp[j] += dp[j - num]
    
    return dp[s]
```

**复杂度 / Complexity:**
- Time: O(n × subset_sum) — much better than O(2^n)
- Space: O(subset_sum) with 1D optimization

---

## 举一反三 / Pattern Connections

| 问题 | 变体特征 | 关键区别 |
|------|----------|----------|
| Coin Change II (#518) | 无限取，求方案数 | 正序遍历 |
| **Target Sum (#494)** | 每数取一次，+/- | 数学转化为子集和 |
| Partition Equal Subset (#416) | 每数取一次，能否？ | dp[j] = bool |
| Ones and Zeroes (#474) | 二维容量背包 | dp[m][n] |

**模式识别信号:** "每个元素选或不选" + "计数" = 01背包求方案数

---

## 🧒 ELI5

把 nums 分成两堆，一堆加起来，一堆减掉。
目标是让差值等于 target。
数学变换发现：只需要数出"和等于某个特定值的子集数量"。
这和 Coin Change II 是同一类问题，只不过每个硬币只能用一次。

---

## 📚 References
- https://leetcode.com/problems/target-sum/ — Problem statement
- https://neetcode.io/problems/target-sum — NeetCode walkthrough
- https://en.wikipedia.org/wiki/Subset_sum_problem — Subset sum problem background
