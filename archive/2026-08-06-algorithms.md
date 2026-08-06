# 💻 算法 / Algorithms — Day 109
## #130 Surrounded Regions (Medium) — 图遍历模式 (7/13)

🧩 **图遍历模式 (7/13)** — building on the BFS/DFS template from Day 101

---

### 🔗 Links
- 🔗 [LeetCode #130](https://leetcode.com/problems/surrounded-regions/) 🟡 Medium
- 📹 [NeetCode Video](https://neetcode.io/problems/surrounded-regions)

---

### 🌍 真实类比 / Real-World Analogy

想象围棋棋盘：被黑子完全包围的白子会被"提子"（消去）。但如果白子延伸到棋盘边缘，就不能被提。这道题就是这个逻辑——被 `X` 完全包围的 `O` 变成 `X`，但边缘连通的 `O` 保留。

*Go board logic: surrounded white stones get captured. But stones connected to the edge are safe. Here: surrounded `O`s → `X`, edge-connected `O`s stay.*

---

### 🧩 模版变形 / Template Variation

```
标准 BFS/DFS 模版用途：  从源节点探索所有可达节点
本题变形：                反向思考——不找"被围的"，而是找"安全的"

关键洞察：
  WRONG approach: Find surrounded O's (hard to determine)
  RIGHT approach: Find SAFE O's (easy — they touch border)
                  Mark safe O's → flip rest

这是模版的"反向用法"：
  Day 101 (Number of Islands): 找连通块
  Day 102 (Max Area of Island): 测连通块大小  
  Day 103 (Clone Graph): 复制连通结构
  Day 104 (Walls and Gates): BFS 多源最短路
  Day 107 (Rotting Oranges): BFS 多源传播
  Day 108 (Pacific Atlantic): 反向 DFS 找可达
  Day 109 (Surrounded Regions): 反向 DFS 找安全 ← TODAY
```

---

### 💡 解题思路 / Approach

```
Step 1: 从四条边出发，DFS/BFS 标记所有与边缘 O 连通的格子
        Start from border cells, mark all O's reachable from border

Step 2: 遍历整个棋盘：
        - 普通 O (未标记) → 变 X (surrounded)
        - 标记过的 O → 恢复 O (safe)
        - X 保持不变

Board:
X X X X        X X X X
X O O X   →   X X X X
X X O X        X X X X
X O X X        X O X X  ← border-connected O stays
```

---

### 🐍 Python Solution with Trace

```python
def solve(board: list[list[str]]) -> None:
    if not board or not board[0]:
        return
    
    ROWS, COLS = len(board), len(board[0])
    
    def dfs(r, c):
        # Mark border-connected O's as safe ('S')
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return
        if board[r][c] != 'O':
            return
        board[r][c] = 'S'  # temporary safe marker
        dfs(r+1, c); dfs(r-1, c)
        dfs(r, c+1); dfs(r, c-1)
    
    # Step 1: Mark border-connected O's
    for r in range(ROWS):
        dfs(r, 0)          # left border
        dfs(r, COLS-1)     # right border
    for c in range(COLS):
        dfs(0, c)          # top border
        dfs(ROWS-1, c)     # bottom border
    
    # Step 2: Flip
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 'O':
                board[r][c] = 'X'   # surrounded → flip
            elif board[r][c] == 'S':
                board[r][c] = 'O'   # safe → restore

# Trace on example:
# Initial:  X X X X        After DFS:  X X X X
#           X O O X                    X O O X  (interior O's)
#           X X O X                    X X O X
#           X O X X                    X S X X  (border O marked S)
# Final:    X X X X
#           X X X X
#           X X X X
#           X O X X  ✅
```

**Complexity:** Time O(M×N), Space O(M×N) stack | 时间 O(MN)，空间 O(MN) 递归栈

---

### 🔄 举一反三 / Pattern Block Connections

| 题目 | 关键变形 |
|------|---------|
| #200 Number of Islands | 直接 DFS 数连通块 |
| #417 Pacific Atlantic | 双向反向 DFS（同本题反向思路）|
| **#130 Surrounded Regions** | 反向 DFS + 临时标记 |
| #207 Course Schedule (next) | DFS 检测环（有向图）|

本题与 Pacific Atlantic Water Flow (Day 108) 是**同一反向思维**：与其问"哪些格子满足条件"，不如从结果出发反推。

*Same reverse-DFS insight as Pacific Atlantic: instead of asking which cells qualify, start from the answer (border) and work inward.*

---

### 📚 References
- https://leetcode.com/problems/surrounded-regions/
- https://neetcode.io/problems/surrounded-regions
- https://www.youtube.com/watch?v=9z2BunfoZ5Y

### 🧒 ELI5
围棋里，被对手棋子完全包围的棋子会被吃掉。但如果棋子连到了棋盘边缘，就安全了。先找到所有安全的棋子，剩下的就全部吃掉。
*In Go: if your stones are surrounded, they get captured. But stones touching the edge are safe. Find safe stones first, capture the rest.*
