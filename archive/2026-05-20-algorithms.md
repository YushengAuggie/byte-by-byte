# 💻 算法 / Algorithms — Day 40

**题目 / Problem:** #138 Copy List with Random Pointer
**难度 / Difficulty:** 🟡 Medium | **模式 / Pattern:** Linked List (6/11)
**阶段 / Phase:** Mastery

---

## 🧩 链表技巧模式 (6/11) — 在第 41 天的模版基础上继续 / Building on the Template from Day 41

前 5 题回顾：Reverse → Merge → Cycle Detection → Reorder → Remove Nth
今天：**深拷贝带随机指针的链表** — 需要 Hash Map，不能用快慢指针

Previous 5: Reverse → Merge → Cycle Detection → Reorder → Remove Nth
Today: **Deep copy a linked list with random pointers** — requires Hash Map, fast-slow pointer won't help here

**与模版的关系：** 快慢指针解决"遍历类"问题，这题是"复制类"问题 — 关键挑战是 random 指针可以指向链表中任意节点，包括还没遍历到的节点。

**Relationship to template:** Fast-slow handles traversal/detection problems; this is a *copy* problem. The challenge: random pointer can point to any node, including ones you haven't visited yet.

---

## 🔗 链接 / Links

- 🔗 [LeetCode #138](https://leetcode.com/problems/copy-list-with-random-pointer/) 🟡 Medium
- 📹 [NeetCode 讲解](https://www.youtube.com/watch?v=5Y2EiZST97Y)

---

## 现实类比 / Real-World Analogy

你有一本通讯录，每条联系人有：
- `next`：下一条联系人
- `random`："最佳朋友"，指向通讯录中的任意一人

你要**完整复制**这本通讯录，包括所有的"最佳朋友"关系。
难点：复制第 1 个人时，他的"最佳朋友"可能是第 5 个人，但第 5 个人还没复制出来。

You have an address book. Each contact has `next` (next person) and `random` (their "best friend" — anyone in the book). Challenge: when copying person #1, their best friend might be person #5, who doesn't exist in the new book yet.

---

## 问题描述 / Problem

```python
# Node definition
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = x
        self.next = next
        self.random = random

# Input: head of linked list, random can point to any node or null
# Output: deep copy — completely new nodes, same structure
```

---

## 解法：两次遍历 + Hash Map / Two-Pass with Hash Map

**核心思路 / Key Insight:**
第一遍：遍历原链表，为每个节点创建对应的新节点，存入 `{old_node: new_node}` 映射。
第二遍：再次遍历，用 hash map 设置每个新节点的 `next` 和 `random`。

Pass 1: Create new node for each original node, store in `{old: new}` map.
Pass 2: Wire up `next` and `random` using the map.

```python
def copyRandomList(head):
    # Edge case
    if not head:
        return None
    
    # Pass 1: Create all new nodes
    old_to_new = {}
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)  # create copy, no links yet
        curr = curr.next
    
    # Pass 2: Wire up next and random
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        if curr.random:
            old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next
    
    return old_to_new[head]
```

**执行追踪 / Trace:**
```
Input: 1 → 2 → 3, random: 1→3, 2→1, 3→2

Pass 1 (create nodes):
old_to_new = {1: Node(1), 2: Node(2), 3: Node(3)}

Pass 2 (wire links):
Node(1).next = Node(2), Node(1).random = Node(3)
Node(2).next = Node(3), Node(2).random = Node(1)
Node(3).next = None,    Node(3).random = Node(2)

Result: New Node(1) → Node(2) → Node(3) ✓
```

---

## 进阶：O(1) 空间的交织法 / Bonus: O(1) Space Interweaving

```python
def copyRandomList_O1(head):
    if not head:
        return None
    
    # Step 1: Interweave — insert copy after each original
    # 1 → 1' → 2 → 2' → 3 → 3'
    curr = head
    while curr:
        copy = Node(curr.val)
        copy.next = curr.next
        curr.next = copy
        curr = copy.next
    
    # Step 2: Set random pointers for copies
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next  # copy's random = original's random's copy
        curr = curr.next.next  # skip the copy
    
    # Step 3: Separate the two lists
    dummy = Node(0)
    copy_curr = dummy
    curr = head
    while curr:
        copy_curr.next = curr.next  # take the copy
        curr.next = curr.next.next  # restore original
        copy_curr = copy_curr.next
        curr = curr.next
    
    return dummy.next
```

**复杂度 / Complexity:**
- Hash Map 法：Time O(n), Space O(n) ✅ 面试首选
- 交织法：Time O(n), Space O(1) ⚡ 进阶

---

## 举一反三 / Pattern Connections (Linked List Block)

| 题目 | 核心技巧 | 与今天的联系 |
|------|---------|------------|
| #206 Reverse | 三指针翻转 | 最基础的链表操作 |
| #141 Cycle | 快慢指针 | 检测环 |
| #19 Remove Nth | 快指针超前 N 步 | 找相对位置 |
| **#138 今天** | **Hash Map / 交织** | 复制结构 |
| #146 LRU Cache | HashMap + 双向链表 | 链表 + 哈希组合 |

**规律：** 链表题要么用指针技巧（快慢、多指针），要么用 Hash Map（复制、随机访问）。

---

## 📚 参考资料 / References

1. [LeetCode #138 官方题解](https://leetcode.com/problems/copy-list-with-random-pointer/editorial/)
2. [NeetCode 视频讲解](https://www.youtube.com/watch?v=5Y2EiZST97Y)
3. [Python Hash Map in Linked List Problems — Real Python](https://realpython.com/python-hash-table/)

---

## 🧒 ELI5

你要抄一张人物关系图。每个人有个"下一位"和一个"随机朋友"。直接抄，抄到第 1 个人时，他的朋友是第 5 个人，第 5 个人还没画出来怎么办？

方法：先把所有人的"空壳"画出来（第一遍），再把所有的连线画上去（第二遍）。这就是两次遍历的核心思想！

Copy a relationship chart: each person has a "next person" and a "random friend." Problem: when copying person #1, their friend is person #5 who doesn't exist yet. Solution: first create all "empty shells" (pass 1), then draw all the connections (pass 2).
