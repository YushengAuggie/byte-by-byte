# 💻 算法 / Algorithms — #322 Coin Change (Medium) — 1-D Dynamic Programming

🧩 **一维DP (8/12)** — building on the template from Day 128 (Min Cost Climbing Stairs)

---

今天的 Coin Change 是 1-D DP 模式块的第 8 题，也是这个模式里最经典的**完全背包变形**。

与之前的 House Robber（每步只能走1或2格）不同，这题每个 coin 可以无限次使用，所以状态转移方向不同。

---

## 🔗 题目链接
- 🔗 [LeetCode #322 — Coin Change](https://leetcode.com/problems/coin-change/)
- 🟡 Medium
- 📹 [NeetCode讲解](https://neetcode.io/problems/coin-change)

---

## 🌍 现实类比

想象你在便利店，手头只有 1元、5元、10元硬币。凑够 12 元最少要几枚？
- 10 + 1 + 1 = 3枚 ✅
- 5 + 5 + 1 + 1 = 4枚 ❌（不是最少）

这就是 Coin Change——**用最少数量的面额凑出目标金额**。

---

## 🧩 模板映射 / Map to Pattern

**模板回顾：**
```python
dp = [0] * (n + 1)
dp[0] = BASE_CASE
for i in range(1, n + 1):
    dp[i] = TRANSITION(dp[i-1], dp[i-2], ...)
return dp[n]
```

**本题映射：**
- `dp[i]` = 凑成金额 i 所需最少硬币数
- `BASE_CASE`: `dp[0] = 0`（凑成0元需要0枚）
- `TRANSITION`: 对每个 coin，`dp[i] = min(dp[i], dp[i - coin] + 1)`
- 初始值：`float('inf')`（表示不可达）

**与 House Robber 的区别：**
- House Robber: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` — 每步选 1 个
- Coin Change: 内层遍历所有 coins — 每步可以用任意 coin（无限次）

---

## 🐍 Python 解法 + 逐步追踪

```python
def coinChange(coins: list[int], amount: int) -> int:
    # dp[i] = min coins needed to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # base case: 0 coins to make amount 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                # use this coin: dp[i-coin] + 1 more coin
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    # inf means amount is not reachable
    return dp[amount] if dp[amount] != float('inf') else -1
```

**逐步追踪 / Trace** — `coins = [1, 5, 10]`, `amount = 12`:

```
dp[0] = 0
dp[1] = min(inf, dp[0]+1) = 1      # 1
dp[2] = min(inf, dp[1]+1) = 2      # 1+1
dp[3] = 3                            # 1+1+1
dp[4] = 4                            # 1*4
dp[5] = min(dp[4]+1, dp[0]+1) = 1  # 5
dp[6] = min(dp[5]+1, dp[1]+1) = 2  # 5+1
...
dp[10] = min(dp[9]+1, dp[5]+1, dp[0]+1) = 1  # 10
dp[11] = 2  # 10+1
dp[12] = 3  # 10+1+1 ✅
```

**时间复杂度：** O(amount × len(coins))
**空间复杂度：** O(amount)

---

## 举一反三 / Same Pattern Connections

| 题目 | 关键区别 | 转移方程 |
|---|---|---|
| #70 Climbing Stairs | 只能+1/+2 | `dp[i] = dp[i-1] + dp[i-2]` |
| #198 House Robber | 不能相邻选 | `dp[i] = max(dp[i-1], dp[i-2]+v)` |
| **#322 Coin Change** ← | coins 无限次，求最小 | `dp[i] = min(dp[i-coin]+1)` |
| #139 Word Break (下题预告) | coins 换成单词 | 类似但 dp 存布尔值 |

> 规律：当元素"可重复使用"时，内层从小到大遍历（完全背包）；"只能用一次"时从大到小（0-1背包）。

---

## 📚 References
- https://leetcode.com/problems/coin-change/editorial/ — 官方题解
- https://neetcode.io/problems/coin-change — NeetCode 视频讲解
- https://en.wikipedia.org/wiki/Change-making_problem — 找零问题数学背景

## 🧒 ELI5
你有1分、5分、1毛的硬币，凑1毛2分最少要几枚？从0开始，每种面额都试一次，选最小的——就是这样。
