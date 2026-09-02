# 💻 算法 / Algorithms — Day 124
**#269 Alien Dictionary** 🔴 Hard — Advanced Graphs (6/6)

🔗 https://leetcode.com/problems/alien-dictionary/
📹 https://neetcode.io/problems/foreign-dictionary

---

## 🧩 Advanced Graphs (6/6) — 收官之作！

这是 Advanced Graphs 模块最后一题。回顾一下整个 block：

| # | 题目 | 算法 |
|---|------|------|
| 1 | Min Cost Connect All Points | Prim's MST |
| 2 | Network Delay Time | Dijkstra |
| 3 | Cheapest Flights Within K Stops | Bellman-Ford / BFS+K |
| 4 | Reconstruct Itinerary | Hierholzer (Euler path) |
| 5 | Swim in Rising Water | Dijkstra / Binary Search+BFS |
| **6** | **Alien Dictionary** | **拓扑排序 Topological Sort** |

今天用的是 **Kahn's BFS topological sort** — 和 Dijkstra 一样用队列，但 **无权** + **有向无环**（DAG）。

---

## 🌍 题目理解 / Problem

外星人字典里有若干排好序的单词。根据单词排列推断字母的字典序。

```
Input: ["wrt","wrf","er","ett","rftt"]
Output: "wertf"
```

**类比**: 你拿到一本字典，书里单词按某种奇怪的字母顺序排好了。你能推断出字母 a < b < c 之间的关系吗？

**核心洞察**: 相邻两个单词做字典序比较，第一个不同的字符就给出一条边 `c1 → c2`（c1 在 c2 之前）。然后对所有边做拓扑排序。

---

## 🗺️ 映射到模式 / Template Mapping

今天不用 Dijkstra 模板，用 **Kahn's Topological Sort**（BFS变种）:

```python
# Kahn's Algorithm
in_degree = {c: 0 for c in chars}
graph = {c: [] for c in chars}

# Build edges from adjacent word pairs
for edge (u, v):
    graph[u].append(v)
    in_degree[v] += 1

# BFS from all zero in-degree nodes
queue = deque([c for c in in_degree if in_degree[c] == 0])
result = []
while queue:
    c = queue.popleft()
    result.append(c)
    for neighbor in graph[c]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

# Cycle detection: if result length != num chars, there's a cycle
```

---

## 🐍 完整解法 / Python Solution

```python
from collections import defaultdict, deque
from typing import List

def alienOrder(words: List[str]) -> str:
    # Step 1: Initialize all characters (every char must appear in output)
    adj = {c: set() for word in words for c in word}
    in_degree = {c: 0 for c in adj}

    # Step 2: Build graph from adjacent word pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        
        # Edge case: "abc" before "ab" is INVALID (longer prefix first)
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""  # Invalid ordering
        
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:  # avoid duplicate edges
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break  # Only first difference matters!
    
    # Step 3: Kahn's BFS topological sort
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    
    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Step 4: Cycle check
    if len(result) != len(in_degree):
        return ""  # Cycle detected = invalid
    
    return "".join(result)
```

**执行追踪 / Trace** for `["wrt","wrf","er","ett","rftt"]`:
```
wrt vs wrf → t→f  (in_degree[f]++)
wrf vs er  → w→e  (in_degree[e]++)
er  vs ett → r→t  (in_degree[t]++)
ett vs rftt→ e→r  (in_degree[r]++)

Graph: w→e, e→r, r→t, t→f
in_degree: {w:0, e:1, r:1, t:1, f:1}

Start queue: [w]
Pop w → result=[w], push e → queue=[e]
Pop e → result=[w,e], push r → queue=[r]
...
Result: "wertf" ✅
```

**复杂度**:
- Time: O(C) where C = total chars in all words
- Space: O(U + min(U², N)) where U = unique chars, N = words

---

## 🔁 举一反三 / Pattern Connections

| 题目 | 联系 |
|------|------|
| Course Schedule (#207) | 同样是拓扑排序检测环 |
| Course Schedule II (#210) | 返回拓扑排序序列 |
| Task Scheduler (#621) | 约束调度，用堆而非BFS |
| Build System (Make/Bazel) | 现实版 alien dictionary |

**关键区别**: Alien Dictionary 难在 **边的构建** 不直接给你，需要从两两比较推导。拓扑排序本身 Course Schedule 已练过。

---

## 📚 References
- https://neetcode.io/problems/foreign-dictionary
- https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
- https://cp-algorithms.com/graph/topological-sort.html

## 🧒 ELI5
想象你看到一堆英文名字，按规定顺序排好了：Alice, Bob, Charlie。你发现 A 排在 B 前面，B 排在 C 前面，所以字母顺序是 A < B < C。外星字典就是这个思路，只是字母我们不认识，要靠相邻单词"推理"出来字母谁先谁后，然后按这个顺序排好输出。
