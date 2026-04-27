# 💻 算法 / Algorithms — Day 32

**题目 / Problem:** #704 Binary Search | 🟢 Easy  
**模式 / Pattern:** Binary Search (第1题，共7题 / Problem 1 of 7)  
**预计阅读 / Read time:** ~4 分钟

---

## 🧩 新模式 / New Pattern: 二分搜索模式 (Binary Search)

📍 **本模式共 7 题 / This block: 7 problems**

```
#704 Binary Search (Easy)                ← 今天 TODAY
#74  Search a 2D Matrix (Medium)
#875 Koko Eating Bananas (Medium)
#153 Find Minimum in Rotated Sorted Array (Medium)
#33  Search in Rotated Sorted Array (Medium)
#981 Time Based Key-Value Store (Medium)
#4   Median of Two Sorted Arrays (Hard)
```

### 什么时候用 / When to Use

当你看到这些信号时，考虑二分搜索：  
Look for these signals to reach for binary search:

- **排序数组** 里找某个值  
- 要求 **O(log n)** 时间复杂度  
- 找 **"满足条件的最小/最大值"**（最小化/最大化）  
- 搜索空间可以 **单调地判断 True/False**

### 识别信号 / Signals

```
sorted array, search, O(log n),
"find minimum that satisfies condition",
"find maximum", monotonic property
```

### 通用模版 / Template

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2  # 避免溢出：left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1   # target 在右半边
        else:
            right = mid - 1  # target 在左半边
    
    return -1  # not found
```

**Time:** O(log n) | **Space:** O(1)

### 核心洞察 / Key Insight

> 每次排除**一半**搜索空间 — 不只用于排序数组，任何单调性都可以二分。  
> Each step eliminates **half** the search space — works for any monotonic property, not just sorted arrays.

---

## 📖 今天的题目 / Today's Problem

**[#704 Binary Search](https://leetcode.com/problems/binary-search/)** 🟢 Easy  
📹 [NeetCode 讲解](https://neetcode.io/problems/binary-search)

---

### 🌍 真实类比 / Real-World Analogy

想象查字典找 "python" 这个词：  
Imagine looking up "python" in a dictionary:

1. 翻到中间页 → "m" 开头，python > m → 翻右边  
2. 翻到右边中间 → "s" 开头，python < s → 翻左边  
3. 找到 "p" 区，再找 "py" → 命中！

每次翻书都排除一半，不需要从第一页翻到最后。  
Each flip eliminates half — no need to read every page.

---

### 🔍 问题描述 / Problem

给定升序整数数组 `nums` 和目标值 `target`，返回 `target` 的下标，不存在返回 `-1`。  
Given a sorted array of integers and a target, return the index of target or -1 if not found.

```
Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4

Input: nums = [-1, 0, 3, 5, 9, 12], target = 2
Output: -1
```

---

### 🗺️ 套用模版 / Map to Template

这就是**模版的原型题** — 直接套用即可！  
This IS the template — apply it directly!

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1   # target must be to the right
        else:
            right = mid - 1  # target must be to the left
    
    return -1
```

### 🔬 执行追踪 / Trace

```
nums = [-1, 0, 3, 5, 9, 12], target = 9

Iteration 1: left=0, right=5, mid=2 → nums[2]=3 < 9 → left=3
Iteration 2: left=3, right=5, mid=4 → nums[4]=9 == 9 → return 4 ✅

nums = [-1, 0, 3, 5, 9, 12], target = 2

Iteration 1: left=0, right=5, mid=2 → nums[2]=3 > 2 → right=1
Iteration 2: left=0, right=1, mid=0 → nums[0]=-1 < 2 → left=1
Iteration 3: left=1, right=1, mid=1 → nums[1]=0 < 2 → left=2
left(2) > right(1) → return -1 ✅
```

---

### ⏱️ 复杂度 / Complexity

| | 时间 Time | 空间 Space |
|---|---|---|
| 二分搜索 | O(log n) | O(1) |
| 暴力 Brute | O(n) | O(1) |

**为什么 O(log n)?** 每次循环 n 减半 → log₂(n) 轮后 n=1。  
**Why O(log n)?** Each iteration halves n → after log₂(n) steps, n=1.

---

### 🔁 举一反三 / Pattern Variations (本模式7题)

| 题号 | 变化点 / What Changes |
|---|---|
| #74 Search 2D Matrix | 搜索空间变成矩阵，但可以展平为有序数组 |
| #875 Koko Eating Bananas | 不是搜索"值"，而是搜索"速度"（二分答案） |
| #153 Find Min Rotated | 数组有旋转，需要判断哪半边是有序的 |
| #33 Search Rotated | 旋转 + 找特定值，两重判断 |
| #4 Median Two Arrays | Hard：搜索空间是分割点 |

模版不变，**变化的是"如何判断往哪边走"**。  
Template stays the same — **what changes is "which direction to go"**.

---

## 📚 References

- https://leetcode.com/problems/binary-search/ — LeetCode #704
- https://neetcode.io/problems/binary-search — NeetCode video walkthrough
- https://cp-algorithms.com/num_methods/binary_search.html — Binary search theory

---

## 🧒 ELI5

猜数字游戏：1到100里猜一个数。你每次猜中间的数（50），我告诉你大了还是小了。你不需要猜100次——最多猜7次就能找到！因为每次都砍掉一半。  
Number guessing game: 1 to 100. You always guess the middle (50), I say higher or lower. You don't need 100 guesses — at most 7! Because each guess cuts the possibilities in half.
