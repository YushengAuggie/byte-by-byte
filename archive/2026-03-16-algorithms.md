# 💻 算法 Day 3 / Algorithms Day 3
**#1 Two Sum (Easy) — Arrays & Hashing**
🔗 https://leetcode.com/problems/two-sum/

---

## 现实类比 / Real-World Analogy

想象你在一家超市，口袋里有 $11，你想找到两件商品，价格加起来正好等于 $11。

笨方法：把每件商品和其他所有商品逐一配对比较 — 效率太低了 O(n²)。

聪明方法：每次拿起一件商品（价格 x），立刻检查你的"已看过价格"笔记本里有没有 `11 - x`。有就找到了！这就是哈希表的思路。

Imagine you're in a supermarket with $11 and want two items that add up to exactly $11. Brute force: compare every pair. Smart way: for each item (price x), instantly check if `11 - x` is already in your "seen prices" notebook. That's the hash map approach.

---

## 题目 / Problem Statement

**中文：** 给定一个整数数组 `nums` 和一个目标值 `target`，找出数组中和为 `target` 的两个数的**下标**。假设每道题恰好只有一个答案，且同一个元素不能使用两次。

**English:** Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`. You may assume exactly one solution exists, and you may not use the same element twice.

```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]   (because nums[0] + nums[1] = 2 + 7 = 9)
```

---

## 逐步思路 / Step-by-Step Walkthrough

### 方法1：暴力 O(n²) — 先理解，别用它

```
For i = 0 (num = 2):
  For j = 1 (num = 7):  2 + 7 = 9 ✅ → return [0, 1]
```

### 方法2：哈希表 O(n) — 这才是正解

核心思路：遍历时，对每个数 `num`，我们不是找"谁加上 num 等于 target"，而是找"target - num 在不在我们之前见过的数里"。

**具体示例追踪：**
```
nums = [2, 7, 11, 15], target = 9
seen = {}  (空字典)

i=0, num=2:
  complement = 9 - 2 = 7
  7 in seen? → No (seen is empty)
  → 把 2 存入 seen: seen = {2: 0}

i=1, num=7:
  complement = 9 - 7 = 2
  2 in seen? → Yes! seen[2] = 0
  → 返回 [seen[2], i] = [0, 1] ✅
```

**再来一个不那么直接的例子：**
```
nums = [3, 2, 4], target = 6
seen = {}

i=0, num=3:
  complement = 6 - 3 = 3
  3 in seen? → No
  seen = {3: 0}

i=1, num=2:
  complement = 6 - 2 = 4
  4 in seen? → No
  seen = {3: 0, 2: 1}

i=2, num=4:
  complement = 6 - 4 = 2
  2 in seen? → Yes! seen[2] = 1
  → 返回 [seen[2], i] = [1, 2] ✅
  (nums[1] + nums[2] = 2 + 4 = 6 ✓)
```

---

## Python 解法 / Python Solution

```python
def twoSum(nums: list[int], target: int) -> list[int]:
    # Hash map: value → index
    # We store numbers we've already visited
    seen = {}
    
    for i, num in enumerate(nums):
        # What number do we NEED to complete the pair?
        complement = target - num
        
        # Check if that number is already in our map
        if complement in seen:
            # Found it! Return both indices
            return [seen[complement], i]
        
        # Haven't found a pair yet; record this number and its index
        seen[num] = i
    
    # Problem guarantees a solution exists, so we won't reach here
    return []


# Test cases
print(twoSum([2, 7, 11, 15], 9))   # [0, 1]
print(twoSum([3, 2, 4], 6))         # [1, 2]
print(twoSum([3, 3], 6))            # [0, 1]
```

---

## 复杂度分析 / Complexity Analysis

```
时间复杂度 Time:  O(n)
  → 只遍历数组一次。哈希表查找是 O(1) 平均。

空间复杂度 Space: O(n)
  → 最坏情况下，哈希表存储 n-1 个元素（最后一对才匹配）。

vs. 暴力 Brute Force:
  Time: O(n²)  — 双重循环
  Space: O(1)  — 不用额外空间
```

**权衡：** 用空间换时间。这通常是对的 — 内存便宜，时间贵。

**Trade-off:** We trade space for time. Usually the right call — memory is cheap, user time is not.

---

## 边界情况 / Edge Cases

```python
# 两个相同的数字
twoSum([3, 3], 6)   # → [0, 1] ✅
# 关键：先检查 complement，再存入 seen
# 这样避免同一元素用两次

# 负数
twoSum([-1, -2, -3, -4, -5], -8)   # → [2, 4] (nums[2]+nums[4] = -3+-5)

# 只有两个元素
twoSum([1, 9], 10)   # → [0, 1]
```

---

## 举一反三 / Pattern Recognition

掌握了"边遍历边建哈希表"这个模式，你可以解决：

- **Two Sum II** (sorted array) — 用双指针，O(1) 空间
- **Two Sum III** (data structure) — 设计一个支持 add/find 的类
- **3Sum** (#15) — 固定一个数，对剩余用双指针
- **4Sum** (#18) — 嵌套一层再用双指针
- **Subarray Sum Equals K** (#560) — 前缀和 + 哈希表

**核心模式：** "我需要找 X，先问问我见过 X 吗？没见过，就记下现在这个。"

**The pattern:** "I need X. Have I seen X? No? Then record what I have now."

---

*Day 3 | 数组与哈希系列 | 昨天：Valid Anagram | 明天：Contains Duplicate*
