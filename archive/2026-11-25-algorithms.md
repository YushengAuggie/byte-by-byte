# Day 157 — Algorithms: Regular Expression Matching
## LeetCode #10 · Hard · 2-D Dynamic Programming (11/11)

---

💻 **算法 / Algorithms** — #10 Regular Expression Matching 🔴 Hard

🧩 **二维动态规划模式 (11/11)** — 收官之作，本模式最难题

[🔗 LeetCode #10](https://leetcode.com/problems/regular-expression-matching/) | [📹 NeetCode](https://neetcode.io/problems/regular-expression-matching)

---

## 回顾本模式 / Pattern Recap (11 problems done!)

从 Day 1 的 Unique Paths 到今天的 Regex Matching，你已完成整个 2D DP 模式：

```
#62  Unique Paths         → 基础网格路径
#1143 LCS               → 字符串对齐
#309 Stock Cooldown      → 状态机DP
#518 Coin Change II      → 背包DP
#494 Target Sum         → 计数DP
#97  Interleaving String → 三字符串对齐
#72  Edit Distance       → 增删改操作
#329 Longest Inc. Path   → 记忆化DFS（矩阵）
#115 Distinct Subseq    → 子序列计数
#312 Burst Balloons     → 区间DP反向思维
#10  Regex Matching     → 状态机+通配符 ← 今天
```

---

## 真实世界类比 / Real-World Analogy

想象你在写一个**简化版 grep**：
- `.` 匹配任意单个字符（像通配符"？"）
- `*` 表示前面那个字符可以出现 0 次或多次

问：`s = "aab"`, `p = "c*a*b"` 能匹配吗？
答：能！`c*` 匹配 0 个 c，`a*` 匹配 2 个 a，`b` 匹配 b ✅

---

## 映射到模板 / Mapping to Template

```python
# 通用模板
dp = [[False] * (m+1) for _ in range(n+1)]
# 今天变形：字符串 s(长度n) vs 模式 p(长度m)
# dp[i][j] = s[:i] 能否被 p[:j] 匹配
```

**状态定义：** `dp[i][j]` = `s[:i]` 是否匹配 `p[:j]`

**转移方程（三种情况）：**
```
Case 1: p[j-1] == s[i-1] 或 p[j-1] == '.'
  → dp[i][j] = dp[i-1][j-1]  （两边都消耗一个字符）

Case 2: p[j-1] == '*'
  → 子情况 2a: 用 0 次前缀字符
      dp[i][j] = dp[i][j-2]   （跳过 x* 这个pattern）
  → 子情况 2b: 用 1+ 次（前缀字符能匹配s[i-1]）
      dp[i][j] = dp[i-1][j]   （消耗一个s字符，pattern不动）
      条件：p[j-2] == s[i-1] 或 p[j-2] == '.'

Case 3: 其他
  → dp[i][j] = False
```

---

## 完整解法 + 追踪 / Full Solution with Trace

```python
def isMatch(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    
    # dp[i][j]: s[:i] matches p[:j]
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    
    # Base case: empty s matches empty p
    dp[0][0] = True
    
    # Base case: empty s can match patterns like a*, a*b*, a*b*c*
    # e.g., dp[0][2] = True if p[1] == '*' (zero occurrences of p[0])
    for j in range(2, m + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    # Fill the table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == '*':
                # Zero occurrences of p[j-2]
                dp[i][j] = dp[i][j - 2]
                # One or more occurrences (if previous char matches)
                if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                # Direct match or wildcard
                dp[i][j] = dp[i - 1][j - 1]
            # else: dp[i][j] remains False
    
    return dp[n][m]
```

**手动追踪 s="aab", p="c*a*b":**
```
    ""  c   *   a   *   b
""  T   F   T   F   T   F
a   F   F   F   T   T   F
a   F   F   F   F   T   F
b   F   F   F   F   F   T  ← 答案！
```

**追踪关键步：**
- `dp[0][2]`: p="c*" → `dp[0][0]` = True ✅ (0个c)
- `dp[0][4]`: p="c*a*" → `dp[0][2]` = True ✅ (0个a)
- `dp[1][4]`: s="a", p="c*a*" → p[3]='*', p[2]='a'==s[0]='a' → `dp[0][4]` = True ✅
- `dp[3][5]`: s="aab", p="c*a*b" → p[4]='b'==s[2]='b' → `dp[2][4]` = True ✅

---

## 复杂度 / Complexity
- **时间**: O(n × m) — 填 n×m 的表格
- **空间**: O(n × m) — 可优化到 O(m)（只需保留上一行）

---

## 举一反三 / Compare Within Pattern Block

这道题综合了本 block 中多道题的思路：

| 技巧 | 来源题目 | 本题应用 |
|------|----------|----------|
| 空字符串 base case | #72 Edit Distance | dp[0][j] 初始化处理 `x*` |
| 状态机转移 | #309 Cooldown | `*` 分两种子状态 |
| 计数/布尔DP | #1143 LCS | 同样的 dp[i-1][j-1] 对角线转移 |
| 跳过选项 | #518 Coin Change II | `dp[i][j-2]`（0次使用）|

**🎯 2D DP 模式终极口诀：**
> "画表格，定含义，看依赖，找转移，别忘边界"
> Draw table → Define meaning → Check dependencies → Find transition → Don't forget base cases

---

## 📝 Quiz
```json
{"question":"s='aa', p='a*'. What does dp[2][2] depend on?","options":["dp[1][2] only","dp[2][0] only","Both dp[2][0] and dp[1][2]","dp[1][1] only"],"correct_index":2}
```

答案解析：`p[1]='*'`，所以 `dp[2][2] = dp[2][0]`（0次使用）OR（`p[0]='a'==s[1]='a'`）`dp[1][2]`（继续匹配）

---

## 📚 References
- [LeetCode #10 Official Solution](https://leetcode.com/problems/regular-expression-matching/editorial/)
- [NeetCode Video Explanation](https://www.youtube.com/watch?v=HAA8mgxlov8)
- [Regex matching state machine — CS Theory](https://en.wikipedia.org/wiki/Regular_expression#Formal_language_theory)

## 🧒 ELI5
想象你在玩一个"猜猜我是谁"的游戏。模式是你的线索卡，字符串是答案。`.` 是个魔法卡，可以匹配任何字母。`a*` 是个"我可以带 0 到无数个 a 朋友"的卡。DP 表格就像在纸上记录每一步"这个线索和这个答案能配上吗"，一格一格填出来，最终右下角告诉你答案。
