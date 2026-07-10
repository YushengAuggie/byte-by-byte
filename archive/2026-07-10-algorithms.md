# Algorithms: Find Median from Data Stream
*Day 87 — #295 Hard — Heap / Priority Queue (7/7) | 2026-07-10*

---

## 💻 算法 / Algorithms

🧩 **堆/优先队列模式 (7/7)** — 收官之作，模式的终极形态
*The final problem of this pattern block — the pattern's ultimate form.*

> 本块回顾 / Block recap: #703 → #1046 → #973 → #215 → #621 → #355 → **#295 (今天)**
> 前 6 题都在"从流/数组中维护 top-K"，今天是**双堆技巧**，维护动态中位数。
> *Previous 6 problems all maintained top-K. Today: two-heap trick for dynamic median.*

---

### 题目 / Problem

🔗 [LeetCode #295 — Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) 🔴 Hard
📹 [NeetCode 讲解](https://neetcode.io/problems/find-median-in-a-data-stream)

**题意：** 设计一个数据结构，支持：
- `addNum(num)` — 向数据流中添加一个数
- `findMedian()` — 返回当前所有数字的中位数

*Design a data structure supporting addNum(num) and findMedian().*

---

### 真实场景 / Real-World Analogy

想象你是一个系统监控工程师，需要**实时**统计服务器响应时间的中位数。每毫秒都有新数据涌入，你不能每次都对全量数据排序（O(n log n) 太慢），你需要一个 O(log n) 的动态解法。

*Imagine monitoring server response times in real-time — you need the median of a data stream without re-sorting every time a new data point arrives.*

---

### 核心洞察：双堆 / Key Insight: Two Heaps

```
数据流中所有数字想象成两半：
左半部分（较小的数）用 max-heap 维护 → 堆顶是左边最大值
右半部分（较大的数）用 min-heap 维护 → 堆顶是右边最小值

[1, 2, 3] | [4, 5, 6, 7]
max-heap    min-heap

中位数 = 两个堆顶的平均值（偶数）
       = 较大堆的堆顶（奇数）

不变量 (Invariant):
1. len(max_heap) == len(min_heap) 或
   len(max_heap) == len(min_heap) + 1
2. max(max_heap) <= min(min_heap)
```

---

### 如何映射到模式模板 / Mapping to Template

基础模板只维护 **单个堆** 来追踪 top-K：
```python
import heapq
heap = []
heapq.heappush(heap, item)
if len(heap) > k:
    heapq.heappop(heap)
```

今天的变体：**维护两个相互平衡的堆**，一个 max-heap（左），一个 min-heap（右），通过动态重平衡维护中位数不变量。这是堆模式的**最复杂形态**。

---

### Python 解法 / Solution

```python
import heapq

class MedianFinder:
    def __init__(self):
        # max-heap for left half (store negatives for Python's min-heap)
        self.left = []   # max-heap (negated)
        # min-heap for right half
        self.right = []  # min-heap

    def addNum(self, num: int) -> None:
        # Step 1: always push to left first
        heapq.heappush(self.left, -num)
        
        # Step 2: ensure left's max <= right's min
        if self.left and self.right and (-self.left[0] > self.right[0]):
            val = -heapq.heappop(self.left)
            heapq.heappush(self.right, val)
        
        # Step 3: rebalance sizes (left can be at most 1 larger)
        if len(self.left) > len(self.right) + 1:
            val = -heapq.heappop(self.left)
            heapq.heappush(self.right, val)
        if len(self.right) > len(self.left):
            val = heapq.heappop(self.right)
            heapq.heappush(self.left, -val)

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return -self.left[0]  # odd total: left has one more
        return (-self.left[0] + self.right[0]) / 2  # even total: average tops

# --- Trace ---
mf = MedianFinder()
mf.addNum(1)  # left=[-1], right=[]       → median = 1.0
mf.addNum(2)  # left=[-1], right=[2]      → median = 1.5
mf.addNum(3)  # left=[-2,-1], right=[3]   → median = 2.0
print(mf.findMedian())  # 2.0
```

**复杂度 / Complexity:**
- `addNum`: Time O(log n) — heap push/pop
- `findMedian`: Time O(1) — just read tops
- Space O(n) — store all elements

---

### 举一反三 / Pattern Connections

本块 7 道题的**难度梯度**很有启发性：

| 题目 | 技巧 | 难度 |
|------|------|------|
| #703 Kth Largest in Stream | 单 min-heap 固定大小 | Easy |
| #1046 Last Stone Weight | 单 max-heap | Easy |
| #973 K Closest Points | 单 max-heap, 距离比较 | Medium |
| #215 Kth Largest in Array | QuickSelect 或堆 | Medium |
| #621 Task Scheduler | 频率计数 + 贪心 | Medium |
| #355 Design Twitter | 多路归并 + heap | Medium |
| **#295 Median from Stream** | **双堆平衡** | **Hard** |

规律：**越复杂的问题，需要维护的堆越多，不变量越精妙。**

---

### 面试常见追问 / Follow-up Questions

**Q: 如果数据流极大（无法全部放内存），怎么办？**
A: 用两个文件做外部排序，或 **t-digest** 算法做近似中位数，牺牲精确度换内存。

**Q: 如果要维护 P99 而不是中位数？**
A: 同样的双堆思路，只是左右堆的大小比例不是 50/50，而是 99/1。

---

### 📚 References

- [LeetCode #295](https://leetcode.com/problems/find-median-from-data-stream/)
- [NeetCode 视频讲解](https://neetcode.io/problems/find-median-in-a-data-stream)
- [Python heapq docs](https://docs.python.org/3/library/heapq.html)

### 🧒 ELI5

把所有数字排成一排，中位数就是最中间的那个。但每次新来一个数，我不想重新排序。我的技巧：用两个魔法盒子。**左边盒子**装较小的数，随时能告诉我最大值。**右边盒子**装较大的数，随时能告诉我最小值。每次加数，我维持两个盒子大小相近，中位数就是两个盒盖上的数！
