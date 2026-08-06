# 💻 算法 / Algorithms — Day 107

> #994 Rotting Oranges (Medium) — 图遍历模式 BFS/DFS (5/13)

🧩 **图遍历模式 (5/13)** — building on the template from Days 101-104

今天是这个模式的第5题。之前：岛屿数量(BFS/DFS)、岛屿最大面积、图克隆(哈希+DFS)、距离最近的0(多源BFS)。今天：**多源 BFS 计算最短时间**——这是模板的一个经典变体。

---

## 题目 / Problem

🔗 [LeetCode #994](https://leetcode.com/problems/rotting-oranges/) 🟡 Medium
📹 [NeetCode 讲解](https://neetcode.io/problems/rotting-fruit)

**场景**：一个 m×n 网格，每个格子：
- `0` = 空
- `1` = 新鲜橘子
- `2` = 腐烂橘子

每分钟，腐烂橘子会让四邻居的新鲜橘子变腐烂。返回所有橘子腐烂所需的**最少分钟数**，如果不可能则返回 `-1`。

**Real-world analogy**: 病毒传播模型 / 社交网络影响力扩散 / CDN 缓存失效波。有多个"感染源"同时扩散，求最长传播路径。

---

## 模板映射 / Template Mapping

标准 BFS 模板 → **多源 BFS** 变体：
- 把所有初始腐烂橘子**同时加入队列**（多个起点）
- 每一轮（minute）处理当前队列全部节点 → level-by-level BFS
- 追踪 `fresh_count`，最终若仍 > 0 返回 -1

```
标准模板: queue = deque([start])  ← 单源
今日变体: queue = deque([all rotten])  ← 多源，同步扩散
```

---

## Python 解法 / Solution

```python
from collections import deque

def orangesRotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    # Step 1: seed all rotten oranges into queue
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, minute)
            elif grid[r][c] == 1:
                fresh += 1

    # Edge case: no fresh oranges
    if fresh == 0:
        return 0

    minutes = 0
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while queue:
        r, c, minute = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2       # rot it
                fresh -= 1
                minutes = minute + 1   # track max time
                queue.append((nr, nc, minute + 1))

    return minutes if fresh == 0 else -1
```

**执行追踪** (小例子: `[[2,1,1],[1,1,0],[0,1,1]]`):
```
初始: queue=[(0,0,0)], fresh=6
min=1: 腐烂(0,1),(1,0) → fresh=4
min=2: 腐烂(0,2),(1,1) → fresh=2
min=3: 腐烂(2,1) → fresh=1
min=4: 腐烂(2,2) → fresh=0
返回: 4 ✓
```

**复杂度**: Time O(m×n), Space O(m×n)

---

## 与模板的关键差异 / Key Difference from Template

| | 标准 BFS (岛屿) | 今日变体 (腐烂橘子) |
|--|--|--|
| 起点 | 单个 | 多个（同时入队） |
| 目标 | 连通性/面积 | 最短时间 |
| visited | 独立 visited 集合 | 原地修改 grid |
| 返回值 | 面积/bool | 最大层数 |

---

## 举一反三 / Pattern Connections

- **Walls and Gates (Day 104)**: 同款多源 BFS，求每个空格到最近门的距离
- **Pacific Atlantic Water Flow (下一题)**: 从两个边界反向 BFS，找交集
- **Course Schedule (即将)**: 同样思路用于拓扑排序（检测环）

---

## 🧒 ELI5

把腐烂橘子想成病人，每分钟传染邻居。BFS 就是"一圈一圈往外扩"——先传第一圈，再传第二圈。多源 BFS 就是同时有多个病人开始传，最后问最远那个健康人什么时候才会被感染。

---

## 📚 References
- https://leetcode.com/problems/rotting-oranges/
- https://neetcode.io/problems/rotting-fruit
- https://cp-algorithms.com/graph/breadth-first-search.html
