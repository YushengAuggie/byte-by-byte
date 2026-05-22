# 💻 算法 / Algorithms — Day 49

**题目 / Problem:** #287 Find the Duplicate Number (Medium)  
**模式 / Pattern:** 🧩 Linked List (8/11) — building on the fast-slow pointer template

---

## 🧩 链表技巧模式 (8/11) — 今天的变体 / Pattern Variation

从 Day 41 的快慢指针模板开始，今天的题目是一个 **"隐式链表"** 的妙用 — 数组本身就是一条链表！

**回顾模板 / Template recap:**
```python
# Fast-slow pointers (cycle / middle)
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is at meeting point if cycle
```

**今天的变化 / What's different today:**
- 不是真正的链表节点，而是用 **数组下标** 模拟 `next` 指针
- `nums[i]` 代表 "从节点 i 出发，下一个节点是 nums[i]"
- 有重复数字 → 必然有环

---

## 🔗 题目链接

- 🔗 [LeetCode #287](https://leetcode.com/problems/find-the-duplicate-number/) 🟡 Medium
- 📹 [NeetCode 解析](https://neetcode.io/problems/find-duplicate-integer)

---

## 现实类比 / Real-world analogy

想象一条单行道，路牌上写着"下一站是 X 号路口"。如果某两个路牌都指向同一个地方，那从起点出发走下去，一定会兜圈子。Floyd 算法就是用一快一慢两辆车检测这个圈。

Imagine a one-way road where each sign says "go to intersection X." If two signs point to the same place, a driver following the signs will eventually loop. Floyd's algorithm uses two cars — one fast, one slow — to detect that loop.

---

## 题目 / Problem

给一个数组 `nums`，包含 `n+1` 个整数，每个数在 `[1, n]` 之间，**只有一个数出现多次**。不能修改数组，空间复杂度 O(1)。

```
Input:  nums = [1, 3, 4, 2, 2]
Output: 2
```

---

## 映射到模板 / Map to Template

```
数组下标:    0 → 1 → 3 → 2 → 4 → 2 (loop!)
nums[i]:     1   3   2   4   2

把 nums[i] 当 next 指针:
- Node 0 → Node nums[0]=1
- Node 1 → Node nums[1]=3
- Node 3 → Node nums[3]=2
- Node 2 → Node nums[2]=4
- Node 4 → Node nums[4]=2  ← loop starts here!
```

重复的数字 `2` 就是环的入口！这和 Linked List Cycle II (#142) 是完全一样的问题！

---

## Python 解法 / Solution

```python
def findDuplicate(nums):
    # Phase 1: Find meeting point inside the cycle
    slow = nums[0]
    fast = nums[0]
    
    while True:
        slow = nums[slow]        # move 1 step
        fast = nums[nums[fast]]  # move 2 steps
        if slow == fast:
            break  # they met inside the cycle
    
    # Phase 2: Find cycle entry (= duplicate number)
    # Reset one pointer to start
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]  # 1 step
        fast = nums[fast]  # 1 step
    
    return slow  # cycle entry = duplicate

# Trace for [1, 3, 4, 2, 2]:  (indices: 0→1, 1→3, 2→4, 3→2, 4→2)
# Phase 1:
# Start:  slow=1, fast=1
# Step 1: slow=nums[1]=3, fast=nums[nums[1]]=nums[3]=2
# Step 2: slow=nums[3]=2, fast=nums[nums[2]]=nums[4]=2  ← meet at 2!
# Phase 2 (reset slow=nums[0]=1, fast=2):
# Step 1: slow=nums[1]=3, fast=nums[2]=4
# Step 2: slow=nums[3]=2, fast=nums[4]=2  ← meet at 2 = duplicate ✓
```

**时间 / Time:** O(n) — 线性扫描  
**空间 / Space:** O(1) — 只用两个指针，不修改数组

---

## 举一反三 / Pattern connections

| 题目 | 链接 |
|------|------|
| #141 Linked List Cycle (Day 43) | 检测环的存在 |
| #142 Linked List Cycle II | 找环入口 — **本题的本质** |
| #287 Find Duplicate (今天) | 隐式链表 → 找环入口 |
| #23 Merge K Sorted Lists (Day 10) | 快慢指针的极限应用 |

**规律：** 凡是需要 O(1) 空间找重复/环，先想"能不能把问题建模成链表+Floyd算法"。

---

## 📚 References
- [LeetCode #287 Discussion — Floyd Cycle Detection Explained](https://leetcode.com/problems/find-the-duplicate-number/solutions/72846/my-easy-understood-solution-with-o1-space-and-on-in-time/)
- [Floyd's Tortoise and Hare — Wikipedia](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare)
- [NeetCode — Find the Duplicate Number](https://neetcode.io/problems/find-duplicate-integer)

## 🧒 ELI5
数组里有个数字出现了两次，就好像一条路上有两个路牌指向同一个地方。用乌龟（慢）和兔子（快）在路上跑，它们一定会在那个"重复的地方"相遇，然后再走一遍就能找到是哪里重复的。
