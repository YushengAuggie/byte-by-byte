# 💻 算法 / Algorithms — Day 60
**Problem:** #297 Serialize and Deserialize Binary Tree 🔴 Hard
**Pattern:** Trees (15/15) — Final problem in the block!
**Date:** 2026-06-22

🔗 LeetCode: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
📹 NeetCode: https://neetcode.io/problems/serialize-and-deserialize-binary-tree

---

## 🧩 树遍历模式 (15/15) — 收官之作！

🧩 **Trees Pattern (15/15)** — building on the DFS template from Day 56

从第 1 题（翻转二叉树）到第 15 题（序列化/反序列化），我们完整走过了树的所有经典问题。今天是这个 block 的终点站。

**今天是变体 / Today's variation:**
不只是"遍历"树，而是需要把树完整地编码成字符串，再从字符串精确还原。核心挑战：如何区分 null 节点和有值节点？

---

## 真实场景 / Real-World Analogy

你在做分布式系统，需要把内存中的决策树发送给另一台机器执行。不能传递指针，只能传字符串或 JSON。序列化 = 把树"打印"成字符串；反序列化 = 从字符串"重建"树。

Redis 存树形结构、网络传输对象、数据库存嵌套文档 — 本质上都是这个问题。

---

## 解题思路 / Approach

**关键洞察：** 用 BFS（层序遍历）序列化，null 节点用特殊标记（如 "N"）占位。反序列化时按队列逐层重建。

也可以用 preorder DFS（前序遍历），两种方法都行，但 BFS 更直观。

```python
from collections import deque

class Codec:
    def serialize(self, root):
        # BFS serialization
        if not root:
            return ""
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            if node is None:
                result.append("N")
            else:
                result.append(str(node.val))
                queue.append(node.left)   # Push left (even if None)
                queue.append(node.right)  # Push right (even if None)
        
        # Trim trailing 'N's for cleaner output (like LeetCode format)
        while result and result[-1] == "N":
            result.pop()
        return ",".join(result)
    
    def deserialize(self, data):
        # BFS deserialization
        if not data:
            return None
        
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        queue = deque([root])
        i = 1  # Index into vals
        
        while queue and i < len(vals):
            node = queue.popleft()
            
            # Left child
            if vals[i] != "N":
                node.left = TreeNode(int(vals[i]))
                queue.append(node.left)
            i += 1
            
            # Right child
            if i < len(vals) and vals[i] != "N":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1
        
        return root
```

## 执行轨迹 / Trace

```
Tree:    1
        / \
       2   3
          / \
         4   5

serialize() BFS 遍历:
  queue: [1]       → append "1", push 2, 3
  queue: [2, 3]    → append "2", push null, null
  queue: [3, N, N] → append "3", push 4, 5
  queue: [N,N,4,5] → N, N, "4", "5"...
  result: "1,2,3,N,N,4,5"

deserialize() 重建:
  root = TreeNode(1), queue = [1]
  pop 1: left=TreeNode(2), right=TreeNode(3)
  pop 2: left=N(skip), right=N(skip)
  pop 3: left=TreeNode(4), right=TreeNode(5)
  ✅ 完整还原
```

**时间复杂度 / Complexity:**
- Time: O(n) — 每个节点访问一次
- Space: O(n) — 队列最大存一层节点，最坏 O(n/2)

---

## 与模版的映射 / Mapping to Template

标准 DFS 模板：
```
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

本题用 BFS 而非 DFS，但核心思想相同：**按某种顺序遍历每个节点，对 null 进行显式处理，保留结构信息。**

DFS 版本（preorder）也完全可行：
```python
# serialize with preorder DFS
def serialize_dfs(root):
    if not root: return "N,"
    return str(root.val) + "," + serialize_dfs(root.left) + serialize_dfs(root.right)
```

---

## 举一反三 / Pattern Connections

这是树 block 的第 15 题，回顾整个 block 的核心递推关系：
- **#226 Invert** → dfs: swap left/right, return node
- **#104 Max Depth** → dfs: return 1 + max(left, right)
- **#543 Diameter** → dfs: 全局维护 max，return 1 + max(left, right)
- **#110 Balanced** → dfs: return height or -1 if unbalanced
- **#124 Max Path Sum** (昨天) → dfs: 全局维护 max，return node.val + max(0, left, right)
- **#297 Serialize** (今天) → BFS 完整遍历，null 也要标记

**规律：** 树问题的难度提升，通常是"返回值语义"变复杂，或者需要额外的全局状态。

---

## 🧒 ELI5

想象你要把一棵家谱树打电话告诉朋友。你按层从上到下说：「1号，左边是2号，右边是3号，2号没孩子，3号左边4号右边5号。」朋友记下来，就能画出一模一样的树。序列化就是你说的那串话，反序列化就是朋友画树的过程。

---

## 📚 References
- LeetCode 297: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
- NeetCode Solution: https://neetcode.io/problems/serialize-and-deserialize-binary-tree
- BFS Tree Traversal: https://en.wikipedia.org/wiki/Breadth-first_search
