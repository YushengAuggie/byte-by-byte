# 💻 算法 / Algorithms — Day 137
## #152 Maximum Product Subarray (Medium) — 1-D Dynamic Programming

🧩 **一维动态规划模式 (9/12)** — 在 Day 129 House Robber 的模板基础上继续

---

### 🔗 链接 / Links
- 🔗 [LeetCode #152](https://leetcode.com/problems/maximum-product-subarray/) 🟡 Medium
- 📹 [NeetCode 讲解](https://www.youtube.com/watch?v=lXVy6YWFcRM)

---

### 🧩 模式回顾 / Pattern Recap (9/12)

本块之前的题目：
- Day 127 #70 Climbing Stairs → `dp[i] = dp[i-1] + dp[i-2]`
- Day 128 #746 Min Cost Climbing Stairs → 最小代价版
- Day 129 #198 House Robber → `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`
- Day 131 #213 House Robber II → 分两段处理环形数组
- Day 132 #5 Longest Palindromic Substring → 二维 DP
- Day 133 #647 Palindromic Substrings → 中心扩展
- Day 134 #91 Decode Ways → `dp[i] = dp[i-1] + dp[i-2]（条件版）`
- Day 136 #322 Coin Change → 完全背包
- **今天 Today: #152 Maximum Product Subarray** ← 这一题有个「陷阱」

**这道题的变体 / Today's twist：** 乘法有负负得正，需要同时追踪最大值和最小值！

---

### 🌍 真实类比 / Real-World Analogy

想象你在分析一只股票的**每日涨跌倍数**（1.2 = 涨 20%，0.5 = 跌 50%，-1 = 做空反转）。你想找连续几天操作下来**收益最大的那一段**。

负数很危险——一个负数会把最大收益变成最大亏损，但两个负数相乘又变成收益。

*Like tracking a stock's daily multipliers — one bad day can flip gains to losses, but two bad days can cancel out.*

---

### 💡 问题分析 / Problem Analysis

```
Input:  nums = [2, 3, -2, 4]
Output: 6  (subarray [2, 3])

Input:  nums = [-2, 0, -1]
Output: 0  (subarray [0])

Input:  nums = [-2, 3, -4]
Output: 24  (subarray [-2, 3, -4], 因为负 × 正 × 负 = 正)
```

**关键洞察 / Key Insight：**
普通 1-D DP 只追踪 `max_so_far`。但乘法中：
- 负数 × 负数 = 正数（最小值可能变成最大值！）
- 所以要**同时追踪 max 和 min**

---

### 🗺️ 映射到模板 / Map to Template

```python
# 标准 1-D DP 模板：
# dp[i] = 以 nums[i] 结尾的最优子数组的结果

# 这题：同时维护两个 dp！
# max_prod[i] = 以 nums[i] 结尾的子数组最大乘积
# min_prod[i] = 以 nums[i] 结尾的子数组最小乘积（负数的"储备"）
```

---

### 🐍 Python 解法 / Solution

```python
def maxProduct(nums: list[int]) -> int:
    # Initialize: single element is both max and min
    cur_max = nums[0]
    cur_min = nums[0]
    result = nums[0]

    for n in nums[1:]:
        # When n is negative, max and min swap!
        # e.g. cur_max=-5, cur_min=10, n=-2
        #   new_max = max(-2, -5*-2=10, 10*-2=-20) = 10
        #   new_min = min(-2, -5*-2=10, 10*-2=-20) = -20
        candidates = (n, cur_max * n, cur_min * n)
        cur_max = max(candidates)
        cur_min = min(candidates)
        result = max(result, cur_max)

    return result

# Trace on [-2, 3, -4]:
# n=-2: max=-2, min=-2, result=-2
# n=3:  candidates=(3, -6, -6) → max=3, min=-6, result=3
# n=-4: candidates=(-4, -12, 24) → max=24, min=-12, result=24 ✓
```

**时间复杂度 / Complexity：** O(n) time, O(1) space

---

### 🔄 举一反三 / Block Connections

| 题目 | 相似点 | 不同点 |
|------|--------|--------|
| #198 House Robber | 也是追踪"以第i个元素结尾"的最优 | 加法，只需 max |
| #322 Coin Change | 1-D DP 结构 | 无界背包，min 操作 |
| #300 LIS（下一题） | 以每个元素结尾的最优 | 需要嵌套循环或二分 |
| **#152 今天** | 同上 | 乘法需同时维护 max + min |

> **规律 / Pattern：** 当操作不是单调的（乘法、异或等），考虑同时维护多个 DP 状态。

---

### 📚 参考资料 / References

- [LeetCode #152 官方题解](https://leetcode.com/problems/maximum-product-subarray/editorial/)
- [NeetCode 1-D DP 系列](https://neetcode.io/roadmap)
- [Kadane's Algorithm 变体 — GeeksForGeeks](https://www.geeksforgeeks.org/maximum-product-subarray/)

### 🧒 ELI5

有一堆数字，你可以选相邻的一段，把它们都乘起来，找出最大的结果。难点是负数——两个负数相乘是正数！所以我们要同时记住"目前最大的"和"目前最小的"，因为最小的乘以一个负数，反而会变成最大的。
