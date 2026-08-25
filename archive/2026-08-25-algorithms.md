# 💻 算法 / Algorithms — Day 94
## #743 Network Delay Time — Medium 🟡
### 🧩 Advanced Graphs (2/6) — building on Dijkstra template from Day 93

---

🔗 [LeetCode #743](https://leetcode.com/problems/network-delay-time/) | 🟡 Medium | 📹 [NeetCode](https://neetcode.io/problems/network-delay-time)

---

### 🧩 Advanced Graphs (2/6) — 用昨天的 Dijkstra 模板解今天的问题

**昨天 (Day 93 #1584):** Prim's 算法求最小生成树 (MST) — 连通所有点的最小代价
**今天 (Day 94 #743):** Dijkstra 求单源最短路径 — 信号从 k 出发，到达所有节点的最短时间

**核心区别 / Key Difference:**
- MST: 找一棵树连通所有点，总权重最小
- Single-Source Shortest Path: 从一个源点出发，到所有其他点的最短距离

---

### 真实场景 / Real-World Analogy

想象一个微服务网络：节点是服务，边是 RPC 调用延迟（毫秒）。
服务 k 广播一条配置变更消息。问题：**所有服务都收到消息需要多长时间？**

答案 = 从 k 出发，到最远节点的最短路径长度（即 max(dist[all nodes])）。

A microservice network: nodes are services, edge weights are RPC latency (ms).
Service k broadcasts a config update. Question: when has EVERY service received it?
Answer = the longest shortest-path from k (the "bottleneck" node).

---

### 问题映射到模板 / Map to Dijkstra Template

```
给定: times = [[2,1,1],[2,3,1],[3,4,1]], n=4, k=2
      表示: 从2→1需1ms, 2→3需1ms, 3→4需1ms

目标: 从 k=2 出发，到达所有节点的最大延迟
答案: dist[1]=1, dist[3]=1, dist[4]=2 → max = 2

如果有节点不可达 → 返回 -1
```

---

### Python 解法 + 逐行追踪 / Solution with Trace

```python
import heapq
from collections import defaultdict

def networkDelayTime(times, n: int, k: int) -> int:
    # Build adjacency list: graph[u] = [(v, w), ...]
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    # Dijkstra from source k
    dist = {node: float('inf') for node in range(1, n + 1)}
    dist[k] = 0
    heap = [(0, k)]  # (distance, node)
    
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:  # stale entry — skip!
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    
    # If any node unreachable → return -1
    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1

# Trace for times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2:
# Initial: dist = {1:inf, 2:0, 3:inf, 4:inf}, heap = [(0,2)]
# Pop (0,2): process neighbors 1 (w=1), 3 (w=1)
#   dist[1]=1, dist[3]=1 → heap = [(1,1),(1,3)]
# Pop (1,1): no neighbors for 1 → nothing
# Pop (1,3): process neighbor 4 (w=1)
#   dist[4]=2 → heap = [(2,4)]
# Pop (2,4): no neighbors → done
# dist = {1:1, 2:0, 3:1, 4:2} → max = 2 ✅
```

**时间复杂度:** O((V+E) log V) — heappush/pop on V nodes, E edges
**空间复杂度:** O(V+E) — adjacency list + dist dict

---

### 举一反三 / Pattern Variations in This Block

| 题目 | 核心变化 | 关键调整 |
|------|---------|---------|
| #1584 Min Cost (Day 93) | MST，非单源最短路 | Prim's / Kruskal's |
| **#743 Network Delay (今天)** | **单源最短路** | **标准 Dijkstra** |
| #787 Cheapest K Stops | 有跳数限制的最短路 | Bellman-Ford 或 BFS+DP |
| #332 Reconstruct Itinerary | 欧拉路径 | DFS + Hierholzer |
| #778 Swim in Rising Water | 最小化最大边 | Dijkstra 变体 (minimax) |
| #269 Alien Dictionary | 拓扑排序 | BFS/DFS 构建依赖图 |

---

### 📚 References
- https://leetcode.com/problems/network-delay-time/
- https://cp-algorithms.com/graph/dijkstra.html — Dijkstra 详解 (含证明)
- https://neetcode.io/problems/network-delay-time

### 🧒 ELI5
像在地图上从家出发，找到去每个朋友家的最短路线。Dijkstra 算法像一个聪明的导航：每次都先走目前看起来最近的路，慢慢把所有路都探索完。最后看最远的朋友家需要走多久——那就是整个消息传播的时间。

Like finding the fastest route from your house to every friend's house. Dijkstra always tries the currently-closest unvisited house next. When everyone's been reached, the answer is the longest "shortest path" — that's the bottleneck.
