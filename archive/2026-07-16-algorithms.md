# 算法 — #90 Subsets II (Medium) — Backtracking

> Day 92 · Expert · LeetCode #90

---

## 💻 算法 / Algorithms — #90 Subsets II (Medium) — 回溯

🧩 **回溯模式 (4/9)** — building on the template from Day 88 (Subsets #78)

今天的变化：数组有**重复元素**，子集不能重复。
Key difference from #78: the input array has **duplicates** — we must avoid duplicate subsets.

---

### 🔗 Links
- 📖 LeetCode: https://leetcode.com/problems/subsets-ii/ 🟡 Medium
- 📹 NeetCode: https://neetcode.io/problems/subsets-ii

---

### 类比 / Real-World Analogy

你从一堆水果中挑选礼品篮，篮子里有 2 个苹果、1 个梨。你不想列出两次"苹果+梨"（因为两个苹果是一样的）。

You're picking gift baskets from: [apple, apple, pear]. You don't want to list "apple+pear" twice just because there are two identical apples.

---

### 问题 / Problem

给定可能包含重复数字的整数数组 `nums`，返回所有可能的**不重复子集**。

Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set) with **no duplicate subsets**.

```
Input:  nums = [1, 2, 2]
Output: [[], [1], [1,2], [1,2,2], [2], [2,2]]
```

---

### 映射到模版 / Map to Pattern Template

```python
def backtrack(path, choices):
    if IS_COMPLETE(path):       # ← always add (subsets = all sizes)
        result.append(path[:])
        return
    for choice in choices:
        if IS_VALID(choice):    # ← SKIP if same value as previous sibling
            path.append(choice)
            backtrack(path, NEXT_CHOICES)
            path.pop()          # undo
```

**关键修改 / Key Modification:**
- Sort first → identical elements are adjacent
- At each level, skip `nums[i] == nums[i-1]` (but only for siblings, not parent-child)

---

### Python Solution with Trace

```python
from typing import List

def subsetsWithDup(nums: List[int]) -> List[List[int]]:
    nums.sort()  # Critical: sort so duplicates are adjacent
    result = []
    
    def backtrack(start: int, path: List[int]):
        result.append(path[:])  # Add current subset (all sizes valid)
        
        for i in range(start, len(nums)):
            # Skip duplicate siblings at the same tree level
            # nums[i] == nums[i-1] AND i > start (not first at this level)
            if i > start and nums[i] == nums[i - 1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1: each element used at most once
            path.pop()
    
    backtrack(0, [])
    return result

# Trace: nums = [1, 2, 2] (sorted)
# backtrack(0, [])
#   ├─ add []
#   ├─ i=0, pick 1 → backtrack(1, [1])
#   │     ├─ add [1]
#   │     ├─ i=1, pick 2 → backtrack(2, [1,2])
#   │     │     ├─ add [1,2]
#   │     │     └─ i=2, pick 2 → backtrack(3, [1,2,2])
#   │     │           └─ add [1,2,2]
#   │     └─ i=2, SKIP (2==2 and i>start=1) ✓ duplicate avoided!
#   ├─ i=1, pick 2 → backtrack(2, [2])
#   │     ├─ add [2]
#   │     └─ i=2, pick 2 → backtrack(3, [2,2])
#   │           └─ add [2,2]
#   └─ i=2, SKIP (2==2 and i>start=0) ✓
#
# Result: [[], [1], [1,2], [1,2,2], [2], [2,2]] ✓
```

**时间/空间复杂度:**
- Time: O(n · 2^n) — up to 2^n subsets, each copied in O(n)
- Space: O(n) recursion depth + O(n · 2^n) for output

---

### 与同模式其他题的对比 / Pattern Variations

```
题目              | 去重方式              | 每个元素能用多次?
------------------|----------------------|------------------
#78 Subsets       | 无重复输入, 不需要    | No (i+1)
#90 Subsets II    | sort + skip siblings | No (i+1)  ← TODAY
#39 Comb Sum      | 无重复输入            | Yes (i, not i+1)
#40 Comb Sum II   | sort + skip siblings | No (i+1)
#46 Permutations  | used[] boolean array  | No (全排列)

核心规律:
- 输入有重复 → sort + skip (if i > start and nums[i] == nums[i-1])
- 元素可重复使用 → backtrack(i, ...) not backtrack(i+1, ...)
- 排列问题 → 用 used[] 数组，不用 start
```

---

### 举一反三 / Pattern Connections

- **#40 Combination Sum II**: 同样的去重技巧，但要求总和 = target（今天先掌握去重，明天加约束）
- **#79 Word Search**: 同样是回溯，但在 2D grid 上，"已访问"替代 `start` 机制
- **#51 N-Queens**: 最复杂的回溯，3 个约束同时检查（行、列、对角线）

---

### 🧒 ELI5
Imagine picking stickers from a pile, but some stickers look exactly the same. When you're choosing the 2nd identical sticker in a row, you think: "Wait, I already tried picking from this position with an identical sticker — I'd get the same result. Skip!" That's all the `if i > start and nums[i] == nums[i-1]: continue` does.

### 📚 References
- https://leetcode.com/problems/subsets-ii/
- https://neetcode.io/problems/subsets-ii
- https://www.geeksforgeeks.org/subsets-with-no-two-adjacent-odd-numbers/
