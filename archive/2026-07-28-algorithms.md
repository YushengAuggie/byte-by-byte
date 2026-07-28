# 💻 算法 / Algorithms — Day 81: #695 Max Area of Island (Medium)

🧩 **图遍历模式 (BFS/DFS) — 2/13** — building on the template from Day 80 (Number of Islands)

---

## 今日题目 / Today's Problem

**#695 Max Area of Island** | 🟡 Medium  
🔗 [LeetCode](https://leetcode.com/problems/max-area-of-island/) | 📹 [NeetCode](https://neetcode.io/problems/max-area-of-island)

---

## 和模板的关系 / How This Maps to the Template

上一题 #200 Number of Islands：**数有多少个连通分量**（count components）  
今天 #695 Max Area of Island：**找最大连通分量的面积**（find max component size）

变化点很小：只需要在 DFS 时**累计格子数**，然后取最大值。

```python
# Day 80 模板回顾 (BFS)
# visited = {start}
# while queue: node = queue.popleft() → 数量 +1 per component

# 今天的变化: 每个连通分量不止 +1，而是累计 DFS 访问的格子数
```

---

## 现实类比 / Real-World Analogy

想象你是地图分析师，手里有一张海洋地图，陆地用 `1` 表示，海洋用 `0`。  
你的任务：找出**面积最大的岛屿**有多大。

You're a GIS analyst. Given a satellite image as a binary grid, find the largest contiguous landmass.

---

## 解题思路 / Solution Approach

```python
from typing import List

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()
        max_area = 0
        
        def dfs(r, c) -> int:
            # Base case: out of bounds, water, or already visited
            if (r < 0 or r >= rows or 
                c < 0 or c >= cols or 
                grid[r][c] == 0 or 
                (r, c) in visited):
                return 0  # contributes 0 area
            
            visited.add((r, c))
            # Count this cell + all 4 neighbors
            return (1 + 
                    dfs(r + 1, c) + 
                    dfs(r - 1, c) + 
                    dfs(r, c + 1) + 
                    dfs(r, c - 1))
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and (r, c) not in visited:
                    area = dfs(r, c)
                    max_area = max(max_area, area)
        
        return max_area
```

---

## 执行追踪 / Step-by-Step Trace

```
grid = [
  [0,1,1,0,0],
  [0,1,0,0,0],
  [0,0,0,1,1],
]

Scan (0,1): island found → DFS
  visit (0,1) → 1
  visit (0,2) → 1
  visit (1,1) → 1
  → area = 3, max_area = 3

Scan (2,3): island found → DFS
  visit (2,3) → 1
  visit (2,4) → 1
  → area = 2, max_area = 3

Return: 3
```

---

## 和 #200 的对比 / Comparison with Number of Islands

| | #200 Number of Islands | #695 Max Area of Island |
|---|---|---|
| 目标 | 计连通分量数 | 找最大分量面积 |
| DFS 返回值 | void (只标记访问) | int (返回格子数) |
| 全局状态 | count++ | max_area = max(...) |
| 时间复杂度 | O(M×N) | O(M×N) |

---

## 复杂度 / Complexity

- **Time:** O(M × N) — 每个格子最多访问一次
- **Space:** O(M × N) — visited set + 递归栈深度

---

## 举一反三 / Pattern Variations

这道题是 Graphs 模块第 2 题。接下来的变体：

- **#133 Clone Graph** — 同样 DFS，但要重建节点（HashMap 追踪映射）
- **#286 Walls and Gates** — BFS 多源同时出发（multi-source BFS）
- **#994 Rotting Oranges** — BFS + 时间模拟（分钟计步）
- **#417 Pacific Atlantic** — 反向 DFS（从边界往内扫）

关键洞察：**岛屿问题 = DFS 统计；最短路径问题 = BFS 层序。**

---

## 📝 Quiz

```json
{"question":"In maxAreaOfIsland, what does the DFS function return when it hits a water cell (grid[r][c]==0)?","options":["1","0","-1","None"],"correct_index":1}
```

---

## 📚 References

- [LeetCode #695](https://leetcode.com/problems/max-area-of-island/)
- [NeetCode Video](https://neetcode.io/problems/max-area-of-island)
- [Graph Algorithms Visualized](https://visualgo.net/en/dfsbfs)

## 🧒 ELI5

你在玩扫雷。陆地格子是安全区，海洋格子是雷。每次发现一块陆地，就用手指（DFS）走遍所有连着的陆地，数数有几格。最后报告走过的最大连续陆地面积。

You're in a maze made of land (1) and water (0). Whenever you step on land, you explore all connected land tiles by walking in 4 directions, counting as you go. You want to find the biggest "island" you can walk across.
