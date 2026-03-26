# 💻 算法 Day 11 / Algorithms Day 11
**#167 Two Sum II — Input Array Is Sorted · 🟡 Medium**
*预计阅读时间 / Estimated reading time: 4 minutes*

---

## 🧩 双指针模式 (2/5) — 继承 Day 10 的模版

*Building on the Two Pointers template from Day 10*

今天是双指针模式的**第 2 题**（共 5 题）。上一题 Valid Palindrome 用双指针判断回文；今天我们用**同样的框架**解决"有序数组找配对"问题。

*This is the 2nd problem in our Two Pointers block (5 total). Yesterday we checked palindromes; today we use the same framework to find pairs in a sorted array.*

**本 block 全部 5 题 / All 5 problems:**
1. ✅ #125 Valid Palindrome (Easy) — Day 10
2. 👈 **#167 Two Sum II (Medium) — TODAY**
3. #15 3Sum (Medium)
4. #11 Container With Most Water (Medium)
5. #42 Trapping Rain Water (Hard)

**通用模版回顾 / Template Recap:**
```python
left, right = 0, len(arr) - 1
while left < right:
    total = arr[left] + arr[right]
    if total == target: return [left, right]
    elif total < target: left += 1   # need bigger sum
    else: right -= 1                  # need smaller sum
```

**与 Valid Palindrome 的对比 / vs Yesterday:**

| | Valid Palindrome | Two Sum II |
|---|---|---|
| 移动条件 / Move when | chars don't match | sum ≠ target |
| 收缩方向 / Shrink | both sides toward middle | whichever side adjusts sum |
| 核心逻辑 / Core | compare chars | adjust sum magnitude |

---

## 题目 / Problem

🔗 [LeetCode #167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · 🟡 Medium
📹 [NeetCode Video](https://neetcode.io/problems/two-sum-ii)

**现实类比 / Real-World Analogy:**

你有一张**已排序**的价目表，要找出恰好等于预算 `target` 的两件商品。
*You have a sorted price list and want to find exactly two items that sum to your budget.*

**题目 / Problem:**
给一个 1-indexed、**非递减排序**的数组，找两个数相加等于 `target`，返回它们的下标（1-indexed）。每个输入保证有唯一解。
*Given a 1-indexed, non-decreasing sorted array, find two numbers that sum to target. Return 1-indexed positions. Exactly one solution exists.*

```
Input:  numbers = [2, 7, 11, 15], target = 9
Output: [1, 2]  (numbers[0] + numbers[1] = 2 + 7 = 9)
```

---

## 💡 套用模版 / Mapping to Template

模版中 `arr[left] + arr[right]` 对应今天的 `numbers[left] + numbers[right]`。

**为什么有序数组可以用双指针？/ Why does sorting enable two pointers?**

关键洞察：数组排序后，如果 `sum < target`，我们**确定**需要更大的值 → 移动左指针。如果 `sum > target`，需要更小的值 → 移动右指针。无序数组无法这样推断！

*Key insight: With a sorted array, if sum < target, we KNOW we need a bigger value → move left. If sum > target, we need smaller → move right. Unsorted arrays can't support this reasoning!*

---

## 🐍 Python 解法 + 逐步追踪 / Solution + Trace

```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1  # 1
    
    while left < right:                 # 2
        current_sum = numbers[left] + numbers[right]  # 3
        
        if current_sum == target:       # 4
            return [left + 1, right + 1]  # convert to 1-indexed
        elif current_sum < target:      # 5
            left += 1   # need bigger number
        else:
            right -= 1  # need smaller number
    
    return []  # guaranteed to find answer, never reaches here
```

**追踪 / Trace** with `numbers = [2, 7, 11, 15], target = 9`:

```
Step 1: left=0, right=3 → 2+15=17 > 9  → right=2
Step 2: left=0, right=2 → 2+11=13 > 9  → right=1
Step 3: left=0, right=1 → 2+7=9  == 9  → return [1, 2] ✅
```

**时间/空间复杂度 / Complexity:**
- ⏱ Time: **O(n)** — each pointer moves at most n steps total
- 💾 Space: **O(1)** — no extra data structures

**vs. Brute Force:** O(n²) with nested loops. Two pointers give a 10-100x speedup on large inputs.

---

## 举一反三 / Pattern Connections

**在本 block 中 / Within this pattern block:**

- **#15 3Sum (下一题):** Same two-pointer idea + outer loop. Fix one element, two-pointer the rest.
- **#11 Container With Most Water:** `left`, `right` move based on which height is smaller — same structure!
- **#42 Trapping Rain Water:** Two pointers + track running max from each side. Most complex variation.

**看到这些信号就想到双指针 / Recognize these signals:**
- ✅ Sorted array
- ✅ "Find pair that sums to X"
- ✅ O(1) space required
- ✅ Palindrome check
- ✅ "Remove duplicates in-place"

---

## 📚 References

1. [LeetCode #167 — Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
2. [NeetCode Two Sum II explanation](https://neetcode.io/problems/two-sum-ii)
3. [Two Pointers pattern guide — LeetCode Patterns](https://leetcode.com/discuss/study-guide/1688903/Solved-all-two-pointers-problems-in-100-days)

---

## 🧒 ELI5

你和朋友站在一排数字两端。你喊出你们俩数字的和。太小就让左边的人向右走一步（换更大的数）；太大就让右边的人向左走一步（换更小的数）；正好就赢了！

*You and a friend stand at opposite ends of a number line. Call out your sum. Too small → left person steps right (bigger number). Too big → right person steps left (smaller). Exact match → win!*
