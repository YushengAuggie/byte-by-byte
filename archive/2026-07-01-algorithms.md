# 💻 算法 / Algorithms — Day 79
## #703 Kth Largest Element in a Stream (Easy) — Heap / Priority Queue
**预计阅读时间 / Est. read time: 4 min**

---

🧩 **新模式 / New Pattern: 堆/优先队列模式 (Heap / Priority Queue)**
📍 这个模式块共 7 道题 / This block: 7 problems

**什么时候用 / When to use:** Top K 问题、合并 K 个有序序列、动态中位数

**识别信号 / Signals:** "top k", "kth largest/smallest", "merge k sorted", "median", "schedule"

**通用模版 / Template:**
```python
import heapq

heap = []
for item in stream:
    heapq.heappush(heap, item)
    if len(heap) > k:
        heapq.heappop(heap)
# heap[0] is the kth largest element
```

**核心洞察 / Key Insight:** 维护大小为 k 的**最小堆** — 堆顶就是第 k 大的元素。比排序整个数组高效得多 (O(n log k) vs O(n log n))。

---

🔗 [LeetCode #703](https://leetcode.com/problems/kth-largest-element-in-a-stream/) 🟢 Easy | 📹 [NeetCode 解析](https://neetcode.io/problems/kth-largest-integer-in-a-stream)

---

## 🌍 真实类比 / Real-World Analogy

想象你是一家音乐平台的数据工程师，需要实时追踪"播放量前 K 名歌曲"。每秒都有新的播放数据进来，你不可能每次都把所有歌曲重新排序——太慢了！

You're a data engineer at a music platform, tracking "top K songs by plays" in real time. New play counts stream in every second—you can't re-sort everything each time.

**解法：** 维护一个大小为 K 的最小堆，堆顶就是"第 K 大"的门槛。

---

## 📋 问题描述 / Problem

设计一个类，找到数据流中第 k 大的元素。注意是第 k 大（排序后倒数第 k 个），不是第 k 个不同的元素。

Design a class `KthLargest` that:
- `__init__(self, k, nums)`: Initialize with k and an initial list
- `add(self, val)`: Add a value to the stream, return the kth largest element

---

## 🗺️ 映射到模版 / Map to Template

**为什么用最小堆，不是最大堆？**
- 最大堆堆顶是最大值，找不到"第 k 大"
- **最小堆大小为 k**：堆顶是堆里最小的，也就是"所有数里第 k 大的"
- 每次加入新值，如果堆大小 > k，弹出最小值（堆顶），保持堆里永远是"最大的 k 个"

```
示例：k=3, nums=[4,5,8,2]
初始堆（大小3）：[4, 5, 8] → 最小堆 = [4, 5, 8]

add(3):  堆 = [3,4,5,8] → 弹出3 → [4,5,8] → 返回 4
add(5):  堆 = [4,5,5,8] → 弹出4 → [5,5,8] → 返回 5
add(10): 堆 = [5,5,8,10] → 弹出5 → [5,8,10] → 返回 5
```

---

## 🐍 Python 解法 / Solution with Trace

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []  # min-heap of size k
        
        for num in nums:
            self.add(num)
    
    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        
        # Keep only the k largest elements
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)  # remove the smallest
        
        # heap[0] is always the kth largest
        return self.heap[0]

# Trace:
# k=3, nums=[4,5,8,2]
# After init:
#   add(4): heap=[4], size<3, return 4 (but k not satisfied yet)
#   add(5): heap=[4,5], size<3
#   add(8): heap=[4,5,8], size=3, return 4
#   add(2): heap=[2,4,5,8] → pop 2 → heap=[4,5,8], return 4
# 
# add(3):  heap=[3,4,5,8] → pop 3 → heap=[4,5,8], return 4  ✓
# add(5):  heap=[4,5,5,8] → pop 4 → heap=[5,5,8], return 5  ✓
```

**复杂度 / Complexity:**
- 时间: O(log k) per `add` call (heap push/pop)
- 空间: O(k) — 堆最多存 k 个元素

---

## 🔄 举一反三 / Pattern Variations

这个模式块的 7 道题，对比理解：

| 题目 | 变化点 / Twist |
|------|---------------|
| **#703 Kth Largest in Stream** ← 今天 | 基础模版，最小堆大小 k |
| **#1046 Last Stone Weight** | 最大堆：每次取两个最大值 |
| **#973 K Closest Points** | 自定义距离作为 key |
| **#215 Kth Largest in Array** | 一次性输入，无流式 |
| **#621 Task Scheduler** | 贪心 + 最大堆调度任务 |
| **#295 Median from Stream** | **两个堆**：一大一小维护中位数 |

---

## 📝 Quiz
```json
{"question":"KthLargest(k=2, nums=[3,1,5]).add(4) returns?","options":["3","4","5","1"],"correct_index":1}
```

---

## 📚 参考资料 / References
- [Python heapq docs](https://docs.python.org/3/library/heapq.html)
- [NeetCode Heap/Priority Queue playlist](https://neetcode.io/roadmap) — Heap section
- [Visualgo Heap visualization](https://visualgo.net/en/heap)

## 🧒 ELI5
想象你要追踪班里前 3 名同学的分数。有新同学进来，你不用给全班重新排名——只需要跟"目前第 3 名"比一比：比他高就换掉他，比他低就不管。这就是最小堆的魔法！
Imagine tracking the top 3 scores in class. When a new score arrives, you only compare against the 3rd-highest—if it beats it, swap in. That's the heap trick!
