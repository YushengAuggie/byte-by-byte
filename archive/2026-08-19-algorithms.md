# 算法 — #323 Number of Connected Components in an Undirected Graph
# Algorithms — #323 Number of Connected Components (Medium) — Graphs

> Day 114 · Pattern Block: 图遍历 (11/13) · Expert Phase

---

## 💻 算法 / Algorithms

🧩 **图遍历模式 (11/13)** — building on the BFS/DFS template from the Graphs block

---

### 📍 Problem Context

🔗 [LeetCode #323](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) 🟡 Medium  
📹 [NeetCode Solution](https://neetcode.io/problems/count-connected-components)

**Previous in this block:**
- #200 Islands → BFS flood fill
- #695 Max Area → DFS with size accumulation  
- #133 Clone Graph → DFS with hash map
- #286 Walls & Gates → Multi-source BFS
- #994 Rotting Oranges → Multi-source BFS with time
- #417 Pacific/Atlantic → Reverse BFS from boundaries
- #130 Surrounded Regions → DFS boundary marking
- #207/#210 Course Schedule → DFS cycle detection + topological sort
- #261 Graph Valid Tree → Union-Find / DFS tree check
- **#323 今天 / TODAY → Count components** ← union-find shines here

---

### 🌍 Real-World Analogy / 真实场景

你在 LinkedIn 后端工作。数据库里有 n 个用户和他们的好友关系。现在要回答：总共有多少个"互不相连的朋友圈"？

You work at LinkedIn. Given n users and friendship edges, how many disconnected "social clusters" exist?

---

### 🧩 模式变体分析 / Pattern Variation

这道题是 Graph Valid Tree (#261) 的延伸：
- Tree: exactly 1 component + no cycle
- **今天: count all components (don't care about cycles)**

两种解法都完美映射到模板：

**解法1: Union-Find (最优)**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # each node is its own root
        self.rank = [0] * n
        self.components = n           # start: n separate components
    
    def find(self, x):
        # path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return  # already connected
        # union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1  # merged two → one fewer component

def countComponents(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components
```

**解法2: DFS (直接用模板)**
```python
def countComponents(n, edges):
    # Build adjacency list
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    count = 0
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)  # explore entire component
    
    for node in range(n):
        if node not in visited:
            dfs(node)   # new unvisited node = new component
            count += 1
    
    return count
```

---

### 📊 执行追踪 / Trace

```
Input: n=5, edges=[[0,1],[1,2],[3,4]]

DFS trace:
  node=0: not visited → dfs(0) → visits 0,1,2 → count=1
  node=1: visited, skip
  node=2: visited, skip  
  node=3: not visited → dfs(3) → visits 3,4 → count=2
  node=4: visited, skip

Output: 2 ✅

Union-Find trace:
  parent = [0,1,2,3,4]
  union(0,1): parent[1]=0, components=4
  union(1,2): find(1)→0, find(2)→2, parent[2]=0, components=3
  union(3,4): parent[4]=3, components=2
  return 2 ✅
```

---

### ⏱️ Complexity

| Solution | Time | Space |
|----------|------|-------|
| DFS/BFS  | O(V+E) | O(V+E) |
| Union-Find | O(E·α(V)) ≈ O(E) | O(V) |

α is the inverse Ackermann function — effectively O(1). **Union-Find wins on space** when you only need component count, not the actual graph structure.

---

### 🔗 举一反三 / Connect the Pattern

| Problem | What's Different | Template Adaptation |
|---------|-----------------|---------------------|
| #261 Graph Valid Tree | Count=1 AND no cycle | UF: union returns false if same root |
| #684 Redundant Connection (next!) | Find the edge that creates a cycle | UF: the union that fails is the answer |
| #127 Word Ladder (block end) | Weighted BFS on implicit graph | BFS with level tracking |

---

### 📚 References
- https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/
- https://neetcode.io/problems/count-connected-components
- https://cp-algorithms.com/data_structures/disjoint_set_union.html

### 🧒 ELI5
你有一堆积木，有些粘在一起了。数一数有几堆独立的积木组。每次把两块粘起来，如果它们本来就一堆，那没变化；否则堆数减1。
You have toy blocks. Some are glued together. Count the separate groups. Each time you glue two blocks: if they're already in the same group, nothing changes; otherwise group count decreases by 1.
