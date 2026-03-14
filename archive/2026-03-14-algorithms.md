# Algorithms Day 1 — #217 Contains Duplicate
*Date: 2026-03-14 | Pattern: Arrays & Hashing | Difficulty: Easy*

---

💻 **算法 Day 1 / Algorithms Day 1** — #217 Contains Duplicate (Easy) — Arrays & Hashing

---

**现实类比 / Real-World Analogy**

想象你在整理一箱名片。你从盒子里一张一张往外拿，每拿出一张，先看看桌上有没有一样的。如果有，说明你有重复的联系人。这就是「哈希集合」的工作方式——把「已见过的」放在一个快速查找的结构里。

*Imagine going through a box of business cards. You pull each card out and check if you've already put one on the table. If you find a match, you have a duplicate. That's exactly what a hash set does — it gives you O(1) lookup for "have I seen this before?"*

---

**题目 / Problem Statement**

给你一个整数数组 `nums`，如果其中存在任何重复值，返回 `true`；否则返回 `false`。

*Given an integer array `nums`, return `true` if any value appears at least twice, `false` if every element is distinct.*

```
Input:  [1, 2, 3, 1]   → Output: True  (1 出现了两次)
Input:  [1, 2, 3, 4]   → Output: False (每个数都唯一)
Input:  [1, 1, 1, 3, 3, 4, 3, 2, 4, 2] → Output: True
```

---

**逐步分析 / Step-by-Step Walkthrough**

**方法一：暴力法（别用这个）**
双重循环，比较每对元素。Time: O(n²)，Space: O(1)
面试中绝对不要停在这里。

**方法二：排序法**
排序后相邻元素比较。Time: O(n log n)，Space: O(1)
稍好，但破坏了原数组顺序。

**方法三：哈希集合（最优解）**
维护一个「已见过」的集合，遍历一次搞定。

```
nums = [1, 2, 3, 1]
seen = {}

Step 1: num=1  → seen={1}           (新元素，加入)
Step 2: num=2  → seen={1,2}         (新元素，加入)
Step 3: num=3  → seen={1,2,3}       (新元素，加入)
Step 4: num=1  → 1 在 seen 里！→ return True ✓
```

---

**Python 解法 / Python Solution**

```python
def containsDuplicate(nums: list[int]) -> bool:
    # Use a hash set for O(1) average-case lookup
    seen = set()
    
    for num in nums:
        if num in seen:
            # Found a duplicate — return immediately (early exit)
            return True
        seen.add(num)
    
    # No duplicates found after full traversal
    return False

# One-liner alternative (Pythonic, but reads the whole list)
# return len(nums) != len(set(nums))
```

**为什么用 `set` 而不是 `list`？**
`x in list` → O(n)，要遍历找
`x in set`  → O(1)，哈希直接定位
*`list` membership check is O(n); `set` uses hashing for O(1) average lookup. This is the key insight.*

---

**复杂度 / Complexity**

| | 暴力法 | 排序法 | 哈希集合 |
|---|---|---|---|
| Time | O(n²) | O(n log n) | **O(n)** |
| Space | O(1) | O(1) | **O(n)** |

最优解是时间-空间的经典权衡：用 O(n) 额外空间换取 O(n) 时间。
*Classic time-space tradeoff: we pay O(n) space to get O(n) time.*

---

**举一反三 / Pattern Recognition**

这道题是「Arrays & Hashing」模式的入口。掌握它，你能解：

1. **#1 Two Sum** — 同样的「已见过」思路，存的是值→索引的映射
2. **#128 Longest Consecutive Sequence** — 先用 set 存所有数，再按规律遍历
3. **#49 Group Anagrams** — 用排序后的字符串作 key，用 dict 分组
4. **#36 Valid Sudoku** — 三个方向各维护一个 set

**核心模式**：每次遇到「需要快速判断某元素是否出现过」，第一反应是 `set`；需要记录「出现次数或位置」，用 `dict`。

*The pattern: whenever you need "have I seen this before?", think `set`. When you need "how many times / where did I see it?", think `dict`. This pattern appears in ~30% of easy/medium array problems.*

---

**Mini Challenge 🎯**

如果题目改成：找到数组中出现超过 n/2 次的元素（保证存在），怎么做？
*What if you need to find the element that appears more than n/2 times? (Boyer-Moore Voting Algorithm — hint for tomorrow's pattern thinking)*
