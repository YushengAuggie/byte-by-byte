# 💻 Day 118 — Algorithms
> 🔥 Expert Level | Advanced Graphs — Pattern Block Start

---

💻 **算法 / Algorithms** — #1584 Min Cost to Connect All Points (Medium)

🧩 **新模式 / New Pattern: 高级图算法 — Advanced Graphs**
📍 This block: 6 problems

**什么时候用 / When to use:** 有权图最短路径（Dijkstra）、最小生成树（Prim/Kruskal）、Union-Find 动态连通性

**识别信号 / Signals:** weighted shortest path, minimum spanning tree, union find, disjoint sets, network connectivity, cost to connect

**通用模版 / Template:**
```python
# Dijkstra's — Shortest Path
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]  # (cost, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue  # stale entry, skip
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist

# Prim's MST — For dense graphs (n^2 edges)
def prim_mst(points):
    n = len(points)
    in_mst = [False] * n
    min_cost = [float('inf')] * n
    min_cost[0] = 0
    heap = [(0, 0)]  # (cost, node)
    total = 0
    while heap:
        cost, u = heapq.heappop(heap)
        if in_mst[u]: continue
        in_mst[u] = True
        total += cost
        for v in range(n):
            if not in_mst[v]:
                w = your_edge_weight(u, v)
                if w < min_cost[v]:
                    min_cost[v] = w
                    heapq.heappush(heap, (w, v))
    return total
```

**核心洞察 / Key Insight:** Dijkstra = BFS + 优先队列（贪心选最短边）。Prim = Dijkstra 的变体，用于最小生成树。两者都用堆 + 懒删除（stale entry check）。

---

## 📍 今日题目 / Today's Problem

🔗 [LeetCode #1584](https://leetcode.com/problems/min-cost-to-connect-all-points/) 🟡 Medium  
📹 [NeetCode Video](https://neetcode.io/problems/min-cost-to-connect-points)

---

## 🌍 真实场景类比 / Real-World Analogy

想象你是城市规划师，要在 n 个村庄之间修路，使所有村庄都能互相到达。修路的费用 = 曼哈顿距离（|x1-x2| + |y1-y2|）。目标：花最少的钱把所有村庄连通。

You're a city planner connecting n villages with roads. Road cost = Manhattan distance. Goal: minimum cost to connect all villages (classic Minimum Spanning Tree).

---

## 🧩 映射到模式 / Map to Pattern

这是一道**最小生成树 (MST)** 问题 — 经典 Prim 算法场景：
- 所有节点两两之间都有边（完全图，n² 条边）
- 求连通所有节点的最小总代价

This is MST, not Dijkstra. Key difference:
- **Dijkstra**: shortest path from one source to all others
- **Prim/Kruskal**: minimum weight to connect ALL nodes

---

## 💡 解法 / Solution

```python
import heapq

def minCostConnectPoints(points: list[list[int]]) -> int:
    n = len(points)
    in_mst = [False] * n
    # min_cost[i] = cheapest edge to add node i to MST
    min_cost = [float('inf')] * n
    min_cost[0] = 0
    heap = [(0, 0)]  # (cost, node_index)
    total = 0
    edges_used = 0

    while edges_used < n:
        cost, u = heapq.heappop(heap)

        # Lazy deletion: skip stale entries
        if in_mst[u]:
            continue

        in_mst[u] = True
        total += cost
        edges_used += 1

        # Update neighbors (all unvisited nodes)
        for v in range(n):
            if not in_mst[v]:
                manhattan = (abs(points[u][0] - points[v][0]) +
                             abs(points[u][1] - points[v][1]))
                if manhattan < min_cost[v]:
                    min_cost[v] = manhattan
                    heapq.heappush(heap, (manhattan, v))

    return total
```

**追踪 Trace** (3 points: [0,0], [2,2], [3,10]):
```
Start: heap=[(0,0)], min_cost=[0, inf, inf]
Pick (0, node=0): total=0, update neighbors
  → node1: manhattan=4, node2: manhattan=13
  heap=[(4,1),(13,2)]

Pick (4, node=1): total=4, update neighbors  
  → node2: manhattan=|3-2|+|10-2|=9 < 13 → update
  heap=[(9,2),(13,2_stale)]

Pick (9, node=2): total=13, done (3 nodes)
Answer: 13
```

**复杂度 / Complexity:**
- Time: O(n² log n) — n² edges, each pushed to heap once
- Space: O(n²) — heap can hold all edges

> 💡 Alternative: Kruskal's with Union-Find is cleaner for sparse graphs. Prim's wins for dense graphs (complete graph = n² edges).

---

## 🔄 举一反三 / Pattern Connections

| 问题 | 核心变化 | 关键差异 |
|------|---------|---------|
| #743 Network Delay Time (下一题) | Dijkstra 单源最短路 | 不是 MST，是 shortest path |
| #787 Cheapest Flights K Stops | Dijkstra + 约束 (k stops) | Bellman-Ford 变体更直接 |
| #778 Swim in Rising Water | 二分 + BFS 或 Prim 变体 | 最小化最大边权 |
| #332 Reconstruct Itinerary | Eulerian path (DFS) | 完全不同，不是 Dijkstra |

---

## 📚 References
- https://neetcode.io/problems/min-cost-to-connect-points
- https://leetcode.com/problems/min-cost-to-connect-all-points/
- https://cp-algorithms.com/graph/mst_prim.html
- https://en.wikipedia.org/wiki/Prim%27s_algorithm

## 🧒 ELI5
把所有点用绳子连起来，每条绳子的费用是两点的曼哈顿距离。你每次选最便宜的绳子，把一个还没连上的点拉进来，直到所有点都连上。这就是 Prim 算法！  
Imagine connecting dots with rope. Each rope costs Manhattan distance. Always grab the cheapest rope that pulls a new dot into your connected group. That's Prim's algorithm for MST!
