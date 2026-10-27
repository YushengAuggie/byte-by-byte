# 💻 算法 / Algorithms — Day 143 | #62 Unique Paths [Medium] — 2-D Dynamic Programming

---

## 🧩 新模式 / New Pattern: 二维动态规划模式 (2-D Dynamic Programming)
📍 This block: 11 problems

**什么时候用 / When to use:** 网格路径、字符串匹配、背包问题 — 当两个维度的子问题都影响当前结果时

**识别信号 / Signals:** grid paths, edit distance, longest common subsequence, knapsack, matrix, "how many ways", "min cost across grid"

**通用模版 / Template:**
```python
dp = [[0] * (m+1) for _ in range(n+1)]
for i in range(1, n+1):
    for j in range(1, m+1):
        dp[i][j] = TRANSITION(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
return dp[n][m]
```

**核心洞察 / Key Insight:** 二维表格填充 — 画出表格手动填几格就能发现转移规律。先推导几个小例子，转移方程自然浮现。

---

## 题目 / Problem

🔗 [LeetCode #62 - Unique Paths](https://leetcode.com/problems/unique-paths/) 🟡 Medium
📹 [NeetCode Solution](https://neetcode.io/problems/count-paths)

**真实类比 / Real-world analogy:**  
想象你在 Google Maps 里从左上角走到右下角，只能向右或向下走。有多少条不同路线？这不只是数学游戏 — 机器人路径规划、包裹配送路由优化都用到同样的思路。

Imagine you're in Google Maps, moving from top-left to bottom-right, only right or down. How many routes exist? This models robot path planning and delivery route optimization.

---

## 映射到模版 / Map to Template

```
dp[i][j] = "到达 (i,j) 的路径数"

转移：dp[i][j] = dp[i-1][j] + dp[i][j-1]
     (从上面来) + (从左边来)

Base case: dp[i][1] = 1, dp[1][j] = 1  (第一行/列只有一条路)
```

手动填 3×3 表格:
```
    c1  c2  c3
r1 [ 1,  1,  1]
r2 [ 1,  2,  3]
r3 [ 1,  3,  6]
```
规律立刻显现：每格 = 上面 + 左边。

---

## Python 解法 / Solution

```python
def uniquePaths(m: int, n: int) -> int:
    # dp[i][j] = number of paths to reach cell (i, j)
    dp = [[1] * n for _ in range(m)]
    
    # First row and first col are all 1s (only one way to reach them)
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]

# Trace: m=3, n=3
# Initial: [[1,1,1],[1,0,0],[1,0,0]]
# i=1,j=1: dp[1][1] = dp[0][1]+dp[1][0] = 1+1 = 2
# i=1,j=2: dp[1][2] = dp[0][2]+dp[1][1] = 1+2 = 3
# i=2,j=1: dp[2][1] = dp[1][1]+dp[2][0] = 2+1 = 3
# i=2,j=2: dp[2][2] = dp[1][2]+dp[2][1] = 3+3 = 6
# Output: 6 ✓
```

**空间优化 / Space Optimization (O(n)):**
```python
def uniquePaths(m: int, n: int) -> int:
    # Only need the previous row — rolling array trick
    row = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            row[j] += row[j-1]  # row[j] = old row[j] + row[j-1]
    return row[-1]
```

**复杂度 / Complexity:**
- Time: O(m × n)
- Space: O(m × n) → O(n) with rolling array

---

## 举一反三 / Connect the Pattern

本 block 11 题都是 2-D DP 的变体，转移方程会越来越复杂：
- **明天 #1143 LCS**: `dp[i][j] = dp[i-1][j-1]+1` if match, else `max(dp[i-1][j], dp[i][j-1])`
- **#72 Edit Distance**: 三向转移 `min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+replace)`
- **#312 Burst Balloons**: 区间 DP，枚举最后一个戳破的气球

每道题的突破口：**先手绘一个小 case 的 dp 表格**。

---

## 📚 References
- [LeetCode #62 Official](https://leetcode.com/problems/unique-paths/)
- [NeetCode: Unique Paths Video](https://neetcode.io/problems/count-paths)
- [CP-Algorithms: DP on Grids](https://cp-algorithms.com/dynamic_programming/dp-on-broken-profile.html)

## 🧒 ELI5
你在方格纸左上角，要走到右下角，只能往右或往下。每格的走法数 = 上面那格 + 左边那格的走法加起来。就像数叉路口有几条路汇进来。
