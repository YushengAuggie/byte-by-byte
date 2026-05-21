# 💻 算法 / Algorithms — Day 48
## #2 Add Two Numbers (Medium) — Linked List

> **模式 / Pattern:** 🧩 链表技巧 (7/11) | **Phase:** Mastery | **预计时间 / Read time:** 4 min

---

🧩 **链表技巧模式 (7/11)** — 在 Day 41 的快慢指针模板基础上延伸
*Building on the fast-slow pointer template from the Linked List block*

---

## 🔗 题目链接 / Links
- 🟡 [LeetCode #2 — Add Two Numbers](https://leetcode.com/problems/add-two-numbers/)
- 📹 [NeetCode Video Solution](https://neetcode.io/problems/add-two-numbers)

---

## 🌍 真实类比 / Real-World Analogy

想象你用算盘做两个大数相加，从个位开始，一位一位加，遇到进位就记下来，传到下一位。链表加法就是这个过程——每个节点是一位数字，从低位到高位。
*Imagine adding two large numbers on an abacus, digit by digit from the ones place, carrying over when needed. This is exactly linked list addition — each node is one digit, least significant first.*

---

## 📝 题目 / Problem

给两个非空链表表示两个非负整数（逆序存储），每节点存一位数。返回两数之和的链表（也逆序）。
*Two non-null linked lists representing non-negative integers stored in reverse order, one digit per node. Return their sum as a linked list (also reversed).*

```
Input:  l1 = 2->4->3  (represents 342)
        l2 = 5->6->4  (represents 465)
Output: 7->0->8       (represents 807)
```

---

## 🧩 和模板的关系 / How It Relates to the Template

这道题不用快慢指针，而是**双指针同步遍历**两个链表 + 进位处理。
它是链表模式的**变体**：不是找环或中点，而是**逐位模拟运算**。

*This problem doesn't use fast-slow pointers but uses **dual pointer simultaneous traversal** + carry tracking. It's a variant: instead of cycle detection or finding the middle, we simulate arithmetic digit by digit.*

**与前面题目的对比 / Contrast with previous problems in the block:**
- #206 Reverse: 修改 `next` 指针方向 → single pointer
- #21 Merge: 比较值，串联节点 → dual pointer merge
- #2 Add: 同步遍历 + 进位 → dual pointer + carry state

---

## 🐍 Python 解法 / Solution

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def addTwoNumbers(l1, l2):
    dummy = ListNode(0)   # sentinel node to simplify result building
    curr = dummy
    carry = 0

    # Traverse both lists until both exhausted AND no carry left
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0  # handle different lengths
        v2 = l2.val if l2 else 0

        total = v1 + v2 + carry
        carry = total // 10        # carry is 0 or 1
        curr.next = ListNode(total % 10)

        # Advance pointers
        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next

# Trace: l1=2->4->3, l2=5->6->4
# Step1: 2+5+0=7, carry=0 → node(7)
# Step2: 4+6+0=10, carry=1 → node(0)
# Step3: 3+4+1=8, carry=0 → node(8)
# Result: 7->0->8 ✓
```

**时间 / Time:** O(max(m, n)) — 遍历较长链表的长度
**空间 / Space:** O(max(m, n)) — 结果链表长度

---

## 💡 关键洞察 / Key Insights

1. **Dummy node 模式** — `dummy = ListNode(0)` 省去了结果链表头节点的特判，是链表题的万能起手式。
   *Dummy node eliminates edge case for result list head — universal linked list trick.*

2. **while l1 or l2 or carry** — 三个条件缺一不可！别忘了最后一位进位（999 + 1 = 1000，最高位进位）。
   *Three exit conditions: both lists AND carry must all be exhausted. Don't miss the final carry (999 + 1 = 1000).*

3. **逆序存储 = 天然对齐** — 个位对个位，不需要翻转。如果是正序存储，要先 reverse 或用栈。
   *Reverse storage = naturally aligned. If digits were stored forward, you'd need to reverse first or use a stack.*

---

## 举一反三 / Connect to the Block

| 题目 | 核心技巧 |
|------|----------|
| #21 Merge Sorted Lists | Dummy node + 比较值串联 |
| **#2 Add Two Numbers** | Dummy node + 进位同步遍历 |
| #23 Merge K Sorted Lists (upcoming) | Dummy node + heap 合并 |

Dummy node 是链表家族的核心模式——出现在 #21, #2, #23, #25。

---

## 📚 References
- [LeetCode Official — Add Two Numbers](https://leetcode.com/problems/add-two-numbers/editorial/)
- [NeetCode — Linked List Patterns](https://neetcode.io/roadmap)
- [GeeksForGeeks — Linked List Arithmetic](https://www.geeksforgeeks.org/add-two-numbers-represented-by-linked-list/)

---

## 🧒 ELI5
就像两个小朋友用手指数数，一人一个数字，从右边开始加。如果加起来超过 9，就进一位（carry = 1）传给下一个。链表就是把这些数字排成一串。
*Like two kids counting fingers, one digit at a time from the right. If the sum is more than 9, they "carry" 1 to the next pair. The linked list is just those digits in a chain.*
