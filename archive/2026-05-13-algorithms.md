# 💻 算法 / Algorithms — #21 Merge Two Sorted Lists (Easy)

> Day 42 · Mastery Phase · ~4 min read

---

🧩 **链表技巧模式 (2/11)** — building on the template from Day 41

今天是链表 block 的第 2 题。昨天（Reverse Linked List）我们用了迭代指针翻转；今天换一个场景：**合并**两个有序链表。注意模板里的快慢指针今天不需要，改用**双指针并行推进**。

This is the 2nd problem in the Linked List block. Yesterday (Reverse Linked List) we used iterative pointer reversal; today we shift to a different scenario: **merging** two sorted lists. The fast-slow pointer template isn't needed here — instead we use **two-pointer parallel traversal**.

---

## 题目 / Problem

🔗 [LeetCode #21](https://leetcode.com/problems/merge-two-sorted-lists/) 🟢 Easy · 📹 [NeetCode](https://www.youtube.com/watch?v=XIdigk956u0)

给定两个有序链表 `l1` 和 `l2`，将它们合并成一个新的有序链表并返回。

Given two sorted linked lists `l1` and `l2`, merge them into a single sorted linked list.

```
Input:  l1 = 1→3→5→None, l2 = 2→4→6→None
Output: 1→2→3→4→5→6→None
```

---

## 现实类比 / Real-World Analogy

两个有序的牌堆（l1 和 l2），你每次从两堆的顶部抽一张，把小的放到结果堆。最后哪堆还有剩的，整个接上去。

You have two sorted decks of cards (l1 and l2). Each round, you peek at both tops and take the smaller card. When one deck runs out, append the rest.

---

## 映射到模式 / Map to Pattern

今天**不用快慢指针**，而是链表的另一个核心技巧：**dummy head（哨兵节点）+ 双指针合并**。

```
Template variation: Dummy head + two-pointer merge

dummy = ListNode(0)  # sentinel, avoids edge cases
cur = dummy
p1, p2 = l1, l2

while p1 and p2:
    pick the smaller node → attach to cur → advance that pointer
    cur = cur.next

attach remaining (p1 or p2)
return dummy.next
```

**为什么用 dummy head?** 避免处理"结果链表第一个节点是谁"的边界情况，统一了逻辑。

---

## Python 解法 + 逐步追踪 / Solution + Trace

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(l1, l2):
    dummy = ListNode(0)   # sentinel node
    cur = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1  # attach l1 node
            l1 = l1.next   # advance l1
        else:
            cur.next = l2  # attach l2 node
            l2 = l2.next   # advance l2
        cur = cur.next     # advance result pointer
    
    # attach remaining nodes (at most one list has leftovers)
    cur.next = l1 if l1 else l2
    
    return dummy.next  # skip the dummy

# Trace: l1 = 1→3→5, l2 = 2→4→6
# Step 1: 1 < 2 → attach 1,  l1=3→5,  cur→1
# Step 2: 2 < 3 → attach 2,  l2=4→6,  cur→2
# Step 3: 3 < 4 → attach 3,  l1=5,    cur→3
# Step 4: 4 < 5 → attach 4,  l2=6,    cur→4
# Step 5: 5 < 6 → attach 5,  l1=None, cur→5
# Loop ends (l1=None). cur.next = l2 (6→None)
# Result: 1→2→3→4→5→6
```

**复杂度 / Complexity**: Time O(m+n) · Space O(1)

---

## 与同 block 题目的联系 / Connection to Block

| 题目 | 核心技巧 | 与今天的关系 |
|------|---------|------------|
| #206 Reverse Linked List | 迭代反转指针 | 指针操作基础 |
| **#21 Merge Two Sorted Lists** | **dummy head + 双指针** | **← 今天** |
| #143 Reorder List | 快慢找中点 → 反转后半 → 合并 | 今天 merge 是子问题！|
| #23 Merge K Sorted Lists | 堆 + 多路 merge | 今天的升级版 |

**关键洞察**: #143 Reorder List 和 #23 Merge K Sorted Lists 都在内部调用今天的 merge 逻辑。学好这题，后面两道 hard/medium 就降维了。

---

## 📚 References

- [LeetCode #21 官方题解](https://leetcode.com/problems/merge-two-sorted-lists/solution/)
- [NeetCode 视频讲解](https://www.youtube.com/watch?v=XIdigk956u0)
- [Linked List Patterns — NeetCode](https://neetcode.io/roadmap)

## 🧒 ELI5

两个装糖果的队伍，糖果按大小排好了。你站中间，每次从两队前面各拿一颗，把小的放进新盒子。哪队先没了，把另一队剩下的全倒进去。

Two queues of candies, sorted by size. You stand in the middle, compare the front of each queue each round, and take the smaller one into your new box. When one queue runs out, pour in everything left from the other.
