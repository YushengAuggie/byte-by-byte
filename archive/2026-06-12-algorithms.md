# Day 64 — Algorithms: #199 Binary Tree Right Side View (Medium)

💻 **算法 / Algorithms** — #199 Binary Tree Right Side View (Medium)

🧩 **树遍历模式 (9/15)** — building on the DFS/BFS template from Day 56

---

## 今日问题与模式 / Today's Problem & Pattern

前面 8 道树题 (Invert → LCA) 主要用 **DFS 递归**。今天的「右视图」有个关键转折——我们需要 **层级信息** (每层最后一个节点)，这让 **BFS (层序遍历)** 成为更自然的选择。这正是对模式的变奏：同一棵树，换个遍历视角。

The previous 8 tree problems primarily used **DFS recursion**. Today's "right side view" has a key twist — we need **level information** (last node per level), making **BFS (level-order traversal)** the more natural fit. This is the pattern variation: same tree, different traversal perspective.

🔗 [LeetCode #199](https://leetcode.com/problems/binary-tree-right-side-view/) 🟡 Medium  
📹 [NeetCode Solution](https://neetcode.io/problems/right-side-view-of-a-binary-tree)

---

## 真实类比 / Real-World Analogy

想象你站在一棵树的 **正右侧**，从上往下看。每层你只能看到最右边的那个节点——左边的节点被遮住了。这就是「右视图」：每层最右边的节点的值。

Imagine standing to the **right side** of a tree, looking in. For each level, you can only see the rightmost node — the left ones are blocked. That's the right side view: the value of the rightmost node at each level.

```
     1            ← 看到 1 (只有一个节点)
    / \
   2   3          ← 看到 3 (最右)
    \   \
     5   4        ← 看到 4 (最右)

输出: [1, 3, 4]
```

---

## 方法对比 / Approach Comparison

### 方法 1：BFS (推荐)
每层处理完取最后一个节点 → 自然对应「右视图」语义

### 方法 2：DFS (更优雅，但反直觉)
先遍历右子树，用 depth 追踪当前层，首次访问某 depth 时即为右视图节点。

---

## BFS 解法 / BFS Solution

```python
from collections import deque
from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rightSideView(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)  # snapshot current level size
        
        for i in range(level_size):
            node = queue.popleft()
            
            # Only record the LAST node in this level
            if i == level_size - 1:
                result.append(node.val)
            
            # Add children for next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result
```

### 执行追踪 / Execution Trace
```
Tree:     1
         / \
        2   3
         \   \
          5   4

Initial queue: [1]

Level 0: size=1, process node 1 → i=0 == size-1 → append 1. Add children: 2, 3
Level 1: size=2, process node 2 (i=0, skip), process node 3 (i=1 == size-1 → append 3). Add 5, 4
Level 2: size=2, process node 5 (i=0, skip), process node 4 (i=1 == size-1 → append 4)

Result: [1, 3, 4] ✓
```

---

## DFS 解法 / DFS Solution (Bonus — More Elegant)

```python
def rightSideView_dfs(root: Optional[TreeNode]) -> List[int]:
    result = []
    
    def dfs(node, depth):
        if not node:
            return
        
        # If visiting this depth for the FIRST time (right-first DFS)
        # then this is the rightmost node at this depth
        if depth == len(result):
            result.append(node.val)
        
        # Visit RIGHT first so right nodes are recorded first
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)
    
    dfs(root, 0)
    return result
```

**核心洞察**：先遍历右子树 + 用 `depth == len(result)` 判断是否是该层首次访问 = 自动只记录最右节点。  
**Key Insight**: Visit right first + `depth == len(result)` as "first visit" check = automatically only records rightmost nodes.

---

## 复杂度 / Complexity

| 解法 | Time | Space |
|------|------|-------|
| BFS | O(n) | O(w) w=最宽层节点数 |
| DFS | O(n) | O(h) h=树高 |

- 平衡树：BFS 空间 O(n/2)，DFS 空间 O(log n)  
- 链状树：BFS 空间 O(1)，DFS 空间 O(n)

---

## 举一反三 / Pattern Connections

这道题是 #102 Binary Tree Level Order Traversal (Day 63) 的直接变体：
- #102 记录每层所有节点 → #199 只记录每层最后一个节点
- 同样的 BFS 骨架，只改了 `result.append` 的条件

连接整个树遍历 Block：
- **#226 Invert** → 修改树结构
- **#102 Level Order** → 层级处理 (BFS)
- **#199 Right Side View** → 层级处理变体 ← 今天
- **#104/#543** → 递归收集信息 (DFS)
- **#235 LCA** → 路径问题 (DFS)

---

## 📚 References
- https://leetcode.com/problems/binary-tree-right-side-view/
- https://neetcode.io/problems/right-side-view-of-a-binary-tree
- https://www.geeksforgeeks.org/print-right-view-binary-tree-2/

## 🧒 ELI5
假设你站在一排树的右边，每层你只能看到最右边的那棵。BFS 就是从上往下，一层一层看，每层最后一棵就是你看到的那棵。

Imagine standing to the right of a row of trees. For each row, you only see the rightmost one. BFS is going row by row from top to bottom, and the last tree in each row is what you see.
