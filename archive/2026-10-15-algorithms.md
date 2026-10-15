# 💻 算法 / Algorithms — Day 139
## #300 Longest Increasing Subsequence (Medium) 🟡
## 🧩 一维动态规划 (11/12) — building on the template from earlier in this block

> 🧩 **1-D DP (11/12)** — 这是本模式倒数第二题。LIS 是 DP 的经典，也是面试高频题。
> Second-to-last in the 1-D DP block. LIS is a DP classic and a high-frequency interview problem.

🔗 [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/) 🟡 Medium
📹 [NeetCode Video](https://neetcode.io/problems/longest-increasing-subsequence)

---

### 🌍 真实场景 / Real-world Analogy

想象你在做一个股票分析工具，需要找出「价格序列中最长的持续上涨片段」（不要求连续）。
You're building a stock analyzer to find the longest sequence of strictly increasing prices (non-contiguous).

`[10, 9, 2, 5, 3, 7, 101, 18]` → 最长上升子序列长度 = 4 (`[2, 3, 7, 101]`)

---

### 📐 映射到模版 / Template Mapping

本题的关键：`dp[i]` = **以 nums[i] 结尾的最长上升子序列长度**

```
dp = [0] * (n + 1)          # 标准模版
dp[0] = BASE_CASE           # → dp[i] = 1 (每个元素自身是长度1的子序列)
for i in range(1, n + 1):
    dp[i] = TRANSITION(...)  # → max(dp[j] + 1) for all j < i where nums[j] < nums[i]
```

与前面题目对比：
- Coin Change (Day 136): `dp[i] = min(dp[i - coin] + 1)` — 外循环是金额，内循环是硬币
- Word Break (Day 138): `dp[i] = any(dp[i-len(w)] and s[i-len(w):i] == w)` — 外循环是位置，内循环是单词
- **LIS (今天)**: `dp[i] = max(dp[j] + 1 for j < i if nums[j] < nums[i])` — 双重循环，两两比较

---

### 🐍 Python 解法 + Trace

```python
from typing import List

def lengthOfLIS(nums: List[int]) -> int:
    n = len(nums)
    # dp[i] = length of LIS ending at index i
    dp = [1] * n  # base case: every element alone is length 1
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                # can extend the subsequence ending at j
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Trace: nums = [10, 9, 2, 5, 3, 7, 101, 18]
# i=0: dp = [1, 1, 1, 1, 1, 1, 1, 1]
# i=3 (nums[3]=5): j=2 (nums[2]=2 < 5) → dp[3] = dp[2]+1 = 2
# i=5 (nums[5]=7): j=3 (5<7) dp[3]=2 → dp[5]=3; j=2 (2<7) dp[2]=1 → dp[5]=max(3,2)=3
# i=6 (nums[6]=101): max over all j → dp[6] = 4
# Result: max([1,1,1,2,2,3,4,4]) = 4 ✓
```

**时间复杂度 / Complexity:** O(n²) time, O(n) space

---

### ⚡ 进阶：O(n log n) — 二分搜索优化

```python
import bisect

def lengthOfLIS_optimized(nums: List[int]) -> int:
    # tails[i] = smallest tail element for all increasing subsequences of length i+1
    tails = []
    
    for num in nums:
        pos = bisect.bisect_left(tails, num)  # find insertion position
        if pos == len(tails):
            tails.append(num)   # extend the longest subsequence
        else:
            tails[pos] = num    # replace to keep tails as small as possible
    
    return len(tails)

# Key insight: tails is always sorted, but does NOT store the actual subsequence!
# tails = [2, 3, 7, 18] at the end, length = 4
# The actual LIS could be [2, 3, 7, 18] or [2, 3, 7, 101]
```

**时间复杂度 / Complexity:** O(n log n) time, O(n) space

---

### 举一反三 / Pattern Connections

本 1-D DP 块（12题）的规律总结：

| 题目 | `dp[i]` 含义 | 转移方向 |
|------|------------|---------|
| Climbing Stairs | 到第i步的方法数 | dp[i-1] + dp[i-2] |
| Coin Change | 凑成 i 元的最少硬币 | min over coins |
| **LIS** | 以i结尾的最长上升子序列 | max over j < i |
| Partition Subset (明天) | 能否凑成 i | or over nums |

**共同点：** 定义好 `dp[i]` 的含义，找到「如何从更小的子问题转移过来」。

---

### 📚 References
- [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/)
- [NeetCode LIS Explanation](https://neetcode.io/problems/longest-increasing-subsequence)
- [Patience Sorting — O(n log n) Visual](https://en.wikipedia.org/wiki/Patience_sorting)

### 🧒 ELI5
你有一排数字，想找最长的一组数，每个都比前一个大（不用挨着）。DP 的做法：对每个数，问「前面有哪些更小的数，它后面接上我能更长？」
You have a row of numbers and want the longest group where each is bigger than the last (not necessarily adjacent). DP says: for each number, ask "which earlier smaller numbers, if I follow them, make the longest chain?"
