# 💻 算法 / Algorithms — Day 31
## #153 Find Minimum in Rotated Sorted Array 🟡 Medium
### 🧩 二分搜索模式 (4/7) — 旋转数组变体

🧩 **二分搜索 (4/7)** — building on the template from Day 28-30

这道题是二分搜索模式的**旋转变体**——数组不再完全有序，但仍保留关键单调性。

*This is the **rotation variant** of binary search — the array isn't fully sorted, but key monotonicity is preserved.*

---

### 链接 / Links
- 🔗 [LeetCode #153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) 🟡
- 📹 [NeetCode Video Solution](https://neetcode.io/problems/find-minimum-in-rotated-sorted-array)

---

### 现实类比 / Real-World Analogy

你有一副扑克牌，原本按 1-52 排好序，但有人从中间切了一刀——比如从第30张切开，变成了 [31,32,...,52,1,2,...,30]。你要找最小值（也就是"切口"在哪里），但你不能逐张翻——只能用"二分猜"。

*You have a deck of cards originally sorted 1-52, but someone cut the deck — e.g., [31,32,...,52,1,2,...,30]. Find the "cut point" (minimum) using binary search, not linear scan.*

---

### 与模板的映射 / Mapping to Template

回顾模板：
```python
# Standard template: find target in sorted array
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
```

**旋转数组的变化：** 我们没有 target，只有一个性质：**最小值右边的所有元素 < arr[right]**，左边的所有元素 > arr[right]（如果被旋转了）。

用 `arr[mid]` vs `arr[right]` 来决定收缩哪一半：
- `arr[mid] > arr[right]`：mid 在左段（较大的一段），最小值在右边 → `left = mid + 1`
- `arr[mid] < arr[right]`：mid 在右段（较小的一段），最小值在左边（含mid） → `right = mid`

*The twist: instead of comparing to a target, compare `arr[mid]` to `arr[right]` to determine which half the minimum lives in.*

---

### Python 解法 + 追踪 / Solution with Trace

```python
def findMin(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    
    while left < right:  # Note: < not <=
        mid = (left + right) // 2
        
        if nums[mid] > nums[right]:
            # mid is in the larger left portion
            # minimum must be to the right of mid
            left = mid + 1
        else:
            # mid is in the smaller right portion
            # minimum could be mid itself
            right = mid
    
    return nums[left]  # left == right == answer

# Trace: [3,4,5,1,2]
# left=0, right=4, mid=2 → nums[2]=5 > nums[4]=2 → left=3
# left=3, right=4, mid=3 → nums[3]=1 <= nums[4]=2 → right=3
# left=3, right=3 → return nums[3] = 1 ✓
```

**为什么用 `left < right` 而不是 `left <= right`？**  
因为 `right = mid`（不是 `mid - 1`），所以收敛时 left==right，不用额外检查。

*Why `left < right`? Because we use `right = mid` (not `mid - 1`), convergence happens at `left == right` — no off-by-one.*

**时间复杂度：** O(log n)  **空间复杂度：** O(1)

---

### 举一反三 / Connect to the Block

这道题在 Binary Search 模式块的位置：

| 题号 | 题目 | 关键变化 |
|------|------|---------|
| #704 | Binary Search | 纯模板 |
| #74 | Search a 2D Matrix | 2D → 1D 映射 |
| #875 | Koko Eating Bananas | 搜索答案空间 |
| **#153** | **Find Min in Rotated** | **旋转数组 → 比 right** |
| #33 | Search in Rotated | 找 target（下一题！） |
| #981 | Time Based KV | 搜索时间戳 |
| #4 | Median of Two Arrays | Hard，合并两段 |

**规律：** #153 和 #33 是姐妹题——先找最小值，再在两段有序数组中找 target。

*#153 and #33 are sibling problems — find the pivot first, then binary search in the correct half.*

---

### 📚 References
- [LeetCode #153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
- [NeetCode Explanation](https://neetcode.io/problems/find-minimum-in-rotated-sorted-array)
- [Binary Search on Rotated Arrays — cp-algorithms](https://cp-algorithms.com/algebra/binary-search.html)

### 🧒 ELI5
想象把一条直线从中间折了一下。折点是最低点。每次猜中间，如果中间比右边高，说明折点在右边；如果中间比右边低，说明折点在左边（或者就是中间自己）。每次都砍掉一半，很快就找到了！

*Imagine folding a line in the middle — the fold is the lowest point. Each guess, if the middle is higher than the right end, the fold is to the right; otherwise it's to the left. Halve the search space each time!*

---

### Quiz
