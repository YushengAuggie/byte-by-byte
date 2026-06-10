# 💻 算法 / Algorithms — Day 61
**Topic:** #572 Subtree of Another Tree (Easy) — Trees Pattern
**Date:** 2026-06-09 | **Phase:** Expert

---

## 💻 算法 / Algorithms
### 🧩 树遍历模式 (6/15) — building on the template from Day 56

今天是树遍历模式第 6 题。前几题（Invert, Max Depth, Diameter, Balanced, Same Tree）都是在练习 DFS 递归的不同"返回值语义"。今天的题把 **Same Tree** 作为子程序来用 — 这是模式复用的典型例子。

This is problem 6/15 in the Trees block. Previous problems trained DFS with different return semantics. Today we **reuse Same Tree as a subroutine** — a classic example of pattern composition.

---

🔗 [LeetCode #572](https://leetcode.com/problems/subtree-of-another-tree/) 🟢 Easy
📹 [NeetCode Video](https://neetcode.io/problems/subtree-of-a-binary-tree)

---

### 🌍 现实类比 / Real-World Analogy

你在 git 历史中搜索一个特定的 commit subtree 结构。`git log --all` 遍历每个 commit 节点，然后检查从那个节点开始的子树是否和目标结构完全匹配。

You're searching git history for a specific commit subtree structure. You walk every commit, then check if the subtree rooted there matches your target exactly.

---

### 📋 题目 / Problem

```
给定两棵二叉树 root 和 subRoot。
判断 subRoot 是否是 root 的某个子树（结构和值都相同）。

Given two binary trees root and subRoot.
Return true if there is a subtree of root with the same
structure and node values as subRoot, false otherwise.

Example:
root =    [3,4,5,1,2]     subRoot = [4,1,2]
         3                          4
        / \                        / \
       4   5                      1   2
      / \
     1   2
→ true (subtree rooted at 4 matches)
```

---

### 🗺️ 映射到模板 / Mapping to Template

```python
# 树遍历模板:
# def dfs(node):
#     if not node: return BASE_CASE
#     left = dfs(node.left)
#     right = dfs(node.right)
#     return COMBINE(node.val, left, right)

# 今天的题需要两层 DFS:
# 1. 外层 DFS: 遍历 root 的每个节点
# 2. 内层 DFS (isSameTree): 从某节点检查是否完全匹配 subRoot
```

**与 Day 60 (Same Tree) 的区别:**
- Same Tree: 检查两棵树从根开始是否完全相同 → 单层 DFS
- Subtree: 检查 root 的 **任意节点** 开始是否匹配 → 双层 DFS

---

### 🐍 Python 解法 / Solution

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        # BASE CASE: subRoot is None → empty tree is always a subtree
        if not subRoot:
            return True
        # If root is exhausted but subRoot isn't, no match
        if not root:
            return False
        
        # Check if current root matches subRoot exactly
        if self.isSameTree(root, subRoot):
            return True
        
        # Otherwise, try left or right subtree (DFS traverse root)
        return (self.isSubtree(root.left, subRoot) or 
                self.isSubtree(root.right, subRoot))
    
    def isSameTree(self, s: Optional[TreeNode], t: Optional[TreeNode]) -> bool:
        # Reuse Same Tree logic from Day 60!
        if not s and not t:
            return True
        if not s or not t:
            return False
        return (s.val == t.val and 
                self.isSameTree(s.left, t.left) and 
                self.isSameTree(s.right, t.right))
```

**执行追踪 / Trace:**
```
root = [3,4,5,1,2], subRoot = [4,1,2]

isSubtree(3, 4):
  isSameTree(3,4)? → 3≠4 → False
  isSubtree(4, 4):
    isSameTree(4,4)?
      4==4 ✓
      isSameTree(1,1)? → True ✓
      isSameTree(2,2)? → True ✓
    → True! ✓
  → return True
```

---

### ⏱️ 复杂度 / Complexity

```
Time:  O(m × n)  — m = root nodes, n = subRoot nodes
                  — 每个 root 节点都可能触发一次 isSameTree
Space: O(h)      — h = height of root (recursion stack)

优化思路 (面试 follow-up):
- Serialize trees → string matching → O(m+n) time
- Hashing subtrees → O(m+n) time
  (但实现复杂，Easy 题不需要)
```

---

### 🔁 举一反三 / Pattern Connections

在这个树遍历模式块中:

| 题目 | 核心操作 | 返回值语义 |
|------|---------|----------|
| #226 Invert Tree | 左右互换 | 返回修改后的节点 |
| #104 Max Depth | 取最大深度 | 返回整数（深度） |
| #543 Diameter | 经过节点的最长路径 | 返回深度，副作用更新全局 |
| #110 Balanced | 检查高度差 | 返回高度，-1 表示不平衡 |
| #100 Same Tree | 比较结构+值 | 返回 bool |
| **#572 Subtree** | **Same Tree 作为子程序** | **返回 bool，双层 DFS** |

**关键洞察:** 遇到"检查某属性是否存在于树中某处"→ 外层 DFS 遍历 + 内层 DFS 检查。

---

### 📚 References

- [LeetCode #572](https://leetcode.com/problems/subtree-of-another-tree/)
- [NeetCode Solution](https://neetcode.io/problems/subtree-of-a-binary-tree)
- [LeetCode Editorial](https://leetcode.com/problems/subtree-of-another-tree/editorial/)

---

### 🧒 ELI5

你想知道你的积木堆里，有没有一个角落和你朋友的积木堆一模一样。你从最顶上开始检查每一块积木，每次都问：从这块积木开始，是不是和朋友的一模一样？（用昨天学的 Same Tree 来问）。只要有一个角落匹配，就返回 true。

You want to know if any corner of your Lego pile looks exactly like your friend's pile. You check each brick one by one, and for each brick, you ask: "Does everything starting from here match my friend's pile?" (using the Same Tree check from yesterday). If any corner matches — you win!
