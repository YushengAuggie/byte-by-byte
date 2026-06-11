# Day 63 — 算法 / Algorithms

💻 **算法 / Algorithms** · Day 63 · Expert Phase

---

## 🧩 树遍历模式 (8/15) — 在 Day 56 模版基础上进化 / Building on Template from Day 56

🔗 [LeetCode #102 — Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) 🟡 Medium  
📹 [NeetCode Video](https://neetcode.io/solutions/binary-tree-level-order-traversal)

---

### 这道题与模板的关系 / How This Maps to the Template

之前几天的树问题都用 **DFS 递归**模板:
```python
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

**今天的变体:这是树遍历模式里的"另一面" — BFS 层序遍历。**  
当问题关心**层级/距离/最短路径**时,DFS 不够用,要换成 **BFS + 队列**。这是树模式必须掌握的第二个工具。

*Today's variation flips the template: when a problem cares about levels, distance, or "closest" — switch from DFS recursion to BFS with a queue.*

---

### 真实场景 / Real-World Analogy

想象公司组织架构图,你想知道"每一层级有哪些人":CEO 是第 0 层,直接下属是第 1 层,以此类推。你不会深挖一条线到底(DFS),而是**一层一层横扫**(BFS)。

*An org chart where you list everyone level by level — CEO, then all VPs, then all directors. You sweep horizontally, not dive deep.*

---

### 问题描述 / Problem

给定二叉树根节点,返回**层序遍历**结果:`[[level0], [level1], ...]`,每个子列表是该层从左到右的节点值。

*Return the level-order traversal: a list of lists, one per level, left to right.*

---

### 核心洞察 / Key Insight

BFS 用队列,但关键技巧是:**每次循环开始时记录当前队列长度 `n`,只处理这 `n` 个节点** — 它们恰好是同一层。处理完这一层,队列里剩下的就是下一层。

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        n = len(queue)          # 当前层节点数 / size of this level
        level = []
        for _ in range(n):      # 只处理这一层
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

**Trace** (树 `[3,9,20,null,null,15,7]`):
- 队列 `[3]` → n=1 → level `[3]`,入队 9,20
- 队列 `[9,20]` → n=2 → level `[9,20]`,入队 15,7
- 队列 `[15,7]` → n=2 → level `[15,7]`
- 结果 `[[3],[9,20],[15,7]]` ✅

**复杂度:** Time O(n) 每个节点访问一次;Space O(n) 队列最多装一整层(最坏 n/2 个叶子)。

---

### 举一反三 / Connect to the Pattern Block

同一个 BFS 框架,改几行就能解:
- **#199 Right Side View** — 每层取最后一个 (`level[-1]`)
- **#1448 Count Good Nodes** — BFS 时带上路径最大值
- **#116 Connect Next Right Pointers** — 用同层关系串指针
- 任何"最短路径/最近"的树/图问题 → 优先想 BFS

> **DFS vs BFS 选择信号:** 关心"整棵子树的聚合值"→ DFS;关心"层级/最短/最近"→ BFS。

---

### 📚 References
- [LeetCode #102](https://leetcode.com/problems/binary-tree-level-order-traversal/)
- [Python collections.deque docs](https://docs.python.org/3/library/collections.html#collections.deque)

🧒 **ELI5:** 像剥洋葱一样,一层一层地数树上的果子,先数最上面一排,再数下面一排。
