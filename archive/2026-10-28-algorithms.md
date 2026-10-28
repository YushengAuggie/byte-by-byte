💻 **算法 / Algorithms** — #1143 Longest Common Subsequence (🟡 Medium) — 2-D Dynamic Programming

🧩 **二维动态规划模式 (2/11)** — building on the template from Day 143 (#62 Unique Paths)

🔗 LeetCode: https://leetcode.com/problems/longest-common-subsequence/
📹 NeetCode: https://www.youtube.com/watch?v=Ua0GhsJSlWM

---

### 从 Unique Paths 到 LCS — 模板的变化 / From Unique Paths to LCS

昨天 Unique Paths 的 `dp[i][j]` 代表"到达格子 (i,j) 的路径数"，转移是 **纯加法**：`dp[i][j] = dp[i-1][j] + dp[i][j-1]`。

今天 LCS 的 `dp[i][j]` 代表 "`text1[:i]` 和 `text2[:j]` 的最长公共子序列长度"。核心变化：**转移取决于两个字符串当前字符是否相等**。

Yesterday: pure additive transition. Today: **conditional transition** — the recurrence branches on whether `text1[i-1] == text2[j-1]`.

---

### 真实场景 / Real-World Analogy

**Git diff / merge** 底层就是 LCS 变体。`diff a.txt b.txt` 要找出两份文件最大重合的行序列，剩下的就是增删。字符串比对、DNA 测序、拼写检查、subtitle 对齐，全是 LCS 家族。

Git `diff` is literally LCS over lines. DNA alignment (BLAST), spell-check, subtitle sync — all LCS-based.

---

### 问题 / Problem

给两个字符串 `text1`, `text2`，返回它们最长公共**子序列**的长度（子序列不要求连续，但保持相对顺序）。

Example: `text1 = "abcde"`, `text2 = "ace"` → `3` (subsequence `"ace"`).

---

### 映射到模板 / Map to Template

```python
# Template reminder:
# dp = [[0] * (m+1) for _ in range(n+1)]
# for i in 1..n: for j in 1..m: dp[i][j] = TRANSITION(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

def longestCommonSubsequence(text1: str, text2: str) -> int:
    n, m = len(text1), len(text2)
    # dp[i][j] = LCS length of text1[:i] and text2[:j]
    # Row 0 and col 0 are the "empty prefix" sentinel — stays 0.
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if text1[i - 1] == text2[j - 1]:
                # Match: extend the LCS of the shorter prefixes by 1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # No match: skip one char from either string, take the better
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]
```

---

### 手动追踪 / Trace: `"abcde"` vs `"ace"`

```
         ""  a   c   e
      ""  0  0   0   0
      a   0  1   1   1
      b   0  1   1   1
      c   0  1   2   2
      d   0  1   2   2
      e   0  1   2  [3]
```

每格看 "左 / 上 / 左上+1(匹配时)"。右下角 **3** 就是答案。手动画一次表格，所有二维 DP 都能秒懂。

---

### 复杂度 / Complexity

- Time: **O(n·m)** — fill entire table
- Space: **O(n·m)** → optimizable to **O(min(n, m))** using 2 rolling rows (or 1 row + prev_diag var)

```python
# Space-optimized O(m)
def lcs(text1, text2):
    if len(text1) < len(text2): text1, text2 = text2, text1
    prev = [0] * (len(text2) + 1)
    for c1 in text1:
        curr = [0] * (len(text2) + 1)
        for j, c2 in enumerate(text2, 1):
            curr[j] = prev[j-1] + 1 if c1 == c2 else max(prev[j], curr[j-1])
        prev = curr
    return prev[-1]
```

---

### 举一反三 / Pattern Siblings

| Problem | 变化 Variation |
|---|---|
| **#72 Edit Distance** (Sat deep dive) | 转移多了 insert/delete/replace 三选 min，而不是 2 选 max |
| **#115 Distinct Subsequences** | 从 "最长" 变 "有多少种"，`+1` 变 `+count` |
| **#97 Interleaving String** | `dp[i][j]` 代表布尔，转移是 OR |
| **#583 Delete Op for Two Strings** | 答案 = `n + m - 2*LCS` |

**核心洞察**：所有 "两个字符串的 DP" 都是 `dp[i][j]` 二维表 + "匹配 vs 不匹配" 分支，只是组合规则不同。

---

### 📚 References
- NeetCode walkthrough: https://neetcode.io/problems/longest-common-subsequence
- CLRS Ch. 15.4 (classic LCS proof): https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
- Python itertools / difflib (built-in LCS via `SequenceMatcher`): https://docs.python.org/3/library/difflib.html

### 🧒 ELI5
两串珠子，颜色一样的能连成一条项链但不能换顺序。你画一张格子：横着是第一串，竖着是第二串。遇到同颜色就从左上角 +1，否则看左边或上面谁大。右下角就是最长那条项链的长度。
