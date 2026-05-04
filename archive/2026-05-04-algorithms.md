# 💻 算法 / Algorithms — Day 30: #875 Koko Eating Bananas (Medium)

> **模式 / Pattern:** Binary Search · **阶段 / Phase:** Mastery · **预计阅读时间 / Read time:** ~4 min

---

🧩 **二分搜索模式 (3/7)** — building on the template from Day 28 & 29

今天的题目是该模式的一个**经典变体**：搜索空间不是数组索引，而是**答案本身**。

Today's problem is a classic variation: the search space is the **answer itself**, not an array index.

📌 **模式系列进度 / Pattern Progress:**
1. ✅ #704 Binary Search (基础 / Basic)
2. ✅ #74 Search a 2D Matrix (2D变体 / 2D variant)
3. 👉 **#875 Koko Eating Bananas** (今天 / Today — 答案空间二分 / Binary search on answer)
4. ⬜ #153 Find Minimum in Rotated Sorted Array
5. ⬜ #33 Search in Rotated Sorted Array
6. ⬜ #981 Time Based Key-Value Store
7. ⬜ #4 Median of Two Sorted Arrays

---

## 题目 / Problem

🔗 [LeetCode #875 – Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) 🟡 Medium  
📹 [NeetCode Solution](https://neetcode.io/problems/eating-bananas)

**题意：** Koko 有 `piles` 堆香蕉，守卫 `h` 小时后回来。她每小时吃 `k` 根，每次只能吃一堆（吃完这堆，剩余时间不能吃别的堆）。求最小的 `k` 使她在 `h` 小时内吃完。

Koko has `piles` of bananas, guards return in `h` hours. She eats `k` bananas/hour, one pile at a time. Find **minimum k** so she finishes in `h` hours.

```
Input: piles = [3, 6, 7, 11], h = 8
Output: 4

At k=4: ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8 hours ✓
At k=3: 1+2+3+4 = 10 hours ✗
```

---

## 🧩 从模版到题目 / Mapping to the Template

**标准模版：** 在数组上搜索 target 的位置  
**Standard template:** Search for target position in array

**今天的变体：** 在 `[1, max(piles)]` 上搜索**最小合法答案**  
**Today's variation:** Search for the **minimum valid answer** in range `[1, max(piles)]`

```
模版变化 / Template adaptation:
- 搜索空间: left=1, right=max(piles)  ← 不是数组索引！
- 判断条件: can_finish(k, h) 替代 arr[mid] == target
- 方向: 如果可以完成，记录答案，继续往左找更小的 k
```

**关键洞察 / Key Insight:** 这是"**在答案空间二分**"的模式。当题目问"找最小的 X 使得条件成立"时，且 X 具有单调性（X越大越容易满足），就用这个模式。

*This is "binary search on answer" pattern. Whenever a problem asks for "minimum X such that condition holds" and the condition is monotone (larger X = easier to satisfy), use this.*

---

## Python 解法 / Solution

```python
from math import ceil
from typing import List

def minEatingSpeed(piles: List[int], h: int) -> int:
    # Search space: [1, max(piles)]
    # If k = max(piles), she can always finish in len(piles) <= h hours
    left, right = 1, max(piles)
    
    def can_finish(k: int) -> bool:
        # Hours needed = sum of ceil(pile / k) for each pile
        return sum(ceil(pile / k) for pile in piles) <= h
    
    result = right  # worst case: eat max pile per hour
    
    while left <= right:
        mid = (left + right) // 2
        if can_finish(mid):
            result = mid     # valid answer, try smaller
            right = mid - 1  # ← go LEFT to find minimum
        else:
            left = mid + 1   # too slow, need to go faster
    
    return result

# Trace for piles=[3,6,7,11], h=8:
# left=1, right=11, mid=6 → can_finish(6): 1+1+2+2=6 ≤ 8 ✓ → result=6, right=5
# left=1, right=5, mid=3  → can_finish(3): 1+2+3+4=10 > 8 ✗ → left=4
# left=4, right=5, mid=4  → can_finish(4): 1+2+2+3=8 ≤ 8 ✓ → result=4, right=3
# left=4 > right=3 → return 4 ✓
```

**复杂度 / Complexity:**
- Time: O(n log m) — n piles, m = max(piles)
- Space: O(1)

---

## 与模版的对比 / vs. Standard Template

| | 基础二分 / Basic | Koko 变体 / Koko Variant |
|---|---|---|
| 搜索空间 | 数组索引 [0, n-1] | 答案范围 [1, max(piles)] |
| mid 含义 | 数组位置 | 候选答案 (eating speed) |
| 判断 | `arr[mid] == target` | `can_finish(mid)` |
| 找到时 | return mid | record result, search left |

---

## 举一反三 / Pattern Connections

同模式的题 / Same pattern:
- **#1011 Capacity to Ship Packages** — 找最小船容量，`can_ship(capacity)` 替代 `can_finish(k)`
- **#410 Split Array Largest Sum** — 找最小的最大子数组和
- **#1482 Minimum Number of Days to Make m Bouquets** — 同样是"最小X满足条件"

口诀：**"最小化最大值 / 最大化最小值"** → 先想二分答案空间。

*Mantra: "minimize the maximum / maximize the minimum" → think binary search on answer.*

---

## 📚 参考资料 / References

- [LeetCode #875 – Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)(https://leetcode.com/problems/koko-eating-bananas/)
- [NeetCode Video Explanation](https://www.youtube.com/watch?v=U2SozAs9RzA)(https://neetcode.io/problems/eating-bananas)
- [Binary Search on Answer – Patterns](https://leetcode.com/discuss/study-guide/786126/Python-Powerful-Ultimate-Binary-Search-Template.-Solved-many-problems)(https://cp-algorithms.com/binary_search.html)

---

## 🧒 ELI5

Koko 要在 8 小时内吃完所有香蕉。她应该每小时吃多少根？我们不需要一个个试 1, 2, 3...，而是用"猜数字"游戏：先猜中间值，如果太慢就往大猜，如果可以就往小猜，每次排除一半的可能性，很快就找到答案！

*Koko needs to finish bananas in 8 hours. Instead of trying speeds 1, 2, 3... one by one, we play a guessing game: guess the middle speed, if too slow guess higher, if fast enough guess lower. Each guess eliminates half the possibilities — that's binary search on the answer space!*
