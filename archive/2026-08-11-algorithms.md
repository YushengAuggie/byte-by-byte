# 💻 算法 / Algorithms — Day 112
## #210 Course Schedule II 🟡 Medium — Graphs (9/13)

🧩 **图遍历模式 (9/13)** — building on the BFS/DFS template from Day 101

今天的变体: 拓扑排序 + 返回实际顺序（不只是判断是否有环）
Today's variation: Topological sort + return actual ordering (not just cycle detection)

---

## 🔗 Links
- 🔗 [LeetCode #210](https://leetcode.com/problems/course-schedule-ii/) 🟡
- 📹 [NeetCode Video](https://www.youtube.com/watch?v=Akt3glAwyfY)

---

## 真实场景 / Real-World Analogy

想象你是一个 CI/CD 系统，要决定微服务的部署顺序：
- 服务 B 依赖服务 A（A 必须先部署）
- 服务 C 依赖 A 和 B
- 如果有循环依赖 → 部署死锁！

Imagine you're a CI/CD system deciding microservice deployment order:
- Service B depends on A (A must deploy first)
- Service C depends on A and B  
- Circular dependency → deployment deadlock!

**这就是 Course Schedule II 的本质。**

---

## 问题描述 / Problem

给你 `n` 门课和先修关系 `prerequisites`，返回修完所有课的顺序。如果无法完成（存在环），返回空数组。

```
Input: numCourses = 4
prerequisites = [[1,0],[2,0],[3,1],[3,2]]

0 → 1 → 3
0 → 2 → 3

Output: [0,2,1,3] or [0,1,2,3]
```

---

## 方法：拓扑排序 (Kahn's Algorithm — BFS)

**核心洞察 / Key Insight**: 入度为 0 的节点 = "没有前置依赖" = 可以最先修

```python
from collections import deque, defaultdict

def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    # Build graph + in-degree count
    graph = defaultdict(list)   # course -> [dependents]
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)  # prereq -> course
        in_degree[course] += 1        # course has one more dependency
    
    # Start with all courses that have no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)          # ✅ take this course
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1     # prereq satisfied
            if in_degree[next_course] == 0:
                queue.append(next_course)   # ready to take!
    
    # If we ordered all courses, no cycle; else cycle exists
    return order if len(order) == numCourses else []

# Trace for [[1,0],[2,0],[3,1],[3,2]]:
# graph: {0:[1,2], 1:[3], 2:[3]}
# in_degree: [0, 1, 1, 2]
# queue: [0]  ← only course 0 has no prereqs
# 
# pop 0 → order=[0], unblock 1 (in[1]=0) and 2 (in[2]=0) → queue=[1,2]
# pop 1 → order=[0,1], unblock 3 (in[3]=1) → queue=[2]
# pop 2 → order=[0,1,2], unblock 3 (in[3]=0) → queue=[3]
# pop 3 → order=[0,1,2,3]
# len(order)==4 ✓ → return [0,1,2,3]
```

**复杂度 / Complexity**: Time O(V+E), Space O(V+E)

---

## 与昨天 Course Schedule (#207) 的区别 / vs Day 111

| | #207 Course Schedule | #210 Course Schedule II |
|--|--|--|
| 目标 | 能否完成所有课？(bool) | 返回修课顺序 (list) |
| 关键变化 | 只需检测环 | 需要记录访问顺序 |
| 实现差异 | `return len(taken) == n` | `return order if len == n else []` |

**模式变体规律**: 同样的 BFS 拓扑排序骨架，只是多存了一个 `order` 列表。

---

## 举一反三 / Pattern Connections

本模式还包括:
- **#207 Course Schedule** (8/13) — 昨天: 只判断环，用 DFS
- **#261 Graph Valid Tree** (10/13) — 下一题: 判断是否为树（无环且连通）
- **#323 Number of Connected Components** (11/13) — Union-Find 更优

**触发信号**: "返回依赖安装顺序" / "构建任务编排" / "任务调度"

---

## 📝 Quiz

```json
{"question":"Course Schedule II 中，当一个节点的 in_degree 降为 0 时，意味着什么？","options":["该节点形成了环","该节点的所有前置课程都已完成","该节点没有后继课程","该节点是图的终点"],"correct_index":1}
```

/tmp/bbb-quiz-2.json written above.

---

## 📚 References
- [Kahn's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm)
- [NeetCode Graphs Playlist](https://neetcode.io/roadmap)
- [Topological Sort — GeeksForGeeks](https://www.geeksforgeeks.org/topological-sorting/)

## 🧒 ELI5
学课程就像做饭的顺序：要做咖喱，先要切洋葱，切洋葱前要买菜。把"没有前提"的事先做，做完之后看看解锁了哪些新步骤，一直到全部做完。如果有"A等B，B等A"的死循环，那就没法做了。

Like cooking: curry requires chopped onions, which requires buying groceries. Start with tasks that have no prerequisites. As you finish each, see what new tasks are now unlocked. If A waits for B and B waits for A — deadlock, nothing gets done.
