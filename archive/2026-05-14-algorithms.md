# 💻 算法 / Algorithms — Day 43
**#141 Linked List Cycle** | 🟢 Easy | Pattern: 链表技巧模式 (3/11)

🔗 [LeetCode #141](https://leetcode.com/problems/linked-list-cycle/) | 📹 [NeetCode Solution](https://neetcode.io/problems/linked-list-cycle-detection)

---

🧩 **链表技巧模式 (3/11)** — building on the template from Day 41-42

今天是链表模式第3题。我们用**快慢指针模板**检测环 — 和之前反转、合并用同一套模板框架，但应用方式不同。

*Day 3 of 11 in the Linked List pattern block. We apply the fast-slow pointer template to cycle detection — same template skeleton, different application.*

---

## 问题 / Problem

给一个链表，判断是否有环。

*Given a linked list, determine if it has a cycle in it.*

```
Input: 3 → 2 → 0 → -4
             ↑_______↑
Output: True (node -4 points back to node 2)

Input: 1 → 2 → None
Output: False
```

---

## 现实类比 / Real-World Analogy

想象两个跑者在跑道上跑步。如果跑道是直线（无环），快跑者跑完就结束了。如果跑道是**环形跑道**，快跑者一定会绕圈超过慢跑者 — 他们必然相遇。

*Two runners on a track. If the track is linear, the fast runner finishes and it's over. If the track is circular, the fast runner laps the slow runner — they WILL meet.*

---

## 模板映射 / Mapping to Template

```python
# Fast-slow pointers (cycle detection)
# Template:
slow = fast = head
while fast and fast.next:
    slow = slow.next        # moves 1 step
    fast = fast.next.next   # moves 2 steps

# If there's a cycle: fast catches slow (they meet)
# If no cycle: fast reaches None
```

---

## Python Solution + Trace

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next       # 1 step
            fast = fast.next.next  # 2 steps
            
            if slow == fast:       # met? cycle exists
                return True
        
        return False  # fast hit None → no cycle
```

**Trace on** `3 → 2 → 0 → -4 → (back to 2)`:
```
Step 0: slow=3,  fast=3
Step 1: slow=2,  fast=0
Step 2: slow=0,  fast=2   (fast lapped back)
Step 3: slow=-4, fast=-4  ← MEET! return True
```

**Why does this work?**
- 无环时：fast 先到 None → O(n) 时间
- 有环时：进入环后，每轮 fast 比 slow 多走1步，相对速度=1，距离缩小1/轮 → 必然相遇 → O(n)

**Complexity:** Time O(n), Space O(1)

**vs naive approach:** 用 HashSet 存已见节点，Space O(n) — 快慢指针更优

---

## 举一反三 / Connect to the Block

这11题都用快慢指针或链表双指针：

| 题目 | 快慢指针用法 |
|------|------------|
| #206 Reverse (Day 41) | 迭代反转，prev/curr 双指针 |
| #21 Merge (Day 42) | 比较头节点，合并两个 |
| **#141 Cycle (Today)** | **Floyd 算法，fast+slow** |
| #143 Reorder List (Next) | 找中点(fast/slow) + 反转后半 |
| #19 Remove Nth (Coming) | 快指针先走N步 |

**关键洞察：** 快慢指针在环题中之所以有效，是因为它们建立了相对速度差 — 数学保证在有限步内相遇。

---

## Quiz

```json
{"question":"In Floyd's cycle detection (fast-slow pointers), if the linked list has NO cycle, what happens?","options":["slow and fast meet at the tail","fast.next becomes None and the loop exits","slow catches up to fast","they run forever"],"correct_index":1}
```

---

## 📚 References
- [LeetCode #141](https://leetcode.com/problems/linked-list-cycle/)
- [Floyd's Cycle Detection Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare)
- [NeetCode Visual Explanation](https://neetcode.io/problems/linked-list-cycle-detection)

## 🧒 ELI5
两只小动物赛跑：一只兔子，一只乌龟，在一条路上。如果路是直的，兔子跑到终点就停了。如果路是圈圈，兔子会绕圈追上乌龟。如果兔子追上乌龟了，就说明路是圈圈（有环！）。

*A rabbit and a tortoise run on a path. If the path is straight, rabbit finishes first and stops. If the path is a loop, rabbit laps the tortoise. If they meet, the path is a loop!*
