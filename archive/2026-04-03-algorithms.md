# 💻 算法 Day 16 / Algorithms Day 16

## 🧩 滑动窗口模式 (2/6) — Building on the template from Day 15

> #3 Longest Substring Without Repeating Characters 🟡 Medium

🔗 [LeetCode #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/)  
📹 [NeetCode Video](https://neetcode.io/problems/longest-substring-without-repeating-characters)

---

**今天的问题是模式的第 2 题（共 6 题）**，我们继续用滑动窗口模板。相比昨天的 #121（股票买卖，只追踪一个 min 值），今天窗口需要追踪「一个集合」——这是滑动窗口真正的威力所在。

Today is problem **2/6** in the Sliding Window block. Unlike #121 (tracking a single min value), today's window tracks a **set of characters** — this is where the pattern gets powerful.

---

### 🗺️ 模板回顾 / Template Recap

```python
left = 0
for right in range(len(arr)):
    window.add(arr[right])      # expand right
    while CONDITION_VIOLATED:
        window.remove(arr[left])  # shrink left
        left += 1
    result = max(result, right - left + 1)
```

**核心洞察 / Key Insight:** 右指针扩张探索，左指针收缩维护约束。每个元素最多进出窗口各一次 → O(n)。

---

### 🌍 真实类比 / Real-World Analogy

想象你在刷 Spotify 播放历史，想找「连续播放、没有重复歌曲」的最长片段。当出现重复时，你从头开始，直到重复歌曲被移出窗口之外。

Imagine scanning your Spotify history for the longest streak where no song repeats. The moment a duplicate appears, you slide your start forward until the duplicate is gone.

---

### 📝 问题 / Problem

给定字符串 `s`，找出不含重复字符的最长子串的长度。

Given string `s`, find the length of the longest substring without repeating characters.

```
Input:  s = "abcabcbb"
Output: 3  ("abc")

Input:  s = "pwwkew"
Output: 3  ("wke")
```

---

### 🗂️ 映射到模板 / Mapping to Template

| 模板元素 | 本题对应 |
|----------|----------|
| `window` | `set()` — 当前窗口中的字符 |
| `CONDITION_VIOLATED` | `arr[right] in window`（出现重复） |
| 扩张 | 把 `s[right]` 加入 set |
| 收缩 | 把 `s[left]` 从 set 移除，`left += 1` |
| `result` | `max(result, right - left + 1)` |

---

### 🐍 Python 解法 + 追踪 / Python Solution + Trace

```python
def lengthOfLongestSubstring(s: str) -> int:
    window = set()       # characters currently in window
    left = 0
    result = 0

    for right in range(len(s)):
        # Shrink window until no duplicate
        while s[right] in window:
            window.remove(s[left])
            left += 1

        # Expand: add new character
        window.add(s[right])
        result = max(result, right - left + 1)

    return result
```

**追踪 "abcabcbb" / Trace:**
```
right=0: window={'a'}, len=1
right=1: window={'a','b'}, len=2
right=2: window={'a','b','c'}, len=3  ← result=3
right=3: 'a' dup! → remove 'a', left=1 → window={'b','c','a'}, len=3
right=4: 'b' dup! → remove 'b', left=2 → window={'c','a','b'}, len=3
right=5: 'c' dup! → remove 'c', left=3 → window={'a','b','c'}, len=3
right=6: 'b' dup! → remove 'a','b', left=5 → window={'c','b'}, len=2
right=7: 'b' dup! → remove 'c','b', left=7 → window={'b'}, len=1
Final: 3 ✅
```

**复杂度 / Complexity:**
- Time: O(n) — each char enters/exits window at most once
- Space: O(min(m, n)) where m = charset size (26 for lowercase)

**优化版 / Optimized (HashMap for O(1) jump):**
```python
def lengthOfLongestSubstring(s: str) -> int:
    char_index = {}  # char → last seen index
    left = 0
    result = 0

    for right, ch in enumerate(s):
        # Jump left past the duplicate directly
        if ch in char_index and char_index[ch] >= left:
            left = char_index[ch] + 1
        char_index[ch] = right
        result = max(result, right - left + 1)

    return result
```
→ 避免 while 循环，直接跳跃 left，同样 O(n) 但常数更小。

---

### 🔄 举一反三 / This Pattern Block

| 题目 | 窗口内容 | 约束条件 |
|------|----------|----------|
| #121 (Day 15) | 单个 min 值 | 无，只追踪最小值 |
| **#3 (今天)** | **字符集合** | **无重复** |
| #424 (下期) | 字符频率 map | 替换次数 ≤ k |
| #567 | 字符频率 map | 频率完全匹配 |
| #76 (Hard) | 字符频率 map | 包含所有目标字符 |

---

### 🧒 ELI5

用两根手指夹住一段字符串，右手不断向右扩张。一旦右手摸到一个和窗口内重复的字母，左手就往右收缩，直到没有重复为止。全程记录最宽的窗口宽度。

Use two fingers on a string. Right finger keeps expanding right. The moment it hits a duplicate, the left finger moves right to shrink the window until no duplicates remain. Track the max width you ever saw.

---

### 📚 References

- [LeetCode #3 — Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
- [NeetCode Explanation](https://neetcode.io/problems/longest-substring-without-repeating-characters)
- [Sliding Window Pattern — GeeksForGeeks](https://www.geeksforgeeks.org/window-sliding-technique/)
