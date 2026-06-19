# 💻 算法 / Algorithms — Day 58
**主题 / Topic:** #105 Construct Binary Tree from Preorder and Inorder (Medium)
**日期 / Date:** 2026-06-18

---

## 💻 算法 / Algorithms

🧩 **树遍历模式 (13/15)** — building on the template from Day 56 (Invert Binary Tree)

今天是树遍历 Block 的第 **13/15** 题。我们已经用 DFS 解决了从 Easy 到 Medium 的树问题，今天遇到一道真正考验"理解遍历顺序"的题目。

---

### 🔗 链接 / Links

- 🟡 [LeetCode #105 — Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)
- 📹 [NeetCode 视频讲解](https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal)

---

### 📖 问题理解 / Problem

**现实类比：** 你有一本书的目录（前序遍历 = 父节点先出现）和索引（中序遍历 = 左→根→右）。这两份信息合在一起，能唯一还原整棵书的章节树。

You have a book's table of contents (preorder = parent appears first) and its index (inorder = left→root→right). Together they uniquely reconstruct the chapter hierarchy tree.

**输入 / Input:**
```
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]
```

**输出 / Output:**
```
    3
   / \
  9  20
    /  \
   15   7
```

**关键洞察 / Key Insight:**
1. **前序遍历的第一个元素 = 当前树的根**
2. 在**中序遍历**中找到根的位置，左边 = 左子树，右边 = 右子树
3. 递归重复以上步骤

---

### 🧩 映射到模式 / Mapping to Pattern

这道题是树遍历模式的**变体**——不是遍历树，而是**重建树**。但核心递归结构一样：

```
def dfs(node):          →    def build(pre_start, pre_end, in_start, in_end):
    if not node: return BASE_CASE   →    if pre_start > pre_end: return None
    left = dfs(node.left)           →    root = TreeNode(preorder[pre_start])
    right = dfs(node.right)         →    in_root = inorder_map[root.val]
    return COMBINE(...)             →    left_size = in_root - in_start
                                         root.left = build(...)
                                         root.right = build(...)
                                         return root
```

**与之前题目的不同点：**
- 普通 DFS（第1-12题）：从根出发，向下递归
- 本题：从"遍历数组"出发，**重建**根再向下递归
- 关键额外技巧：用 **HashMap** 预存中序下标，O(1) 查找

---

### 💡 Python 解题 / Solution

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def buildTree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    # O(1) lookup: value -> inorder index
    inorder_map = {val: idx for idx, val in enumerate(inorder)}

    def build(pre_start, pre_end, in_start, in_end):
        # Base case: empty range
        if pre_start > pre_end:
            return None

        # Preorder[pre_start] is ALWAYS the current root
        root_val = preorder[pre_start]
        root = TreeNode(root_val)

        # Find root in inorder → splits left/right subtree
        in_root = inorder_map[root_val]
        left_size = in_root - in_start  # how many nodes in left subtree

        # Recurse: left subtree
        root.left = build(
            pre_start + 1,              # skip root in preorder
            pre_start + left_size,      # left subtree takes left_size nodes
            in_start,
            in_root - 1                 # left of root in inorder
        )

        # Recurse: right subtree
        root.right = build(
            pre_start + left_size + 1,  # right subtree starts after left
            pre_end,
            in_root + 1,                # right of root in inorder
            in_end
        )

        return root

    return build(0, len(preorder) - 1, 0, len(inorder) - 1)
```

---

### 🔍 执行追踪 / Trace

```
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]
inorder_map = {9:0, 3:1, 15:2, 20:3, 7:4}

build(0, 4, 0, 4):
  root = 3, in_root = 1, left_size = 1
  left  = build(1, 1, 0, 0)  → root=9, no children → TreeNode(9)
  right = build(2, 4, 2, 4):
    root = 20, in_root = 3, left_size = 1
    left  = build(3, 3, 2, 2) → root=15, no children → TreeNode(15)
    right = build(4, 4, 4, 4) → root=7,  no children → TreeNode(7)
    → TreeNode(20, 15, 7)
  → TreeNode(3, 9, TreeNode(20, 15, 7))
```

---

### ⏱️ 复杂度 / Complexity

- **时间 Time:** O(n) — 每个节点访问一次，HashMap 查找 O(1)
- **空间 Space:** O(n) — HashMap + 递归栈 O(h)，最坏 O(n)

---

### 举一反三 / Pattern Connections

**同 Block 的后续挑战（14/15, 15/15）：**

| 题目 | 难点 | 与本题的联系 |
|------|------|-------------|
| #124 Binary Tree Maximum Path Sum (Hard) | 返回值语义复杂（全局变量技巧）| 同样是递归返回 left/right，但需要"全局最大"外部状态 |
| #297 Serialize and Deserialize BT (Hard) | 编码+解码，本质是 DFS 重建 | 直接复用本题思路！序列化=前序遍历，反序列化=重建 |

**一句话总结：** 本题是 #297 的前置知识——学会"从遍历序列重建树"，Serialize/Deserialize 就迎刃而解。

---

### 📚 References

- [LeetCode #105 Official Solution](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/editorial/)
- [NeetCode Explanation](https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal)
- [Visualizing Tree Reconstruction](https://visualgo.net/en/bst)

### 🧒 ELI5

前序遍历就像你介绍家庭成员的顺序："我是爸爸，我有左孩子小明，小明有……"  
中序遍历就像家庭合照的站位：左边的是左子树，中间是根，右边是右子树。  
有了这两个信息，就能唯一确定谁是谁的爸爸！

Preorder = introducing family members: "I'm Dad, my left child is Xiaoming..."  
Inorder = family photo positions: left group = left subtree, middle = root, right group = right subtree.  
With both, you can always figure out who's whose parent!
