# 💻 算法 / Algorithms — Day 83 (Expert)
**Date:** 2026-07-30 | **LeetCode #286 Walls and Gates** | 🟡 Medium

---

🧩 **图遍历模式 (4/13)** — building on the BFS/DFS template from Day 79

---

## 问题 / Problem

你有一个 `m × n` 的网格，包含：
- `-1` = 墙壁 (Wall)
- `0` = 门 (Gate)  
- `INF = 2147483647` = 空房间 (Empty room)

**任务：** 把每个空房间填上它到最近门的距离。

You have an `m × n` grid with -1 (walls), 0 (gates), and INF (empty rooms).  
**Fill each empty room with the distance to its nearest gate.**

🔗 [LeetCode #286](https://leetcode.com/problems/walls-and-gates/) | 📹 [NeetCode](https://neetcode.io/problems/islands-and-treasure)

---

## 真实类比 / Real-world Analogy

想象你在设计医院，需要告诉每位病人他们离最近急救室有多远。  
从所有急救室同时出发找病人，比从每个病人出发找急救室快多了。

Imagine a hospital layout — you need to tell each patient how far they are from the nearest ER. Starting from ALL ERs simultaneously and expanding outward is much faster than checking from each patient.

---

## 模式映射 / Pattern Mapping

这道题是经典 **多源 BFS (Multi-source BFS)**：

```
普通 BFS: 从1个起点出发
Multi-source BFS: 从「所有门」同时出发

关键洞察 / Key Insight:
- 先把所有 gate(0) 加入队列
- BFS 自然保证「第一次到达」= 最短距离
- 比「从每个房间跑一次 BFS」快 O(mn) 倍
```

---

## Python 解法 / Solution

```python
from collections import deque

def walls_and_gates(rooms: list[list[int]]) -> None:
    """
    Multi-source BFS from all gates simultaneously.
    Modifies rooms in-place.
    """
    if not rooms:
        return
    
    INF = 2147483647
    m, n = len(rooms), len(rooms[0])
    queue = deque()
    
    # Step 1: Seed queue with all gates
    for r in range(m):
        for c in range(n):
            if rooms[r][c] == 0:
                queue.append((r, c))
    
    # Step 2: BFS outward from all gates simultaneously
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Only update unvisited empty rooms
            if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1  # distance = parent + 1
                queue.append((nr, nc))

# Example trace:
# INF -1  0  INF
# INF INF INF -1
# INF -1  INF -1
# 0  -1  INF INF
#
# After BFS:
# 3  -1  0  1
# 2  2   1  -1
# 1  -1  2  -1
# 0  -1  3  4
```

**复杂度 / Complexity:**
- Time: O(mn) — each cell visited once
- Space: O(mn) — queue size

---

## 与模板的对比 / Template Comparison

```python
# 标准 BFS 模板 vs 本题
# Standard:              This problem:
queue = deque([start])   queue = deque([all gates])   # 多源！
visited = {start}        INF值本身就是 "未访问" 标记    # 无需 visited set
                         rooms[nr][nc] = rooms[r][c]+1 # 记录距离
```

**关键变化 / Key Difference:** 多源 BFS 不需要单独的 `visited` 集合——更新值本身就标记了"已访问"。

---

## 举一反三 / Block Connection

| 题目 | BFS变体 |
|------|---------|
| #200 Number of Islands | 单源 DFS/BFS，计数连通块 |
| #695 Max Area of Island | DFS + 面积计数 |
| **#286 Walls and Gates** | **多源 BFS，最短距离** |
| #994 Rotting Oranges (下一道) | 多源 BFS + 时间追踪 |

Rotting Oranges 是本题的变体——从所有烂橙子出发，问多少步让所有橙子腐烂。

---

## 📝 Quiz

```json
{"question":"Walls and Gates 为什么用 Multi-source BFS 而不是从每个房间单独做 BFS？","options":["因为 BFS 不能处理多个起点","Multi-source BFS 保证每个房间在第一次被到达时就是最短距离，单源版本要做 O(mn) 次 BFS","Multi-source BFS 使用更少内存","因为图里有负权边"],"correct_index":1}
```

---

## 🧒 ELI5
想象把所有门同时点火，火焰向四周蔓延。每个房间第一次被火碰到时，记下走了几步。这就是它离最近门的距离。  
Imagine lighting all gates on fire at the same time. Each room records how many steps it took for the fire to reach it — that's its distance to the nearest gate.

---

## 📚 References
- [LeetCode #286](https://leetcode.com/problems/walls-and-gates/)
- [Multi-source BFS Explained — NeetCode](https://neetcode.io/problems/islands-and-treasure)
- [BFS Shortest Path — CP-algorithms](https://cp-algorithms.com/graph/breadth-first-search.html)
