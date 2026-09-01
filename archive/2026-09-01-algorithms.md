# 💻 算法 / Algorithms — Day 123

🧩 **高级图算法模式 (5/6)** — building on the template from Day 118 (Min Cost), Day 119 (Network Delay), Day 122 (Reconstruct Itinerary)

---

## #778 Swim in Rising Water 🔴 Hard

🔗 https://leetcode.com/problems/swim-in-rising-water/
📹 https://neetcode.io/problems/swim-in-rising-water

---

### 真实类比 / Real-World Analogy

想象一张地形图，数字代表海拔。水位从 0 开始逐渐上升。你站在左上角，想游到右下角。**你能在水位达到 t 之前到达吗？**

Imagine a topographic map where numbers represent elevation. Water rises from 0. You're at top-left, want to reach bottom-right. **Can you swim there before time t?**

**本质：** 找从 (0,0) 到 (n-1,n-1) 的路径，使路径上**最大值最小化**。这是 Dijkstra 的变体——不是累加权重，而是取 max。

---

### 如何映射到模板 / Mapping to the Pattern Template

```python
# Standard Dijkstra: minimize sum of weights
# dist[v] = min(dist[u] + weight(u,v))

# Swim in Rising Water: minimize MAXIMUM elevation along path
# dist[v] = min(max(dist[u], grid[r][c]))
#                    ^^^
#                    This is the key change!
```

变体规律（Variation Rule）:
- **最短路径（加权）** → `new_dist = dist[u] + w` (Network Delay)
- **最小生成树** → `new_dist = w` (Min Cost Connect Points)
- **Minimax 路径** → `new_dist = max(dist[u], grid[r][c])` ← **TODAY**

---

### Python 解法 + Trace

```python
import heapq

def swimInWater(grid: list[list[int]]) -> int:
    n = len(grid)
    # (max_elevation_so_far, row, col)
    heap = [(grid[0][0], 0, 0)]
    visited = set()
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    
    while heap:
        t, r, c = heapq.heappop(heap)
        
        if (r, c) in visited:
            continue
        visited.add((r, c))
        
        # Reached destination
        if r == n-1 and c == n-1:
            return t
        
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n and (nr,nc) not in visited:
                # Key: take max of current path max and neighbor elevation
                new_t = max(t, grid[nr][nc])
                heapq.heappush(heap, (new_t, nr, nc))
    
    return -1  # unreachable

# Trace on grid = [[0,2],[1,3]]:
# heap: [(0, 0, 0)]
# pop (0,0,0): push (max(0,2),0,1)=(2,0,1), (max(0,1),1,0)=(1,1,0)
# pop (1,1,0): push (max(1,3),1,1)=(3,1,1)
# pop (2,0,1): (1,1) already in queue
# pop (3,1,1): DESTINATION → return 3
```

**时间复杂度 / Complexity:** O(n² log n) — n² cells, each pushed once  
**空间复杂度 / Space:** O(n²)

---

### 为什么不用 Binary Search + BFS？

另一个常见解法：二分答案 t，用 BFS 验证"水位 ≤ t 时能否到达"。  
`O(n² log n)` — 相同复杂度，但 Dijkstra 更直接。

---

### 举一反三：本 Pattern 的变体规律

| 问题 | 权重含义 | Dijkstra 更新 |
|---|---|---|
| #743 Network Delay | 传播时间（累加） | `d[u] + w` |
| #1584 Min Cost Points | 曼哈顿距离（累加） | `d[u] + dist` |
| **#778 Swim in Water** | 海拔障碍（取 max） | `max(d[u], elev)` |
| #787 Flights K Stops | 代价（带约束累加） | Bellman-Ford |

---

### 📝 Quiz
```json
{"question":"Swim in Rising Water 的 Dijkstra 变体关键在于？","options":["new_t = t + grid[nr][nc]","new_t = max(t, grid[nr][nc])","new_t = min(t, grid[nr][nc])","new_t = grid[nr][nc]"],"correct_index":1}
```

---

### 🧒 ELI5

你想去朋友家，但路上有些山。水位一直在涨。你要找一条路，让你爬的**最高的山最矮**——这样你等水涨到那个高度就够了。Dijkstra 帮你每次都走"目前最矮的最高山"那条路。

---

### 📚 References
- https://leetcode.com/problems/swim-in-rising-water/
- https://neetcode.io/problems/swim-in-rising-water
- https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
