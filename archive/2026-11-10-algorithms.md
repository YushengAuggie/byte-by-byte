# #329 Longest Increasing Path in a Matrix — 2-D DP + Memoization

> Day 152 | Algorithms | 2026-11-10 | Hard 🔴

---

💻 **算法 / Algorithms** *(4 min)*

🧩 **二维动态规划模式 (8/11)** — building on the template from Days 101-151

---

### 今天的变奏 / Today's Variation

标准 2-D DP 从左上到右下填表。今天的问题打破了这一规律：**路径方向不固定**，任意上下左右移动，只要值严格递增。这迫使我们使用 **DFS + 记忆化（自顶向下 DP）** 代替自底向上填表。

*Standard 2-D DP fills a table top-left to bottom-right. Today's problem breaks that: direction is unconstrained — move any of 4 directions as long as values strictly increase. This forces **DFS + Memoization (top-down DP)** instead of bottom-up.*

---

### 🔗 Links

- LeetCode: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/ 🔴 Hard
- NeetCode: https://neetcode.io/problems/longest-increasing-path-in-a-matrix

---

### 真实类比 / Real-World Analogy

想象地形图上的水流：水只往更低的地方流，找出最长的水流路径。每个格子就是一个海拔高度。

*Imagine water flow on a terrain map: water only flows downhill. Find the longest path water can travel. Each cell is an elevation.*

---

### 模板映射 / Map to Pattern Template

```
标准 Bottom-Up 模板:         今天的变奏:
──────────────────────       ──────────────────────────
dp = 2D table               memo = 2D table (lazy)
Fill left→right, top→down   Fill on-demand via DFS
dp[i][j] = f(neighbors)     dfs(r, c) = 1 + max(dfs(nr, nc))
                                         for valid neighbors
```

**关键区别 / Key Difference:**
- 标准 DP: 明确的状态转移顺序（拓扑顺序已知）
- 今天: 拓扑顺序**不明确** → 用 DFS 自动探索，memo 避免重复计算

---

### Python 解法 / Solution

```python
from functools import lru_cache
from typing import List

def longestIncreasingPath(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    @lru_cache(maxsize=None)
    def dfs(r: int, c: int) -> int:
        # Returns the longest increasing path starting at (r, c)
        best = 1  # path of just this cell
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and matrix[nr][nc] > matrix[r][c]):
                best = max(best, 1 + dfs(nr, nc))
        return best
    
    # Try every cell as a starting point
    return max(dfs(r, c) for r in range(rows) for c in range(cols))

# --- Trace Example ---
# matrix = [
#   [9, 9, 4],
#   [6, 6, 8],
#   [2, 1, 1]
# ]
# dfs(2,1): neighbors where val > 1 → (2,0)=2 and (1,1)=6
#   dfs(2,0): neighbors where val > 2 → (1,0)=6
#     dfs(1,0): neighbors where val > 6 → (0,0)=9, (0,1)=9
#       dfs(0,0)=1, dfs(0,1)=1  → dfs(1,0)=2
#     dfs(2,0) = 1 + dfs(1,0) = 3
#   dfs(1,1): neighbors where val > 6 → (1,2)=8
#     dfs(1,2): neighbors where val > 8 → none → dfs(1,2)=1
#     dfs(1,1) = 2
#   dfs(2,1) = 1 + max(dfs(2,0)=3, dfs(1,1)=2) = 4  ← longest
# Answer: 4, path: 1→2→6→9 starting at (2,1)
```

**复杂度 / Complexity:**
- Time: O(m × n) — 每个格子只计算一次
- Space: O(m × n) — memo table + recursion stack

---

### 举一反三 / Connect the Pattern Block

| 问题 | 变奏点 |
|------|--------|
| **#62 Unique Paths** | Bottom-up, 1 direction only |
| **#1143 LCS** | 2 strings, `dp[i][j]` depends on `dp[i-1][j-1]` |
| **#72 Edit Distance** | 3 choices at each cell |
| **今天 #329** | 4 directions, DFS-first, memo |
| **下一题 #115 Distinct Subsequences** | 1D subproblem extended to 2D |

---

### 🧒 ELI5

你在爬山，但只能往更高的地方走。从每个起点出发，找到最长的爬山路。已经算过的起点，用小本本记着，下次直接查，不用重新爬。

*You're hiking but can only go uphill. Start from every point, find the longest uphill path. Write down results in a notebook so you never hike the same path twice.*

---

### 📚 References

- https://leetcode.com/problems/longest-increasing-path-in-a-matrix/ — Problem statement
- https://neetcode.io/problems/longest-increasing-path-in-a-matrix — Video walkthrough
- https://cp-algorithms.com/dynamic_programming/dp-on-directed-acyclic-graphs.html — DP on DAGs
