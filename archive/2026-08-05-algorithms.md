# 💻 算法 / Algorithms — Day 108

## 🧩 图遍历模式 (6/13) — Pacific Atlantic Water Flow

> 在 Day 101 的模板基础上进阶 / Building on the BFS/DFS template from Day 101

**这道题的特别之处**：不是"从起点出发找终点"，而是**反向思维** — 从两个大洋的边界**逆流而上**，找能同时到达两个大洋的格子。

What makes this different: instead of flowing downhill from cells to ocean, we **reverse the direction** — BFS/DFS uphill from both ocean boundaries, find cells reachable from both.

---

## 🔗 题目链接 / Links

- 🟡 **Medium** | [LeetCode #417 — Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/)
- 📹 [NeetCode Video](https://neetcode.io/problems/pacific-atlantic-water-flow)

---

## 🌊 真实场景类比 / Real-World Analogy

想象一个地形图：左上角是太平洋，右下角是大西洋。雨水从高处流向低处，最终流入大洋。哪些格子的雨水**同时**能流进两个大洋？

这就像找"双重流域分水岭"— 那些既属于太平洋流域、又属于大西洋流域的高地。

Imagine a terrain map: Pacific is top-left/left/top edges, Atlantic is bottom-right/right/bottom edges. Water flows downhill. Which cells can reach **both** oceans?

---

## 💡 核心洞察 / Key Insight: 逆流思维

**正向思维（难）**: 从每个格子 DFS，看能不能同时到达两个海岸 → O(m×n×(m×n)) 太慢

**逆向思维（优）**: 
1. 从太平洋边界出发，BFS **逆流向上**（只走不低于当前高度的格子）→ 标记所有能流入太平洋的格子
2. 从大西洋边界出发，同理
3. 两个集合的**交集**就是答案

Naive: DFS from every cell to check both oceans → O(m²n²)  
Smart: BFS backward from ocean boundaries → O(mn)

---

## 🐍 Python 解法 / Solution

```python
from collections import deque
from typing import List

def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    if not heights:
        return []
    
    rows, cols = len(heights), len(heights[0])
    
    def bfs(starts):
        """BFS from boundary, going uphill (reverse flow)"""
        visited = set(starts)
        queue = deque(starts)
        
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and (nr, nc) not in visited
                        and heights[nr][nc] >= heights[r][c]):  # uphill!
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return visited
    
    # Pacific: top row + left column
    pacific_starts = [(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)]
    # Atlantic: bottom row + right column
    atlantic_starts = [(r, cols-1) for r in range(rows)] + [(rows-1, c) for c in range(cols)]
    
    pacific_reachable = bfs(pacific_starts)
    atlantic_reachable = bfs(atlantic_starts)
    
    # Intersection = can reach both
    return [[r, c] for r, c in pacific_reachable & atlantic_reachable]
```

---

## 🔍 执行追踪 / Trace (3×3 example)

```
heights = [
  [1, 2, 2],
  [3, 2, 3],
  [2, 4, 5]
]

Pacific starts: (0,0),(1,0),(2,0),(0,1),(0,2)
Atlantic starts: (0,2),(1,2),(2,2),(2,0),(2,1)

Pacific BFS (uphill from left/top):
  → visits: (0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2) almost all

Atlantic BFS (uphill from right/bottom):
  → starts at (2,2)=5, can go to (2,1)=4, (1,2)=3, etc.

Intersection → cells reachable from both
Result: [[0,2],[1,2],[1,1],[2,0],[2,1],[2,2]]
```

---

## ⏱️ 复杂度 / Complexity

| | Time | Space |
|--|------|-------|
| BFS×2 | O(m×n) | O(m×n) |
| vs Naive | O(m²n²) | O(mn) |

---

## 🔄 模板变体对比 / Template Variation vs Previous Problems

| Problem | Start Point | Direction | Goal |
|---------|-------------|-----------|------|
| #200 Islands | Any unvisited land | All 4 dirs (same height) | Count components |
| #994 Rotting Oranges | All rotten cells | BFS outward | Min time |
| **#417 Pacific Atlantic** | **Both ocean boundaries** | **Uphill (≥ current)** | **Intersection of two BFS** |

**关键变体 / Key twist**: 两次独立 BFS + 求交集。这个"从边界逆流"的技巧在很多矩阵题里都会出现！

---

## 举一反三 / Related Problems in This Block

- **#130 Surrounded Regions** (Day 109): 同样用"从边界出发"思路，标记不被围的 'O'
- **#207 Course Schedule** (Day 110): 图的有向性，拓扑排序检测环
- **逆向BFS** 是一个通用技巧：当正向太慢时，考虑从目标反推

---

## 📚 References
- https://leetcode.com/problems/pacific-atlantic-water-flow/editorial/
- https://neetcode.io/problems/pacific-atlantic-water-flow
- https://en.wikipedia.org/wiki/Drainage_basin

## 🧒 ELI5
想象地图上有两片海。从每片海的海岸线开始，逆着水流方向（往高处走），把能到达的格子都涂色。太平洋涂蓝色，大西洋涂红色。最后找紫色格子（蓝+红）就是答案！

Imagine coloring from each ocean's shoreline, going uphill. Pacific turns cells blue, Atlantic turns them red. Cells that get colored purple (both) are your answer!
