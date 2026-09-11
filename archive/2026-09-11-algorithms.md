# 💻 算法 / Algorithms — Day 132
## #5 Longest Palindromic Substring 🟡 Medium
🧩 **一维动态规划模式 (5/12)** — building on the template from Day 126

---

## 回顾模版 / Pattern Recap

这是本 DP 模块第 5 题。前 4 题（爬楼梯、最小费用爬楼梯、打家劫舍 I & II）都是**线性 1D DP**——每个状态只依赖前几个状态。今天的变化：**状态是二维的 `dp[i][j]`**，但问题本质仍是 1D DP 的思维：定义子问题 → 写转移方程 → 确定 base case。

This is problem 5/12 in the 1-D DP block. The twist: today's DP table is 2D `dp[i][j]`, but the thinking pattern is the same.

---

## 真实场景 / Real-World Analogy

想象 DNA 序列分析：找最长的回文子序列，用于检测基因突变对称区域。或者拼写检查器需要找最长的"镜像"词根。

DNA sequence analysis: find the longest symmetric (palindromic) region — same idea.

---

## 问题 / Problem

🔗 [LeetCode #5](https://leetcode.com/problems/longest-palindromic-substring/) | 📹 [NeetCode](https://neetcode.io/problems/longest-palindromic-substring)

给你一个字符串 `s`，返回其中最长的回文子串。
Given string `s`, return the longest palindromic substring.

```
Input: s = "babad"
Output: "bab" (or "aba")

Input: s = "cbbd"
Output: "bb"
```

---

## 两种解法 / Two Approaches

### 方法一：中心扩展法 O(n²) 时间 O(1) 空间 ✅ 推荐

**思路**：每个字符（或相邻两字符）都可以是回文的中心，向外扩展。

```python
def longestPalindrome(s: str) -> str:
    res = ""
    res_len = 0

    for i in range(len(s)):
        # Odd length palindromes (single char center)
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if (r - l + 1) > res_len:
                res = s[l:r+1]
                res_len = r - l + 1
            l -= 1
            r += 1

        # Even length palindromes (two char center)
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if (r - l + 1) > res_len:
                res = s[l:r+1]
                res_len = r - l + 1
            l -= 1
            r += 1

    return res
```

**Trace for "babad":**
```
i=0 'b': odd → "b"; even l=0,r=1 'b'≠'a' stop
i=1 'a': odd → expand: l=0,r=2 'b'=='b' → "bab" (len 3)
i=2 'b': odd → expand: l=1,r=3 'a'=='a' → "aba" (also len 3, no update since equal)
...
Result: "bab"
```

### 方法二：DP 表格法 O(n²) 时间 O(n²) 空间

```python
def longestPalindrome_dp(s: str) -> str:
    n = len(s)
    # dp[i][j] = True if s[i..j] is palindrome
    dp = [[False] * n for _ in range(n)]
    
    res = s[0]
    
    # Every single char is a palindrome
    for i in range(n):
        dp[i][i] = True
    
    # Fill by length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 2:
                dp[i][j] = (s[i] == s[j])
            else:
                dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]
            
            if dp[i][j] and length > len(res):
                res = s[i:j+1]
    
    return res
```

**与模版的关系：** `dp[i][j]` 的转移依赖 `dp[i+1][j-1]`，这是"收缩"的子问题，而不是线性的前几个。DP 的核心不变：**定义子问题 + 找转移方程**。

---

## 复杂度 / Complexity
- 中心扩展：Time **O(n²)** | Space **O(1)** ← 首选
- DP 表格：Time **O(n²)** | Space **O(n²)**
- （有 Manacher's Algorithm 可达 O(n)，但面试基本不考）

---

## 举一反三 / Block Connection

| 题目 | 模式变化 |
|------|---------|
| #647 Palindromic Substrings (下一题!) | 计数而非找最长 → 中心扩展同样适用 |
| #516 Longest Palindromic Subsequence | 子序列 vs 子串，状态转移不同 |
| #5 (今天) | 子串，中心扩展最优 |

---

## 📝 Quiz
```json
{"question":"What is the time and space complexity of the expand-around-center approach for Longest Palindromic Substring?","options":["O(n) time, O(1) space","O(n²) time, O(1) space","O(n²) time, O(n²) space","O(n log n) time, O(n) space"],"correct_index":1}
```

---

## 📚 References
- https://leetcode.com/problems/longest-palindromic-substring/
- https://neetcode.io/problems/longest-palindromic-substring
- https://en.wikipedia.org/wiki/Longest_palindromic_substring

## 🧒 ELI5
找最长回文子串就像找镜子里的字：从每个字母出发，向两边扩展，只要两边相等就继续，记录最长的那个。
It's like standing in the middle and checking if the letters on both sides match — keep going as long as they do, and track the longest mirror you found.
