# 💻 算法 / Algorithms — Day 46
## #226 Invert Binary Tree (Easy) — Trees

---

🧩 **新模式 / New Pattern: 树遍历模式 (Tree Traversal)**
📍 This block: 15 problems (Easy → Hard)

**什么时候用 / When to use:** 二叉树遍历、路径问题、验证 BST、层序遍历
**识别信号 / Signals:** binary tree, BST, path sum, level order, depth, validate

**通用模版 / Template:**
```python
def dfs(node):
    if not node:
        return BASE_CASE      # e.g. 0, None, True, []
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

**核心洞察 / Key Insight:**
几乎所有树问题都是 DFS 递归 — 关键是定义好**返回值语义**：我要从子树得到什么？
*Almost all tree problems are DFS recursion — the key is defining the **return value semantics**: what do I need back from each subtree?*

---

🔗 [LeetCode #226](https://leetcode.com/problems/invert-binary-tree/) 🟢 Easy
📹 [NeetCode 视频](https://neetcode.io/problems/invert-a-binary-tree)

---

### 🌍 真实类比 / Real-World Analogy

想象你有一棵组织架构图，需要把左右子公司互换 —— 每个节点都要把左右孩子对调，然后递归处理。就像镜像翻转一面镜子：每个小镜子都要翻，大镜子才完整翻好。

*Imagine an org chart where you need to mirror left and right subsidiaries at every level. Like reflecting in a mirror: every node must swap its children for the whole tree to be inverted.*

---

### 🗺️ 映射到模板 / Mapping to Template

```
BASE_CASE = None (空节点不需要处理)
left  = dfs(node.left)   → 反转左子树，返回反转后的根
right = dfs(node.right)  → 反转右子树，返回反转后的根
COMBINE = swap(left, right) → 把返回结果互换赋给 node
```

---

### 💻 Python 解法 / Solution

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invertTree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    # Base case: empty node — nothing to invert
    if not root:
        return None
    
    # Post-order: recurse first, then process current node
    left  = invertTree(root.left)
    right = invertTree(root.right)
    
    # COMBINE: swap left and right children
    root.left  = right
    root.right = left
    
    return root

# Trace example:
#      4                4
#    /   \    →       /   \
#   2     7         7     2
#  / \ / \         / \   / \
# 1  3 6  9       9  6  3  1
#
# invertTree(4):
#   invertTree(2) → returns root of [2, right=1, left=3]
#   invertTree(7) → returns root of [7, right=6, left=9]
#   swap: 4.left = [7...], 4.right = [2...]
#   return 4
```

**Time Complexity:** O(n) — visit every node once
**Space Complexity:** O(h) — recursion stack, h = height (O(log n) balanced, O(n) skewed)

---

### 🔄 举一反三 / Block Connections

这个模板后续会用于：
- **#104 最大深度** — `COMBINE = 1 + max(left, right)`，返回深度数字
- **#543 直径** — `COMBINE` 更新全局最大值，返回单边最长路径
- **#110 平衡树** — `COMBINE` 检查 `abs(left - right) <= 1`，返回高度或 -1（invalid）
- **规律**：越是 Easy，COMBINE 越简单；Hard 题的 COMBINE 会更新全局变量

*The template evolution:*
- *#104: return depth (int), COMBINE = 1 + max(l, r)*
- *#543: track global max, return single-arm length*
- *#124 Hard: track global max path sum, return best single-arm sum*

---

### 📚 References

- [LeetCode #226 官方题解](https://leetcode.com/problems/invert-binary-tree/editorial/)
- [NeetCode Trees Playlist](https://neetcode.io/roadmap) → Trees section
- [Visualgo BST Traversal](https://visualgo.net/en/bst) — 可视化树遍历

---

### 🧒 ELI5

有一棵圣诞树，每个树枝都有左小树枝和右小树枝。反转就是把每个树枝的左右小树枝互换。先处理最小的树枝（叶子），再处理大的，最后换根。

*You have a Christmas tree. At every branch, swap the left and right sub-branches. Start with the tiniest branches (leaves), work your way up, and finally swap the two main branches at the top.*
