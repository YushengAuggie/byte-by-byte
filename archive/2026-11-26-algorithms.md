# 💻 算法 / Algorithms — Day 158
> #53 Maximum Subarray · Medium 🟡 · Greedy Pattern Block (1/8)

---

## 🧩 新模式 / New Pattern: 贪心 (Greedy)
📍 This block: 8 problems
- #53 Maximum Subarray ← TODAY
- #55 Jump Game
- #45 Jump Game II
- #134 Gas Station
- #846 Hand of Straights
- #1899 Merge Triplets to Form Target Triplet
- #763 Partition Labels
- #678 Valid Parenthesis String

**什么时候用 / When to use:** 局部最优选择能推导出全局最优解 — Local optimal choices lead to globally optimal solution

**识别信号 / Signals:**
- "maximum / minimum" with a natural greedy choice
- Interval scheduling (按某标准排序后贪心选取)
- Jump game patterns (from each position, make best local move)
- Gas station / circular problems

**通用模版 / Template:**
```python
# 1. 排序 (if needed) / Sort by some criteria
items.sort(key=lambda x: x.end)  # or ratio, weight, etc.

# 2. 贪心选取 / Greedily pick
result = 0
for item in items:
    if CAN_PICK(item):  # local decision
        result += item.value  # commit to it

# Pattern: at each step, ask "what's the best local choice?"
# Then PROVE why local best = global best (exchange argument)
```

**核心洞察 / Key Insight:**
贪心的难点不是写代码，是**证明贪心策略的正确性** — 通常用"交换论证"(exchange argument)：假设最优解不用我的贪心选择，把它换成贪心选择，证明结果不会变差。

The hard part isn't coding, it's *proving* your greedy strategy is correct. The standard technique: "exchange argument" — assume the optimal solution doesn't use the greedy choice; swap it in and show the result doesn't get worse.

---

## 今日题目 / Today's Problem

🔗 [LeetCode #53 — Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) 🟡 Medium  
📹 [NeetCode Video](https://neetcode.io/problems/maximum-subarray)

---

## 现实类比 / Real-World Analogy

想象你是股票交易员，每天的盈亏记录在数组里：`[-3, 1, 5, -2, 8, -6, 2]`。你想找一段**连续的交易日**，让这段时间的总盈亏最大。你不需要知道"最优起止日"是哪天 — 只需要在每天决定：我要继续持仓，还是放弃之前的亏损、今天重新开始？

Imagine you're a trader tracking daily P&L. At each day, you make one greedy decision: "carry forward my running profit, or cut losses and restart from today?"

---

## 题目理解 / Problem

```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Explain: [4, -1, 2, 1] has the largest sum = 6
```

---

## 映射到模板 / Mapping to Template

**贪心选择 / Greedy choice:** 在每个位置 i，我们决定：
1. **延续** 之前的 subarray (加上 `nums[i]`)
2. **重新开始** 从 `nums[i]` 单独起步

如何决定？如果当前 `current_sum < 0`，继续只会拖累 `nums[i]`，不如重置。

```python
def maxSubArray(nums):
    max_sum = nums[0]       # global best seen
    current_sum = nums[0]   # running greedy candidate
    
    for n in nums[1:]:
        # Greedy decision: restart if current sum is negative
        if current_sum < 0:
            current_sum = n      # cut the dead weight
        else:
            current_sum += n     # extend the subarray
        
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**执行追踪 / Trace:** `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`
```
i=0: cur=-2, max=-2
i=1: cur<0 → reset, cur=1, max=1
i=2: cur=1-3=-2, max=1
i=3: cur<0 → reset, cur=4, max=4
i=4: cur=4-1=3, max=4
i=5: cur=3+2=5, max=5
i=6: cur=5+1=6, max=6  ← answer
i=7: cur=6-5=1, max=6
i=8: cur=1+4=5, max=6
```

**复杂度 / Complexity:** Time O(n) · Space O(1) — 一次遍历，不需要额外空间

---

## 为什么贪心正确？/ Why is greedy correct?

**交换论证 / Exchange argument:**
若最优子数组的某个前缀和 < 0，去掉这个前缀，剩余子数组的和**更大或相等**。因此最优子数组的任何前缀和都 ≥ 0。这正是我们贪心重置的条件。

If any prefix of the optimal subarray has sum < 0, dropping it only improves or maintains the total. So the optimal subarray never starts with a negative-sum prefix — exactly what our reset condition enforces.

---

## 变体 / Variants (同一模式)

```python
# 进阶: 返回子数组的起止下标 / Return indices too
def maxSubArrayWithIndices(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    start = end = 0
    temp_start = 0
    
    for i in range(1, len(nums)):
        if current_sum < 0:
            current_sum = nums[i]
            temp_start = i         # potential new start
        else:
            current_sum += nums[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end
```

---

## 举一反三 / Pattern Connections

| 题目 Problem | 贪心核心 Greedy Core |
|---|---|
| **#55 Jump Game** (下一题) | 维护 max_reach，能到 i 就更新 |
| **#45 Jump Game II** | 在当前跳跃范围内选最远的落点 |
| **#134 Gas Station** | total_gain≥0 → 一定有解；从最低点后出发 |
| **#763 Partition Labels** | 每个字符最后出现位置决定分区边界 |

---

## 🧒 ELI5

你在玩一个游戏，每天可以收钱或欠钱。你想找一段最赚钱的连续日期。贪心策略：如果你现在已经亏钱了，就重新开始计算 — 亏损的历史只会拖累未来。

You're tracking money each day. Greedy strategy: if you're currently in the red, start fresh — a negative running total can only make future days worse.

## 📚 References
- [LeetCode #53](https://leetcode.com/problems/maximum-subarray/)
- [NeetCode — Maximum Subarray](https://neetcode.io/problems/maximum-subarray)
- [Kadane's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maximum_subarray_problem)
- [Greedy Algorithms — MIT OpenCourseWare](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)
