# 💻 算法 / Algorithms — Day 153
## #115 Distinct Subsequences [Hard] — 2-D Dynamic Programming (9/11)

🧩 **二维动态规划模式 (9/11)** — 延续 Day 149 (Interleaving String) 的模版

---

## 🔗 Links
- LeetCode: https://leetcode.com/problems/distinct-subsequences/ 🔴 Hard
- NeetCode: https://neetcode.io/problems/count-subsequences

---

## 现实类比 / Real-world Analogy

想象你在做文本搜索：给定一份长文档 `s` 和一个关键词 `t`，问关键词以**子序列**形式出现在文档里多少次（字符可以不连续，但顺序不变）。这就是 Distinct Subsequences 的核心——计算**路径数量**，而非判断是否存在。

---

## 问题定义

给定字符串 `s` 和 `t`，计算 `s` 的子序列中有多少个等于 `t`。

```
s = "rabbbit", t = "rabbit"
输出: 3
(三种方式选取 rabbit，对应三个不同的 'b' 被跳过)
```

---

## 映射到模版 / Map to Template

这是**计数型** 2D DP，不同于之前的：
- Day 141 Edit Distance → **最小代价**
- Day 148 Target Sum → **组合计数**（1D 背包）
- Day 149 Interleaving String → **可行性判断**

今天：`dp[i][j]` = s 的前 i 个字符中，t 的前 j 个字符作为子序列出现的次数。

**转移规律（画表格找）：**

```
     ""  r  a  b  b  i  t       ← t (j轴)
""    1  0  0  0  0  0  0
r     1  1  0  0  0  0  0
a     1  1  1  0  0  0  0
b     1  1  1  1  0  0  0
b     1  1  1  2  1  0  0
b     1  1  1  3  3  0  0
i     1  1  1  3  3  3  0
t     1  1  1  3  3  3  3   ← 答案!
```

规律：
- `s[i] == t[j]`：既可以"用 s[i] 匹配 t[j]"(`dp[i-1][j-1]`)，也可以"跳过 s[i]"(`dp[i-1][j]`)
  → `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]`
- `s[i] != t[j]`：只能跳过 s[i]
  → `dp[i][j] = dp[i-1][j]`

---

## Python 解法 + 执行追踪

```python
def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    
    # dp[i][j] = count of t[:j] in s[:i] as subsequence
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base: empty t is a subsequence of any s prefix (1 way)
    for i in range(m + 1):
        dp[i][0] = 1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Always carry forward: skip s[i-1]
            dp[i][j] = dp[i-1][j]
            # If chars match, also add paths that USE s[i-1]
            if s[i-1] == t[j-1]:
                dp[i][j] += dp[i-1][j-1]
    
    return dp[m][n]

# Trace: s="rabbbit", t="rabbit"
# After filling: dp[7][6] = 3  ✓
```

**空间优化**（O(n) 滚动数组）：
```python
def num_distinct_optimized(s: str, t: str) -> int:
    n = len(t)
    dp = [0] * (n + 1)
    dp[0] = 1  # empty t base case
    
    for ch in s:
        # Traverse RIGHT TO LEFT to avoid using updated values
        for j in range(n, 0, -1):
            if ch == t[j-1]:
                dp[j] += dp[j-1]
    
    return dp[n]
```

**复杂度**：Time O(m×n)，Space O(m×n) → 优化后 O(n)

---

## 举一反三 / Pattern Connections

| 题目 | DP 类型 | 转移核心 |
|------|---------|----------|
| Edit Distance (#72) | 最小代价 | min(insert, delete, replace) |
| Interleaving String (#97) | 可行性 | OR 操作 |
| **Distinct Subsequences (#115)** | **计数** | **加法累积** |
| Burst Balloons (#312) ← 下一题 | 区间 DP | 区间分割 |

**关键区别**：当 DP 问"有多少种方式"时，转移用**加法**；问"能否"时用**OR**；问"最优"时用**min/max**。

---

## 📚 References
- https://leetcode.com/problems/distinct-subsequences/editorial/
- https://neetcode.io/solutions/distinct-subsequences
- https://cp-algorithms.com/dynamic_programming/subsequence_counting.html

## 🧒 ELI5
你有一堆字母积木 "rabbbit"，想从里面挑出 "rabbit" 的顺序排列。每次挑可以跳过一些积木，但顺序不能变。问一共有几种挑法。表格帮你数清楚每个位置"之前有多少种合法选法"，最后格子里的数字就是答案。
