# 💻 算法 / Algorithms — #76 Minimum Window Substring (Hard)

> Day 21 · Phase: Growth · Est. 4 min
> 🧩 **滑动窗口模式 (5/6)** — building on the template from Day 17

---

## 🧩 滑动窗口 (5/6) — 模式回顾 / Pattern Recap

这是滑动窗口第 5 题（共 6 题）。今天我们看最难的变体：**最小窗口子串**。
*This is problem 5/6 in our Sliding Window block. Today: the hardest variant — Minimum Window Substring.*

**本块所有题 / Block problems:**
1. #121 Best Time to Buy and Sell Stock (Easy) ✅
2. #3 Longest Substring Without Repeating Characters (Medium) ✅
3. #424 Longest Repeating Character Replacement (Medium) ✅
4. #567 Permutation in String (Medium) ✅
5. **#76 Minimum Window Substring (Hard) ← 今天 / Today**
6. #239 Sliding Window Maximum (Hard) → 明天 / Tomorrow

**模版回顾 / Template Recap:**
```python
left = 0
for right in range(len(arr)):
    window.add(arr[right])  # expand right
    while CONDITION_VIOLATED:
        window.remove(arr[left])  # shrink left
        left += 1
    result = update(result, right - left + 1)
```
**核心洞察 / Key Insight:** 右指针扩张探索，左指针收缩维护约束。每个元素最多进出窗口各一次 → O(n)

---

## 题目 / Problem

🔗 [LeetCode #76 — Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) 🔴 Hard
📹 [NeetCode 讲解](https://www.youtube.com/watch?v=jSto0O4AJbM)

**题意：** 给定字符串 `s` 和 `t`，找 `s` 中包含 `t` 所有字符的最短子串。
*Find the minimum window in `s` that contains all characters of `t`.*

```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: "BANC" is the smallest window containing A, B, C
```

---

## 现实类比 / Real-World Analogy

想象你在新闻文章中找一段话，必须包含"人工智能"、"融资"、"OpenAI"这三个词。你希望找到包含这三个词的最短段落——不是全文，而是最紧凑的片段。这就是最小窗口子串问题。

*Imagine you're searching a news article for a passage that must contain "artificial intelligence", "funding", and "OpenAI". You want the shortest paragraph that includes all three — not the whole article, the most compact snippet. That's this problem.*

---

## 与模版的映射 / Mapping to Template

| 模版概念 | 本题实现 |
|----------|----------|
| `window.add()` | 右指针字符加入窗口计数 `window[c] += 1`，若满足 t 的需求则 `formed += 1` |
| `CONDITION_VIOLATED` → shrink when? | `formed == required`（已包含所有字符）时**收缩**（找更短的） |
| `window.remove()` | 左指针字符移出，若不再满足需求 `formed -= 1` |
| `result` | 记录 `(window_size, left, right)` 最小值 |

⚠️ **关键区别 vs 前几题：** 之前是窗口违反约束时收缩；本题是窗口**满足条件时**收缩（贪心地找更短）。
*Key difference vs. previous problems: we shrink when the window IS valid (greedy — find shorter), not when it's invalid.*

---

## Python 解法 + 追踪 / Solution + Trace

```python
from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""
    
    # Count chars needed from t
    need = Counter(t)          # {'A':1, 'B':1, 'C':1}
    required = len(need)       # 3 distinct chars needed
    
    window = {}
    formed = 0                 # how many chars satisfy their count in t
    
    # (window_length, left, right)
    best = float("inf"), 0, 0
    
    left = 0
    for right in range(len(s)):
        c = s[right]
        window[c] = window.get(c, 0) + 1
        
        # Check if this char now satisfies t's requirement
        if c in need and window[c] == need[c]:
            formed += 1
        
        # Shrink while window is valid (all chars present)
        while formed == required:
            # Update best
            win_len = right - left + 1
            if win_len < best[0]:
                best = (win_len, left, right)
            
            # Remove left char
            left_c = s[left]
            window[left_c] -= 1
            if left_c in need and window[left_c] < need[left_c]:
                formed -= 1
            left += 1
    
    return "" if best[0] == float("inf") else s[best[1]:best[2]+1]
```

**追踪 / Trace** (`s = "ADOBECODEBANC"`, `t = "ABC"`):
```
right=0(A): window={A:1}, formed=1
right=1(D): window={A:1,D:1}, formed=1
right=2(O): formed=1
right=3(B): window={..B:1}, formed=2
right=4(E): formed=2
right=5(C): window={..C:1}, formed=3 ← 满足!
  shrink: best=(6,0,5)="ADOBEC", remove A → formed=2
right=...继续扩张...
right=9(B): formed=3 again
  shrink: best=min(6, right-left+1)...
最终: best="BANC" (length 4) ✅
```

**复杂度 / Complexity:**
- ⏱ Time: O(|s| + |t|) — 每个字符最多进出窗口一次
- 🗂 Space: O(|s| + |t|) — 窗口计数哈希表

---

## 举一反三 / Connect to the Block

| 题目 | 约束类型 | 收缩时机 |
|------|----------|----------|
| #567 Permutation in String | 窗口 = 固定大小 | 固定长度收缩 |
| #3 Longest Substring | 无重复字符 | 有重复时收缩 |
| **#76 Min Window** | 包含所有目标字符 | **满足条件时贪心收缩** |
| #239 Sliding Window Max | 最大值 | 固定大小 (明天!) |

---

## 📝 Quiz

```json
{"question":"In #76 Minimum Window Substring, when do we shrink the left pointer?","options":["When the window is invalid (missing chars from t)","When the window is valid (contains all chars of t)","When the window size exceeds len(t)","When we find a repeated character"],"correct_index":1}
```

---

## 📚 References

- [LeetCode #76 Official](https://leetcode.com/problems/minimum-window-substring/)
- [NeetCode Video Explanation](https://www.youtube.com/watch?v=jSto0O4AJbM)
- [Sliding Window Patterns — LeetCode Discuss](https://leetcode.com/discuss/study-guide/1773891/sliding-window-technique-and-question-bank)

---

## 🧒 ELI5

想象你有一盒彩色积木，我给你一张清单说"我需要红、蓝、绿各一块"。你从左到右扫描这盒积木，用一个滑动框框住它们。当框里有清单上所有颜色时，你试着从左边缩小这个框（看能不能更短）。一旦缺了某个颜色，就从右边继续扩大。最后记录你找到的最小的框。

*Imagine a box of colored blocks, and I give you a checklist: "I need one red, one blue, one green." You scan the blocks left to right with a sliding frame. When the frame contains all the colors, you try to shrink it from the left (can it be shorter?). Once you're missing a color, expand from the right. Record the smallest valid frame you found.*
