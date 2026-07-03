# 💻 算法 / Algorithms — Day 65
**题目 / Problem:** #1046 Last Stone Weight (Easy)
**模式 / Pattern:** Heap / Priority Queue (2/7)
**预计阅读 / Read time:** 4 min

---

🧩 **堆/优先队列模式 (2/7)** — 在 Day 79 的模版基础上继续
Building on the Heap/Priority Queue template from Day 79 (Kth Largest in Stream)

---

## 回顾模版 / Template Recap

```python
import heapq

# Python heapq = min-heap by default
# For max-heap: negate the values!
heap = []
heapq.heappush(heap, -value)   # push (negated for max-heap)
top = -heapq.heappop(heap)     # pop max (negate back)
```

**核心洞察 / Key Insight:** Python 只有 min-heap，模拟 max-heap 的方法是**取反**。这题需要反复取最大的两块石头，完美匹配 max-heap。

Python only has min-heap. To simulate max-heap: **negate values**. This problem needs to repeatedly grab the 2 largest stones — perfect max-heap use case.

---

## 题目 / Problem

🔗 [LeetCode #1046](https://leetcode.com/problems/last-stone-weight/) 🟢 Easy  
📹 [NeetCode Solution](https://www.youtube.com/watch?v=B-QCq79-Vfw)

**场景 / Analogy:** 你在玩石头碰撞游戏。每轮取出最重的两块石头相撞：如果一样重，两块都消失；如果不一样重，较轻的消失，较重的剩下 `(y - x)` 重量。最后返回剩余石头重量，或 0。

You have a pile of stones. Each round: smash the 2 heaviest. If equal weight → both gone. If different → heavier stone survives with weight `y - x`. Return last stone's weight, or 0.

```
输入: stones = [2,7,4,1,8,1]
轮1: 取 8,7 → 碰撞 → 剩 1 → stones = [2,4,1,1,1]
轮2: 取 4,2 → 碰撞 → 剩 2 → stones = [2,1,1,1]
轮3: 取 2,1 → 碰撞 → 剩 1 → stones = [1,1,1]
轮4: 取 1,1 → 碰撞 → 剩 0 → stones = [1]
输出: 1
```

---

## 与模版的映射 / Mapping to Template

| 模版概念 | 本题应用 |
|---------|---------|
| Max-heap (negate) | 存石头重量（取反） |
| heappop × 2 | 取最重的两块 |
| heappush | 碰撞后放回剩余 |
| 终止条件 | heap 长度 ≤ 1 |

---

## Python 解法 / Solution

```python
import heapq

def lastStoneWeight(stones: list[int]) -> int:
    # Convert to max-heap by negating all values
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)          # O(n) heapify
    
    while len(max_heap) > 1:
        y = -heapq.heappop(max_heap) # largest stone
        x = -heapq.heappop(max_heap) # second largest
        
        if y != x:
            # Remaining stone has weight (y - x)
            heapq.heappush(max_heap, -(y - x))
    
    # Return last stone or 0
    return -max_heap[0] if max_heap else 0

# Trace with [2,7,4,1,8,1]:
# heap = [-8,-7,-4,-2,-1,-1]
# Round 1: y=8, x=7 → push -1 → [-4,-2,-1,-1,-1]
# Round 2: y=4, x=2 → push -2 → [-2,-1,-1,-1]
# Round 3: y=2, x=1 → push -1 → [-1,-1,-1]
# Round 4: y=1, x=1 → equal, no push → [-1]
# Return 1 ✓
```

**复杂度 / Complexity:**
- 时间 Time: O(n log n) — n 次 heapop/heappush，每次 O(log n)
- 空间 Space: O(n) — heap 大小

---

## 和前一题的区别 / Difference from Day 79 (Kth Largest in Stream)

| | Kth Largest in Stream | Last Stone Weight |
|-|----------------------|-------------------|
| Heap type | Min-heap (keep top-k) | Max-heap (always grab max) |
| Heap size | Fixed at k | Shrinks over time |
| Operation | Add then maybe pop | Always pop 2, maybe push 1 |
| Python trick | Direct min-heap | Negate for max-heap |

---

## 举一反三 / Connect to the Pattern Block

这个模版块里的其他题：
- **Day 79 已学:** #703 Kth Largest in Stream (min-heap, size k)
- **下一题:** #973 K Closest Points to Origin (max-heap of size k, 比较距离)
- **最终 Boss:** #295 Find Median from Data Stream (两个 heap，一 max 一 min)

Pattern progression: single heap → fixed-size heap → two heaps

---

## 📚 References
- [Python heapq docs](https://docs.python.org/3/library/heapq.html)
- [NeetCode Heap Playlist](https://neetcode.io/roadmap)
- [Visualizing heaps](https://visualgo.net/en/heap)

## 🧒 ELI5
你有一堆积木，每次拿出最高的两块互相撞，高的那块变矮。一直这么玩，最后看剩多少高度。堆（heap）就像一个魔法盒子，每次都能最快找到最高那块积木。

You have a pile of blocks. Each time, grab the 2 tallest and smash them — the taller one shrinks. A heap is like a magic box that always finds the tallest block instantly.
