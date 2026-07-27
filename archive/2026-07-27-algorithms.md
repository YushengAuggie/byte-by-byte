# 算法 / Algorithms — Day 101
**#200 Number of Islands (Medium) · Graphs · Day 80/150**

---

## 💻 算法 / Algorithms — #200 Number of Islands 🟡 — Graphs

---

## 🧩 新模式 / New Pattern: 图遍历模式 (BFS/DFS)

📍 **This block:** 13 problems

**什么时候用 / When to use:** 连通性、最短路径、拓扑排序、岛屿问题  
When to use: connected components, shortest path, topological sort, grid/matrix traversal, islands

**识别信号 / Signals:** connected components, shortest path, topological sort, grid/matrix traversal, islands

**通用模版 / Template:**
```python
# BFS Template
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = {start}
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# DFS Template (Iterative)
def dfs(graph, start):
    stack = [start]
    visited = {start}
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

# DFS Template (Recursive)
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
```

**核心洞察 / Key Insight:** BFS = 最短路径（无权图），DFS = 连通性/路径探索。visited 集合防止死循环  
BFS = shortest path (unweighted), DFS = connectivity/path exploration. `visited` set prevents infinite loops.

---

### 🔗 Links
- [LeetCode #200](https://leetcode.com/problems/number-of-islands/) 🟡 Medium
- [NeetCode Video](https://neetcode.io/problems/count-islands)

---

### 现实类比 / Real-World Analogy

想象你有一张卫星地图，上面有陆地 `'1'` 和海洋 `'0'`。  
你需要数清楚有多少块独立的陆地（岛屿）。

这就像 **感染控制**：每次发现一个新病例（未访问的 `'1'`），就把该病例的所有相连感染区域标记为已处理，然后统计独立的爆发次数。

Imagine a satellite map with land `'1'` and ocean `'0'`.  
You need to count distinct landmasses. Think of it like **infection control**: each new unvisited `'1'` starts a new outbreak cluster — mark all connected cells and count clusters.

---

### 题目 → 套用模式 / Problem → Map to Template

```
grid:
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1

Answer: 3 islands
```

**映射到图遍历模版：**
- 节点 Node = grid cell `(row, col)`
- 邻居 Neighbor = 上下左右四个方向
- 访问标记 Visited = 修改 grid 为 `'0'` (原地标记) 或用 visited set
- 每次发现未访问的 `'1'`，启动 BFS/DFS，计数器 +1

---

### Python Solution with Trace

```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r, c):
        # Base case: out of bounds or water
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        # Mark as visited (sink the island)
        grid[r][c] = '0'
        
        # Explore 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':  # Found unvisited land
                islands += 1        # New island!
                dfs(r, c)           # Sink entire island
    
    return islands

# Trace on small example:
# grid = [["1","1","0"],["0","1","0"],["0","0","1"]]
# (0,0) = '1' → islands=1, DFS sinks (0,0),(0,1),(1,1)
# (2,2) = '1' → islands=2, DFS sinks (2,2)
# Result: 2
```

**时间复杂度 / Time:** O(M×N) — visit each cell once  
**空间复杂度 / Space:** O(M×N) — recursion stack in worst case (all land)

---

### BFS 版本 / BFS Alternative

```python
from collections import deque

def numIslands_bfs(grid):
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                grid[r][c] = '0'
                queue = deque([(r, c)])
                while queue:
                    row, col = queue.popleft()
                    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'  # Mark immediately to avoid duplicate queue entries
                            queue.append((nr, nc))
    
    return islands
```

**BFS vs DFS 选哪个？/ Which to choose?**
- DFS：代码更简洁；深度大时有栈溢出风险  
- BFS：无递归栈溢出；更适合"最短路径"变体  
- 对本题：两者等价，DFS 更简洁

---

### 举一反三 / Pattern Block Preview (1/13)

| 题目 | 变化点 Twist |
|------|-------------|
| **#695 Max Area** (next) | 不只是数个数，还要统计最大面积 |
| **#994 Rotting Oranges** | BFS + 时间层 (multi-source BFS) |
| **#207 Course Schedule** | 有向图 + 环检测 (cycle detection) |
| **#127 Word Ladder** | BFS 最短路径（字符变换） |

核心模版不变，关键是识别：**这是连通性问题还是最短路径问题？**  
The template stays the same — just identify: **connectivity vs. shortest path?**

---

### 📚 References
- [LeetCode #200 — Number of Islands](https://leetcode.com/problems/number-of-islands/)
- [NeetCode — Graphs Playlist](https://neetcode.io/roadmap)
- [Graph Algorithms Visualization](https://visualgo.net/en/graphds)

### 🧒 ELI5
**想象你在玩扫雷，但反过来：**  
找到一块陆地，就把所有相连的陆地都染成蓝色（变成水）。  
数一数你染了几次，就是有几座岛屿！

**Think of it like Minesweeper in reverse:**  
When you find land, flood all connected land with water.  
Count how many times you flood — that's your answer!

---

### 📝 Quiz
```json
{"question":"#200 Number of Islands — 为什么 BFS 比 DFS 更适合超大 grid？","options":["BFS 时间复杂度更低","BFS 避免了递归栈溢出 (stack overflow)","BFS 不需要 visited 集合","BFS 代码更简洁"],"correct_index":1}
```
