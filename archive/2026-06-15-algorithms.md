# 💻 算法 / Algorithms — Day 66
## #1448 Count Good Nodes in Binary Tree (Medium)

**⏱️ 阅读时间：约4分钟 / Reading time: ~4 min**

🔗 [LeetCode](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) 🟡 Medium | 📹 [NeetCode](https://neetcode.io/problems/count-good-nodes-in-binary-tree)

---

### 🧩 树遍历模式 (10/15) — 在 Day 57 的模版基础上延伸

```
🧩 Trees (10/15) — building on the DFS template from Day 57
```

今天的问题是带"路径状态"的 DFS 变体：在递归过程中，我们需要把**当前路径最大值**传递下去。

This is a **DFS with carried state** variant: pass the max value seen on the current root-to-node path down through recursion.

---

### 🌏 真实世界类比 / Real-World Analogy

想象你在爬山，从山脚到每个地点有一条路径。一个地点是"好地点"，如果你到达那里的时候，它的海拔不低于路上经过的任何一个地点。问：共有多少个"好地点"？

Imagine hiking: a location is "good" if its elevation is ≥ all previous stops on that trail from base. Count such locations.

---

### 📖 问题描述 / Problem

给一棵二叉树，若从根到节点 X 的路径上，没有任何节点的值 **大于** X.val，则 X 是**好节点**。返回好节点的总数。

A node X is **good** if no node on the path from root to X has a value greater than X.val. Return the count of good nodes.

```
    3
   / \
  1   4
 /   / \
3   1   5

Good nodes: 3 (root), 3 (left-left), 4, 5 → Answer: 4
```

---

### 🗺️ 映射到模版 / Map to Template

```python
def dfs(node):
    if not node: return BASE_CASE      # 0
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(node.val, left, right)
```

今天的变化：**模板加一个参数** `max_so_far`

```python
def dfs(node, max_so_far):
    if not node: return 0              # BASE_CASE = 0
    
    is_good = 1 if node.val >= max_so_far else 0
    new_max = max(max_so_far, node.val)
    
    left = dfs(node.left, new_max)     # pass state DOWN
    right = dfs(node.right, new_max)
    
    return is_good + left + right      # COMBINE
```

**核心洞察 / Key insight:** 路径最大值是"向下传递的状态"，不是向上聚合的结果。比较：求直径时最大深度是"向上聚合"的。

*Path max is **top-down** state; contrast with diameter where max depth is **bottom-up** aggregated.*

---

### 🐍 Python 解法 with Trace

```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, max_val):
            if not node:
                return 0
            
            # Is this node good?
            is_good = 1 if node.val >= max_val else 0
            
            # Update max for children
            new_max = max(max_val, node.val)
            
            return is_good + dfs(node.left, new_max) + dfs(node.right, new_max)
        
        return dfs(root, float('-inf'))  # root is always good

# Trace on example:
# dfs(3, -inf): 3 >= -inf ✅, new_max=3
#   dfs(1, 3):  1 >= 3? ❌, new_max=3
#     dfs(3, 3): 3 >= 3? ✅ → 1
#   dfs(4, 3):  4 >= 3? ✅, new_max=4
#     dfs(1, 4): 1 >= 4? ❌ → 0
#     dfs(5, 4): 5 >= 4? ✅ → 1
# Total: 1 + 0 + 1 + 1 + 1 = 4 ✅
```

**复杂度 / Complexity:**
- ⏱️ Time: O(n) — visit each node once
- 💾 Space: O(h) — recursion stack, h = tree height

---

### 🔁 举一反三 / Pattern Connections

| Problem | What you pass down | What you return up |
|---------|-------------------|--------------------|
| Max Depth (#104, Day 57) | nothing | max depth |
| Good Nodes (#1448, Today) | `max_so_far` | count |
| Path Sum II | `remaining` target | list of paths |
| Validate BST (#98, Day 67) | `(min, max)` bounds | bool |

**规律 / Pattern:** 需要路径上的累积信息 → 往下传参数。需要子树的聚合结果 → 从下往上返回。

*Need cumulative path info → pass it down. Need subtree aggregation → return it up.*

---

### 🧒 ELI5

你走迷宫，随身带一个"见过的最高数字"的记事本。每到一个房间，如果这个房间的数字 ≥ 记事本上的数字，就是"好房间"，把记事本更新。最后数有几个好房间。

Walk a maze carrying a notepad showing "highest number seen so far." A room is "good" if its number ≥ notepad. Update notepad, keep walking. Count good rooms.

---

### 📝 Quiz
```json
{"question":"Count Good Nodes: what's the initial value passed to root?","options":["0","float('-inf')","root.val","None"],"correct_index":1}
```

---

### 📚 References
- 🔗 https://leetcode.com/problems/count-good-nodes-in-binary-tree/
- 🔗 https://neetcode.io/problems/count-good-nodes-in-binary-tree
- 🔗 https://www.youtube.com/watch?v=7cp5imvDzl4 (NeetCode video)
