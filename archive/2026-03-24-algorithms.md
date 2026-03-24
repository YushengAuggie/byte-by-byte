# 💻 算法 Day 10 / Algorithms Day 10

**#125 Valid Palindrome (Easy)** — 双指针模式 / Two Pointers

---

## 🧩 新模式 / New Pattern: 双指针模式 (Two Pointers)

📍 这个模式块共 5 道题 / This block: 5 problems

| # | 题目 | 难度 |
|---|------|------|
| 1 | #125 Valid Palindrome ← **今天 / TODAY** | 🟢 Easy |
| 2 | #167 Two Sum II | 🟡 Medium |
| 3 | #15 3Sum | 🟡 Medium |
| 4 | #11 Container With Most Water | 🟡 Medium |
| 5 | #42 Trapping Rain Water | 🔴 Hard |

---

### 什么时候用 / When to Use

排序数组中找配对、回文检测、原地操作时，想到双指针。

Use Two Pointers when: sorted array + find a pair, palindrome detection, in-place removal, merging sorted arrays.

### 识别信号 / Signals

> sorted array · find pair with sum · palindrome · remove in-place · merge sorted · container/water problems

### 通用模版 / Template

```python
def two_pointer_template(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current = arr[left] + arr[right]      # or some condition on left/right
        
        if current == target:
            return [left, right]              # found it
        elif current < target:
            left += 1                         # need bigger value → move left pointer right
        else:
            right -= 1                        # need smaller value → move right pointer left
    
    return []                                 # not found
```

**核心洞察 / Key Insight:** 排序 + 两端逼近，从 O(n²) 嵌套循环降到 O(n) 单次扫描。
Sorted order + converging from both ends → eliminates the need for nested loops.

---

## 📖 今日题目 / Today's Problem

🔗 [LeetCode #125 — Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) 🟢 Easy
📹 [NeetCode 讲解](https://neetcode.io/problems/is-palindrome)

---

### 🌍 现实类比 / Real-World Analogy

想象你是一个质检员，要验证一条传送带上的字符串"从两头读是否一样"。你派两个检查员分别站在传送带两端，同时向中间走，每步对比字母（跳过非字母数字的字符）。两人相遇时没有发现不同，就通过！

Think of two inspectors walking from both ends of a conveyor belt toward the middle, each checking only alphanumeric items and skipping punctuation/spaces.

---

### 🧩 如何映射到模版 / Mapping to Template

经典双指针，但有两个变化：
1. **不是排序数组**——我们用双指针做"对比"而不是"求和"
2. **需要跳过非字母数字字符**——在移动指针前先跳过无效字符

Classic Two Pointers, with two modifications:
1. No sorted array → use pointers for **comparison**, not sum-seeking
2. Skip non-alphanumeric chars before comparing

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric from the left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric from the right
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

---

### 🔍 代码追踪 / Code Trace

Input: `"A man, a plan, a canal: Panama"`

```
left=0  right=29  → 'A' vs 'a' → match  → left=1,  right=28
left=1  right=28  → skip ' '   → left=2
left=2  right=28  → 'm' vs 'm' → match  → left=3,  right=27
left=3  right=27  → 'a' vs 'a' → match  → left=4,  right=26
left=4  right=26  → 'n' vs 'n' → match  → ...
...
→ All chars match → return True ✅
```

Input: `"race a car"`

```
left=0  right=9   → 'r' vs 'r' → match
left=1  right=8   → 'a' vs 'a' → match
left=2  right=7   → 'c' vs 'c' → match
left=3  right=6   → 'e' vs 'a' → ❌ MISMATCH → return False
```

---

### 📊 复杂度 / Complexity

| | Time | Space |
|---|------|-------|
| Two Pointer | **O(n)** | **O(1)** |
| Built-in reverse | O(n) | O(n) — creates new string |

**Space O(1) is the win here** — we never create a cleaned copy of the string.

---

### 🔄 举一反三 / Pattern Connections

这道题是双指针的"热身"——纯粹的左右逼近。接下来的题目会在这个基础上加难度：

| 题目 | 变化 | 核心差异 |
|------|------|---------|
| **#167 Two Sum II** | 有序数组找和 | 移动指针基于 sum vs target |
| **#15 3Sum** | 三数之和 | 固定一个数 + 双指针找剩余两个 |
| **#11 Container With Most Water** | 面积最大化 | 移动较短的那边指针 |
| **#42 Trapping Rain Water** | 复杂水位计算 | 双指针维护左右最大高度 |

---

## 📚 参考资料 / References

1. [LeetCode #125 — Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)
2. [NeetCode — Two Pointers Pattern](https://neetcode.io/roadmap)
3. [Python str.isalnum() docs](https://docs.python.org/3/library/stdtypes.html#str.isalnum)

---

## 🧒 ELI5 / 用小孩能理解的话说

回文就像照镜子——左边和右边要一样。我们用两只手，一只从左摸，一只从右摸，跳过空格和标点，对比每个字母。如果两只手中间相遇了都没发现不同，就是回文！

A palindrome is like a mirror — left side = right side. We use two fingers, one from each end, skip spaces/punctuation, compare each letter. If both fingers meet in the middle without finding a mismatch → palindrome!
