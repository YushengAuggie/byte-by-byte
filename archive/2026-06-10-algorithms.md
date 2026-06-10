# Day 62 — 算法 / Algorithms

💻 **算法 / Algorithms** · Day 62 · Expert Phase

---

## 🧩 树遍历模式 (7/15) — 在 Day 56 模版基础上进化 / Building on Template from Day 56

🔗 [LeetCode #235 — Lowest Common Ancestor of a BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) 🟡 Medium  
📹 [NeetCode Video](https://neetcode.io/solutions/lowest-common-ancestor-of-a-binary-search-tree)

---

### 这道题与模板的关系 / How This Maps to the Tree Template

通用模板：
```python
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

**今天的变体：利用 BST 性质，不需要遍历两边！**  
普通二叉树的 LCA 需要检查两边子树。但 BST 有大小关系，我们可以**直接决定往哪走**，时间从 O(n) 降到 O(h)。

*Today's variation: BST gives us ordering. Instead of blindly recursing both sides, we can navigate with purpose — like binary search on a tree.*

---

### 真实场景 / Real-World Analogy

想象公司组织架构树（BST 按员工 ID 排序）。CEO 是根节点，你要找两个员工的最近共同上级——不需要遍历整棵树，只要根据 ID 大小往左或往右走就能找到。

*A company org chart sorted by employee ID. Finding the lowest common manager for two employees — you don't scan everyone, just navigate by ID.*

---

### 问题描述 / Problem

给定一棵 BST 和两个节点 `p`、`q`，找它们的**最近公共祖先（LCA）**。

LCA 定义：节点 `v` 是 `p` 和 `q` 的 LCA，当且仅当 `v` 的子树同时包含 `p` 和 `q`（节点可以是自身的祖先）。

*Given a BST and two nodes p, q, find their Lowest Common Ancestor — the deepest node that has both p and q as descendants (a node is a descendant of itself).*

---

### BST 的关键洞察 / BST Key Insight

```
BST property: left < node < right

Three cases when at node curr:
  1. p.val < curr.val AND q.val < curr.val  →  LCA is in LEFT subtree
  2. p.val > curr.val AND q.val > curr.val  →  LCA is in RIGHT subtree  
  3. Otherwise (split point!)               →  curr IS the LCA
     - includes: p.val <= curr.val <= q.val
     - or: curr == p or curr == q
```

---

### Python 解法 + 追踪 / Solution with Trace

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Recursive approach — maps directly to DFS template
def lowestCommonAncestor_recursive(root, p, q):
    # BASE_CASE: if root is None (shouldn't happen in valid BST)
    if not root:
        return None
    
    # BST property: both in left subtree
    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor_recursive(root.left, p, q)
    
    # BST property: both in right subtree
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestor_recursive(root.right, p, q)
    
    # Split point — current node is the LCA
    return root  # COMBINE is just: return current node

# Iterative approach — O(1) space (preferred!)
def lowestCommonAncestor(root, p, q):
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left        # Both smaller: go left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right       # Both larger: go right
        else:
            return curr             # Split point = LCA
    return None

# Trace on example:
#       6
#      / \
#     2   8
#    / \ / \
#   0  4 7  9
#     / \
#    3   5
# 
# p=2, q=8: at 6 → 2<6 but 8>6 → SPLIT → return 6  ✓
# p=2, q=4: at 6 → both < 6 → go left
#           at 2 → 2==p, 4>2 → SPLIT → return 2  ✓
# p=7, q=9: at 6 → both > 6 → go right  
#           at 8 → 7<8 but 9>8 → SPLIT → return 8  ✓
```

**复杂度 / Complexity:**
- Time: O(h) — h is tree height; O(log n) balanced, O(n) worst case skewed
- Space: O(1) iterative / O(h) recursive (call stack)

*Why better than O(n)? We never visit nodes we don't need. BST ordering = free navigation.*

---

### 与同 Pattern 其他题的联系 / Connection to Pattern Block

| # | 题目 | 用到什么 |
|---|---|---|
| #226 Invert Binary Tree | 模板基础：left/right swap | postorder |
| #104 Max Depth | COMBINE = max(left, right) + 1 | postorder |
| #543 Diameter | COMBINE = 全局更新 max | postorder |
| **#235 LCA of BST** | **利用 BST 性质跳过分支** | **iterative / guided** |
| #98 Validate BST (upcoming) | 利用 BST 范围约束 | inorder / bounds |
| #230 Kth Smallest (upcoming) | Inorder traversal = sorted order | inorder |

**关键进化：** 前面几题都是"盲目递归两边"，这道题利用 BST 性质变成"有目的地导航"——类似二分查找。

*Evolution: Previous problems blindly recurse both sides. This one uses BST ordering to navigate — like binary search but on a tree.*

---

### 举一反三 / Generalization

**如果是普通二叉树（非 BST）呢？** → LeetCode #236

```python
def lca_generic_tree(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca_generic_tree(root.left, p, q)
    right = lca_generic_tree(root.right, p, q)
    if left and right:
        return root   # p and q in different subtrees
    return left or right  # One subtree contains both
```

*Same template, but no BST optimization — must check both sides. O(n) time.*

---

### Quiz

```json
{"question":"In a BST, when does the current node become the LCA of p and q?","options":["When p.val == q.val","When p and q are in different subtrees (split point)","When the current node equals p","When the current node is the root"],"correct_index":1}
```

---

### 📚 References

- [LeetCode #235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)
- [NeetCode Solution](https://neetcode.io/solutions/lowest-common-ancestor-of-a-binary-search-tree)
- [Binary Search Tree Properties — CS Visualizations](https://visualgo.net/en/bst)
- [LCA Algorithm Overview — CP-Algorithms](https://cp-algorithms.com/graph/lca.html)

---

### 🧒 ELI5

想象一棵家谱树，但是按名字字母顺序排列（左边名字小，右边名字大）。你要找 Alice 和 Eve 的最近共同祖先：从根节点开始，如果两人名字都比当前节点小就往左走，都大就往右走，一旦一个在左一个在右，当前节点就是答案！

*Imagine a family tree sorted alphabetically. To find Alice and Eve's nearest common ancestor: start at the root, go left if both names are "smaller," go right if both are "larger." The moment they'd split to different sides — that's your answer!*
