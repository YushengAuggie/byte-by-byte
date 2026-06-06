# 💻 算法 / Algorithms — Day 50
## #100 Same Tree — Easy 🟢 | Trees Pattern (5/15)
> ⏱️ 预计阅读时间 / Est. read time: 4 min

---

🧩 **Trees 模式 (5/15)** — 复用 Day 54 引入的树遍历模板

Building on the **树遍历模式** template from the start of this block.

**模版回顾 / Template Recap:**
```python
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

---

## 🔗 Links
- LeetCode: https://leetcode.com/problems/same-tree/ 🟢
- NeetCode: https://www.youtube.com/watch?v=vRbbcKXCxOw

---

## 真实场景类比 / Real-World Analogy

你在做文件系统**差异比较** (diff)：两棵目录树是否完全相同？每个节点（文件/文件夹）的名字、位置都必须一样。

You're doing a **file system diff**: are two directory trees exactly identical? Every node's name and position must match.

---

## 问题分析 / Problem

给定两棵二叉树，判断它们是否**结构相同且节点值相同**。

Given two binary trees, determine if they are **structurally identical and nodes have the same values**.

```
    1             1
   / \           / \
  2   3         2   3
p = q → True

    1             1
   /               \
  2                 2
p ≠ q → False
```

---

## 映射到模版 / Map to Template

这道题是**双树同步 DFS** — 模板的自然扩展：

```
BASE_CASE: 两个都是 None → True; 一个是 None → False
COMBINE: node values 相等 AND 左子树相同 AND 右子树相同
```

---

## Python 解法 / Solution

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isSameTree(p: TreeNode, q: TreeNode) -> bool:
    # BASE CASE: both None → structurally equal at this position
    if not p and not q:
        return True
    # one is None, other isn't → mismatch
    if not p or not q:
        return False
    # COMBINE: values must match AND both subtrees must match
    return (p.val == q.val and
            isSameTree(p.left, q.left) and
            isSameTree(p.right, q.right))

# Trace example:
#       1             1
#      / \           / \
#     2   3         2   3
#
# isSameTree(1, 1):
#   1 == 1 ✓
#   isSameTree(2, 2):
#     2 == 2 ✓, isSameTree(None,None)=True, isSameTree(None,None)=True → True
#   isSameTree(3, 3):
#     3 == 3 ✓, ... → True
#   → True ✅
```

**时间复杂度 / Complexity:** O(n) time, O(h) space where h = tree height

---

## 这道题 vs 同系列 / Variation from Block

| 问题 | 关键变化 | 模版调整 |
|------|----------|----------|
| #226 Invert Binary Tree | 改变结构 | COMBINE 交换左右子树 |
| #104 Max Depth | 返回数值 | COMBINE 取 max |
| #110 Balanced | 返回高度+是否平衡 | COMBINE 返回元组 |
| **#100 Same Tree** | **双树同步** | **参数变成两个节点** |
| #572 Subtree of Another Tree (下一题) | 包含关系 | isSameTree + 递归检查 |

**注意**：下一题 #572 直接调用这道题的函数！学好这道，下道题轻松解。

**Note:** #572 literally calls `isSameTree` as a helper! Master this and the next problem is easy.

---

## 举一反三 / Pattern Connections

**双指针 DFS 模式** — 两棵树同步遍历：
- #100 Same Tree → 完全相同
- #572 Subtree → 包含关系
- #951 Flip Equivalent → 镜像等价
- #1367 Linked List in Binary Tree → 链表在树中

---

## 📚 References
- [LeetCode #100](https://leetcode.com/problems/same-tree/)
- [NeetCode Video](https://www.youtube.com/watch?v=vRbbcKXCxOw)
- [Tree traversal patterns](https://leetcode.com/discuss/study-guide/1213olo/binary-trees-study-guide)

## 🧒 ELI5

判断两棵树是否一样，就像比对两张照片：先看根节点的脸，再看左手，再看右手。每个部位都一样，才算相同。

Checking if two trees are the same is like comparing two photos side by side: check the root's face, then left arm, then right arm. Every part must match.
