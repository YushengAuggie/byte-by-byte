# 💻 算法 Day 2 / Algorithms Day 2
**#242 Valid Anagram（有效的字母异位词）— Easy | Pattern: Arrays & Hashing**

---

## 生活类比 / Real-World Analogy

想象你有两袋相同字母的乐高积木。不管你怎么排列，只要袋子里的积木种类和数量完全一样，就是"字母异位词"。我们要做的，就是**数清楚每个袋子里有什么积木**。

*Imagine two bags of Lego pieces. As long as both bags contain the exact same types and counts of pieces — no matter how they're arranged — they're anagrams. Our job: count the pieces in each bag and compare.*

---

## 题目 / Problem Statement

**中文:** 给定两个字符串 `s` 和 `t`，判断 `t` 是否是 `s` 的字母异位词（即用完全相同的字母，重新排列而成）。

**English:** Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise. An anagram uses the same characters with the same frequencies.

```
Input: s = "anagram", t = "nagaram"   → Output: True
Input: s = "rat",     t = "car"       → Output: False
```

---

## 解题思路 / Step-by-Step Walkthrough

**核心想法 / Core Idea:**
字母异位词 = 每个字符出现的次数完全相同。
*Anagrams have identical character frequency distributions.*

**方法: 哈希表计数 / Method: Hash Map Counting**

用一个字典，遍历 `s` 时 +1，遍历 `t` 时 -1。最后所有值都是 0 → 是异位词。
*Use one dictionary: +1 for each char in `s`, -1 for each char in `t`. If all values are 0 → anagram.*

### 具体追踪 / Concrete Trace

`s = "anagram"`, `t = "nagaram"`

**遍历 s (+1):**
```
'a' → count['a'] = 1
'n' → count['n'] = 1
'a' → count['a'] = 2
'g' → count['g'] = 1
'r' → count['r'] = 1
'a' → count['a'] = 3
'm' → count['m'] = 1
```
状态 / State: `{'a':3, 'n':1, 'g':1, 'r':1, 'm':1}`

**遍历 t (-1):**
```
'n' → count['n'] = 0
'a' → count['a'] = 2
'g' → count['g'] = 0
'a' → count['a'] = 1
'r' → count['r'] = 0
'a' → count['a'] = 0
'm' → count['m'] = 0
```
状态 / State: `{'a':0, 'n':0, 'g':0, 'r':0, 'm':0}`

**所有值为 0 → True ✅**

---

## Python 解法 / Python Solution

```python
from collections import defaultdict

def isAnagram(s: str, t: str) -> bool:
    # Quick check: different lengths can't be anagrams
    # 长度不同直接排除
    if len(s) != len(t):
        return False
    
    # Count character frequencies
    # 统计每个字符出现的频率
    count = defaultdict(int)
    
    # +1 for every char in s
    for char in s:
        count[char] += 1
    
    # -1 for every char in t
    for char in t:
        count[char] -= 1
    
    # If all zeros, they have the same characters
    # 所有计数为零，说明字符完全匹配
    return all(v == 0 for v in count.values())


# 更 Pythonic 的写法 / More Pythonic version:
from collections import Counter

def isAnagram_v2(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)
```

---

## 复杂度分析 / Complexity Analysis

| | 复杂度 / Complexity | 说明 / Explanation |
|---|---|---|
| 时间 / Time | O(n) | n = len(s)，遍历两次 / two passes |
| 空间 / Space | O(k) | k = 字符集大小，最多26个字母 / at most 26 letters |

**为什么不排序？/ Why not sort?**
排序是 O(n log n)，哈希表是 O(n)，更快。面试时提出这个比较能加分。
*Sorting is O(n log n) vs O(n) for hash map. Always worth mentioning this tradeoff in interviews.*

---

## 边界情况 / Edge Cases

```python
isAnagram("a", "a")     # True  — single char match
isAnagram("a", "b")     # False — single char mismatch
isAnagram("", "")       # True  — both empty (Counter({}) == Counter({}))
isAnagram("ab", "a")    # False — length check catches this early
isAnagram("aa", "bb")   # False — same length, different chars
```

---

## 举一反三 / Pattern Recognition

这道题的核心模式：**用哈希表统计频率，再比较**。以下题目用同一个模式：

*Core pattern: **use a hash map to count frequencies, then compare**. Same pattern appears in:*

| 题目 / Problem | 变化 / Twist |
|---|---|
| #49 Group Anagrams | 把所有互为异位词的字符串分组 / group all anagrams together |
| #438 Find All Anagrams in a String | 滑动窗口找所有异位词位置 / sliding window to find positions |
| #383 Ransom Note | 一个字符串能否由另一个构成 / can s be built from t's chars |

**进阶思考 / Follow-up:**
如果字符串包含 Unicode（中文、emoji）怎么办？用 `Counter` 依然 work，因为它对任何 hashable 字符都有效。
*What if strings contain Unicode (Chinese, emoji)? `Counter` still works — it handles any hashable character.*

---
*Day 2 of 100 | #ByteByByte | Arrays & Hashing 系列*
