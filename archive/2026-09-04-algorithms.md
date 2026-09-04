# 算法 / Algorithms — Day 126 — #70 Climbing Stairs

💻 **算法 / Algorithms** — #70 Climbing Stairs (Easy) — 1-D Dynamic Programming

---

🧩 **新模式 / New Pattern: 一维动态规划模式 (1-D DP)**
📍 This block: 12 problems (#70, #746, #198, #213, #5, #647, #91, #322, #152, #139, #300, #416)

**什么时候用 / When to use:**
最优子结构 + 重叠子问题、计数路径数、求最大/最小值、判断能否到达

**识别信号 / Signals:**
`minimum cost`, `maximum profit`, `number of ways`, `can you reach`, `optimal`, `longest`, `fewest`

**通用模版 / Template:**
```python
dp = [0] * (n + 1)
dp[0] = BASE_CASE          # define carefully
for i in range(1, n + 1):
    dp[i] = TRANSITION(dp[i-1], dp[i-2], ...)  # the key step
return dp[n]
# Space optimization: often can reduce to O(1) with two variables
```

**核心洞察 / Key Insight:**
定义 `dp[i]` 的含义 → 找状态转移方程 → 确定 base case。先写递归（top-down）再优化成迭代（bottom-up）。

---

### 今日问题 / Today's Problem

🔗 [LeetCode #70](https://leetcode.com/problems/climbing-stairs/) 🟢 Easy · 📹 [NeetCode](https://neetcode.io/problems/climbing-stairs)

**现实类比：** 你爬楼梯去面试，每次可以迈 1 级或 2 级台阶，共 n 级。有多少种走法？（焦虑程度不计 😅）

*Real-world analogy: Climbing stairs to your interview. You can take 1 or 2 steps at a time. n stairs total. How many distinct ways?*

---

### 套用模版 / Mapping to Template

**定义 `dp[i]`：** 爬到第 i 级台阶的不同方法数
*Define `dp[i]` = number of distinct ways to reach stair i*

**状态转移 / Transition:**
到达第 i 级，只能从 i-1（迈1步）或 i-2（迈2步）过来：
```
dp[i] = dp[i-1] + dp[i-2]
```
这正是 Fibonacci！DP 和 Fibonacci 本质相同。

**Base cases:**
```
dp[1] = 1  (only one way: take 1 step)
dp[2] = 2  (two ways: 1+1 or 2)
```

---

### Python 解法 + 追踪 / Solution with Trace

```python
def climbStairs(n: int) -> int:
    if n <= 2:
        return n
    
    # Bottom-up DP, space-optimized to O(1)
    prev2, prev1 = 1, 2  # dp[1], dp[2]
    
    for i in range(3, n + 1):
        curr = prev1 + prev2  # dp[i] = dp[i-1] + dp[i-2]
        prev2, prev1 = prev1, curr
    
    return prev1

# Trace for n=5:
# i=3: curr=1+2=3,  prev2=2, prev1=3
# i=4: curr=2+3=5,  prev2=3, prev1=5
# i=5: curr=3+5=8,  prev2=5, prev1=8
# return 8
```

**复杂度 / Complexity:**
- Time: O(n) — one pass
- Space: O(1) — only two variables (optimized from O(n) array)

---

### 直观验证 / Quick Verification

```
n=1 → 1 way:  [1]
n=2 → 2 ways: [1,1], [2]
n=3 → 3 ways: [1,1,1], [1,2], [2,1]
n=4 → 5 ways: [1,1,1,1], [1,1,2], [1,2,1], [2,1,1], [2,2]
```
1, 2, 3, 5, 8... 这就是 Fibonacci 数列！ *That's just Fibonacci!*

---

### 举一反三 / Pattern Connections

这个 12 题的 1-D DP 模块中，每题都是在问"如何优化到达第 i 个状态？"：
- **#746 Min Cost Climbing Stairs** — 同结构，加了 cost，取 min 而非 sum
- **#198 House Robber** — 不能选相邻元素，转移方程变成 `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`
- **#322 Coin Change** — 从每个 coin 转移，取 min，完全背包变形

*Each problem in this block = "find the optimal way to reach state i using previous states." Same skeleton, different transition logic.*

---

📚 **References:**
- https://leetcode.com/problems/climbing-stairs/ — Problem statement
- https://neetcode.io/problems/climbing-stairs — NeetCode video walkthrough
- https://cp-algorithms.com/dynamic_programming/intro-to-dp.html — DP fundamentals

🧒 **ELI5:** 你只能走1步或2步。到第5级，就等于从第4级走1步 + 从第3级走2步，所以方法数 = ways(4) + ways(3)。一层一层推上去，不用重复计算。
