# 💻 算法 / Algorithms — Day 117: Edit Distance (Medium) — #72

🧩 **二维动态规划模式 (7/11)** — building on the 2-D DP template from earlier in this block

---

## #72 Edit Distance — 编辑距离

🔗 https://leetcode.com/problems/edit-distance/
🟡 Medium
📹 https://www.neetcode.io/problems/edit-distance

---

### 现实类比 / Real-World Analogy

想象你在做**拼写检查器**。用户输入 "horse"，正确词是 "ros"。
你需要计算最少几步操作（插入、删除、替换）把一个词变成另一个词。
这就是编辑距离，Git diff、DNA 序列比对、搜索纠错都用这个。

*Imagine building a spell checker: user typed "horse", correct is "ros". How many insert/delete/replace operations to transform one to the other? That's edit distance — used in Git diff, DNA alignment, search autocomplete.*

---

### 问题定义

```
Input: word1 = "horse", word2 = "ros"
Output: 3

Explanation:
horse → rorse (replace h→r)
rorse → rose  (delete r)
rose  → ros   (delete e)
```

操作代价: insert=1, delete=1, replace=1

---

### 映射到2-D DP模板

```python
# Template:
# dp = [[0] * (m+1) for _ in range(n+1)]
# for i in range(1, n+1):
#     for j in range(1, m+1):
#         dp[i][j] = TRANSITION(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

# For Edit Distance:
# dp[i][j] = min edit distance between word1[:i] and word2[:j]
```

**State:** `dp[i][j]` = minimum operations to convert `word1[:i]` → `word2[:j]`

**Base cases:**
- `dp[0][j] = j` (insert j chars from empty string)
- `dp[i][0] = i` (delete i chars to reach empty string)

**Transition (这就是关键):**
```
if word1[i-1] == word2[j-1]:
    dp[i][j] = dp[i-1][j-1]          # 字符相同，不需要操作
else:
    dp[i][j] = 1 + min(
        dp[i-1][j],    # delete from word1
        dp[i][j-1],    # insert into word1
        dp[i-1][j-1]   # replace
    )
```

---

### 完整解法 + 手动追踪

```python
def minDistance(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    
    # Build dp table with base cases
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base cases: empty string transformations
    for i in range(n + 1):
        dp[i][0] = i  # delete all chars from word1
    for j in range(m + 1):
        dp[0][j] = j  # insert all chars from word2
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # free diagonal move
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # delete
                    dp[i][j-1],    # insert
                    dp[i-1][j-1]   # replace
                )
    
    return dp[n][m]
```

**追踪 "horse" → "ros":**
```
    ""  r  o  s
""   0  1  2  3
h    1  1  2  3
o    2  2  1  2
r    3  2  2  2
s    4  3  3  2
e    5  4  4  3   ← answer: 3
```

画出这个表格，每个格子只看三个方向（上、左、左上），立刻就懂转移规律。

**Complexity:** Time O(n×m), Space O(n×m) → can optimize to O(m) with rolling array

---

### 空间优化 (Space O(m))

```python
def minDistance(word1: str, word2: str) -> int:
    m = len(word2)
    prev = list(range(m + 1))  # prev row
    
    for i, c1 in enumerate(word1, 1):
        curr = [i] + [0] * m
        for j, c2 in enumerate(word2, 1):
            if c1 == c2:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
        prev = curr
    
    return prev[m]
```

---

### 举一反三 — 本 Block 的其他2-D DP

| 题目 | dp[i][j] 含义 | 转移特点 |
|------|---------------|----------|
| #1143 LCS | 前i个和前j个的最长公共子序列 | 相同char时+1 |
| **#72 Edit Distance** | word1[:i]→word2[:j]的最少操作 | 3向min |
| #97 Interleaving String | s1[:i]+s2[:j]能否构成s3[:i+j] | 布尔OR |
| #115 Distinct Subsequences | s[:i]中有几个t[:j]的子序列 | 叠加计数 |

**通用技巧:** 所有字符串匹配类2-D DP，先在纸上画一个3×3的小表格手动填，转移方程一眼就出来。

---

### 📚 References
- https://leetcode.com/problems/edit-distance/ — Problem statement
- https://www.neetcode.io/problems/edit-distance — NeetCode video walkthrough
- https://en.wikipedia.org/wiki/Levenshtein_distance — Levenshtein distance (history and applications)

### 🧒 ELI5
想象你在玩文字拼图游戏，规则是每次只能做三件事：加一个字母、删一个字母、换一个字母。
DP 就是: 先解决小问题（空字符串变成小单词），然后把答案存在表格里，
用已有的答案推出新的答案，不用从头重新算。

---

**Quiz:**
```json
{"question":"Edit Distance的空间复杂度优化后是?","options":["O(n*m)","O(n+m)","O(m)","O(1)"],"correct_index":2}
```
