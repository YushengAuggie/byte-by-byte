# 💻 算法 / Algorithms — #230 Kth Smallest Element in a BST (Medium)

> **Day 68 · Expert Phase · ~4 min read**
> 🧩 **树遍历模式 (12/15)** — 在第 Day 57 的模板基础上延伸

---

## 🧩 树遍历模式 (12/15) — 从 Day 57 模板延伸

之前的模板：后序 DFS（左 → 右 → 当前）。
今天的变体：**中序 DFS（左 → 当前 → 右）** — BST 的中序遍历天然有序！

Previous pattern: post-order DFS (left → right → current).
Today's twist: **in-order DFS** — because a BST's in-order traversal yields sorted values automatically.

```
模板变体对比:
Post-order: left, right, THEN process node  → aggregation (depth, path sum)
In-order:   left, THEN process node, right  → BST sorted traversal
Pre-order:  THEN process node, left, right  → serialization, path recording
```

---

## 题目 / Problem

🔗 [LeetCode #230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) 🟡 Medium
📹 [NeetCode Video](https://neetcode.io/problems/kth-smallest-integer-in-bst)

**真实类比 / Real-world analogy:**
你有一个员工薪资 BST（左小右大）。老板问："第 3 低的薪资是多少？" — 你不用排序整个数组，只需按序遍历到第 k 个就停下。

You have a salary BST (left < right). The boss asks: "What's the 3rd lowest salary?" You don't need to sort everything — just traverse in order and stop at the k-th element.

**问题:** 给一棵 BST，找第 k 小的元素（k 从 1 开始）。
Given a BST, return the k-th smallest value (1-indexed).

```
Input: root = [3,1,4,null,2], k = 1

      3
     / \
    1   4
     \
      2

In-order: 1, 2, 3, 4
Output: 1
```

---

## 解题思路 / Approach — 映射到中序模板

**BST 的关键性质:** 中序遍历（左→根→右）结果是**升序排列**。
**Key BST property:** In-order traversal yields values in ascending order.

所以第 k 小 = 中序遍历的第 k 个节点。

**方法一: 迭代中序（推荐，面试首选）**
Iterative in-order (preferred for interviews — early termination):

```python
def kthSmallest(root, k: int) -> int:
    stack = []
    current = root
    count = 0

    while current or stack:
        # Go as far left as possible
        while current:
            stack.append(current)
            current = current.left

        # Process node (this is "in-order" moment)
        current = stack.pop()
        count += 1
        if count == k:
            return current.val  # Early exit!

        # Move to right subtree
        current = current.right
```

**执行追踪 / Trace** (root=[3,1,4,null,2], k=1):
```
Step 1: Push 3, push 1, push null → stack=[3,1], current=None
Step 2: Pop 1, count=1, k=1 → RETURN 1 ✓
```

**方法二: 递归（清晰，但无法早退）**
Recursive (cleaner, but can't early-terminate):

```python
def kthSmallest(root, k: int) -> int:
    result = []

    def inorder(node):
        if not node or len(result) == k:
            return
        inorder(node.left)         # left first
        result.append(node.val)    # process current
        inorder(node.right)        # then right

    inorder(root)
    return result[k - 1]
```

---

## 复杂度 / Complexity

| | Time | Space |
|---|---|---|
| Iterative | O(H + k) — H = tree height | O(H) stack |
| Recursive | O(H + k) | O(H) call stack |

H = O(log n) for balanced, O(n) for skewed.

**为什么是 O(H + k)？** 先走 H 步到最左，再数 k 步。

---

## Follow-up (面试加分项!)

> "如果 BST 频繁插入/删除，查询 k-th 会很慢。怎么优化？"
> "If the BST is modified frequently, how do you optimize repeated k-th queries?"

**解法:** 在每个节点存 `left_count`（左子树节点数），可以 O(log n) 查询：
Store `left_count` at each node → O(log n) per query:

```python
# Node stores: val, left, right, left_count
# If k <= node.left_count: go left
# If k == left_count + 1: current is answer
# Else: k -= (left_count + 1), go right
```

---

## 举一反三 / Pattern Connections

在同一个树遍历模式块中 (In the same Trees pattern block):
- **#98 Validate BST** (Day 67): 中序遍历验证递增 → 同样利用中序性质
- **#235 LCA of BST** (Day 57): 利用 BST 的大小性质做方向决策
- **#105 Construct from Preorder+Inorder** (下一题): 用中序恢复树结构

---

## 📚 References

- [LeetCode #230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
- [NeetCode Solution](https://neetcode.io/problems/kth-smallest-integer-in-bst)
- [BST In-order Traversal — Wikipedia](https://en.wikipedia.org/wiki/Tree_traversal#In-order,_LNR)

---

## 🧒 ELI5

BST 就像一个自动整理好的书架，左边的书永远比右边便宜。找第 k 便宜的书，只要从最左边开始数，数到第 k 本停下来就行。

A BST is like a self-sorted bookshelf where left books always cost less than right ones. To find the k-th cheapest, just start from the leftmost book and count to k — no need to sort anything first.
