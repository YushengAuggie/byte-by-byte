# 💻 算法 / Algorithms — Day 22
**题目 / Problem:** #239 Sliding Window Maximum 滑动窗口最大值
**难度 / Difficulty:** 🔴 Hard | **阶段 / Phase:** Growth

🧩 **Sliding Window 模式 (6/6)** — 滑动窗口块的收官题！
Building on the template established in this block's Day 16 kickoff.

---

## 🧩 模式回顾 / Pattern Recap (Block 6/6 — Final Problem!)

这是滑动窗口块的最后一题，也是最难的一题。回顾整个块：

| # | 题目 | 关键变体 |
|---|------|---------|
| 1 | Best Time to Buy & Sell Stock | 最简单的滑动窗口思想 |
| 2 | Longest Substring Without Repeating Chars | HashSet 跟踪窗口内容 |
| 3 | Longest Repeating Character Replacement | 频率数组 + 贪心缩窗 |
| 4 | Permutation in String | 固定大小窗口 |
| 5 | Minimum Window Substring | 变长窗口 + 双频率计数 |
| 6 | **Sliding Window Maximum** ← 今天 | **Monotonic Deque** 维护最大值 |

今天的新武器：**单调队列 (Monotonic Deque)** — 窗口内的最大值追踪器

---

## 🔗 Links
- [LeetCode #239](https://leetcode.com/problems/sliding-window-maximum/) 🔴 Hard
- [NeetCode Video](https://www.youtube.com/watch?v=DfljaUwZsOk)

---

## 真实场景 / Real-World Analogy

你在监控一个股票价格流，需要知道过去 k 分钟内的最高价。价格滚动刷新，你不能存所有历史数据，要在 O(n) 时间给出每一刻的窗口最大值。

You're monitoring a stock price stream and need the highest price in the last k minutes. Prices roll in continuously — you need the window max at every step, in O(1) per step.

---

## 问题 / Problem

给定数组 `nums` 和窗口大小 `k`，返回每个窗口的最大值。

```
Input:  nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3, 3, 5, 5, 6, 7]

Window [1,3,-1] → max = 3
Window [3,-1,-3] → max = 3
Window [-1,-3,5] → max = 5
...
```

---

## 核心洞察 / Key Insight: Monotonic Deque

**普通方法：** 每个窗口扫一遍 → O(nk)，太慢

**单调队列：** 维护一个**递减**的双端队列，存的是**索引**：
- 新元素进来时，把队列里所有**比它小的**尾部元素弹出（它们永远不可能是最大值了）
- 队头过期时（超出窗口）弹出
- 队头永远是当前窗口最大值的索引

**比喻 / Analogy:** 像选举队伍里的候选人 — 如果新来一个更强的候选人，前面弱的都没资格了，直接淘汰！

---

## Python 解法 / Python Solution

```python
from collections import deque
from typing import List

def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    result = []
    dq = deque()  # stores INDICES, values are decreasing
    
    for right in range(len(nums)):
        # Step 1: Remove elements outside window from front
        while dq and dq[0] < right - k + 1:
            dq.popleft()
        
        # Step 2: Remove smaller elements from back
        # (they can never be maximum while nums[right] is in window)
        while dq and nums[dq[-1]] < nums[right]:
            dq.pop()
        
        dq.append(right)
        
        # Step 3: Window is full — record maximum (front of deque)
        if right >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Trace: nums = [1,3,-1,-3,5,3,6,7], k=3
# right=0: dq=[0]        → no output yet
# right=1: pop 0 (1<3), dq=[1]    → no output yet
# right=2: dq=[1,2]      → result=[3]  (nums[1]=3)
# right=3: dq=[1,2,3]    → result=[3,3] (nums[1]=3)
# right=4: pop 1(out of window), pop 2,3 (smaller), dq=[4] → result=[3,3,5]
# right=5: dq=[4,5]      → result=[3,3,5,5]
# right=6: pop 4,5, dq=[6] → result=[3,3,5,5,6]
# right=7: pop 6, dq=[7]  → result=[3,3,5,5,6,7] ✓
```

**复杂度 / Complexity:**
- Time: **O(n)** — every element enters/leaves deque at most once
- Space: **O(k)** — deque holds at most k indices

---

## 与模版的映射 / Mapping to Template

```
通用模版:          本题实现:
left = 0           隐式: left = right - k + 1
for right in ...:  for right in range(len(nums)):
  add(arr[right])    dq.append(right) + pop smaller
  while VIOLATED:    while dq[0] < right - k + 1
    remove left        dq.popleft()
  result = update    result.append(nums[dq[0]])
```

**本题的特殊之处：** 固定窗口大小 + 用单调队列代替简单的 add/remove，维护区间最大值。

---

## 举一反三 / Pattern Connections

整个 Sliding Window 块学到了什么？

1. **固定窗口** (Permutation in String) — `right - left == k - 1` 时收缩
2. **可变窗口** (Minimum Window Substring) — 满足条件时收缩
3. **单调结构** (今天) — 不只记录元素，还维护有序性

**延伸：** 单调队列思想在 DP 优化中也常见（如跳跃游戏变体、接雨水 II）

---

## 📚 References
- [LeetCode #239 — Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
- [NeetCode Solution Explanation](https://www.youtube.com/watch?v=DfljaUwZsOk)
- [Monotonic Queue — CP Algorithms](https://cp-algorithms.com/data_structures/stack_queue_modification.html)

---

## 🧒 ELI5

想象你在坐过山车，窗口就是你能看到的 k 个座位。你想知道这 k 个座位里最高的人是谁。

单调队列就像一个"最强人选队列" — 新来的人如果比队伍里的人高，就把矮的踢出去。队头永远是当前最高的人！

Imagine you're on a rollercoaster and can see k seats at a time. The monotonic deque is like a "strongest candidate" line — when someone taller arrives, shorter people behind get kicked out. The front of the line is always the tallest person in your current view!
