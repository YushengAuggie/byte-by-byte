# 💻 算法 / Algorithms — Day 147

🧩 **二维动态规划模式 (4/11)** — building on the template introduced earlier in this block

**#518 Coin Change II** 🟡 Medium
- 🔗 https://leetcode.com/problems/coin-change-ii/
- 📹 https://neetcode.io/problems/coin-change-ii

---

## 模式回顾 / Pattern Recap (4th problem in block)

之前的题：
- #62 Unique Paths → dp[i][j] = dp[i-1][j] + dp[i][j-1] （计数路径）
- #1143 LCS → dp[i][j] = match ? dp[i-1][j-1]+1 : max(dp[i-1][j], dp[i][j-1])
- #309 Stock Cooldown → 状态机 DP，`hold/sold/cooldown`

**今天的变化 / What's different today:**
Coin Change II 是**无界背包（Unbounded Knapsack）**——每枚硬币可以无限次使用。这不同于 LCS 的"用完就没"，也不同于 Unique Paths 的纯方向移动。关键区别：`dp[i][j-coins[i-1]]` 而非 `dp[i-1][j-coins[i-1]]`（允许重复用同一个物品）。

---

## 现实类比 / Real-World Analogy

想象你去超市，只有 1 元、5 元、10 元的硬币，想凑出刚好 15 元。有多少种凑法？

- [10, 5], [10, 1, 1, 1, 1, 1], [5, 5, 5], [5, 5, 1×5], ...

Coin Change II 就是枚举所有这些组合数。

---

## 问题 / Problem

给定硬币面额数组 `coins` 和目标金额 `amount`，返回凑出该金额的**组合数**（不计顺序）。

```python
# Example
coins = [1, 2, 5], amount = 5
# Output: 4
# [1,1,1,1,1], [1,1,1,2], [1,2,2], [5]
```

---

## 如何映射到模板 / Mapping to 2-D DP Template

```
dp[i][j] = 用前 i 种硬币凑出金额 j 的组合数

i → coins (行)
j → amount 0..amount (列)

状态转移：
  不用 coin[i]: dp[i][j] = dp[i-1][j]
  用 coin[i]:   dp[i][j] += dp[i][j - coin[i]]   ← 注意是 dp[i], 不是 dp[i-1]！
                                                    ← 因为硬币可重复使用

Base case: dp[i][0] = 1 (凑出 0 元只有一种方法：什么都不选)
```

---

## Python 解法 + 追踪 / Solution with Trace

```python
def change(amount: int, coins: list[int]) -> int:
    # 2-D DP: dp[i][j] = ways using first i coins to make amount j
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n + 1)]
    
    # Base case: 0 ways using 0 coins, except amount=0
    for i in range(n + 1):
        dp[i][0] = 1  # 1 way to make 0: choose nothing
    
    for i in range(1, n + 1):
        for j in range(1, amount + 1):
            dp[i][j] = dp[i-1][j]  # don't use coin[i-1]
            if j >= coins[i-1]:
                dp[i][j] += dp[i][j - coins[i-1]]  # use coin[i-1] (reusable!)
    
    return dp[n][amount]

# Trace: coins=[1,2,5], amount=5
# dp[0]: [1, 0, 0, 0, 0, 0]   (0 coins, only j=0 is valid)
# dp[1] (coin=1): [1, 1, 1, 1, 1, 1]  (all amounts via 1s)
# dp[2] (coin=2): [1, 1, 2, 2, 3, 3]
# dp[3] (coin=5): [1, 1, 2, 2, 3, 4]  ← dp[3][5] = dp[2][5] + dp[3][0] = 3+1 = 4 ✓
```

**空间优化（重要！）/ Space Optimization:**

```python
def change(amount: int, coins: list[int]) -> int:
    # Optimize to O(amount) space
    # Key: iterate coins outer, amount inner (ensures unbounded use)
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] += dp[j - coin]
    
    return dp[amount]

# Time: O(n * amount), Space: O(amount)
# IMPORTANT: outer=coins, inner=amount → each coin counted unlimited times
# If reversed: outer=amount, inner=coins → 0/1 knapsack (each coin once)
```

---

## 举一反三 / Connections in This Block

| 题目 | 与今天的联系 |
|------|-------------|
| #62 Unique Paths | 也是计数，但路径是单向的（只能右/下），无"重复使用" |
| #1143 LCS | 匹配问题，dp[i][j] 取决于 dp[i-1][j-1]（用了就消耗） |
| #309 Cooldown | 也是无限次操作，但用状态机建模而非背包 |
| #494 Target Sum (next) | 0/1 背包的变体——每个数只能用一次，加 or 减 |

---

## 复杂度 / Complexity
- **时间**: O(n × amount) — 填满二维表
- **空间**: O(amount) — 压缩为一维后

---

## 📚 References
- https://leetcode.com/problems/coin-change-ii/editorial/
- https://neetcode.io/problems/coin-change-ii
- https://cp-algorithms.com/dynamic_programming/knapsack.html

## 🧒 ELI5
你有 1 分、2 分、5 分的硬币，想用它们凑出 5 分，问有多少种方法。我们做一张表：行是"我可以用的硬币种类"，列是"目标金额"。从小到大填表——每格的答案 = "不用这个硬币的方法数" + "用了这个硬币后剩余金额的方法数"。因为硬币可以反复用，所以"用了这个硬币"是看同一行（不是上一行）。
