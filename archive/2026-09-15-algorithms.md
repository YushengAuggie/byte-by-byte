# 算法 / Algorithms — Day 133
**日期 / Date:** 2026-09-15 | **题目 / Problem:** #647 Palindromic Substrings | **难度:** Medium 🟡
**模式 / Pattern:** 1-D Dynamic Programming (6/12)

---

## 💻 算法 / Algorithms — #647 Palindromic Substrings (Medium) 🟡

🧩 **一维动态规划模式 (6/12)** — 基于第 126 天的 DP 模板继续深化

---

### 🔗 Links
- 🔗 LeetCode: https://leetcode.com/problems/palindromic-substrings/
- 📹 NeetCode: https://neetcode.io/problems/palindromic-substrings

---

### 🌏 与模板的联系 / Building on the Pattern

上一题 (#5 Longest Palindromic Substring, Day 132) 找的是**最长回文子串**，今天 #647 找的是**所有回文子串的数量**。两者核心技术相同：**中心扩展法 (Expand Around Center)**，但返回值不同。

Previous problem (#5) found the *longest* palindromic substring. Today we count *all* palindromic substrings. Same core technique, different output.

---

### 🧩 从模板到今天的变体 / Pattern Variation

```
通用 1-D DP 模板:
dp[i] = TRANSITION(dp[i-1], dp[i-2], ...)

但本题更优解是: 中心扩展法
对每个中心点，向外扩展，每扩展一次就计一个回文
→ 不需要 DP 表，O(n²) 时间 O(1) 空间
```

**和 Day 132 (#5 Longest Palindromic Substring) 的对比：**
```
Day 132: 返回最长回文字串本身  → 记录 max_len, start
Day 133: 返回所有回文数量    → 每次扩展成功 count += 1
```

---

### 🌍 真实类比 / Real-World Analogy

想象你在审核一个 DNA 序列，需要找出所有"回文酶切位点"（回文序列）——每个位置都可能是回文的中心。从每个位置向外扩展，一旦不匹配就停止。

Imagine scanning a DNA sequence for all palindromic restriction sites — every position can be a center. Expand outward, stop when it breaks.

---

### 🎯 问题 / Problem

给定字符串 `s`，返回其中**回文子串的数量**。

> 单个字符也算回文。`"aaa"` 有 6 个回文子串：`"a"`, `"a"`, `"a"`, `"aa"`, `"aa"`, `"aaa"`

---

### ✅ Python 解法 / Solution with Trace

```python
def countSubstrings(s: str) -> int:
    count = 0
    n = len(s)
    
    def expand(left: int, right: int) -> int:
        """从中心向外扩展，返回回文数量 / Expand from center, count palindromes"""
        local_count = 0
        while left >= 0 and right < n and s[left] == s[right]:
            local_count += 1   # found a palindrome
            left -= 1          # expand outward
            right += 1
        return local_count
    
    for i in range(n):
        count += expand(i, i)      # 奇数长度 / odd length: center at i
        count += expand(i, i + 1)  # 偶数长度 / even length: center between i and i+1
    
    return count

# Trace for s = "aaa":
# i=0: expand(0,0)→ "a"=count 1; expand(0,1)→ s[0]='a'==s[1]='a' count 1, then -1>=0? no → 1
# i=1: expand(1,1)→ "a" 1; then "aaa" 1 → expand(1,2)→ "aa" 1 → total so far = 1+1+1+1+1 = 5
# i=2: expand(2,2)→ "a" 1; expand(2,3)→ out of bounds 0
# Total = 6 ✅
```

**复杂度 / Complexity:**
- ⏱ Time: O(n²) — 每个中心最多扩展 n 次
- 💾 Space: O(1) — 无额外数组

---

### 🔄 举一反三 / Connect to Pattern Block

这个模式块的 12 题都共享同一个核心思想：**定义子问题 → 找转移关系**：

| 题目 | 子问题定义 | 转移方程 |
|---|---|---|
| #70 Climbing Stairs | dp[i] = ways to reach step i | dp[i-1] + dp[i-2] |
| #198 House Robber | dp[i] = max money using first i houses | max(dp[i-1], dp[i-2]+nums[i]) |
| #5 Longest Palindrome | expand(center) → max length | 中心扩展 |
| **#647 今天** | **expand(center) → count palindromes** | **中心扩展，count++** |

**下一题预告 (Day 134): #91 Decode Ways** — 又回到 dp[i] = dp[i-1] + dp[i-2] 形式，但带条件判断

---

### 📝 Quiz
> 对于字符串 `s = "abc"`, `countSubstrings(s)` 返回什么？

<details><summary>查看答案 / Show Answer</summary>

**答案: 3**

- "a" (回文), "b" (回文), "c" (回文)
- "ab" ❌, "bc" ❌, "abc" ❌

每个单字符都是回文，但没有长度 > 1 的回文子串。

</details>

---

### 📚 References
- https://leetcode.com/problems/palindromic-substrings/ — LeetCode #647
- https://neetcode.io/problems/palindromic-substrings — NeetCode video
- https://cp-algorithms.com/string/manacher.html — Manacher's Algorithm (O(n) solution)

### 🧒 ELI5
把字符串里每个位置当作镜子的中心，向两边看：左右字母一样？这就是个回文，数一个！左右不一样了就停。每个位置试两次：当奇数回文的中心（单字符），和偶数回文中间缝的中心（双字符）。

Treat each position as a mirror center — look left and right. If they match, it's a palindrome, count it! Try each position twice: as center of odd-length palindromes and as the gap between even-length ones.
