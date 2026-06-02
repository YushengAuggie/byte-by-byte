# 💻 算法 / Algorithms — Day 48
**#543 Diameter of Binary Tree (Easy) — Trees**
*2026-06-02 | Expert Phase*

---

## 🧩 树遍历模式 (3/15) — 延续上一次的模版

接续第 1 题（Invert Binary Tree）和第 2 题（Maximum Depth），今天的 **Diameter** 是模版的第一个"变奏"——DFS 返回值不再是节点值，而是**路径长度**，但核心骨架完全相同。

*Building on Invert Binary Tree (Day 1 of block) and Maximum Depth (Day 2), today's Diameter is the first "variation" — the DFS return value is no longer the node value but a path length. The skeleton is identical.*

---

## 题目 / Problem

🔗 [LeetCode #543](https://leetcode.com/problems/diameter-of-binary-tree/) 🟢 Easy
📹 [NeetCode Video](https://neetcode.io/problems/binary-tree-diameter)

给定一棵二叉树的根节点，返回这棵树的**直径**（任意两节点之间最长路径的边数）。路径**不一定**经过根节点。

*Given the root of a binary tree, return the length of the diameter — the longest path between any two nodes (measured in edges). The path may or may not pass through the root.*

---

## 🌍 现实类比 / Real-World Analogy

想象一个公司的汇报链（树形结构）。直径 = 公司里距离最远的两名员工之间需要经过多少层级。可能路径是：前端工程师 → 前端 Lead → CTO → 后端 Lead → 数据库工程师。

*Think of a company org chart. Diameter = the maximum number of levels between any two employees. The longest path might go: Frontend Dev → Frontend Lead → CTO → Backend Lead → DB Engineer.*

---

## 💡 映射到模版 / Mapping to the Template

```python
# General Tree DFS Template:
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

对于 Diameter 问题：
- `BASE_CASE` = `0`（空节点贡献 0 条边）
- `dfs(node)` 返回：从当前节点往下最多能延伸多少条边（= depth）
- `COMBINE`：**当前节点的直径候选** = `left + right`，用 nonlocal 变量 `res` 收集全局最大值
- 最终 `return max(left, right) + 1`（向父节点报告深度）

**关键洞察 / Key Insight**：`dfs` 的返回值（深度）和我们要求的答案（直径）是**不同概念**！用一个外部变量 `res` 在每个节点"路过时"更新最大直径。

---

## Python 解法 / Python Solution

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def diameterOfBinaryTree(root: Optional[TreeNode]) -> int:
    res = 0  # Track the global maximum diameter
    
    def dfs(node) -> int:
        nonlocal res
        if not node:
            return 0          # Base case: empty node has depth 0
        
        left = dfs(node.left)   # Max depth going left
        right = dfs(node.right) # Max depth going right
        
        # At this node, the diameter candidate = left + right edges
        res = max(res, left + right)
        
        # Return depth (for parent's calculation)
        return 1 + max(left, right)
    
    dfs(root)
    return res
```

### 执行追踪 / Trace
```
Tree:   1
       / \
      2   3
     / \
    4   5

dfs(4) → return 1
dfs(5) → return 1
dfs(2): left=1, right=1 → res = max(0, 1+1) = 2, return 2
dfs(3) → return 1
dfs(1): left=2, right=1 → res = max(2, 2+1) = 3, return 3

Answer: 3  (path: 4 → 2 → 1 → 3)
```

### 复杂度 / Complexity
- **Time**: O(n) — visit every node once
- **Space**: O(h) — recursion stack, h = tree height

---

## 举一反三 / Pattern Connections

同一 Trees 模版块中的变体规律：

| 问题 | dfs 返回值 | 全局变量 | 返回语义 |
|------|-----------|---------|---------|
| #104 Max Depth | 无需 | 无 | 深度 |
| **#543 Diameter** | 深度 | `res`(直径) | 深度 |
| #110 Balanced Tree (下一题) | 深度/-1 | 无 | 深度或-1标记失衡 |
| #124 Max Path Sum (Hard) | 单侧最大和 | `res`(路径和) | 单侧最大和 |

**规律**：当答案是"跨越某节点的左右子树"时，用 nonlocal 变量收集；返回值只向父汇报单侧信息。

---

## 📝 Quiz
```json
{"question":"In diameterOfBinaryTree, what does the dfs function RETURN vs what goes into 'res'?","options":["Both return the diameter","dfs returns depth; res tracks max(left+right)","dfs returns diameter; res tracks depth","dfs returns node count; res tracks edge count"],"correct_index":1}
```

---

## 📚 References
- [LeetCode #543 Official](https://leetcode.com/problems/diameter-of-binary-tree/editorial/)
- [NeetCode Trees Playlist](https://neetcode.io/courses/dsa-for-beginners/27)
- [Visualgo Binary Tree](https://visualgo.net/en/bst)

## 🧒 ELI5

树的直径就是树里最长的一条路。聪明的做法是：每到一个节点，就看左边最深有多深、右边最深有多深，两个加起来就是经过这个节点的最长路。记下所有节点的"最长路"里面最大的那个。

*The diameter is the longest path in the tree. The trick: at each node, check how deep it goes left and right, add them together (that's the path through this node), and track the maximum across all nodes.*
