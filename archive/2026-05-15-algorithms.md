# 💻 算法 / Algorithms — Day 44
## #143 Reorder List 🟡 Medium — Linked List Pattern (4/11)

🔗 [LeetCode #143](https://leetcode.com/problems/reorder-list/) · 📹 [NeetCode Solution](https://neetcode.io/problems/reorder-linked-list)

---

🧩 **链表技巧模式 (4/11)** — building on the template from Day 41 (Reverse Linked List)

今天的题是链表模式的**综合题** — 同时用到找中点、反转链表、合并三个技巧。

---

### 题目 / Problem

给定链表 `1 → 2 → 3 → 4 → 5`，就地重排为 `1 → 5 → 2 → 4 → 3`。
规律：把后半段**倒过来**，然后和前半段**交叉合并**。

Given linked list `1→2→3→4→5`, reorder in-place to `1→5→2→4→3`.

---

### 现实类比 / Real-World Analogy

排队等电影票：前半队人保持原位，后半队人**调头**，然后两队交替插队合并。

Like a theater line: keep the first half in order, reverse the second half, then interleave them.

---

### 如何映射到模版 / Mapping to Template

这道题是**三步走**，每一步都来自同一个链表工具箱：

```
Step 1: 找中点 (Fast-Slow Pointers)
Step 2: 反转后半段 (Reverse Template)  
Step 3: 交叉合并 (Merge Template)
```

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reorderList(head: Optional[ListNode]) -> None:
    if not head or not head.next:
        return

    # Step 1: Find middle using fast-slow pointers
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # slow is now at the middle

    # Step 2: Reverse the second half
    prev, curr = None, slow.next
    slow.next = None  # Cut the list in half
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    # prev is now the head of reversed second half

    # Step 3: Merge two halves by interleaving
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2
```

**执行追踪 / Trace:** `1→2→3→4→5`
```
After Step 1: slow=3, list: 1→2→3 | 4→5
After Step 2: second half reversed: 5→4
After Step 3 (iter 1): 1→5→2→... second=4
After Step 3 (iter 2): 1→5→2→4→3
Result: 1→5→2→4→3 ✓
```

**复杂度 / Complexity:** Time O(n) · Space O(1)

---

### 与同模式题目的对比 / Variations in this Pattern

| 题目 | 用到的技巧 |
|------|-----------|
| #206 Reverse Linked List | 反转 |
| #21 Merge Two Sorted Lists | 合并 |
| #141 Linked List Cycle | 快慢指针(环检测) |
| **#143 Reorder List** ← 今天 | **找中点 + 反转 + 合并 (三合一)** |
| #19 Remove Nth From End | 快慢指针(间距k) |

**今天的关键洞察：** Reorder List 是链表模式的"Boss题"——它不引入新技巧，而是要求你在一题中正确地**组合**三个已知工具，且顺序和边界条件不能出错。

---

### 举一反三 / Pattern Connections

- 这道题的 Step 2 = #206 Reverse Linked List 的完整实现
- Step 3 的 interleave 逻辑 ≈ #21 Merge Two Sorted Lists，但没有顺序比较
- 下一题 #19 Remove Nth From End 只需 fast-slow 找位置，是这个模式的简化版

---

### 🧒 ELI5

把一列火车从中间切成两截，后半截倒过来，然后把两截一节一节交替拼接。

---

### 📚 References
- https://leetcode.com/problems/reorder-list/
- https://neetcode.io/problems/reorder-linked-list
- https://cs.stackexchange.com/questions/11349/what-is-a-linked-list-in-data-structures
