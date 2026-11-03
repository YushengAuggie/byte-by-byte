# 💻 算法 / Algorithms — Day 146
**#309 Best Time to Buy and Sell Stock with Cooldown (Medium) — 2-D Dynamic Programming**

---

🧩 **二维动态规划 (3/11)** — 在 Day 143 模版基础上继续
Building on the 2-D DP template from Day 143

今天这题**看起来像 1-D DP**（只有一个数组 prices），但它实际上是一个**状态机 DP** — 每个时间点有多个"状态维度"，本质是二维的。

---

## 🎯 问题 / Problem

🔗 [LeetCode #309](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) 🟡 Medium
📹 [NeetCode](https://neetcode.io/problems/buy-and-sell-stock-with-cooldown)

**给你一个价格数组，每次卖出后必须冷静一天（不能买入）。求最大利润。**
Given prices array; after selling, you must wait 1 day before buying again. Maximize profit.

```
Input: prices = [1, 2, 3, 0, 2]
Output: 3
Explanation: Buy on day 0 (price=1), sell on day 1 (price=2),
             cooldown on day 2, buy on day 3 (price=0), sell on day 4 (price=2)
```

---

## 🔗 映射到模版 / Mapping to Pattern

二维DP的本质：`dp[i][state]`，其中：
- `i` = 第 i 天
- `state` = 当前状态 (3种)

```
状态机 / State Machine:

  HOLDING ──sell──→ SOLD
     ↑                │
   buy               cooldown
     │                ↓
  IDLE  ←──────── COOLDOWN
```

**三个状态 / Three States:**
- `HOLDING`: 持有股票中
- `SOLD`: 刚卖出（下一天必须进入 COOLDOWN）
- `IDLE`: 空仓且不在冷静期（可以买入）

---

## 🐍 Python Solution with Trace

```python
from typing import List

def maxProfit(prices: List[int]) -> int:
    # State machine DP
    # holding = max profit while holding stock
    # sold    = max profit on day we just sold
    # idle    = max profit while not holding, not in cooldown
    
    holding = -prices[0]  # bought on day 0
    sold = 0              # can't have sold on day 0
    idle = 0              # started idle
    
    for price in prices[1:]:
        prev_holding = holding
        prev_sold = sold
        prev_idle = idle
        
        # Today I'm holding: either I was already holding,
        # or I was idle yesterday and bought today
        holding = max(prev_holding, prev_idle - price)
        
        # Today I just sold: I was holding and sold today
        sold = prev_holding + price
        
        # Today I'm idle: I was idle, or I was in cooldown (just sold yesterday)
        idle = max(prev_idle, prev_sold)
    
    # Can't end while holding → max of sold or idle
    return max(sold, idle)
```

**手动追踪 / Manual Trace** `prices = [1, 2, 3, 0, 2]`:

```
Day 0 (price=1): holding=-1, sold=0,  idle=0
Day 1 (price=2): holding=max(-1, 0-2)=-1
                 sold   =max(-1+2)=1
                 idle   =max(0, 0)=0
Day 2 (price=3): holding=max(-1, 0-3)=-1
                 sold   =max(-1+3)=2
                 idle   =max(0, 1)=1
Day 3 (price=0): holding=max(-1, 1-0)=1  ← 冷静完买入!
                 sold   =max(-1+0)=-1
                 idle   =max(1, 2)=2
Day 4 (price=2): holding=max(1, 2-2)=1
                 sold   =max(1+2)=3       ← 最终卖出
                 idle   =max(2, -1)=2

Result: max(sold=3, idle=2) = 3 ✅
```

**复杂度 / Complexity:**
- Time: O(n)
- Space: O(1) — 只用三个变量！

---

## 🧩 与模版的区别 / Difference from Template

经典二维 DP 模版（LCS、网格路径）用 `dp[i][j]` 二维数组。

这道题的"第二维"是**状态**而不是第二个序列 — 状态空间被压缩成了 3 个变量。这是 2-D DP 的一个重要变体：**状态机 DP**。

```
经典 2D DP:     dp[i][j] = f(dp[i-1][j], dp[i][j-1], ...)
状态机 DP:      dp[i][state] = f(dp[i-1][other_states])
这道题:         holding/sold/idle = f(prev_holding/sold/idle, price)
```

---

## 举一反三 / Pattern Block Connection

| 题目 | 模版变体 |
|------|---------|
| #62 Unique Paths | 纯网格，`dp[i][j] = dp[i-1][j] + dp[i][j-1]` |
| #1143 LCS | 字符串匹配，第二维是字符位置 |
| **#309 今天** | 状态机，第二维是持仓状态 |
| #518 Coin Change II | 背包，第二维是剩余金额 |
| #72 Edit Distance | 字符串编辑，转移更复杂 |

---

## 📚 References

1. [LeetCode #309 Official Solution](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/editorial/)
2. [NeetCode Video Explanation](https://youtu.be/I7j0F7AHpb8)
3. [State Machine DP Explained — CS Dojo](https://www.youtube.com/c/CSDojo)

---

## 🧒 ELI5

想象你炒股有个规定：卖完股票必须冷静一天才能再买。
就像你卖了一个玩具后，妈妈规定你第二天才能买新的。

你需要时刻记住自己现在是"有玩具"、"刚卖掉玩具"还是"没玩具但可以买了"三种状态之一，然后每天做最优决策。
