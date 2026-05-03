# 💻 算法 / Algorithms — #74 Search a 2D Matrix (Medium)

> **Day 33 · Mastery Phase · ~4 min read**
> 🧩 **二分搜索模式 (2/7)** — building on the template from Day 32

---

## 🧩 模式回顾 / Pattern Recap

上次我们学了 Binary Search 的基础模版（#704）：

```python
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
```

今天的变化：**一维数组 → 二维矩阵**。关键洞察：把 2D 矩阵**展平**成 1D 数组，索引转换即可。

Today's variation: apply binary search on a **2D matrix** by treating it as a virtual 1D array.

---

## 题目 / Problem

🔗 [LeetCode #74 - Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) 🟡 Medium
📹 [NeetCode Video](https://neetcode.io/problems/search-2d-matrix)

**条件 / Constraints:**
- 每行从左到右排序
- 每行第一个元素 > 上一行最后一个元素
- 也就是说：整个矩阵可以看成一个有序的 1D 数组！

```
Matrix:
[[ 1,  3,  5,  7],
 [10, 11, 16, 20],
 [23, 30, 34, 60]]

Target = 3 → True
Target = 13 → False
```

---

## 真实类比 / Real-World Analogy

想象一本英文词典：每页按字母排序，而且每页的第一个单词比前页最后一个单词靠后。你要找 "mango"——你不需要一页一页翻，先用二分找到页数，再在那页里二分找单词。

A dictionary where pages are sorted A-Z AND words within pages are sorted. You binary search the page number first, then binary search within the page. This matrix does both in one pass.

---

## 模版映射 / Map to Template

**核心技巧：把 2D 坐标转换成 1D 索引**

```python
# m rows, n cols
# 1D index i → 2D coords: row = i // n, col = i % n
# Example: matrix[1][2] in a 4-col matrix → 1D index = 1*4 + 2 = 6
```

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1  # treat as 1D array
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = matrix[mid // n][mid % n]  # convert 1D → 2D
        
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False
```

---

## 执行追踪 / Trace

```
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
m=3, n=4 → 1D range [0, 11]

Iter 1: mid=5 → matrix[5//4][5%4] = matrix[1][1] = 11 > 3 → right=4
Iter 2: mid=2 → matrix[2//4][2%4] = matrix[0][2] = 5 > 3  → right=1
Iter 3: mid=0 → matrix[0//4][0%4] = matrix[0][0] = 1 < 3  → left=1
Iter 4: mid=1 → matrix[1//4][1%4] = matrix[0][1] = 3 == 3 → True ✅
```

**复杂度 / Complexity:**
- Time: **O(log(m×n))** — 把 m×n 个元素当成 1D 数组二分
- Space: **O(1)**

---

## 举一反三 / Connect to the Pattern Block

| 题目 | 核心变化 | 难点 |
|------|---------|------|
| #704 Binary Search | 标准 1D 数组 | 基础 |
| **#74 今天** | 2D → 1D 映射 | 坐标转换 |
| #875 Koko Eating Bananas | 搜索"最小速度" | 搜索空间是答案，不是数组 |
| #153 Find Min in Rotated | 数组被旋转过 | 判断哪半边有序 |
| #4 Median of Two Sorted | 两个数组 | Hard，归并思路 |

**核心洞察：** Binary Search 不只能搜索已知数组 — 你可以搜索任何单调的**答案空间**！

---

## 📝 Quiz

```json
{"question":"In a 3x4 matrix, 1D index 9 maps to which 2D coordinate?","options":["[2][1]","[2][2]","[3][0]","[2][3]"],"correct_index":0}
```

💡 `9 // 4 = 2, 9 % 4 = 1` → `matrix[2][1]`

---

## 📚 References

- [LeetCode #74](https://leetcode.com/problems/search-a-2d-matrix/)
- [NeetCode Solution](https://neetcode.io/problems/search-2d-matrix)
- [Binary Search Patterns — NeetCode 150](https://neetcode.io/roadmap)

---

## 🧒 ELI5

把一个 3×4 的格子想象成展开的 12 格纸带。你要找第 9 格在哪一行：`9 ÷ 4 = 第2行（余1）`，所以是第 2 行第 1 列。有了这个魔法公式，二维的东西就变成一维了，然后直接套二分搜索！

Imagine unrolling a 3×4 grid into a 12-slot tape. To find slot 9: `9 ÷ 4 = row 2, remainder 1 = col 1`. With this magic formula, 2D becomes 1D, and you can binary search it directly!
