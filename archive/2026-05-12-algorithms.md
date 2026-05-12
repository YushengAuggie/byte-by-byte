# 💻 算法 / Algorithms — Day 35
## #206 Reverse Linked List (Easy) — 链表技巧模式
> Mastery Phase · ~4 min read

---

## 🧩 新模式 / New Pattern: 链表技巧模式
📍 This block: 11 problems

**什么时候用 / When to use:** 链表反转、环检测、合并、找中点

**识别信号 / Signals:** reverse, cycle detection, merge, find middle, remove nth from end

**通用模版 / Template:**
```python
# Fast-slow pointers (cycle / middle)
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is at middle (or meeting point if cycle)
```

**核心洞察 / Key Insight:** 快慢指针解决大部分链表问题 — 环检测、找中点、找倒数第 k 个

---

## 今日题目 / Today's Problem

🔗 [LeetCode #206 - Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) 🟢 Easy
📹 [NeetCode Video](https://neetcode.io/problems/reverse-a-linked-list)

### 🌍 真实类比 / Real-World Analogy

想象一列火车 A→B→C→D，你要把它反向接成 D→C→B→A。
你无法"整体翻转"，只能一节一节重新连接。

Imagine a train A→B→C→D. You need to reconnect it as D→C→B→A. You can't flip the whole thing — you must relink one car at a time.

### 📋 问题描述 / Problem

给一个链表头节点，反转链表，返回新的头节点。

Given the head of a singly linked list, reverse the list, and return the reversed list's head.

```
Input:  1 → 2 → 3 → 4 → 5 → None
Output: 5 → 4 → 3 → 2 → 1 → None
```

### 🗺️ 映射到模式 / Map to Pattern Template

这道题不用快慢指针，用的是**三指针反转**模式，但属于链表操作的基础 — 后续的链表题（Reorder List, Reverse in K-Group）都建立在这个操作上。

```python
prev = None
curr = head
while curr:
    next_node = curr.next  # save next
    curr.next = prev       # reverse the pointer
    prev = curr            # advance prev
    curr = next_node       # advance curr
return prev
```

### 💻 完整解法 + 执行追踪 / Solution + Trace

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    curr = head
    
    while curr:
        next_node = curr.next  # save next before overwriting
        curr.next = prev       # reverse the arrow
        prev = curr            # prev advances forward
        curr = next_node       # curr advances forward
    
    return prev  # prev is new head when curr becomes None

# Trace: 1 → 2 → 3 → None
# Step 1: prev=None, curr=1, next=2 → 1.next=None, prev=1, curr=2
# Step 2: prev=1,    curr=2, next=3 → 2.next=1,    prev=2, curr=3
# Step 3: prev=2,    curr=3, next=None → 3.next=2, prev=3, curr=None
# Return: 3 → 2 → 1 → None ✅
```

### ⏱️ 复杂度 / Complexity
- **Time:** O(n) — 遍历每个节点一次
- **Space:** O(1) — 原地操作，只用3个指针

### 🔄 举一反三 / Pattern Variations

这是链表块的第1题，后续变体：
- **#21 Merge Two Sorted Lists** — 双指针归并（模式应用）
- **#143 Reorder List** — 先找中点，再反转后半段，再合并
- **#25 Reverse Nodes in K-Group** — 每K个做一次reverse，hard版

关键洞察：当你看到需要"反转"或"重排"链表时，先想能不能局部应用这个三指针模式。

---

### 📚 References
- https://leetcode.com/problems/reverse-linked-list/
- https://neetcode.io/problems/reverse-a-linked-list
- https://cs.stackexchange.com/questions/68/what-are-the-typical-use-cases-for-doubly-linked-lists

### 🧒 ELI5
想象你有一排小朋友手牵手：甲→乙→丙。你让他们反过来牵手：丙→乙→甲。
方法：从头开始，让每个人松开前面的手，改牵后面的人。三个变量分别记住"前一个"、"当前"、"下一个"，一步步走完就行了。

Imagine kids holding hands in a line: A→B→C. To reverse: go step by step, make each child let go and grab the previous child's hand instead. Three pointers track "prev", "current", and "next" so you don't lose anyone.
