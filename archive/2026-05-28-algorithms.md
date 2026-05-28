# 💻 算法 / Algorithms — Day 45
## #25 Reverse Nodes in K-Group — Hard
**模式 / Pattern:** 链表技巧模式 (Linked List) | 11/11 — 最终章！

---

🧩 **链表技巧模式 (11/11) — 本模式最后一题！**
Building on the template from Day 41 (Reverse Linked List)

这是链表模块的**压轴 Hard 题**。回顾一下我们走过的路：

| # | 题目 | 核心技巧 |
|---|---|---|
| 1 | Reverse Linked List | 迭代/递归反转 |
| 2 | Merge Two Sorted Lists | 双指针合并 |
| 3 | Linked List Cycle | 快慢指针 |
| 4 | Reorder List | 找中点 + 反转 + 合并 |
| 5 | Remove Nth from End | 双指针间距 n |
| 6 | Copy List with Random Pointer | HashMap 映射 |
| 7 | Add Two Numbers | 模拟进位 |
| 8 | Find the Duplicate Number | Floyd 判圈 |
| 9 | LRU Cache | 双向链表 + HashMap |
| 10 | Merge K Sorted Lists | 堆/分治 |
| **11** | **Reverse Nodes in K-Group** | **分组反转** ← 今天 |

---

## 🔗 题目链接 / Links
- 🟥 LeetCode: https://leetcode.com/problems/reverse-nodes-in-k-group/
- 📹 NeetCode: https://neetcode.io/problems/reverse-nodes-in-k-group

---

## 现实类比 / Real-World Analogy

想象一队士兵 `[1,2,3,4,5,6]`，每 k=2 人一组，原地调换站位：
`[2,1,4,3,6,5]`

就像 **撤销/重做历史** 的批量反转操作 — 每次撤销 k 步，顺序倒转。

Imagine a line of soldiers `[1,2,3,4,5,6]`. Every k=2, reverse their positions: `[2,1,4,3,6,5]`.
Like a **batch undo operation** — reverse every k operations at once.

---

## 问题分析 / Problem Breakdown

```
Input:  1 → 2 → 3 → 4 → 5,  k=2
Output: 2 → 1 → 4 → 3 → 5

Input:  1 → 2 → 3 → 4 → 5,  k=3
Output: 3 → 2 → 1 → 4 → 5
```

难点：
1. 如何检查剩余节点是否有 k 个？
2. 如何记录反转前后的连接点？

---

## 如何映射到模式 / Mapping to Template

这题**不直接用快慢指针**，但用的是链表反转的核心操作——这是模式的变体：

```
标准模版：slow/fast 指针
本题变体：
  1. 用辅助函数检查是否还有 k 个节点 (类似 fast 指针向前探路)
  2. 每次反转 k 个节点 (核心操作与 #206 相同)
  3. 用 dummy head 统一处理边界
```

---

## Python 解法 / Solution with Trace

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseKGroup(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    group_prev = dummy  # tail of the last reversed group
    
    while True:
        # Step 1: Check if k nodes remain (like fast pointer scouting ahead)
        kth = get_kth(group_prev, k)
        if not kth:
            break  # fewer than k nodes left — keep as-is
        
        group_next = kth.next  # node AFTER this k-group
        
        # Step 2: Reverse k nodes (same as #206 Reverse Linked List!)
        prev, curr = group_next, group_prev.next
        while curr != group_next:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        
        # Step 3: Re-link
        # group_prev.next is still pointing to OLD head of group (now tail)
        tmp = group_prev.next  # old head = new tail
        group_prev.next = kth  # connect prev group to new head (kth)
        group_prev = tmp        # advance group_prev to new tail
    
    return dummy.next


def get_kth(curr: ListNode, k: int) -> Optional[ListNode]:
    """Advance k steps from curr; return None if not enough nodes."""
    while curr and k > 0:
        curr = curr.next
        k -= 1
    return curr
```

### 执行追踪 / Trace (k=2, [1,2,3,4])

```
初始:    dummy → 1 → 2 → 3 → 4
                 ↑           ↑
          group_prev    

轮1: kth=node(2), group_next=node(3)
     反转 [1,2]: 2 → 1 → 3 → 4
     dummy → 2 → 1 → 3 → 4
              ↑
         group_prev

轮2: kth=node(4), group_next=None
     反转 [3,4]: 4 → 3 → None
     dummy → 2 → 1 → 4 → 3
                  ↑
             group_prev

轮3: get_kth 返回 None → break

结果: 2 → 1 → 4 → 3 ✓
```

---

## 复杂度 / Complexity

- **时间 Time:** O(n) — 每个节点最多访问两次 (一次 get_kth，一次 reverse)
- **空间 Space:** O(1) — 原地操作，只用常数额外指针

---

## 举一反三 / Pattern Connection

学完整个链表模块，这道 Hard 题其实是 #206 (反转链表) + #141 (快慢指针探路) 的组合：

- `get_kth` = 快指针向前探 k 步
- 内层反转 = 完全复用 #206 的代码
- 核心洞察：**Hard 题往往是多个 Easy 技巧的组合**

After the full linked list block, this Hard problem is literally #206 + #141 combined:
- `get_kth` = fast pointer scouting k steps ahead
- Inner reversal = exact same code as #206
- Key insight: **Hard problems are often compositions of Easy techniques**

---

## 📚 References
- [LeetCode #25](https://leetcode.com/problems/reverse-nodes-in-k-group/)
- [NeetCode explanation](https://neetcode.io/problems/reverse-nodes-in-k-group)
- [Linked List patterns — NeetCode roadmap](https://neetcode.io/roadmap)

## 🧒 ELI5
给一排玩具按每 k 个一组，把每组里面的顺序倒过来。比如 k=3，[1,2,3,4,5,6] 变成 [3,2,1,6,5,4]。秘诀是先看看够不够 k 个，够的话就原地翻转，然后把各组拼在一起。

Given a row of toys, reverse every k of them. k=3: [1,2,3,4,5,6] → [3,2,1,6,5,4]. The trick: check if k nodes exist, reverse them in place, stitch the groups together.
