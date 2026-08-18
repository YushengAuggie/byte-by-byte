# 💻 算法 / Algorithms — #261 Graph Valid Tree (Medium)

🧩 **图遍历模式 (10/13)** — building on the BFS/DFS template from Day 101

---

## 今天的变体：判断是否为合法树

🔗 [LeetCode #261](https://leetcode.com/problems/graph-valid-tree/) 🟡 Medium  
📹 [NeetCode 视频](https://neetcode.io/problems/valid-tree)

---

## 什么是合法树？What makes a valid tree?

一棵合法树满足两个条件：
1. **没有环（Acyclic）** — n 个节点恰好 n-1 条边
2. **完全连通（Fully connected）** — 所有节点可达

> 🌍 现实类比：局域网拓扑检测。你有 n 台服务器，n-1 条网线，如果每台机器都能互联互通（且没有冗余链路），这就是一棵生成树。

---

## 与模版的映射

```
标准图遍历模版:
  visited = {start}
  queue = deque([start])
  while queue:
      node = queue.popleft()
      for neighbor in graph[node]:
          if neighbor not in visited:
              visited.add(neighbor)
              queue.append(neighbor)

Graph Valid Tree 的关键：
  1. 预检：edges != n-1 → 直接 False（排除有环或不连通）
  2. BFS 遍历起点 0
  3. 遍历后 len(visited) == n → 连通
```

---

## Python 解法（附逐步追踪）

```python
from collections import defaultdict, deque
from typing import List

def validTree(n: int, edges: List[List[int]]) -> bool:
    # Step 1: Quick check — a tree with n nodes has exactly n-1 edges
    if len(edges) != n - 1:
        return False

    # Step 2: Build adjacency list (undirected)
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Step 3: BFS from node 0
    visited = {0}
    queue = deque([0])

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Step 4: All nodes must be reachable
    return len(visited) == n
```

**追踪示例 / Trace:**
```
n=5, edges=[[0,1],[0,2],[0,3],[1,4]]

len(edges) = 4 = n-1 ✅

graph: {0:[1,2,3], 1:[0,4], 2:[0], 3:[0], 4:[1]}

BFS from 0:
  queue=[0], visited={0}
  pop 0 → neighbors 1,2,3 → visited={0,1,2,3}, queue=[1,2,3]
  pop 1 → neighbor 4 → visited={0,1,2,3,4}, queue=[2,3,4]
  pop 2 → neighbor 0 (already visited)
  pop 3 → neighbor 0 (already visited)
  pop 4 → neighbor 1 (already visited)

len(visited)=5 == n=5 → True ✅
```

**复杂度 / Complexity:**  
- 时间：O(V + E)  
- 空间：O(V + E)

---

## 🔁 为什么 `len(edges) != n-1` 就能提前判断？

- n-1 条边 + 连通 = 树（数学定理）
- 边太少 → 不连通（森林）
- 边太多 → 必有环

这是此题比普通 BFS/DFS 更优雅的地方：用一行数学条件排除大量无效案例。

---

## 举一反三：Graph 模式同类题

| 题目 | 核心变化 |
|------|---------|
| #207 Course Schedule | 有向图检测环（拓扑排序） |
| #684 Redundant Connection | 找第一条产生环的边 |
| #323 Number of Connected Components | 计算连通分量数 |
| #200 Number of Islands | 二维网格图遍历 |

**规律**：树 = n-1 条边 + 连通 → 检测树/森林时必用此技巧。

---

## 📚 References
- https://leetcode.com/problems/graph-valid-tree/
- https://neetcode.io/problems/valid-tree
- https://en.wikipedia.org/wiki/Tree_(graph_theory)

## 🧒 ELI5
想象 5 个城市要用公路连起来。如果用了 4 条路（城市数-1），每个城市都能到达其他城市，那就是一棵"生成树"——刚好够用，不多也不少。多一条路就会形成环，少一条就有城市孤立。
