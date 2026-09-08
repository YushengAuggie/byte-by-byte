# 💻 算法 / Algorithms — Day 129

## 🧩 一维动态规划模式 (3/12) — 延续 Day 126 的模板

🔗 [LeetCode #198 House Robber](https://leetcode.com/problems/house-robber/) 🟡 Medium  
📹 [NeetCode 讲解](https://neetcode.io/problems/house-robber)

---

## 🌍 现实类比 / Real-World Analogy

你是一个小偷，要在一条街上决定抢哪些房子。但相邻两家不能同时抢（会触发警报）。每家房子有不同的现金，你要最大化收益。

*You're a robber deciding which houses to rob on a street. Adjacent houses can't both be robbed (alarm goes off). Maximize total loot.*

---

## 📐 与模板的映射 / Mapping to Template

**模板回顾** (来自 Day 126):
```python
dp = [0] * (n + 1)
dp[0] = BASE_CASE
for i in range(1, n + 1):
    dp[i] = TRANSITION(dp[i-1], dp[i-2], ...)
```

**House Robber 的映射**:
- `dp[i]` = 抢前 i 间房子能拿到的最大金额
- `BASE_CASE`: `dp[0] = 0`, `dp[1] = nums[0]`
- `TRANSITION`: `dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])`
  - 不抢第 i 间: `dp[i-1]` (和前 i-1 间一样)
  - 抢第 i 间: `dp[i-2] + nums[i-1]` (必须跳过第 i-1 间)

**和 Day 128 (Min Cost Climbing Stairs) 的区别**:
- Day 128: 两种路径都合法，取最小代价
- 今天: 选择是"抢或不抢"，不是"跨1步或2步"，但转移方程结构**完全相同**！

---

## 💻 Python 解法 / Solution

```python
def rob(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]
    
    # dp[i] = max money from first i houses
    dp = [0] * (n + 1)
    dp[1] = nums[0]
    
    for i in range(2, n + 1):
        # Skip house i, or rob house i (skip house i-1)
        dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])
    
    return dp[n]

# Space-optimized O(1) version
def rob_optimized(nums: list[int]) -> int:
    prev2, prev1 = 0, 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr
    return prev1
```

**执行轨迹 / Trace** (nums = [2, 7, 9, 3, 1]):
```
i=1: dp[1] = 2           (只有房子0)
i=2: dp[2] = max(2, 0+7) = 7   (跳房子0，抢房子1)
i=3: dp[3] = max(7, 2+9) = 11  (跳房子1，抢房子0+2)
i=4: dp[4] = max(11, 7+3) = 11 (不需要房子3)
i=5: dp[5] = max(11, 11+1) = 12 ✅
```

**时间复杂度**: O(n) | **空间复杂度**: O(1) (优化后)

---

## 🔗 举一反三 / Pattern Connections

这个 block 的 12 道题，本质上都在问：**如何在有约束的序列上找最优值**

| 题目 | 约束 | 状态定义 |
|------|------|---------|
| #70 Climbing Stairs | 每次1或2步 | dp[i] = ways to reach step i |
| #746 Min Cost | 最小花费到顶 | dp[i] = min cost to reach i |
| **#198 House Robber** | **相邻不能选** | **dp[i] = max loot in first i** |
| #213 House Robber II | 首尾相连（明天！） | Run #198 twice, skip first/last |

**规律**: 转移方程都只看 `dp[i-1]` 和 `dp[i-2]`——这是**线性DP的核心特征**。

---

## 📚 References
- [LeetCode #198](https://leetcode.com/problems/house-robber/)
- [NeetCode 1-D DP Playlist](https://neetcode.io/roadmap)
- [DP Patterns — LeetCode Discuss](https://leetcode.com/discuss/general-discussion/458695/dynamic-programming-patterns)

---

## 🧒 ELI5
你有一排糖果盒，不能拿相邻两个，怎么拿最多？每次想：我拿这个盒子（加上前前个的最优）好，还是不拿（等于前一个的最优）好？两个里取最大。

*You have a row of candy boxes, can't take two adjacent ones. Each box: take it (add to what you got 2 boxes ago) or skip (keep what you had 1 box ago). Take the max.*

---

## 📝 Quiz
