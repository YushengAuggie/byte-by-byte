# 💻 Day 116 — Algorithms
> #684 Redundant Connection — Medium — Graphs (12/13)

---

# 💻 算法 / Algorithms — #684 Redundant Connection 🟡

🧩 **图遍历模式 (12/13)** — building on the BFS/DFS template from Day 101

---

## 题目 / Problem

🔗 [LeetCode #684](https://leetcode.com/problems/redundant-connection/) 🟡 Medium
📹 [NeetCode Solution](https://neetcode.io/problems/redundant-connection)

给定一个 n 个节点的**无向图**，最初是一棵树（无环）。有一条额外的边被加入，使得图中存在一个环。找出并返回这条**多余的边**。

*Given an undirected graph that was originally a tree, find the one extra edge that creates a cycle. Return it.*

---

## 真实类比 / Real-World Analogy

想象公司组织架构图（树结构）。某人同时汇报给两个老板 — 这就产生了一个"环"。你需要找出哪条汇报关系是多余的（后加入的）。

*Company org chart: normally a tree. Someone reports to two managers — that creates a cycle. Find the redundant reporting relationship.*

---

## 这道题 vs 模板的不同 / How It Differs from Base Template

普通 BFS/DFS 探索整个图；这道题需要**增量检测环**：
- 每次加入一条边，检查两端节点是否已连通
- 已连通 → 这条边就是多余的
- 最优解：**Union-Find（并查集）**，不是纯 BFS/DFS

---

## Union-Find 解法 / Solution

```python
class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        n = len(edges)
        parent = list(range(n + 1))  # parent[i] = i initially
        rank = [1] * (n + 1)

        def find(x):
            # Path compression: flatten the tree as we find root
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # halving
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return False  # already connected → redundant edge!
            # Union by rank: attach smaller tree under larger
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            rank[rx] += rank[ry]
            return True

        for u, v in edges:
            if not union(u, v):
                return [u, v]
        return []
```

---

## 执行追踪 / Trace

```
edges = [[1,2],[1,3],[2,3]]

初始: parent = [0,1,2,3]

union(1,2): find(1)=1, find(2)=2 → different → merge → parent[2]=1
union(1,3): find(1)=1, find(3)=3 → different → merge → parent[3]=1
union(2,3): find(2)=find(1)=1, find(3)=find(1)=1 → SAME! → return [2,3]
```

---

## 复杂度 / Complexity

- **Time:** O(n · α(n)) — α是反阿克曼函数，近似O(1)
- **Space:** O(n)

---

## 举一反三 / Pattern Block Connections

| 题目 | 用到的图技术 |
|------|------------|
| #200 Number of Islands | DFS/BFS flood fill |
| #207 Course Schedule | DFS cycle detection (directed) |
| #261 Graph Valid Tree | Union-Find / DFS |
| **#684 Redundant Connection** | **Union-Find 增量** |
| #127 Word Ladder (next!) | BFS shortest path |

> 关键洞察：Union-Find 擅长**增量连通性检测**；BFS/DFS 适合一次性探索

---

## Quiz

```json
{"question":"In Union-Find, what does 'path compression' do?","options":["Removes edges from the graph","Makes every node point directly to root during find()","Compresses the graph into fewer nodes","Sorts nodes by their rank"],"correct_index":1}
```

---

## 📚 References

- [Union-Find — CP-Algorithms](https://cp-algorithms.com/data_structures/disjoint_set_union.html)
- [NeetCode Graphs Playlist](https://neetcode.io/roadmap)

## 🧒 ELI5

想象一群小朋友玩"找朋友"游戏。Union-Find 就像给每个小朋友一个队长。两人握手时，先检查他们是否已经是同一队的——是的话，这次握手就多余了！
