# 💻 算法 / Algorithms — Day 27: #84 Largest Rectangle in Histogram 🔴 Hard

> **阶段 / Phase:** Mastery | **模式 / Pattern:** 单调栈 (Stack) — 7/7 | **阅读时间 / Read time:** ~4 min

---

🧩 **单调栈模式 (7/7)** — 收尾之作 / Final Problem in Block

本题是单调栈模块的**最后一题也是最难一题**。掌握它，说明你真正理解了单调栈的本质。

This is the **hardest and final problem** in the monotonic stack block. If you understand this one, you've truly internalized the pattern.

---

## 🔗 Links

- [LeetCode #84](https://leetcode.com/problems/largest-rectangle-in-histogram/) 🔴 Hard
- [NeetCode Video](https://neetcode.io/problems/largest-rectangle-in-histogram)

---

## 现实类比 / Real-World Analogy

想象你在城市中查看一排楼，要找出能在这排楼里画出的最大矩形广告牌（宽度不限，但高度不能超过范围内最矮的楼）。你需要找到哪一段楼的组合能撑起最大的广告牌面积。

Imagine you're looking at a city skyline and want to find the largest billboard that fits within it — the billboard can span multiple buildings but its height is limited by the shortest building in that span.

---

## 问题描述 / Problem

给定一个直方图，每个 bar 有高度 `heights[i]`，找出可以组成的最大矩形面积。

```
Input:  heights = [2, 1, 5, 6, 2, 3]
Output: 10

Visualization:
  6
  5 6
  5 6
2   2 2 3
2 1 2 2 2 3
[2, 1, 5, 6, 2, 3]
         ↑↑
  area = 5×2 = 10
```

---

## 映射到单调栈模版 / Mapping to Template

**模版回顾 / Template Recall:**
```python
stack = []
for i, num in enumerate(arr):
    while stack and arr[stack[-1]] < num:
        idx = stack.pop()
        result[idx] = num  # next greater
    stack.append(i)
```

**本题的关键洞察 / Key Insight for this problem:**

> 对于每个 bar，它能参与的最大矩形宽度 = **向左延伸直到遇到比它矮的 bar** + **向右延伸直到遇到比它矮的 bar**。

For each bar, the maximum rectangle it participates in spans from its **left boundary** (first shorter bar to the left) to its **right boundary** (first shorter bar to the right).

**模版变体 / Template Variation:**
- 原始模版：找**下一个更大**元素（单调递减栈）
- 本题：找**下一个更小**元素（单调递增栈）
- 每当弹出元素时，弹出的元素 = 以该高度为准的矩形的高度，此时可以计算面积

---

## Python 解法 + 追踪 / Solution with Trace

```python
def largestRectangleArea(heights: list[int]) -> int:
    max_area = 0
    # stack stores (start_index, height)
    # start_index = leftmost index this height can extend to
    stack = []  # monotonic increasing stack
    
    for i, h in enumerate(heights):
        start = i
        # while top of stack has height >= current h, pop and calculate
        while stack and stack[-1][1] >= h:
            idx, height = stack.pop()
            # width = current position - start of popped bar
            max_area = max(max_area, height * (i - idx))
            # current bar can extend back to where popped bar started
            start = idx
        stack.append((start, h))
    
    # remaining bars in stack extend to end of array
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
    
    return max_area

# Trace: heights = [2, 1, 5, 6, 2, 3]
# i=0, h=2: stack=[(0,2)]
# i=1, h=1: pop (0,2) → area=2×1=2; start=0; stack=[(0,1)]
# i=2, h=5: stack=[(0,1),(2,5)]
# i=3, h=6: stack=[(0,1),(2,5),(3,6)]
# i=4, h=2: pop (3,6)→area=6×1=6; pop (2,5)→area=5×2=10 ✓; start=2
#           stack=[(0,1),(2,2)]
# i=5, h=3: stack=[(0,1),(2,2),(5,3)]
# End: (5,3)→3×1=3; (2,2)→2×4=8; (0,1)→1×6=6
# max_area = 10 ✅
```

**时间复杂度 / Complexity:** O(n) — each index pushed/popped at most once
**空间复杂度 / Space:** O(n) — stack

---

## 与同块问题的对比 / Comparison with Block Problems

| 题目 | 技巧 | 关键 |
|------|------|------|
| #20 Valid Parentheses | 匹配括号 | 字符入栈 |
| #155 Min Stack | 辅助栈维护最小值 | 双栈 |
| #150 RPN Evaluation | 操作数入栈，遇操作符弹栈 | 数字栈 |
| #739 Daily Temperatures | 单调递减栈，找下一个更大 | 索引入栈 |
| #853 Car Fleet | 排序+栈，模拟追及 | 逆序遍历 |
| **#84 Histogram** | **单调递增栈，弹出时计算面积** | **extend-left 技巧** |

**规律 / Pattern:** 随着题目推进，栈内存储的信息越来越复杂：字符 → 数字 → 索引 → (索引, 高度) 元组

---

## 举一反三 / Related Problems

- [85. Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) — 本题的升级版，矩阵中的最大矩形
- [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — 已做过，同样用单调栈/双指针

---

## 📚 References

1. [NeetCode — Largest Rectangle in Histogram](https://neetcode.io/problems/largest-rectangle-in-histogram)
2. [Monotonic Stack Explained — Visualized](https://algo.monster/liteproblems/84)
3. [LeetCode Discuss — Multiple Approaches](https://leetcode.com/problems/largest-rectangle-in-histogram/solutions/)

---

## 🧒 ELI5 / 小孩版解释

你有一排积木，高度各不同。要找最大矩形，就问每块积木：「你能向左右各延伸多远，且所有经过的地方都比你矮或一样高？」——答案就是以你的高度为准，能撑起的最大矩形。单调栈帮你快速找到「左边第一个比你矮的」和「右边第一个比你矮的」。

You have a row of towers of different heights. For each tower, ask: "How far left and right can I stretch while all towers in between are at least as tall as me?" That stretch × your height = your rectangle. The monotonic stack helps you instantly find where each tower's reach stops.
