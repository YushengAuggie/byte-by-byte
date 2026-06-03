# 💻 算法 / Algorithms — #110 Balanced Binary Tree (Easy)

> Day 58 · Expert Phase · Pattern: Trees (4/15) · ~4 min read

---

## 🧩 Trees 模式回顾 (4/15) — Building on the template from Day 54

上次模式介绍 (Day 54 / #226 Invert Binary Tree) 建立了树遍历的通用模板：

```python
def dfs(node):
    if not node: return BASE_CASE
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

今天的平衡树检测是这个模板的一个**变体**：关键是**返回值需要携带两种信息** (高度 + 是否平衡)，而不仅仅是单一值。

Today's problem is a **variation**: the key insight is the return value needs to carry **two pieces of information** (height + is_balanced), not just one.

---

## 题目 / Problem

🔗 [LeetCode #110 Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) 🟢 Easy  
📹 [NeetCode Solution](https://neetcode.io/problems/balanced-binary-tree)

判断一棵二叉树是否**高度平衡**：每个节点的左右子树高度差不超过 1。

Determine if a binary tree is **height-balanced**: for every node, the left and right subtree heights differ by at most 1.

```
Example:
    3
   / \
  9  20
    /  \
   15   7

→ True (all nodes balanced)

    1
   / \
  2   2
 / \
3   3
/
4
→ False (node 2 has left height 2, right height 0 → diff = 2)
```

---

## 现实类比 / Real-World Analogy

想象一棵公司组织架构树 🏢。"平衡"意味着每个 manager 的两个部门人数大致相同。如果一个部门有 100 人，另一个只有 1 人，这棵"树"就失衡了。AVL 树就是数据结构中强制平衡的二叉搜索树。

Think of a company org chart 🏢. "Balanced" means every manager's two sub-departments are roughly the same size. An AVL tree is exactly a balanced BST — it enforces this property after every insertion.

---

## 如何映射到模板 / Mapping to Template

**朴素方法 (❌ O(n²)):** 对每个节点调用 `height()`，总共调用 O(n log n) ~ O(n²) 次。

**优化方法 (✅ O(n)):** 让 `dfs` 同时返回高度 AND 是否平衡。一次遍历搞定。

```python
# TEMPLATE KEY INSIGHT: return value = (height, is_balanced)
# BASE_CASE when null: (0, True)
# COMBINE: check both subtrees balanced + height diff ≤ 1

def isBalanced(root):
    def dfs(node):
        # BASE_CASE
        if not node:
            return (0, True)  # (height, is_balanced)
        
        # Recurse on children
        left_h, left_ok = dfs(node.left)
        right_h, right_ok = dfs(node.right)
        
        # COMBINE
        balanced = left_ok and right_ok and abs(left_h - right_h) <= 1
        height = 1 + max(left_h, right_h)
        
        return (height, balanced)
    
    _, result = dfs(root)
    return result
```

---

## 执行追踪 / Trace

```
Tree:    3
        / \
       9  20
         /  \
        15   7

dfs(15) → (1, True)
dfs(7)  → (1, True)
dfs(20) → left_h=1, right_h=1, diff=0 ≤ 1 → (2, True)
dfs(9)  → (1, True)
dfs(3)  → left_h=1, right_h=2, diff=1 ≤ 1 → (3, True)

Result: True ✅
```

---

## 复杂度 / Complexity

- **Time:** O(n) — visit every node exactly once
- **Space:** O(h) — call stack depth = tree height; O(log n) balanced, O(n) worst case (skewed tree)

---

## 另一种写法 / Alternative: Early Exit with -1 Sentinel

```python
def isBalanced(root):
    def dfs(node):
        if not node: return 0
        
        left = dfs(node.left)
        if left == -1: return -1  # short-circuit: already unbalanced
        
        right = dfs(node.right)
        if right == -1: return -1
        
        if abs(left - right) > 1: return -1  # mark as unbalanced
        return 1 + max(left, right)
    
    return dfs(root) != -1
```

This avoids tuple unpacking — returns -1 as a sentinel for "unbalanced". Cleaner in some languages.

---

## 举一反三 / Pattern Connections

这道题和 Trees 模式其他题的关系：

| 题目 | 返回值语义 | 变化点 |
|------|-----------|--------|
| #104 Max Depth | `int` (高度) | 最简单，单值返回 |
| #543 Diameter | `int` (半径), 更新全局 | 需要全局变量存最大值 |
| **#110 Balanced** | `(height, bool)` | **今天** — 元组返回 |
| #100 Same Tree | `bool` | 比较两棵树，不是一棵 |
| #124 Max Path Sum | `int` (单侧最大), 更新全局 | Hard 版的 #543 |

**规律 / Pattern:** 树 DFS 的"变化"几乎只在返回值语义上！掌握这个，后面 11 道题都有迹可循。

---

## 📚 References

- [LeetCode #110 Official Solution](https://leetcode.com/problems/balanced-binary-tree/solution/)
- [NeetCode - Balanced Binary Tree](https://neetcode.io/problems/balanced-binary-tree)
- [AVL Trees - Wikipedia](https://en.wikipedia.org/wiki/AVL_tree)
- [Visual Tree Traversals - CS Visualized](https://btholt.github.io/complete-intro-to-computer-science/avl-trees)

---

## 🧒 ELI5

检查一棵树是否平衡，就像检查你的行李箱两侧装的东西是否差不多重 🧳。如果左边装了 10 件衣服，右边只有 1 件，就失衡了。从树叶开始，一层一层往上检查每个"节点"两侧是否差不多高。

Checking if a tree is balanced is like checking if your suitcase is packed evenly 🧳. If the left side has 10 clothes and the right has 1, it's lopsided. We check from the leaves up — at each node, are both sides roughly the same height?
