# 算法 / Algorithms — Day 137
## #152 Maximum Product Subarray (Medium) — 1-D Dynamic Programming

🧩 **一维动态规划 (9/12)** — 在 Day 128 的模版基础上继续
Building on the 1-D DP template from this block

🔗 https://leetcode.com/problems/maximum-product-subarray/ 🟡
📹 https://www.youtube.com/watch?v=lXVy6YWFcRM (NeetCode)

---

### 这道题为什么特殊？/ Why This Problem is Tricky

乘法不像加法——负数 × 负数 = 正数！这意味着当前的"最小值"可能在遇到下一个负数后变成"最大值"。

Unlike sum problems, **multiplication flips signs**. The current minimum could become the maximum when multiplied by a negative number.

**真实类比：** 股票的收益率复合——连续两个亏损季度（-50%，-50%），如果能配对可能反而有特殊意义。

---

### 与模版的映射 / Mapping to the Pattern Template

标准 1-D DP 只跟踪一个值 `dp[i]`。但这道题需要**同时跟踪最大值和最小值**：

Standard 1-D DP tracks one state. This problem needs **two states** simultaneously:

```python
# Standard template:
# dp[i] = TRANSITION(dp[i-1])

# This problem's variant:
# dp_max[i] = max product ending at i
# dp_min[i] = min product ending at i  (crucial for negatives!)
```

---

### Python 解法 + 详细注释 / Solution with Trace

```python
def maxProduct(nums: list[int]) -> int:
    # Track both max and min products ending at current index
    # Space-optimized: O(1) instead of O(n) array
    cur_max = nums[0]
    cur_min = nums[0]
    result = nums[0]

    for n in nums[1:]:
        # When n is negative, max and min swap roles!
        # e.g., cur_max=6, cur_min=-2, n=-3:
        #   candidates: 6*-3=-18, -2*-3=6, -3
        #   new_max=6, new_min=-18
        candidates = (n * cur_max, n * cur_min, n)
        cur_max = max(candidates)
        cur_min = min(candidates)
        result = max(result, cur_max)

    return result
```

**Trace through `[-2, 3, -4]`:**
```
Start: cur_max=-2, cur_min=-2, result=-2

n=3:  candidates=(-6, -6, 3) → cur_max=3, cur_min=-6
      result = max(-2, 3) = 3

n=-4: candidates=(3*-4=-12, -6*-4=24, -4)
      cur_max=24, cur_min=-12
      result = max(3, 24) = 24  ✓
```

**Complexity:** Time O(n), Space O(1) ✅

---

### 与同模式其他题的联系 / Connections in This Block

| 题目 | dp[i] 的含义 | 需要几个状态？ |
|------|------------|-------------|
| #70 Climbing Stairs | 到达 i 的方法数 | 1 (dp[i-1] + dp[i-2]) |
| #198 House Robber | 抢到 i 的最大值 | 1 |
| **#152 Max Product** | **以 i 结尾的最大乘积** | **2 (max + min)** |
| #300 LIS (next) | 以 i 结尾的最长递增子序列 | 1 |

**关键洞察：** 当问题有"翻转性质"（负数乘法、买卖股票中的持仓状态），标准单状态 DP 不够，需要额外状态。

---

### 📝 Quiz
```json
{"question":"nums=[-2,0,-1], maxProduct returns?","options":["0","2","-1","1"],"correct_index":0}
```
*(提示：0 把乘积归零，[0] 和 [-1] 都不如 0)*

---

### 📚 References
- https://leetcode.com/problems/maximum-product-subarray/
- https://neetcode.io/problems/maximum-product-subarray
- https://en.wikipedia.org/wiki/Maximum_subarray_problem

### 🧒 ELI5
你要找连续乘起来最大的一段数字。难点是负数乘负数会变正，所以你得同时记住"目前最大"和"目前最小"，随时准备翻转。
Find the contiguous subarray with the largest product. The twist: negatives flip signs, so track both the running max AND min — the min could become the new max when you hit another negative.
