# 💻 算法 / Algorithms — Day 96
## #332 Reconstruct Itinerary (Hard) — Advanced Graphs (4/6)

🧩 **高级图算法模式 (4/6)** — building on the template from Days 118–121

> Block so far: Min Cost to Connect All Points (Prim's) → Network Delay Time (Dijkstra) → Cheapest Flights Within K Stops (Bellman-Ford) → **今天：Reconstruct Itinerary (Eulerian Path)**

**关键变化 / What's Different Today:**
前三题都是"最优路径"问题，用 Dijkstra 或 Bellman-Ford。今天这题是**遍历每条边恰好一次**——这是欧拉路径（Eulerian Path），需要 Hierholzer 算法，不是 Dijkstra！这是 Advanced Graphs 块里最大的模式转变。

---

🔗 [LeetCode #332](https://leetcode.com/problems/reconstruct-itinerary/) 🔴 Hard
📹 [NeetCode Video](https://neetcode.io/problems/reconstruct-itinerary)

---

## 现实类比 → 问题

**类比：** 你有一堆机票，每张都必须用上。必须从 JFK 出发，构造字母序最小的行程。机票是有向边，机场是节点。

**问题：** 给定 `tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]`，返回 `["JFK","MUC","LHR","SFO","SJC"]`。

**关键约束：**
1. 必须用完所有机票（每条边恰好走一次）→ **Eulerian Path**
2. 多解时取字母序最小 → 邻居排序

---

## 从模式模板到这题的映射

```
Dijkstra 模板中的 dist[] → 这里不需要（不求最短路）
Dijkstra 的 heapq → 变成排序的 deque/list（按字母序弹出）
"找最优" → 变成 "后序 DFS + 结果反转"
```

**Hierholzer 算法核心：**
- DFS 深入，直到走投无路
- 走投无路时，把当前节点加入**结果尾部**（post-order）
- 最后反转结果 → 欧拉路径

---

## Python 解法 + 逐步 Trace

```python
from collections import defaultdict

def findItinerary(tickets):
    # Build adjacency list (sorted for lexical order)
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):  # reverse sort so we can pop() from end
        graph[src].append(dst)
    
    result = []
    
    def dfs(airport):
        while graph[airport]:
            next_dst = graph[airport].pop()  # smallest lexical (we added in reverse)
            dfs(next_dst)
        result.append(airport)  # post-order: add when no more outgoing edges
    
    dfs("JFK")
    return result[::-1]  # reverse to get correct order

# Trace: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
# graph: JFK→[SFO,ATL], SFO→[ATL], ATL→[SFO,JFK]  (sorted desc, pop gives smallest)
# 
# dfs(JFK) → pop ATL → dfs(ATL)
#   dfs(ATL) → pop JFK → dfs(JFK)
#     dfs(JFK) → pop SFO → dfs(SFO)
#       dfs(SFO) → pop ATL → dfs(ATL)
#         dfs(ATL) → pop SFO → dfs(SFO)
#           dfs(SFO) → no neighbors → result.append(SFO)
#         result.append(ATL)
#       result.append(SFO)  ← wait, SFO already returned
#     result.append(JFK)
#   result.append(ATL)
# result.append(JFK)
# result (reversed) = ["JFK","ATL","JFK","SFO","ATL","SFO"] ✓
```

**时间复杂度：** O(E log E) — 排序边  
**空间复杂度：** O(V + E)

---

## 为什么后序 + 反转？

直觉：如果你遇到"死路"（dead end），那个节点只能是路径的**最后一站**。后序遍历保证了死路节点先入 result，反转后它们在末尾。

```
有死路的图：
JFK → A → B（死路）
JFK → C → A

正序 DFS 先进死路 B → post-order: B, A, ...
反转后 A 在 B 前面 ✓
```

---

## 举一反三：与同块其他题的关系

| 题目 | 核心算法 | 关键问题 |
|------|---------|---------|
| Min Cost All Points | Prim's/Kruskal | 最小生成树，无向 |
| Network Delay Time | Dijkstra | 单源最短路，有向 |
| Cheapest Flights K Stops | Bellman-Ford | 限制步数的最短路 |
| **Reconstruct Itinerary** | **Hierholzer DFS** | **每条边走一次** |
| Swim in Rising Water (next) | Dijkstra/Binary Search | 最小化最大值 |

---

## Quiz
```json
{"question":"Reconstruct Itinerary 中，为什么把节点加入 result 要用 post-order（后序）？","options":["A: 字母序小的先处理","B: 走投无路的节点必须放路径末尾，后序+反转保证正确顺序","C: DFS 天然就是后序","D: 避免重复访问节点"],"correct_index":1}
```

---

## 📚 References
- [Hierholzer's Algorithm — CP-Algorithms](https://cp-algorithms.com/graph/euler_path.html)
- [NeetCode Reconstruct Itinerary](https://neetcode.io/problems/reconstruct-itinerary)
- [Eulerian Path — Wikipedia](https://en.wikipedia.org/wiki/Eulerian_path)

## 🧒 ELI5
想象你要用完所有路线卡，每张用一次，从家出发。如果你遇到走投无路了，那个地方一定是终点。把所有"走投无路"的地方按顺序记下来，倒过来读，就是你的完整行程！
