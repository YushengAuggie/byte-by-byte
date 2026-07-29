# 算法 / Algorithms — Day 103: Clone Graph (#133)

## 💻 算法 / Algorithms — #133 Clone Graph (Medium) — Graphs

🧩 **图遍历模式 (BFS/DFS) (3/13)** — building on the template from Day 101–102

今天是图遍历 Block 第 3 题。前两题（Number of Islands, Max Area of Island）是在**网格/矩阵**上 DFS/BFS。今天的 Clone Graph 是在**普通节点图**上 BFS，核心挑战从"防止回访"变成"**建映射表（old → new node）**"。

Today is Block Problem 3/13. The first two (Islands, Max Area) used DFS/BFS on a grid. Clone Graph is BFS on a general node graph — the core challenge shifts from "avoid revisit" to **"build an old→new node mapping"**.

---

### 🔗 Links
- [LeetCode #133 Clone Graph](https://leetcode.com/problems/clone-graph/) 🟡 Medium
- [NeetCode Video](https://www.youtube.com/watch?v=mQeF6bN8hMk)

---

### 🌍 Real-World Analogy / 现实类比

想象你拿到一份组织架构图（org chart），每个人有指向同事的引用。你需要**完全复制**这张图，但不能让新人和旧人共享同一个节点对象。

Imagine you receive an org chart where each person holds references to their direct colleagues. You need to **deep clone** the entire graph — new people, same connections — without sharing any object between original and copy.

---

### 🧩 与模板的映射 / Mapping to the Template

标准 BFS 模板 → Clone Graph 变体：

```
visited = {start}  →  cloned = {node: Node(node.val)}  # old→new mapping
```

`cloned` 字典同时充当 `visited` 集合（防重复）和克隆节点的存储。

The `cloned` dict acts as both the `visited` set (prevent revisit) and the clone node store.

---

### 💡 Problem → Pattern → Solution

**问题 / Problem**：给定连通无向图的一个节点，返回整张图的深拷贝。

**关键洞察 / Key Insight**：
1. 建一个 `HashMap[old_node → new_node]` — 这是防重和建连接的核心
2. BFS 遍历所有节点，每次给邻居建克隆（如果没建过）
3. 把克隆的邻居挂到当前克隆节点上

```python
from collections import deque
from typing import Optional

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: Optional[Node]) -> Optional[Node]:
    if not node:
        return None
    
    # old → new mapping (also serves as visited set)
    cloned = {node: Node(node.val)}
    queue = deque([node])
    
    while queue:
        curr = queue.popleft()
        
        for neighbor in curr.neighbors:
            if neighbor not in cloned:
                # First time seeing this neighbor — clone it
                cloned[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            
            # Connect current clone to neighbor clone
            cloned[curr].neighbors.append(cloned[neighbor])
    
    return cloned[node]
```

---

### 📊 Execution Trace / 执行追踪

```
Graph: 1 - 2
       |   |
       4 - 3

Step 1: Start with node 1, create clone[1] = Node(1), queue = [1]
Step 2: Process 1, neighbors = [2, 4]
  → clone[2] = Node(2), clone[4] = Node(4), queue = [2, 4]
  → clone[1].neighbors = [clone[2], clone[4]]
Step 3: Process 2, neighbors = [1, 3]
  → 1 already cloned → just link
  → clone[3] = Node(3), queue = [4, 3]
  → clone[2].neighbors = [clone[1], clone[3]]
... (continue until all nodes processed)

Result: 完整的深拷贝，没有任何共享节点
```

---

### ⏱ Complexity
- **Time**: O(V + E) — visit every vertex and edge once
- **Space**: O(V) — cloned mapping + queue

---

### 🔁 与本 Block 其他题的比较 / Variations in This Block

| 题目 | 核心变化 | vs Clone Graph |
|------|---------|---------------|
| #200 Number of Islands | grid + mark visited in-place | 无需映射表 |
| #695 Max Area of Island | grid + track count | 无需映射表 |
| **#133 Clone Graph** | **old→new mapping is BFS** | **今天的题** |
| #994 Rotting Oranges | BFS with time steps | 多源 BFS |
| #207 Course Schedule | 有向图 + 检测环 | 拓扑排序 |

**举一反三**：如果要克隆一棵二叉树，是同样的思路 — 用 `old → new` 映射。但树没有环，不需要 visited 检查。

---

### 📚 References
- https://leetcode.com/problems/clone-graph/
- https://www.youtube.com/watch?v=mQeF6bN8hMk
- https://cp-algorithms.com/graph/breadth-first-search.html

### 🧒 ELI5
你有一张手绘的人脉关系图（每个人认识哪些人）。有人让你复印一份，但**不能用同一张纸**——必须画全新的。你从任意一个人开始，把他画到新纸上，然后一个一个走遍他认识的所有人，每人都画新的，直到所有人都画完。用一张便条纸记住"旧的→新的"对应关系，防止重复画。

You have a hand-drawn social network. Someone asks for a copy — but not a photocopy, a completely **redrawn** version. Start from one person, draw them on the new page, then walk through everyone they know, drawing each fresh. Keep a sticky note of "original → copy" mappings so you never draw the same person twice.
