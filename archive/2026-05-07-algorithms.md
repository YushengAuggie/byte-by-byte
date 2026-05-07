# 💻 算法 / Algorithms — Day 37
**题目 / Problem:** #33 Search in Rotated Sorted Array 🟡 Medium
**模式 / Pattern:** 二分搜索 Binary Search (5/7)
**LeetCode:** https://leetcode.com/problems/search-in-rotated-sorted-array/
**NeetCode:** https://neetcode.io/problems/find-target-in-rotated-sorted-array

---

## 🧩 Binary Search (5/7) — 在模板基础上变化

Building on the template from Day 32 (Binary Search block, problem 1: #704).

**回顾模板 / Template Recap:**
```python
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
```

**今天的变化 / Today's twist:** 数组是"旋转"过的排序数组 — 标准二分不能直接用，因为整体不再单调递增。需要**先判断哪半边是有序的**，再决定往哪边搜。

The array is a rotated sorted array — standard binary search breaks because the array isn't fully monotonic. Key insight: **even in a rotated array, at least one half is always sorted**.

---

## 现实类比 / Real-World Analogy

想象一叠按年份排好的文件，有人把后半段搬到了前面。比如原来是 `[1,2,3,4,5,6,7]`，变成了 `[4,5,6,7,1,2,3]`。虽然整体乱了，但每次切开，**至少一边是连续有序的**。你用这个性质来决定往哪边找。

Like a sorted stack of papers where someone moved the back half to the front. Though the whole stack is "rotated", when you split it in half, **at least one side is always in order**. Use that to decide which direction to search.

---

## 问题分析 / Problem Breakdown

```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4 (index of 0)

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Constraints:
- All values unique
- Time: O(log n)
```

---

## 映射到模板 / Mapping to Template

标准二分用 `arr[mid] vs target` 决定方向。旋转数组要**先确认有序半边**，再用范围检查决定方向。

```
Standard:  is target LEFT or RIGHT of mid?
Rotated:   WHICH HALF is sorted? Is target IN that sorted half?
```

**两个判断 / Two checks:**
1. 左半边有序？`nums[left] <= nums[mid]`
2. Target 在左半边范围内？`nums[left] <= target < nums[mid]`

---

## Python 解法 + Trace / Solution with Trace

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Check if LEFT half is sorted
        if nums[left] <= nums[mid]:
            # target in left sorted range?
            if nums[left] <= target < nums[mid]:
                right = mid - 1  # go left
            else:
                left = mid + 1   # go right
        else:
            # RIGHT half must be sorted
            # target in right sorted range?
            if nums[mid] < target <= nums[right]:
                left = mid + 1   # go right
            else:
                right = mid - 1  # go left
    
    return -1

# Trace: nums=[4,5,6,7,0,1,2], target=0
# Iteration 1: left=0, right=6, mid=3 → nums[3]=7, not target
#   Left sorted? nums[0]=4 <= nums[3]=7 ✅
#   target=0 in [4,7)? NO → left = mid+1 = 4
# Iteration 2: left=4, right=6, mid=5 → nums[5]=1, not target
#   Left sorted? nums[4]=0 <= nums[5]=1 ✅
#   target=0 in [0,1)? YES → right = mid-1 = 4
# Iteration 3: left=4, right=4, mid=4 → nums[4]=0 == target ✅
# Return 4
```

**时间复杂度 / Complexity:**
- Time: O(log n) — 每次排除一半
- Space: O(1) — 原地操作

---

## 与同模式题目对比 / Pattern Comparison

| 题目 | 变化点 | 关键差异 |
|------|--------|---------|
| #704 Binary Search | 标准排序数组 | 直接比较 |
| #153 Find Minimum in Rotated | 找旋转点 | 不需要 target，只找最小值 |
| **#33 Search in Rotated** | 找 target | 先判断有序半边 |
| #981 Time Based KV (下一题) | 时间戳 + 字符串 | 二分 + 条件判断 |

**核心洞察：** #153 找的是旋转点（pivot），#33 在知道有旋转的情况下找 target。两题都利用了"至少一边有序"这个性质。

---

## 举一反三 / Generalization

**同类变形：**
- 数组有重复元素时 → `nums[left] == nums[mid]` 时无法判断哪边有序，需要 `left++` 跳过 (LeetCode #81)
- 旋转后找最小值 → 不用 target，只看旋转点 (#153)
- 2D Matrix 搜索 → 先二分找行，再二分找列 (#74)

---

## 📝 Quiz

**问题:** 对于旋转数组 `[6,7,1,2,3,4,5]`，`mid=3`（值为2），`target=7`，下一步应该：
A) right = mid - 1  
B) left = mid + 1  
C) return mid  
D) return -1

<details><summary>答案 / Answer</summary>
**A) right = mid - 1**

Left half: `[6,7,1,2]` — nums[left]=6 > nums[mid]=2，左半边**不**是有序的。
Right half: `[2,3,4,5]` — 右半边有序。
target=7 在右半边范围 (2,5] 内吗？不在。
所以 target 在左半边 → right = mid - 1，往左搜。
</details>

---

## 📚 References
- [NeetCode Video — Search in Rotated Sorted Array](https://www.youtube.com/watch?v=U8XENwh8Oy8)
- [LeetCode #33 Editorial](https://leetcode.com/problems/search-in-rotated-sorted-array/editorial/)
- [Binary Search Patterns — LeetCode Explore](https://leetcode.com/explore/learn/card/binary-search/)

## 🧒 ELI5
把书架上的书按字母排好，然后把后半段搬到前面。要找某本书：先看中间那本，判断左边还是右边是"整齐的"，再判断要找的书在不在那个整齐的那半里，决定往哪边找。每次排除一半，找到为止。

Like a shelf of books sorted A-Z, then someone moved the Z-M books to the front. To find a book: look at the middle, figure out which half is "in order", check if your book would be in that ordered half, then search there. Eliminate half each time.
