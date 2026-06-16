# 💻 算法 / Algorithms — Day 67
**题目 / Problem:** #98 Validate Binary Search Tree (Medium)
**模式 / Pattern:** 树遍历模式 (Trees) — 第 11/15 题
**预计阅读 / Read time:** ~4 min

---

## 💻 算法 / Algorithms

🧩 **树遍历模式 (11/15)** — building on the template from Day 56

这是 Trees 板块第 11 题，我们已经掌握了 DFS 递归框架。今天的关键是：**BST 验证不是每个节点和左右孩子比，而是和整棵子树的范围比。**

*We're 11/15 into the Trees block. Today's key insight: BST validation isn't comparing a node to its direct children — it's checking against the valid range of the entire subtree.*

---

### 🔗 Links

- 📌 [LeetCode #98](https://leetcode.com/problems/validate-binary-search-tree/) 🟡 Medium
- 📹 [NeetCode Video](https://neetcode.io/problems/valid-binary-search-tree)

---

### 🌍 现实类比 / Real-World Analogy

想象你在验证一棵公司组织架构：CEO 薪资必须高于所有下属，且每一层的薪资范围都有上下限约束。不是只看"老板比直属下属高"就够了——你得确保整条链路都满足范围约束。

*Like verifying salary hierarchy in an org chart: it's not enough that a manager earns more than direct reports — every node must fit within valid bounds for its entire chain.*

---

### 🗺️ 映射到模版 / Map to Template

```python
# 基础模版
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)

# 今天的变体：传入范围边界
# Today's variation: pass valid range bounds down
def dfs(node, min_val, max_val):
    if not node: return True  # BASE_CASE = valid
    if not (min_val < node.val < max_val):
        return False
    left = dfs(node.left, min_val, node.val)   # must be < node.val
    right = dfs(node.right, node.val, max_val) # must be > node.val
    return left and right                       # COMBINE
```

**与之前题目的区别 / What's different from previous problems:**
- Day 56 (Max Depth): 返回整数（深度），bottom-up 合并
- Day 60 (Count Good Nodes): 自顶向下传递当前路径最大值
- **今天**: 自顶向下传递**双边界** (min, max)，验证合法性

---

### 🐍 完整解法 + 追踪 / Solution with Trace

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root: Optional[TreeNode]) -> bool:
    def validate(node, min_val, max_val):
        # Base case: empty node is valid
        if not node:
            return True
        
        # Current node must be strictly within (min_val, max_val)
        if not (min_val < node.val < max_val):
            return False
        
        # Recurse: left subtree bounded above by node.val
        #          right subtree bounded below by node.val
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    # Start with infinite bounds
    return validate(root, float('-inf'), float('inf'))

# Trace for BST: [5,1,4,null,null,3,6]  → Invalid
#        5           validate(5, -inf, +inf)
#       / \            5 in (-inf, +inf) ✅
#      1   4           validate(1, -inf, 5) → 1 in (-inf,5) ✅
#         / \          validate(4, 5, +inf) → 4 NOT in (5,+inf) ❌
#        3   6       → return False ✅ (correctly invalid)

# Trace for valid BST: [2,1,3]
#        2           validate(2, -inf, +inf) → ✅
#       / \          validate(1, -inf, 2) → 1 in (-inf,2) ✅
#      1   3         validate(3, 2, +inf) → 3 in (2,+inf) ✅
#                  → return True ✅
```

**复杂度 / Complexity:**
- 时间 Time: **O(n)** — 每个节点访问一次
- 空间 Space: **O(h)** — 递归栈，h=树高；平衡树 O(log n)，最坏 O(n)

---

### ❌ 常见错误 / Common Mistake

```python
# WRONG: 只比较父子节点，忽略全局范围
# This fails for [5, 4, 6, null, null, 3, 7]
def isValidBST_WRONG(root):
    def check(node):
        if not node: return True
        if node.left and node.left.val >= node.val: return False
        if node.right and node.right.val <= node.val: return False
        return check(node.left) and check(node.right)
    # ❌ node 6's left child 3 < 5 (root), violates BST!
    # But this code says it's valid because 3 < 6 locally

# CORRECT: 传递边界 / Pass bounds
def isValidBST_CORRECT(root):
    def validate(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return validate(node.left, lo, node.val) and \
               validate(node.right, node.val, hi)
    return validate(root, float('-inf'), float('inf'))
```

---

### 举一反三 / Pattern Connections

这道题在 Trees 板块的位置：
- **#235 LCA of BST** (Day 62): 利用 BST 性质找分叉点 → 方向类似（利用范围导航）
- **#230 Kth Smallest in BST** (Day 68): 利用中序遍历天然有序
- **#105 Construct BST from Preorder/Inorder** (Day 70): 用范围界定子树

**通用洞察**: BST 问题 = 普通树 DFS + 利用 BST 有序性（范围/中序）

---

### 📚 参考资料 / References

1. [LeetCode #98 Discussion](https://leetcode.com/problems/validate-binary-search-tree/solutions/)
2. [NeetCode BST Explanation](https://neetcode.io/problems/valid-binary-search-tree)
3. [BST Properties — CS Visualizations](https://visualgo.net/en/bst)

---

### 🧒 ELI5

*验证 BST 就像检查每层楼的门牌号：不只是"这层比下面高"，而是每个房间的号码必须在整栋楼允许的范围内。*

*Validating a BST is like checking room numbers floor by floor: it's not just "higher than below" — every room must be within its globally allowed range.*
