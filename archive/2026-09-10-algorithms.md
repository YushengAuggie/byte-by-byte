# 💻 算法 / Algorithms — Day 131
**#213 House Robber II (Medium) — 1-D Dynamic Programming (4/12)**

🧩 **一维动态规划 (3/12 → 4/12)** — building on the template from Day 126-128

今天是 House Robber II，是 House Robber (#198) 的变种。关键变化：**房子围成一圈**。

---

## 🔗 Links
- LeetCode: https://leetcode.com/problems/house-robber-ii/ 🟡 Medium
- NeetCode: https://neetcode.io/problems/house-robber-ii

---

## 问题描述 / Problem

你是个小偷，要抢一排**围成圆圈**的房子。相邻房子不能同时抢，且第一和最后一个房子也算相邻（因为是圆圈）。求最大抢劫金额。

```
Input: nums = [2, 3, 2]
Output: 3  (不能同时抢 nums[0]=2 和 nums[2]=2，因为它们相邻)

Input: nums = [1, 2, 3, 1]
Output: 4  (抢 nums[0]=1 和 nums[2]=3)
```

---

## 🧩 如何套用模版 / Mapping to Template

**变化点：** 圆圈 → 第一和最后不能同时选 → 怎么处理？

**洞察：** 只需跑**两次线性 House Robber**：
1. 跑 `nums[0..n-2]`（包含第一个，不含最后一个）
2. 跑 `nums[1..n-1]`（不含第一个，包含最后一个）
3. 取两者最大值

这样永远保证首尾不会同时被选！

```
nums = [2, 3, 2]

Run 1: [2, 3]   → max = 3  (只抢第二个)
Run 2: [3, 2]   → max = 3  (只抢第二个)
Answer: max(3, 3) = 3 ✅
```

---

## Python 解法 / Solution

```python
from typing import List

def rob(nums: List[int]) -> int:
    if len(nums) == 1:
        return nums[0]
    
    def rob_linear(houses: List[int]) -> int:
        """Standard House Robber on a linear array."""
        prev2, prev1 = 0, 0
        for h in houses:
            # Choose: rob current (prev2 + h) or skip (prev1)
            prev2, prev1 = prev1, max(prev1, prev2 + h)
        return prev1
    
    # Case 1: include first house, exclude last
    # Case 2: exclude first house, include last
    return max(
        rob_linear(nums[:-1]),  # nums[0..n-2]
        rob_linear(nums[1:])    # nums[1..n-1]
    )

# Trace: nums = [1, 2, 3, 1]
# rob_linear([1, 2, 3]) → prev trace:
#   h=1: prev2=0, prev1 = max(0, 0+1) = 1
#   h=2: prev2=1, prev1 = max(1, 0+2) = 2
#   h=3: prev2=2, prev1 = max(2, 1+3) = 4
#   → returns 4
# rob_linear([2, 3, 1]) → prev trace:
#   h=2: prev2=0, prev1 = 2
#   h=3: prev2=2, prev1 = max(2, 0+3) = 3
#   h=1: prev2=3, prev1 = max(3, 2+1) = 3
#   → returns 3
# max(4, 3) = 4 ✅
```

**Time:** O(n) | **Space:** O(1)

---

## 与同块问题的对比 / Pattern Block Comparison

| 问题 | 关键变化 | 解法策略 |
|------|----------|----------|
| #70 Climbing Stairs | 基础 DP，两步或一步 | `dp[i] = dp[i-1] + dp[i-2]` |
| #746 Min Cost Climbing Stairs | 有代价的爬楼梯 | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` |
| #198 House Robber | 线性数组，不能取相邻 | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` |
| **#213 House Robber II** | **圆形数组** | **两次线性 House Robber，取最大** |

**规律：** 圆形约束 = 分两种情况跑线性 DP，化圆为线。

---

## 举一反三 / Connect the Dots

**下一题预告 (#5 Longest Palindromic Substring)：**
也是 1-D DP，但方向变了——不是从左到右，而是**以每个字符为中心向外扩展**。
注意感受同一个模版框架下，状态定义的灵活性。

---

## 📝 Quiz
