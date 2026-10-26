💻 **算法 / Algorithms**
*Day 142 · #416 Partition Equal Subset Sum (Medium) 🟡*

🧩 **一维动态规划 (12/12)** — 收官之战，建立在整个 1-D DP 模版之上

---

## 题目 / Problem

🔗 https://leetcode.com/problems/partition-equal-subset-sum/
📹 https://neetcode.io/problems/partition-equal-subset-sum

给定整数数组 `nums`，判断能否将其分成两个元素和**相等**的子集。

Given array `nums`, return `True` if you can partition it into two subsets with equal sum.

**Example:**
```
nums = [1, 5, 11, 5]  →  True  ([1, 5, 5] and [11])
nums = [1, 2, 3, 5]   →  False
```

---

## 现实类比 / Real-World Analogy

公平分家产：父亲去世，留下 N 件价值不同的藏品。你和弟弟能不能各拿一半（总价值相等）？这就是 Partition Equal Subset Sum。

Settling an estate: can two heirs split N items of varying value into equal halves?

---

## 与模版的映射 / Mapping to Template

这道题的核心洞察：把"能否凑出总和 `target = sum//2`"转化为 **0/1 背包**问题。

```python
# 标准 1-D DP 模版变种 (0/1 背包)
dp = [False] * (target + 1)
dp[0] = True         # base case: 凑出 0 总是可行

for num in nums:
    # 倒序遍历！防止同一个数用两次
    for j in range(target, num - 1, -1):
        dp[j] = dp[j] or dp[j - num]

return dp[target]
```

**为什么倒序？** 正向遍历 `dp[j]` 会用到本轮刚更新的 `dp[j-num]`，相当于同一个数用了两次。倒序保证每个 `num` 只用一次（0/1 背包 vs 完全背包的核心区别）。

---

## 完整解法 / Full Solution with Trace

```python
def canPartition(nums: list[int]) -> bool:
    total = sum(nums)
    # odd sum → impossible to split into two equal halves
    if total % 2 != 0:
        return False
    
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in nums:
        # iterate right-to-left to avoid reusing the same num
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    
    return dp[target]
```

**手动 trace：** `nums = [1, 5, 11, 5]`, `target = 11`

```
初始:  dp = [T, F, F, F, F, F, F, F, F, F, F, F]
num=1: dp = [T, T, F, F, F, F, F, F, F, F, F, F]
num=5: dp = [T, T, F, F, F, T, T, F, F, F, F, F]
num=11:dp = [T, T, F, F, F, T, T, F, F, F, F, T] ← dp[11]=True!
num=5: dp = [T, T, F, F, F, T, T, F, F, F, T, T]  (dp[11] already True)
return dp[11] → True
```

> 💡 可以加 `if dp[target]: return True` 提前退出（优化），但不影响正确性。

---

## 复杂度 / Complexity

- **Time:** O(n × target) = O(n × sum/2)
- **Space:** O(target) ← 1-D 滚动数组优化

---

## 举一反三 / Pattern Connections

这是整个 1-D DP 模块（12题）的**收官题**，来看模式进化：

| 题目 | DP 含义 | 关键变化 |
|------|---------|---------|
| #70 Climbing Stairs | dp[i] = ways | 简单加法转移 |
| #198 House Robber | dp[i] = max profit | 跳跃转移 |
| #322 Coin Change | dp[i] = min coins | 完全背包（正序） |
| #139 Word Break | dp[i] = reachable | 字符串 DP |
| **#416 Partition** | **dp[j] = achievable** | **0/1 背包（倒序）** |

💡 **最终洞察：** DP 模版不是背公式，而是**定义清楚 dp[i] 的含义**，转移自然就出来了。

---

## Quiz / 小测验

```json
{"question":"canPartition([1,5,11,5]) 中为什么内层循环要倒序遍历？","options":["A. 防止同一个数被选多次","B. 减少时间复杂度","C. 避免数组越界","D. 保证 dp[0]=True"],"correct_index":0}
```

---

## 📚 References

- https://neetcode.io/problems/partition-equal-subset-sum — NeetCode video solution
- https://leetcode.com/problems/partition-equal-subset-sum/editorial/ — Official editorial
- https://en.wikipedia.org/wiki/Knapsack_problem — 0/1 Knapsack background

## 🧒 ELI5

有一堆积木，每块有重量。能不能分成两堆，让两堆重量相同？你把目标重量当成背包容量，每块积木决定放不放进去。dp[j]=True 表示"用已经看过的积木，能凑出重量 j"。倒序是为了每块积木只用一次。
