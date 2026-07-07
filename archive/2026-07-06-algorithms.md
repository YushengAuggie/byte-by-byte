# 💻 算法 / Algorithms — Day 83 · #973 K Closest Points to Origin (Medium)

🧩 **堆/优先队列模式 (3/7)** — building on the template from Day 79 (Kth Largest in Stream) and Day 81 (Last Stone Weight)

---

## 题目 / Problem

🔗 [LeetCode #973](https://leetcode.com/problems/k-closest-points-to-origin/) 🟡 Medium  
📹 [NeetCode Solution](https://neetcode.io/problems/k-closest-points-to-origin)

**今天的变化 / What's different from previous problems in this block:**
- Day 79 (Kth Largest in Stream): 1D stream, max-heap with size-k filter
- Day 81 (Last Stone Weight): simulation, always pop 2 max elements
- **Today**: 2D distance comparison, need to return K points (not just count/value)

**关键变化**: 堆的 key 不再是值本身，而是**距离** — 且需要存储原始点以便返回结果。
**Key shift**: heap key is now a *derived metric* (distance), not the raw value, and we must store the original point.

---

## 现实类比 / Real-World Analogy

你在做外卖 APP。用户要找最近的 K 家餐厅。暴力方法：把全城餐厅按距离排序。聪明方法：维护一个大小为 K 的"候选最近列表"，遍历餐厅时，如果有更近的就换掉最远的那家。

You're building a delivery app. Find the K nearest restaurants. Brute force: sort all restaurants by distance. Smart: maintain a "top-K nearest" heap, swap out the farthest whenever you find something closer.

---

## 模版映射 / Mapping to the Pattern Template

```python
# 通用模版 / General Template (from Day 79):
heap = []
for item in stream:
    heapq.heappush(heap, item)
    if len(heap) > k:
        heapq.heappop(heap)

# 今天的应用 / Today's Application:
# item → (-distance, x, y)  ← 取负值让 heapq (min-heap) 行为像 max-heap
# 维护大小为k的"最大距离堆" → pop掉最远的 → 留下最近的k个
```

---

## 解法 / Solution with Trace

```python
import heapq
from typing import List

def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    # Max-heap trick: negate distance so Python's min-heap pops the FARTHEST point
    heap = []  # stores (-dist_squared, x, y)
    
    for x, y in points:
        dist = x*x + y*y  # skip sqrt — monotonic, doesn't affect ordering
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)  # remove the farthest point
    
    return [[x, y] for _, x, y in heap]
```

**逐步追踪 / Trace** — `points = [[1,3],[-2,2],[3,1],[0,1]]`, `k = 2`

```
Point [1,3]:  dist=10, heap=[(-10, 1, 3)]         size=1 ≤ k, no pop
Point [-2,2]: dist=8,  heap=[(-10,1,3),(-8,-2,2)] size=2 ≤ k, no pop
Point [3,1]:  dist=10, heap adds (-10,3,1) → size=3 > k
              pop farthest: (-10,1,3) or (-10,3,1) [tied] → one removed
              heap=[(-10,3,1),(-8,-2,2)]  ← still has dist=10 point!
Point [0,1]:  dist=1,  heap adds (-1,0,1) → size=3 > k
              pop farthest: (-10,3,1) removed
              heap=[(-8,-2,2),(-1,0,1)]

Result: [[-2,2],[0,1]]  ✓
```

**复杂度 / Complexity:**
- Time: **O(n log k)** — n points, each heap op is O(log k)
- Space: **O(k)** — heap stores at most k+1 points

---

## 为什么不用排序？/ Why Not Just Sort?

```python
# ❌ 暴力排序 / Brute force sort
points.sort(key=lambda p: p[0]**2 + p[1]**2)
return points[:k]  # O(n log n) — slower for large n, small k

# ✅ 堆方法 / Heap approach  
# O(n log k) — much faster when k << n
# Example: n=1,000,000, k=10
# Sort: 1M * 20 = 20M ops
# Heap: 1M * log(10) ≈ 3.3M ops  ← 6x faster
```

---

## 举一反三 / Connect to Pattern Block

```
Block so far:
#703 Kth Largest in Stream  → size-k min-heap, return top element
#1046 Last Stone Weight     → always pop 2 max, simulate
#973 K Closest Points ←     → size-k max-heap (negated), return all k elements

Coming next:
#215 Kth Largest in Array   → same as #703 but not streaming — can use QuickSelect O(n) average!
#621 Task Scheduler         → heap for scheduling, not just finding — frequency counting
#355 Design Twitter         → heap merge (K sorted streams)
#295 Find Median            → TWO heaps (max-heap + min-heap)
```

**进阶挑战 / Pro Challenge:** Can you solve this with QuickSelect in O(n) average? (Hint: partition around k-th distance)

---

## 📚 References

- [LeetCode #973 — K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)
- [NeetCode Video — K Closest Points](https://neetcode.io/problems/k-closest-points-to-origin)
- [Python heapq docs](https://docs.python.org/3/library/heapq.html)
- [QuickSelect Algorithm](https://en.wikipedia.org/wiki/Quickselect)

---

## 🧒 ELI5

你有一堆弹珠，要找离你最近的3颗。  
方法1：把所有弹珠按距离排好序，取前3个（慢）。  
方法2：拿一个只能装3颗的小盒子。遍历每颗弹珠，如果比盒子里最远的还近，就换进去。  
最后盒子里剩的就是答案！堆就是那个"智能小盒子"。

You have a bag of marbles. Find the 3 closest to you. Method 2: keep a box that holds only 3 marbles. If you find one closer than the farthest in the box, swap it in. The heap IS that smart box.

---
