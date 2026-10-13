💻 **算法 / Algorithms** — #139 Word Break (Medium) — 1-D Dynamic Programming

🧩 **一维动态规划 (10/12)** — building on the template from Day 128 (Climbing Stairs)

> 📊 NeetCode: 107/150 · Pattern progress: 10/12 in 1-D DP block
> 🔗 LeetCode: https://leetcode.com/problems/word-break/ 🟡 Medium
> 📹 NeetCode: https://neetcode.io/solutions/word-break

---

### 这题和模板的变化 / What's different from the template

前面 9 题 (#70, #198, #322, #152, …) 的 `dp[i]` 都是**数值**（步数、金额、乘积、方案数）。今天：

Previous 9 problems used `dp[i]` as a **number** (steps, amount, product, count). Today:

| 项 | 之前 | 今天 (#139) |
|---|---|---|
| `dp[i]` 的含义 | 到位置 i 的最优值 | **布尔**：前 i 个字符能否被切分 |
| 转移 | `dp[i] = min/max(dp[j] + cost)` | `dp[i] = any(dp[j] and s[j:i] in words)` |
| 子问题枚举 | 固定几个（i-1, i-2, i-coin） | **扫描所有切点 j < i** |

**核心升级：** `dp[i]` 可以是**任意类型**（bool, set, list），不止数字。能否切分 → bool。能切分成几种 → int。所有切分方案 → list（这就是 #140 Word Break II）。

---

### 现实类比 / Real-world analogy

你在读一段**没有空格的日文/中文**："applepenapple"。手里有词典 `{apple, pen}`。能不能从左到右**贪心地**找词？不行 — "aa**lan**da" 可能切成 "aa / lan / da" 或 "aal / an / da"，贪心会漏情况。所以要 DP：**"前 i 个字符能否切分" 只依赖于 "是否存在切点 j 使得前 j 个能切分 且 s[j:i] 是词"**。

---

### 问题 / Problem

Given `s` and a `wordDict`, return True if `s` can be segmented into a space-separated sequence of dictionary words.

```
s = "leetcode", wordDict = ["leet","code"] → True   ("leet code")
s = "applepenapple", wordDict = ["apple","pen"] → True
s = "catsandog", wordDict = ["cats","dog","sand","and","cat"] → False
```

### 映射到模板 / Map to template

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict)              # O(1) lookup
    max_len = max(map(len, wordDict))     # prune inner loop
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True                          # BASE CASE: empty prefix is "segmentable"

    for i in range(1, n + 1):
        # TRANSITION: try every split point j; only check j within max_len
        for j in range(max(0, i - max_len), i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break                     # one witness is enough
    return dp[n]
```

### Trace: `s = "leetcode"`, dict = {leet, code}

```
i=0: dp[0]=True (base)
i=1..3: no word matches s[0:1..3]       → dp=F
i=4: j=0, s[0:4]="leet" ∈ dict, dp[0]=T → dp[4]=True ✅
i=5..7: try all j; need dp[j]=T and s[j:i]∈dict → none
i=8: j=4, s[4:8]="code" ∈ dict, dp[4]=T → dp[8]=True ✅
return dp[8] = True
```

### Complexity

- Time: **O(n² · k)** where k = avg word length (for `s[j:i]` hash). With `max_len` prune → O(n · max_len · k).
- Space: **O(n)** for dp + O(W) for word set.
- 可以用 Trie 优化到 O(n²) 常数更小 — 见 #140.

---

### 举一反三 / Variations in the same block

| 问题 | dp[i] 含义 | 关键区别 |
|---|---|---|
| **#139 Word Break (今天)** | 能否切分 (bool) | 任意切点 j, 任意词 |
| #140 Word Break II | 所有切分方案 (list) | 要用 DFS + memo，不是纯 DP |
| #322 Coin Change | 最少硬币数 (int) | 固定硬币集 → 固定几个 j |
| #300 LIS | 最长递增子序列长度 | 内循环看 **所有 j < i**，但条件是 `nums[j] < nums[i]` |

**共同点：** 内层循环**扫描所有合法前缀 j < i**，不是固定 i-1、i-2。这是 "1-D DP 带全扫描" 的子类。LIS、Word Break、Perfect Squares (#279) 都属于这一类。

---

### 📚 References

- NeetCode Word Break: https://neetcode.io/solutions/word-break
- LeetCode editorial: https://leetcode.com/problems/word-break/editorial/
- CP-Algorithms — DP intro: https://cp-algorithms.com/dynamic_programming/intro-to-dp.html

### 🧒 ELI5

一长串没空格的字符，手里有词典。从前往后一步步问："到目前为止能切好吗？"— 只要存在一个"回头看"的位置，使**那里之前**切得好 **AND** 中间那段是词典里的词，就 OK。
