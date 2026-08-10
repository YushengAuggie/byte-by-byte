# 💻 算法 / Algorithms — Day 87: #207 Course Schedule (Medium) — Graphs

🧩 **图遍历模式 (8/13)** — building on the template from Day 101 (Number of Islands)

今天是图遍历第 8 题，这是一个**拓扑排序**的经典应用。
Today is Graph block problem 8/13 — classic **topological sort** application.

---

## 问题 / Problem

🔗 [LeetCode #207](https://leetcode.com/problems/course-schedule/) 🟡 Medium  
📹 [NeetCode Solution](https://neetcode.io/problems/course-schedule)

**给你 n 门课程，prerequisites[i] = [a, b] 表示学 a 前必须先学 b。问能否完成所有课程？**
Given n courses and prerequisites[i] = [a, b] meaning you must take b before a. Can you finish all courses?

---

## 现实类比 / Real-World Analogy

想象你在设计一个 CI/CD pipeline：
Imagine designing a CI/CD pipeline:

- `deploy` 依赖 `test`，`test` 依赖 `build`
- 如果 `build` 又依赖 `deploy` → **循环依赖！pipeline 无法执行**
- 同理，课程的循环依赖（课程 A 需要 B，B 需要 A）= 无法完成

**本质：检测有向图中是否有环 / Detect cycle in directed graph**

---

## 这道题如何套用模板 / Mapping to Pattern

标准 BFS 模板处理的是"找到什么"，这道题用 **BFS + 入度（Kahn's Algorithm）**：

```
核心变化 (vs. 标准 BFS):
- 不从随机节点出发，从入度为 0 的节点出发（没有先决条件的课）
- 每处理一个节点，把邻居入度 -1
- 如果邻居入度变 0，加入队列
- 最后：如果处理了所有节点 → 无环 ✅；否则有环 ❌
```

---

## Python 解法 / Solution

```python
from collections import deque, defaultdict

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    # Build adjacency list + in-degree count
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)  # prereq → course
        in_degree[course] += 1
    
    # Start with all courses that have no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    completed = 0
    
    while queue:
        node = queue.popleft()
        completed += 1                  # "取完"这门课
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1   # 先决条件满足，入度 -1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return completed == numCourses      # 全部完成 = 无环
```

**执行轨迹 / Trace (3 courses: [[1,0],[2,1]]):**
```
prereqs: 0→1→2 (linear chain)
in_degree: [0, 1, 1]
queue: [0]  (only 0 has no prereq)

Step 1: pop 0, completed=1, neighbor 1: in_degree[1]=0 → add to queue
Step 2: pop 1, completed=2, neighbor 2: in_degree[2]=0 → add to queue  
Step 3: pop 2, completed=3

completed(3) == numCourses(3) → True ✅
```

**复杂度 / Complexity:** Time O(V+E), Space O(V+E)

---

## 举一反三 / Connect to Pattern Block

| 题目 | 图类型 | 核心变化 |
|------|--------|---------|
| #200 Number of Islands | 网格图 | BFS 标记连通区域 |
| #994 Rotting Oranges | 网格图 | 多源 BFS 计层数 |
| **#207 Course Schedule** | **有向图** | **BFS + 入度（拓扑排序）** |
| #210 Course Schedule II | 有向图 | 拓扑排序返回顺序 |
| #127 Word Ladder | 隐式图 | BFS 找最短转换路径 |

**关键区别：**
- 无向图 BFS → 用 `visited` 防重复
- 有向图拓扑 → 用 `in_degree` 决定入队顺序

---

## 📝 Quiz

```json
{"question":"Course Schedule 中，如果最终 completed < numCourses，说明什么？","options":["所有课程都可以完成","图中存在环（循环依赖）","图的边数不够","起始节点选错了"],"correct_index":1}
```

---

## 📚 References
- https://leetcode.com/problems/course-schedule/
- https://neetcode.io/problems/course-schedule
- https://cp-algorithms.com/graph/topological-sort.html

## 🧒 ELI5
像玩积木：先找没有放在其他积木上面的（入度 0），把它拿走，再找下一个自由的。如果最后还有积木拿不到（因为相互压着），就说明有循环，游戏无法完成。
