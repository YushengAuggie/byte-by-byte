# 💻 算法 / Algorithms — #23 Merge K Sorted Lists (Hard)
*Day 52 · Expert Phase · ~4 min read*

---

🧩 **链表技巧模式 (10/11)** — building on the Linked List template

今天是链表模式块的**倒数第二题**，也是本块难度最高的题目。前面我们用快慢指针解决了大部分问题，但 Merge K Sorted Lists 需要一个新武器：**最小堆（Min-Heap）**。这是 Linked List 模式与 Heap 模式的交汇点。

*This is the second-to-last problem in our Linked List block and the hardest. We've used fast-slow pointers for most problems, but Merge K Sorted Lists needs a new weapon: **Min-Heap**. This is where Linked List meets Heap patterns.*

---

## 题目 / Problem

🔗 [LeetCode #23 — Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) 🔴 Hard
📹 [NeetCode Video](https://neetcode.io/problems/merge-k-sorted-linked-lists)

给你 `k` 个有序链表，合并成一个有序链表并返回。

*Given `k` sorted linked lists, merge them into one sorted linked list.*

```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
```

---

## 真实类比 / Real-World Analogy

想象你是外卖平台的调度员，手上有 K 条送餐队列，每条队列按预计到达时间排好序。你需要给客户一个统一的"全局最早到达"顺序。每次你要从 K 个队列的**队头**里，挑出时间最早的那个。

*Imagine you're a delivery dispatcher with K sorted queues of orders (sorted by ETA). You need to output a single global earliest-first stream. At each step, you pick the earliest head across all K queues.*

---

## 解法：最小堆 / Min-Heap Approach

### 思路 / Intuition

每次我们需要找"K 个链表头节点中最小的那个"。暴力法每次 O(K)，K 个节点总共 O(N*K)。用最小堆可以把每次选最小降到 O(log K)，总时间 O(N log K)。

```python
import heapq
from typing import Optional, List

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    # Min-heap: (value, index, node)
    # index is tie-breaker (ListNode not comparable)
    heap = []
    
    # Initialize heap with head of each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    # Dummy head simplifies edge cases
    dummy = ListNode(0)
    curr = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node        # attach smallest node
        curr = curr.next
        
        if node.next:           # push next from same list
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

### 执行追踪 / Trace

```
lists = [[1,4,5], [1,3,4], [2,6]]

Initial heap: [(1,0,L0), (1,1,L1), (2,2,L2)]

Step 1: pop (1,0,L0→4) → output 1, push (4,0,L0→4)
Step 2: pop (1,1,L1→3) → output 1, push (3,1,L1→3)
Step 3: pop (2,2,L2→6) → output 2, push (6,2,L2→6)
Step 4: pop (3,1,L1→4) → output 3, push (4,1,L1→4)
Step 5: pop (4,0,L0→5) → output 4, push (5,0,L0→5)
Step 6: pop (4,1,None) → output 4, no push
Step 7: pop (5,0,None) → output 5, no push
Step 8: pop (6,2,None) → output 6, no push

Result: 1→1→2→3→4→4→5→6 ✅
```

### 复杂度 / Complexity
- **Time:** O(N log K) where N = total nodes, K = number of lists
- **Space:** O(K) for the heap

---

## 与模版的关联 / Connection to Template

我们的链表模版是快慢指针 — 今天没有用。但这道题展示了链表问题有时需要**其他数据结构辅助**：
- 单链表操作 → 快慢指针
- 多路归并 → Min-Heap
- 两两合并 → Divide & Conquer (也可解此题，见下)

**备选：Divide & Conquer**
```python
def mergeKLists(lists):
    if not lists: return None
    if len(lists) == 1: return lists[0]
    
    mid = len(lists) // 2
    left = mergeKLists(lists[:mid])
    right = mergeKLists(lists[mid:])
    return mergeTwoLists(left, right)  # same as Day 42 #21
```
同样 O(N log K)，且复用了 Day 42 的 mergeTwoLists！

---

## 举一反三 / Pattern Connections

本块其他题对比：
| 题目 | 技巧 | 关键点 |
|------|------|--------|
| #21 Merge Two Sorted Lists | 双指针 | K=2 的特殊情况 |
| #23 Merge K Sorted Lists (今天) | Min-Heap / D&C | K 路归并 |
| #25 Reverse Nodes in K-Group (明天) | 递归 / 迭代 | 本块压轴 |

---

## 📚 参考资料 / References

- [LeetCode #23 Solutions](https://leetcode.com/problems/merge-k-sorted-lists/solutions/)
- [NeetCode — Merge K Sorted Lists](https://neetcode.io/problems/merge-k-sorted-linked-lists)
- [Python heapq documentation](https://docs.python.org/3/library/heapq.html)

---

## 🧒 ELI5

有 K 个已经排好序的队伍，你要把他们合成一个大队伍。聪明的办法：用一个"魔法盒子"（最小堆），每次把 K 个队伍的**排头兵**放进去，自动帮你找出谁最小，让那个人先走，然后再从他的队伍里叫下一个人进来。

*You have K sorted lines of people and need to merge them into one line. Smart way: use a magic box (min-heap). Put the front person from each line in the box. The box always tells you who's shortest. That person leaves, and you bring in the next person from their original line.*
