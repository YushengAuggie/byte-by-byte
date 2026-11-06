# 💻 算法 / Algorithms — Day 149
## #97 Interleaving String (Medium) — 2-D Dynamic Programming (6/11)

🧩 **二维DP模式 (6/11)** — 建立在 Day 143 (Unique Paths)、Day 144 (LCS)、Day 146 (Cooldown)、Day 147 (Coin Change II)、Day 148 (Target Sum) 的模板之上

---

🔗 [LeetCode #97](https://leetcode.com/problems/interleaving-string/) 🟡 Medium | 📹 [NeetCode](https://neetcode.io/problems/interleaving-string)

---

## 问题 / Problem

给你三个字符串 `s1`、`s2`、`s3`，判断 `s3` 是否是 `s1` 和 `s2` 的**交错字符串**。即：`s3` 可以由 `s1` 和 `s2` 的字符交替拼成，且保持各自的相对顺序。

Given strings s1, s2, s3, determine if s3 is formed by an interleaving of s1 and s2.

```
s1 = "aab", s2 = "axy", s3 = "aaxaby"

s3: a  a  x  a  b  y
    ↑s1 ↑s2 ↑s2 ↑s1 ↑s1 ↑s2  ✅
```

---

## 真实类比 / Real-World Analogy

两条流水线同时生产零件，装箱时可以任意交替从两条线取件，但每条线自己的顺序不能乱。问：能不能组成某个特定顺序的成品？这就是"交错合并"。

---

## 映射到模板 / Map to Pattern

```python
# 二维DP模板：dp[i][j] = 用了 s1[:i] 和 s2[:j] 能否组成 s3[:i+j]
dp = [[False] * (len(s2)+1) for _ in range(len(s1)+1)]

# 转移方程：
# dp[i][j] = (dp[i-1][j] and s1[i-1]==s3[i+j-1])  ← 取 s1 的第 i 个字符
#           OR (dp[i][j-1] and s2[j-1]==s3[i+j-1]) ← 取 s2 的第 j 个字符
```

**与之前问题的区别**：
- Unique Paths：转移只看方向（右/下），不看字符值
- LCS：转移看两串字符是否相等
- **Interleaving**：转移看当前字符是否匹配 s3 的下一个位置 — 新增字符匹配维度

---

## 完整解法 / Solution

```python
def isInterleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    
    # Edge case: total length must match
    if m + n != len(s3):
        return False
    
    # dp[i][j] = can s1[:i] + s2[:j] form s3[:i+j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True  # empty + empty = empty ✅
    
    # Base case: only s1, no s2
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]
    
    # Base case: only s2, no s1
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            k = i + j - 1  # index into s3
            # Take from s1 OR take from s2
            dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[k]) or \
                       (dp[i][j-1] and s2[j-1] == s3[k])
    
    return dp[m][n]
```

---

## 手动追踪 / Manual Trace

```
s1="aab", s2="axy", s3="aaxaby"

    ""  a   x   y
""  T   T   F   F
a   T   T   T   F
a   T   F   T   F  (← dp[2][2]=T: s1[:2]+s2[:2] 交错 = s3[:4]="aaxa" ✅)
b   F   F   T   T  ← dp[3][3] = True ✅
```

---

## 空间优化 / Space Optimization

```python
# 可以压缩到 O(n) 空间，只保留一行
dp = [False] * (n + 1)
dp[0] = True
for j in range(1, n + 1):
    dp[j] = dp[j-1] and s2[j-1] == s3[j-1]

for i in range(1, m + 1):
    dp[0] = dp[0] and s1[i-1] == s3[i-1]
    for j in range(1, n + 1):
        k = i + j - 1
        dp[j] = (dp[j] and s1[i-1] == s3[k]) or \
                (dp[j-1] and s2[j-1] == s3[k])

return dp[n]
```

**复杂度 / Complexity**: Time O(m×n), Space O(n)

---

## 举一反三 / Pattern Variations

| 问题 | DP维度 | 转移条件 |
|------|--------|---------|
| Unique Paths | 2D | 无条件 (方向) |
| LCS | 2D | 字符相等 → 对角线 |
| Edit Distance (下一题!) | 2D | 相等/替换/插入/删除 |
| **Interleaving** | 2D | 字符匹配 s3 + OR 逻辑 |

**关键洞察**：二维DP的核心是"两个序列的双指针状态"，每一格 `dp[i][j]` 代表消耗 s1 的前 i 个 + s2 的前 j 个的某种结论。

---

## 📚 References

- https://leetcode.com/problems/interleaving-string/
- https://neetcode.io/problems/interleaving-string
- https://cp-algorithms.com/dynamic_programming/intro-to-dp.html

## 🧒 ELI5

你有两盒乐高，红色和蓝色。规则：每次只能从一盒取一块，但每盒的顺序不能打乱。问：能不能拼出一个指定颜色顺序的作品？DP表格的每个格子记录"用了红盒前i块、蓝盒前j块，能不能拼到作品的第i+j个位置"。

---

## 🎯 Quiz

```json
{"question":"What is the time complexity of the 2D DP solution for Interleaving String?","options":["O(m+n)","O(m*n)","O(m*n*k) where k=len(s3)","O(2^(m+n))"],"correct_index":1}
```
