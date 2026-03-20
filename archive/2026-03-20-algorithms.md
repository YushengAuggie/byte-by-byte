# 💻 算法 Day 7 (4 min read) / Algorithms Day 7
## #238 Product of Array Except Self (Medium) — Arrays & Hashing / Prefix Products

🔗 [LeetCode #238: Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) 🟡 Medium
📹 [NeetCode Solution](https://neetcode.io/problems/products-of-array-discluding-self)

---

### 🌎 Real-World Analogy / 现实类比

想象你是一家工厂的质检员，流水线上有 N 个零件，每个都有一个重量。你的任务是：对于每个零件，快速计算出**其他所有零件的总重量之积**（不能把该零件自己算进去）。

最笨的方法？每次都把其他所有零件重新乘一遍 — O(n²)，太慢了。
聪明的方法？先从左到右算一遍"前缀积"，再从右到左算一遍"后缀积"，两个一乘就得到答案！

---

### 📋 Problem Statement / 题目

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`.

给定整数数组 `nums`，返回数组 `answer`，使得 `answer[i]` 等于 `nums` 中除 `nums[i]` 之外所有元素的乘积。

**Constraint**: Must run in O(n) time, **without using division** (不能用除法).

**Example:**
```
Input:  nums = [1, 2, 3, 4]
Output:       [24, 12,  8,  6]

Check: 
  answer[0] = 2 * 3 * 4 = 24  ✓
  answer[1] = 1 * 3 * 4 = 12  ✓
  answer[2] = 1 * 2 * 4 =  8  ✓
  answer[3] = 1 * 2 * 3 =  6  ✓
```

---

### 🔍 Step-by-Step Walkthrough / 逐步分析

**Key Insight**: For position `i`, the answer = (product of everything to the LEFT of i) × (product of everything to the RIGHT of i)

```
nums =   [ 1,   2,   3,   4 ]
index:     0    1    2    3

Left prefix products (prefix[i] = product of nums[0..i-1]):
prefix = [ 1,   1,   2,   6 ]
          ^     ^    ^    ^
          i=0   1*1  1*2  1*2*3
         (nothing (only (1,2   (1,2,3
          left)   nums[0])  left) left)

Right suffix products (suffix[i] = product of nums[i+1..end]):
suffix = [24,  12,   4,   1 ]
          ^     ^    ^    ^
        2*3*4  3*4   4   (nothing
                          right)

answer[i] = prefix[i] * suffix[i]:
  [0]: 1 * 24 = 24
  [1]: 1 * 12 = 12
  [2]: 2 *  4 =  8
  [3]: 6 *  1 =  6
```

**Space Optimization**: We can do this in O(1) extra space (output array doesn't count) by computing prefix in the output array first, then multiplying suffix on-the-fly from right to left.

---

### 🐍 Python Solution / Python 解法

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n
    
    # Pass 1: Fill answer[i] with the PREFIX product (product of everything LEFT of i)
    # After this pass: answer = [1, 1, 2, 6] for input [1, 2, 3, 4]
    prefix = 1
    for i in range(n):
        answer[i] = prefix      # store product of everything before i
        prefix *= nums[i]       # update running prefix
    
    # Pass 2: Multiply answer[i] by the SUFFIX product (product of everything RIGHT of i)
    # We traverse right-to-left, tracking running suffix product
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix     # multiply in the suffix product
        suffix *= nums[i]       # update running suffix

    return answer

# Test it:
print(productExceptSelf([1, 2, 3, 4]))    # → [24, 12, 8, 6]
print(productExceptSelf([-1, 1, 0, -3, 3]))  # → [0, 0, 9, 0, 0]
```

**Trace with [1, 2, 3, 4]:**
```
After Pass 1 (prefix):
  i=0: answer[0] = 1,  prefix = 1
  i=1: answer[1] = 1,  prefix = 2
  i=2: answer[2] = 2,  prefix = 6
  i=3: answer[3] = 6,  prefix = 24
  answer = [1, 1, 2, 6]

After Pass 2 (suffix, right to left):
  i=3: answer[3] = 6  * 1 = 6,   suffix = 4
  i=2: answer[2] = 2  * 4 = 8,   suffix = 12
  i=1: answer[1] = 1  * 12 = 12, suffix = 24
  i=0: answer[0] = 1  * 24 = 24, suffix = 24
  answer = [24, 12, 8, 6]  ✓
```

---

### ⏱️ Complexity / 复杂度

| | Complexity |
|---|---|
| **Time** | O(n) — two linear passes |
| **Space** | O(1) extra (output array doesn't count per problem rules) |

---

### 举一反三 / Pattern Recognition

**The Prefix/Suffix Pattern** unlocks many problems:
- Any time you need "everything except me" → think prefix × suffix
- **Variant**: [LeetCode #42: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — uses max-prefix and max-suffix arrays
- **Variant**: [LeetCode #152: Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) — track both max and min prefix (negatives flip signs!)
- **Variant**: [LeetCode #724: Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) — prefix sum version of the same idea

**Follow-up interview questions:**
1. "What if the array contains zeros?" → The code already handles it correctly (the zero propagates into the suffix/prefix)
2. "Can you solve it with O(n²) first, then optimize?" → Always a good way to start
3. "What about overflow?" → Use Python (arbitrary precision) or modular arithmetic

---

📚 **深入学习 / Learn More:**
- 📹 [NeetCode Solution Video](https://neetcode.io/problems/products-of-array-discluding-self) — best visual explanation of the prefix/suffix approach
- [Arrays & Hashing Pattern Guide — NeetCode Roadmap](https://neetcode.io/roadmap) — see the Arrays & Hashing section for this pattern
- Related: [LeetCode #42: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) 🔴 Hard | [LeetCode #152: Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) 🟡 Medium

🧒 **ELI5:** If you have 4 friends and you want to know how many handshakes happen when you're NOT included, you count all the handshakes to your left, then all the handshakes to your right, and multiply them together — that's your answer!
