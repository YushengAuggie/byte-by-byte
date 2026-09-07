# 💻 算法 / Algorithms — Day 128 · #746 Min Cost Climbing Stairs 🟢 Easy

🧩 **一维动态规划 (2/12)** — 基于前一天 Day 127 的模板继续

> 📌 前一天（Day 126）我们学了 #70 Climbing Stairs，建立了 1-D DP 模板。今天是同一模式的变体，看看**有了成本**后如何修改。

---

## 问题背景 / Problem Context

你在爬楼梯，每一级台阶有个"体力成本" cost[i]。从第 i 级迈步需要消耗 cost[i]，之后可以走 1 步或 2 步。你可以从第 0 级或第 1 级出发，到达**最顶端**（数组之外）。求最小总成本。

**Real-world analogy:** Like planning a road trip — some waypoints have gas/toll costs. You can skip waypoints (jump 2 steps), but you pay when you leave a waypoint. Minimize total trip cost.

🔗 [LeetCode #746](https://leetcode.com/problems/min-cost-climbing-stairs/) | 🟢 Easy | 📹 [NeetCode](https://www.youtube.com/watch?v=ktmzAZWkEZ0)

---

## 🧩 与模板对比 / Mapping to Pattern Template

```
昨天 #70 Climbing Stairs:
  dp[i] = 到达第 i 级的【方法数】
  dp[i] = dp[i-1] + dp[i-2]

今天 #746 Min Cost Climbing Stairs:
  dp[i] = 到达第 i 级的【最小成本】
  dp[i] = min(dp[i-1] + cost[i-1],
              dp[i-2] + cost[i-2])
          ↑ 从上一级走来            ↑ 从两级外走来

变化: 求 min 而非 count，加了 cost[] 作为"权重"
```

---

## 💡 思路与解法 / Solution

### Step 1: 定义 dp[i]
`dp[i]` = **到达第 i 级台阶的最小成本**（注意：到达，还没出发，不含 cost[i]）

### Step 2: 状态转移
- 从第 i-1 级走来：需要先到达 i-1，再付 cost[i-1]，走一步
- 从第 i-2 级走来：需要先到达 i-2，再付 cost[i-2]，走两步

```python
dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])
```

### Step 3: Base cases
- `dp[0] = 0`（从第 0 级出发，还未付费）
- `dp[1] = 0`（也可以从第 1 级出发）

### Step 4: 目标
`dp[len(cost)]` — 到达顶端（数组外）

---

## 🐍 Python 解法 + Trace

```python
def minCostClimbingStairs(cost: list[int]) -> int:
    n = len(cost)
    dp = [0] * (n + 1)
    # dp[0] = dp[1] = 0 (can start from 0 or 1 for free)
    
    for i in range(2, n + 1):
        from_one_below = dp[i-1] + cost[i-1]  # 从i-1走来，付cost[i-1]
        from_two_below = dp[i-2] + cost[i-2]  # 从i-2走来，付cost[i-2]
        dp[i] = min(from_one_below, from_two_below)
    
    return dp[n]

# Trace: cost = [10, 15, 20]
# dp[0] = 0, dp[1] = 0
# i=2: min(dp[1]+cost[1], dp[0]+cost[0]) = min(0+15, 0+10) = 10
# i=3: min(dp[2]+cost[2], dp[1]+cost[1]) = min(10+20, 0+15) = 15
# return dp[3] = 15  ✓ (0→1步→3: 付15)
```

**⚡ 空间优化 O(1):**
```python
def minCostClimbingStairs(cost: list[int]) -> int:
    prev2, prev1 = 0, 0  # dp[0], dp[1]
    
    for i in range(2, len(cost) + 1):
        curr = min(prev1 + cost[i-1], prev2 + cost[i-2])
        prev2, prev1 = prev1, curr
    
    return prev1
```

**复杂度:** Time O(n), Space O(1)

---

## 🔄 举一反三 / Connect to the Block

| 题目 | dp[i] 含义 | 转移方程 |
|------|-----------|---------|
| #70 Climbing Stairs | 到达i的**方法数** | dp[i-1] + dp[i-2] |
| **#746 Min Cost** | 到达i的**最小成本** | min(prev1+cost, prev2+cost) |
| #198 House Robber (下一题) | 偷前i家的**最大金额** | max(dp[i-1], dp[i-2]+nums[i]) |

> 规律：DP 类型变了（count → min → max），**模板框架不变**，只改 transition 函数和 base case。

---

## 📚 References
- https://leetcode.com/problems/min-cost-climbing-stairs/
- https://neetcode.io/problems/min-cost-climbing-stairs
- https://en.wikipedia.org/wiki/Dynamic_programming

## 🧒 ELI5
楼梯每一格都要付"过路费"。你从第0格或第1格出发（免费）。每次可以走1步或2步。到了一格才付钱，然后决定跳1步还是2步。问最少花多少钱爬到顶？就像选路线绕收费站，每次都选便宜的那条。
