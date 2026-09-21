# 💻 算法 / Algorithms — Day 134

🧩 **一维动态规划 (7/12)** — building on the template from Day 126

> #91 Decode Ways | 🟡 Medium | 1-D Dynamic Programming
> 🔗 https://leetcode.com/problems/decode-ways/
> 📹 https://neetcode.io/problems/decode-ways

---

## 现实类比 / Real-World Analogy

想象你收到了一封摩尔斯电码电报，数字串 `"226"` 可以被解读为：
- `2-2-6` → B-B-F
- `22-6` → V-F
- `2-26` → B-Z

总共 3 种方式。**解码方案数** 正是这道题的核心。

You receive a Morse-code-like telegram. `"226"` could mean "BBF", "VF", or "BZ" — 3 ways. Decode Ways asks: how many valid decodings exist?

---

## 题目 / Problem

给定只含数字的字符串 `s`，字母 A-Z 编码为 1-26。返回解码方案总数。
Given digit string `s`, letters A–Z encode as 1–26. Return total number of decodings.

```
Input: s = "226"      Output: 3
Input: s = "06"       Output: 0  # "06" invalid, '0' has no mapping
Input: s = "11106"    Output: 2
```

---

## 模板映射 / Map to Pattern Template

```python
# 一维DP模版回顾:
# dp = [0] * (n + 1)
# dp[0] = BASE_CASE
# for i in range(1, n+1):
#     dp[i] = TRANSITION(dp[i-1], dp[i-2], ...)
# return dp[n]

# Decode Ways 映射:
# dp[i] = number of ways to decode s[:i]
# BASE: dp[0] = 1 (empty string → 1 way), dp[1] = 0 if s[0]=='0' else 1
# TRANSITION:
#   - single digit valid (s[i-1] != '0')       → dp[i] += dp[i-1]
#   - two digits valid (10 <= int(s[i-2:i]) <= 26) → dp[i] += dp[i-2]
```

**与模板的区别 / What's different from template:**
- 两个来源：单字符 + 双字符（类似 House Robber 的两个选择，但这里是**加法**而非 max）
- '0' 是陷阱：s[i]='0' 时单字符无效；s[i-1]='0' 时双字符无效

---

## 完整解法 / Full Solution

```python
def numDecodings(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)
    
    dp[0] = 1          # empty prefix → 1 way (base case)
    dp[1] = 0 if s[0] == '0' else 1  # first char
    
    for i in range(2, n + 1):
        one = int(s[i-1])        # current single digit
        two = int(s[i-2:i])      # current two-digit number
        
        # Single digit valid: 1–9
        if one != 0:
            dp[i] += dp[i-1]
        
        # Two digits valid: 10–26
        if 10 <= two <= 26:
            dp[i] += dp[i-2]
    
    return dp[n]
```

## 执行追踪 / Trace: s = "226"

```
i=0: dp[0] = 1
i=1: s[0]='2' ≠ '0' → dp[1] = 1
i=2: one=2, two=22
     one≠0 → dp[2] += dp[1] = 1
     10≤22≤26 → dp[2] += dp[0] = 1
     dp[2] = 2
i=3: one=6, two=26
     one≠0 → dp[3] += dp[2] = 2
     10≤26≤26 → dp[3] += dp[1] = 1
     dp[3] = 3  ✓
```

## 空间优化 / Space Optimization O(1)

```python
def numDecodings(s: str) -> int:
    prev2, prev1 = 1, 0 if s[0] == '0' else 1
    
    for i in range(2, len(s) + 1):
        curr = 0
        if s[i-1] != '0':
            curr += prev1
        if 10 <= int(s[i-2:i]) <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr
    
    return prev1
```

**复杂度 / Complexity:** Time O(n) | Space O(1)

---

## 举一反三 / Connect to Block

| 题目 | 与本题关系 |
|------|-----------|
| #70 Climbing Stairs | 每步可走1或2级 → 同样 dp[i] = dp[i-1] + dp[i-2] |
| #198 House Robber | 选/不选 + 两个来源，但用 max 而非 sum |
| #5 Palindromic Substring | dp[i] 来自之前状态但二维，更复杂 |
| #322 Coin Change (下一块) | 从计数变成最小值，转移函数变 min |

**关键洞察 / Key Insight:** `dp[i] = dp[i-1] + dp[i-2]` 在计数问题中很常见，但每道题的**有效性条件**不同。Decode Ways 的核心难点是 0 的处理。

---

## 📚 References
- https://leetcode.com/problems/decode-ways/
- https://neetcode.io/problems/decode-ways
- https://en.wikipedia.org/wiki/Dynamic_programming

## 🧒 ELI5
就像切蛋糕：你可以每次切一片（一个数字），也可以切两片（两个数字）。但有些切法是无效的（数字超过26或是0开头）。DP 帮你数出所有有效的切法数量。

Like slicing a cake: each cut covers one or two digits, but some slices are invalid (>26 or leading zero). DP counts all valid slicing combos.
