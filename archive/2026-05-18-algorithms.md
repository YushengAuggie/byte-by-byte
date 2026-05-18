# 💻 算法 / Algorithms — #19 Remove Nth Node From End of List (Medium)

> 📅 Day 46 | ⏱️ 4 min read | 🟡 Medium | 🧩 Linked List (5/11)

---

🧩 **链表技巧模式 (5/11)** — 延续 Day 41 开始的模式

> 今天是链表模式的第5题。前4题：#206 Reverse → #21 Merge → #141 Cycle → #143 Reorder
> Today is the 5th problem in the Linked List block. You already have: reverse, merge, cycle detection, reorder.

**今天的新变化 / What's new today:**  
前4题主要用快慢指针找中点或检测环。今天用快慢指针的**变体** — 用固定间距的双指针找"倒数第 N 个节点"。核心洞察从"speed ratio"变成"distance gap"。

---

## 🔗 Links

- 🔗 [LeetCode #19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) 🟡 Medium
- 📹 [NeetCode Solution](https://neetcode.io/solutions/remove-nth-node-from-end-of-list)

---

## 🌍 Real-World Analogy

你在一个很长的火车上。列车长想删掉从车尾数第 N 节车厢，但他在车头，看不到车尾，也不知道火车总长度。他只能从车头往车尾走一次。

怎么做？他派出两个列车员：一号先走 N 步，然后两人同时往前走。当一号到终点时，二号正好站在目标车厢前面。

*You're on a very long train. The conductor wants to remove the Nth car from the tail but is standing at the head with no view of the total length. Solution: two conductors — one walks N steps ahead, then both walk in sync until the first reaches the end. The second is now right behind the target car.*

---

## 🎯 Problem

```
Given a linked list, remove the nth node from the end.
Return the head of the modified list.

Example:
1 → 2 → 3 → 4 → 5, n=2
              ↑ remove this
Result: 1 → 2 → 3 → 5
```

**关键约束：** One pass preferred. n is always valid.

---

## 🧩 模板映射 / Mapping to Pattern Template

标准快慢指针模板是 `fast.next.next`（速度比 2:1 找中点）。  
今天的变体：**fixed-gap two pointers**（固定间距，速度相同）。

```
Template (from Day 41): fast moves 2x, slow moves 1x
                        → finds middle

Today's variation:      fast starts N steps ahead, then both move 1x
                        → fast at end means slow is N steps from end
```

这个变体你会在以下场景反复用到：
- 找倒数第 K 个节点（本题）
- 找链表后 1/3 处的节点
- 任何"相对位置"问题

---

## 🐍 Python Solution

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    # Dummy node handles edge case: removing the head itself
    dummy = ListNode(0, head)
    
    fast = dummy
    slow = dummy
    
    # Advance fast by n+1 steps (not n) so slow lands on the node BEFORE target
    # Why n+1? We need slow to be the predecessor for the delete operation
    for _ in range(n + 1):
        fast = fast.next
    
    # Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next
    
    # slow.next is the node to delete
    slow.next = slow.next.next
    
    return dummy.next

# --- Trace for [1,2,3,4,5], n=2 ---
# After setup:
#   dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
#   fast, slow both at dummy

# After n+1=3 steps, fast is at node 3:
#   fast = 3, slow = dummy

# While loop (fast moves until None):
#   fast=4, slow=1
#   fast=5, slow=2  
#   fast=None, slow=3  ← STOP

# slow is at node 3, which is one BEFORE the target (node 4)
# slow.next = slow.next.next → skip node 4
# Result: 1 -> 2 -> 3 -> 5 ✓
```

**为什么 n+1 不是 n？**  
删除操作需要修改 `predecessor.next`，所以 slow 必须停在目标节点的**前一个**，因此 fast 要多走1步。

---

## ⏱️ Complexity

| | Time | Space |
|--|------|-------|
| This solution | O(n) | O(1) |
| Naive (2 passes) | O(n) | O(1) |
| Stack-based | O(n) | O(n) |

一次遍历，常数空间 — 这是最优解。

---

## 🔄 举一反三 / Pattern Connections

| 问题 | 技巧 | 与今天的关系 |
|------|------|-------------|
| #141 Linked List Cycle (Day 43) | fast=2x, slow=1x 检测环 | 同样双指针，不同速度比 |
| #143 Reorder List (Day 44) | fast=2x 找中点 | 速度变体 |
| **今天 #19** | fast 领先 N 步找倒数第 N | 间距变体 |
| #876 Middle of Linked List | fast=2x 找中点 | 最基础的快慢指针 |

**规律：** 链表的双指针解法，调整的只有两个参数：**速度比**（2:1 vs 1:1）和**初始间距**（0 vs N）。

---

## 📝 Quiz

```json
{"question":"To remove the Nth node from the end in ONE pass, where should 'slow' pointer stop?","options":["Exactly at the Nth node from end","At the node BEFORE the Nth node from end","At the Nth node from start","At the middle of the list"],"correct_index":1}
```

---

## 🧒 ELI5

想象你有一根绳子，但不知道它有多长。你想剪掉从末尾数第2段。怎么办？用两根手指：右手先走2步，然后两手同时往前走，右手碰到尽头时，左手就在要剪的地方旁边了！

*Imagine a rope of unknown length. You want to cut the 2nd segment from the end. Use two fingers: right hand walks 2 steps ahead, then both move together. When the right hand hits the end, the left hand is right next to the cut point!*

---

## 📚 References

- [LeetCode #19 Discussion](https://leetcode.com/problems/remove-nth-node-from-end-of-list/solutions/)
- [NeetCode — Remove Nth Node From End of List](https://neetcode.io/solutions/remove-nth-node-from-end-of-list)
- [Two Pointer Patterns — LeetCode Patterns](https://seanprashad.com/leetcode-patterns/)
