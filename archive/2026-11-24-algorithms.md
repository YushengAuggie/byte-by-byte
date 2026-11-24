# 💻 算法 / Algorithms — Day 156
## #312 Burst Balloons — Hard — 2-D Dynamic Programming (10/11)

🧩 **二维DP模式 (10/11)** — 在 Day 100 的模版基础上演进

> 本题是 2-D DP 系列最难也最经典的"区间 DP"变体。与前九题不同，它不是填充矩形网格，而是在**区间**上定义子问题。

---

### 🔗 Links

- 🔗 LeetCode: https://leetcode.com/problems/burst-balloons/ 🔴 Hard
- 📹 NeetCode: https://www.youtube.com/watch?v=VFskby7lUbw

---

### 🌍 真实类比 / Real-World Analogy

想象你在拆除一排建筑物，每拆一栋获得奖励 = 左邻 × 自己 × 右邻的价值。**关键决策**：你选择**最后**拆哪一栋。

This is like demolishing buildings where reward = left × current × right. The key insight: think about which building you demolish **last** in a range, not first.

---

### 💡 为什么这题难 / Why This Is Hard

**直觉**（错误）：每次戳价值最高的气球 → 贪心，WA。

**正确思路**：逆向思维。与其想"先戳哪个"，想"**这个区间最后戳哪个**"。

当气球 `k` 是区间 `[i, j]` 中**最后一个**被戳的，它两侧的气球已经全消失了，所以收益是固定的：`nums[i-1] * nums[k] * nums[j+1]`。

```
区间 DP 状态定义：
dp[i][j] = 戳爆区间 (i, j) 内所有气球的最大硬币数
           注意：i 和 j 本身是边界，不会被戳

转移方程：
for k in range(i+1, j):        # k 是这个区间最后被戳的
    coins = nums[i]*nums[k]*nums[j]  # k左右都已清空，邻居是i和j
    dp[i][j] = max(dp[i][j], dp[i][k] + coins + dp[k][j])

初始化：
nums = [1] + nums + [1]        # 两端加哨兵
dp = [[0]*(n+2) for _ in range(n+2)]
```

---

### 🐍 Python Solution with Trace

```python
def maxCoins(nums: list[int]) -> int:
    # Add sentinel balloons at both ends
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    # Enumerate by interval length (bottom-up)
    # l = length of open interval (i, j), so at least 2 apart
    for length in range(2, n):        # interval gap
        for left in range(0, n - length):
            right = left + length
            # Try each k as the LAST balloon popped in (left, right)
            for k in range(left + 1, right):
                coins = nums[left] * nums[k] * nums[right]
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k] + coins + dp[k][right]
                )

    return dp[0][n - 1]  # full range with sentinels


# Trace: nums = [3, 1, 5, 8]
# After padding: [1, 3, 1, 5, 8, 1]
# dp[0][5] = answer = 167
```

**复杂度 Complexity:**
- Time: O(n³) — 三重循环
- Space: O(n²) — DP 表

---

### 🔁 与同系列对比 / Pattern Variations

| 题目 | 区别 Difference |
|---|---|
| Edit Distance (Day 151) | 标准二维网格 DP，转移来自上/左/斜 |
| Distinct Subsequences (Day 153) | 单向网格，只往右下走 |
| **Burst Balloons (今天)** | **区间 DP！子问题是子区间，不是子矩阵** |
| Regular Expression Matching (Day 157) | 二维 + 通配符，转移更复杂 |

**核心差异**：Burst Balloons 用"枚举最后一个元素"代替"枚举相邻子结构"，是区间 DP 的精髓。

---

### 📝 Quiz

```json
{"question":"Burst Balloons 中 dp[i][j] 的含义是？","options":["戳爆所有气球的最大收益","戳爆闭区间[i,j]内气球的最大收益","戳爆开区间(i,j)内气球的最大收益（i和j是哨兵/边界）","以i为第一个戳、j为最后一个戳的最大收益"],"correct_index":2}
```

---

### 🧒 ELI5

拆积木游戏：你有一排积木，每次拆一块得分 = 左邻 × 自己 × 右邻。  
技巧：不要想"先拆哪块"，要想"**这一段最后留哪块**"——因为只有最后那块的邻居是固定的！

---

### 📚 References
- https://leetcode.com/problems/burst-balloons/editorial/
- https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html
- https://www.youtube.com/watch?v=VFskby7lUbw
