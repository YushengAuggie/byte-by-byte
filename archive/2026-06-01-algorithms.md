# 算法：二叉树最大深度 / Maximum Depth of Binary Tree

> 📅 Day 56 · 💻 LeetCode #104 · 🟢 Easy · Expert Phase

---

## 💻 算法 / Algorithms

🧩 **树遍历模式 (2/15)** — building on the template from Day 55 (Invert Binary Tree)

今天是树遍历 Pattern Block 的第 2 题。上一题 Invert Binary Tree 教会我们：**后序遍历 + 返回处理好的节点**。今天我们换一种返回值语义：**返回数值（深度）而不是节点**。

*This is problem 2/15 in the Trees pattern block. Yesterday's Invert Binary Tree taught us: post-order traversal + return processed node. Today we change the return type: return a number (depth) instead of a node.*

---

### 🔗 Links
- 📝 [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) 🟢 Easy
- 📹 [NeetCode Video](https://neetcode.io/problems/depth-of-binary-tree)

---

### 现实类比 / Real-World Analogy

想象你是一个侦察员，要测量一棵树的高度。你的策略：**先让左右两个助手各自测量子树高度，然后取最大值 +1（加上你站的这一层）**。你不需要知道整棵树的结构，只需要递归地信任你的助手。

*Imagine you're a scout measuring a tree's height. Your strategy: send left and right assistants to measure sub-tree heights, then take the max + 1 (for your current level). You don't need to know the full tree structure — just recursively trust your assistants.*

---

### 模版映射 / Template Mapping

```python
# 通用模版 / Universal template:
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)

# 今天的映射 / Today's mapping:
# BASE_CASE = 0       (空节点深度为0)
# COMBINE = max(left, right) + 1   (取最大子深度 + 当前层)
```

---

### Python 解法 / Solution

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root: Optional[TreeNode]) -> int:
    # Base case: empty tree has depth 0
    if not root:
        return 0
    
    # Recursively get depth of left and right subtrees
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    # Current depth = max of children + 1 (for current node)
    return max(left_depth, right_depth) + 1

# Alternative: BFS (level-order) approach
from collections import deque

def maxDepthBFS(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    
    queue = deque([root])
    depth = 0
    
    while queue:
        depth += 1
        # Process entire level at once
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return depth
```

---

### 执行追踪 / Trace

```
Tree:       3
           / \
          9   20
             /  \
            15    7

maxDepth(3):
  left  = maxDepth(9)
            left  = maxDepth(None) → 0
            right = maxDepth(None) → 0
            → max(0, 0) + 1 = 1
  right = maxDepth(20)
            left  = maxDepth(15)
                        → max(0, 0) + 1 = 1
            right = maxDepth(7)
                        → max(0, 0) + 1 = 1
            → max(1, 1) + 1 = 2
  → max(1, 2) + 1 = 3 ✅
```

---

### 复杂度 / Complexity

| | DFS | BFS |
|--|-----|-----|
| Time | O(n) — visit every node once | O(n) |
| Space | O(h) — call stack, h = height | O(w) — queue, w = max width |

**DFS vs BFS 选哪个？**
- 平衡树：DFS space O(log n)，BFS O(n/2) → 用 DFS
- 极度倾斜树 (skewed)：DFS space O(n)（相当于链表），BFS O(1) → 用 BFS
- 实际面试：DFS 更简洁，通常优先

---

### 🔄 Pattern 变体 / Pattern Variations

与同一 Block 的其他题对比 — **同样的模板，不同的 COMBINE 函数**：

| 题目 | BASE_CASE | COMBINE |
|------|-----------|---------|
| #226 Invert | None | swap left/right, return node |
| **#104 Max Depth** | **0** | **max(left, right) + 1** |
| #543 Diameter | 0 | diameter = max(diameter, left+right); return max(left,right)+1 |
| #110 Balanced | 0 | if abs(left-right)>1: return -1; else return max+1 |

看到规律了吗？**模板不变，只改 COMBINE 逻辑。** 这就是模式学习的威力。

---

### 📚 References
- [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
- [NeetCode Solution](https://neetcode.io/problems/depth-of-binary-tree)
- [Visualize tree recursion](https://visualgo.net/en/bst)

### 🧒 ELI5

问树有多高？让左边的小助手量左边，右边的小助手量右边，然后取最高的那个 +1（加上你自己这一层）。空树高度是 0。就这么简单！

*Asking how tall a tree is? Let your left helper measure the left side, right helper measure the right side, then take the taller one + 1 (for your current level). Empty tree = height 0. That's it!*
