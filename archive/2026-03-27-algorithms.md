# 💻 算法 Day 12 / Algorithms Day 12
## #15 3Sum — Medium — Two Pointers (3/5)

> **难度 / Difficulty:** 🟡 Medium | **阶段 / Phase:** Growth | **预计时间 / Read time:** 4 min

---

## 🧩 双指针模式 (3/5) — 继续 Day 9 引入的模版

Building on the **双指针模式 / Two Pointers** template from Day 9 (Valid Palindrome).

**模式回顾 / Pattern Recap:**
```python
left, right = 0, len(arr) - 1
while left < right:
    total = arr[left] + arr[right]
    if total == target: return [left, right]
    elif total < target: left += 1
    else: right -= 1
```
**本模块问题 / Block Problems:**
1. ✅ #125 Valid Palindrome (Easy) — Day 9
2. ✅ #167 Two Sum II (Medium) — Day 11
3. 👉 **#15 3Sum (Medium) — TODAY**
4. 🔜 #11 Container With Most Water (Medium)
5. 🔜 #42 Trapping Rain Water (Hard)

**今天的变化 / Today's Twist:** 从找"2个数之和"升级到找"3个数之和为0"，需要先固定一个数，再用双指针扫余下部分。

---

## 🔗 题目链接 / Links

- 📝 [LeetCode #15 — 3Sum](https://leetcode.com/problems/3sum/)
- 📹 [NeetCode — 3Sum Solution](https://neetcode.io/problems/three-integer-sum)

---

## 🌍 真实场景类比 / Real-World Analogy

想象你在整理一箱重量不等的砝码，你想找到**三个**砝码，使它们的重量加起来恰好为零（一正一负加中间值）。

逐一穷举三个砝码的所有组合是 O(n³)，太慢了。如果先把砝码**按重量排序**，固定最左边的砝码，然后用左右两个指针扫剩余部分，就能降到 O(n²)。

Imagine sorting weights in a box and finding **three** that sum to zero. Brute force is O(n³). Sort them, fix the leftmost, and use two pointers for the rest → O(n²).

---

## 📋 问题描述 / Problem

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that:
- `i != j`, `i != k`, `j != k`
- `nums[i] + nums[j] + nums[k] == 0`

The solution set **must not contain duplicate triplets.**

```
Input:  nums = [-1, 0, 1, 2, -1, -4]
Output: [[-1, -1, 2], [-1, 0, 1]]
```

---

## 🗺️ 映射到模版 / Mapping to Template

**核心思路：** 排序后，外层遍历固定 `nums[i]`，内层用双指针找 `nums[left] + nums[right] == -nums[i]`。

```
Fixed:   nums[i] = -1   target for inner = 0 - (-1) = 1
Array:   [-4, -1, -1, 0, 1, 2]  (sorted)
              i  L        R
              
Step 1: left=-1, right=2 → sum=1 ✅ found! → skip duplicates
Step 2: left=0,  right=1 → sum=1 ✅ found!
Step 3: left >= right → stop inner loop
```

---

## 🐍 Python 解法 + 逐行追踪 / Solution + Trace

```python
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()                           # [-4, -1, -1, 0, 1, 2]
    result = []
    
    for i in range(len(nums) - 2):        # fix the first element
        if nums[i] > 0:                   # sorted: if first > 0, no solution
            break
        if i > 0 and nums[i] == nums[i-1]:  # skip duplicates for i
            continue
        
        left, right = i + 1, len(nums) - 1  # two pointers for the rest
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # skip duplicates for left and right
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1   # need larger sum
            else:
                right -= 1  # need smaller sum
    
    return result

# Trace with nums = [-1, 0, 1, 2, -1, -4]:
# After sort: [-4, -1, -1, 0, 1, 2]
# i=0: nums[i]=-4, left=1(-1), right=5(2) → sum=-3 → left++
#       left=2(-1), right=5(2) → sum=-3 → left++
#       left=3(0),  right=5(2) → sum=-2 → left++
#       left=4(1),  right=5(2) → sum=-1 → left++
#       left>=right → stop
# i=1: nums[i]=-1, left=2(-1), right=5(2) → sum=0 ✅ append [-1,-1,2]
#       skip dups → left=3(0), right=4(1) → sum=0 ✅ append [-1,0,1]
#       left>=right → stop
# i=2: nums[i]=-1 == nums[i-1]=-1 → skip (duplicate!)
# i=3: nums[i]=0, left=4(1), right=5(2) → sum=3 → right--
#       left>=right → stop
# Result: [[-1,-1,2], [-1,0,1]] ✅
```

**时间复杂度 / Time Complexity:** O(n log n) sort + O(n²) = **O(n²)**
**空间复杂度 / Space Complexity:** O(1) extra (excluding output)

---

## ⚡ 与模版的关键差异 / Key Differences from Template

| | Two Sum II (Day 11) | 3Sum (Today) |
|--|--|--|
| 目标 | 找2个数之和 = target | 找3个数之和 = 0 |
| 结构 | 单层双指针 | 外层 for + 内层双指针 |
| 去重 | 不需要 | 必须跳过重复元素 |
| 复杂度 | O(n) | O(n²) |

---

## 🔁 举一反三 / Pattern Connections

- **#11 Container With Most Water (下一题):** 同样外层遍历 + 内层双指针，但优化目标不同（最大面积 vs 零和）
- **#42 Trapping Rain Water (最难题):** 双指针 + 边界最大值，是本模式的终极形态
- **变体：** 4Sum (#18) = 再加一层 for 循环 → O(n³)，同样思路

---

## 📚 参考资料 / References

- 🔗 [LeetCode #15 — 3Sum](https://leetcode.com/problems/3sum/)
- 🔗 [NeetCode Video Solution](https://neetcode.io/problems/three-integer-sum)
- 🔗 [Two Pointers Pattern — LeetCode Explore](https://leetcode.com/explore/learn/card/array-and-string/205/array-two-pointer-technique/)

---

## 🧒 ELI5

想象你有一堆正数和负数的磁铁，你要找三块加起来刚好等于零。

先把它们从小到大排好，然后：拿起最左边的那块，再用两只手各从左右两边向中间夹。夹到了就记录下来，没夹到就根据总和太大还是太小来移动手。

这样就不用每三块都试一遍，快很多！
