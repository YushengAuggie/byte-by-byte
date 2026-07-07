# 💻 算法 / Algorithms — Day 84
## #621 Task Scheduler (Medium) — Heap / Priority Queue

🧩 **堆/优先队列模式 (5/7)** — 在 Kth Largest in Stream、Last Stone Weight、K Closest Points 的基础上进阶

---

## 中文部分

### 🔗 链接
- LeetCode: https://leetcode.com/problems/task-scheduler/ 🟡 Medium
- NeetCode: https://neetcode.io/problems/task-scheduling

---

### 🧩 模板回顾 (5/7)

上次我们用最小堆处理了 "K Closest Points"（维护大小为 k 的堆）。今天的 Task Scheduler 是一个**不同的堆变体**：我们需要贪心地总是选"剩余最多的任务"来最小化总时间。

```
第 1 题: #703 Kth Largest in Stream → 维护大小 k 的最小堆
第 2 题: #1046 Last Stone Weight    → 最大堆 + 模拟
第 3 题: #973 K Closest Points      → 维护大小 k 的最大堆（反转距离）
第 4 题: #215 Kth Largest in Array  → QuickSelect 或堆
第 5 题: #621 Task Scheduler         → 最大堆 + 等待队列（今天）
第 6 题: #355 Design Twitter         → 堆合并多个 feed
第 7 题: #295 Find Median            → 双堆（最大+最小）
```

**今天的变体**：不是 top-k，而是"贪心调度 + 冷却时间"。

---

### 🎯 问题理解

给你一个任务列表（如 `['A','A','A','B','B','B']`）和冷却时间 `n`。
同一任务两次执行之间必须间隔 ≥ n 个时间单位。求完成所有任务的最少时间。

**真实场景类比**：CPU 调度。高频任务（如缓存刷新）不能连续执行，需要冷却防止过热。

```
n=2, tasks = [A,A,A,B,B,B]

时间轴: A → B → idle → A → B → idle → A → B
         1   2    3     4   5    6      7   8
结果: 8 个时间单位
```

---

### 💡 核心洞察：为什么用堆？

**贪心规则**：每次优先执行剩余次数最多的任务 → 最小化 idle 时间。
**堆的作用**：在 O(log k) 内找到当前最高频任务。

---

### 🐍 Python 解法（堆 + 等待队列）

```python
import heapq
from collections import Counter, deque

def leastInterval(tasks: list[str], n: int) -> int:
    # Step 1: Count frequencies
    freq = Counter(tasks)
    
    # Max-heap: Python's heapq is min-heap, so negate counts
    # heap: [-count, task]
    max_heap = [-cnt for cnt in freq.values()]
    heapq.heapify(max_heap)
    
    # Wait queue: [(available_time, -count)]
    wait_queue = deque()
    
    time = 0
    
    while max_heap or wait_queue:
        time += 1
        
        if max_heap:
            # Execute the most frequent task
            neg_cnt = heapq.heappop(max_heap)
            neg_cnt += 1  # count decreases by 1 (neg becomes less negative)
            
            if neg_cnt != 0:
                # Task still has remaining count; can run again at time + n
                wait_queue.append((time + n, neg_cnt))
        
        # Check if any task in wait queue is now available
        if wait_queue and wait_queue[0][0] == time:
            _, neg_cnt = wait_queue.popleft()
            heapq.heappush(max_heap, neg_cnt)
    
    return time

# Trace for tasks = [A,A,A,B,B,B], n=2
# Heap initial: [-3, -3] (A=3, B=3)
# t=1: pop A (-3→-2), wait until t=3. Heap: [-3]. Wait: [(3,-2)]
# t=2: pop B (-3→-2), wait until t=4. Heap: []. Wait: [(3,-2),(4,-2)]
# t=3: Heap empty → idle. But (3,-2) is available → push back. Heap: [-2]
# t=4: pop A (-2→-1), wait until t=6. (4,-2) available → push B. Heap: [-2]
# t=5: pop B (-2→-1), wait until t=7. Heap: []. Wait: [(6,-1),(7,-1)]
# t=6: Heap empty → idle. (6,-1) available → push A. Heap: [-1]
# t=7: pop A (-1→0), done. (7,-1) available → push B. Heap: [-1]
# t=8: pop B, done. Total: 8 ✅
```

**时间复杂度**: O(n log k)，n = 任务总数，k = 不同任务种类数（≤26）
**空间复杂度**: O(k)

---

### 🔗 与模式中其他题目对比

| 题目 | 堆类型 | 核心操作 | 关键差异 |
|------|--------|----------|----------|
| #703 Kth Largest Stream | 最小堆(大小k) | 维护 top-k | 固定堆大小 |
| #1046 Last Stone Weight | 最大堆 | 弹出两个合并 | 两次 pop |
| #973 K Closest Points | 最大堆(大小k) | 维护 k 近 | 距离比较 |
| **#621 Task Scheduler** | **最大堆+队列** | **调度+等待** | **时间轴 + 冷却** |
| #355 Design Twitter | 堆合并 | 多路归并 | 跨 feed |
| #295 Find Median | 双堆 | 平衡两堆 | 维护中位数 |

**Task Scheduler 的独特性**：引入了"时间"维度。不只是从堆里取最大，还要考虑冷却窗口，用 deque 追踪何时可以重新调度。

---

### 举一反三

**相同模式的变种**：
- "Design Twitter" (#355) — 同样需要从多个频率列表调度
- "Reorganize String" (#767) — 类似的贪心，确保相邻字符不同

**数学捷径**（面试中可以提到）：
```python
def leastInterval_math(tasks, n):
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(1 for v in freq.values() if v == max_freq)
    # Formula: max((max_freq-1)*(n+1) + max_count, len(tasks))
    return max((max_freq - 1) * (n + 1) + max_count, len(tasks))
```
但面试时优先展示堆解法，更能体现你的思维过程。

---

## 📚 References
- [LeetCode #621 Discussion](https://leetcode.com/problems/task-scheduler/solutions/)
- [NeetCode Video Explanation](https://neetcode.io/problems/task-scheduling)
- [Heap Pattern Overview — NeetCode](https://neetcode.io/roadmap)

## 🧒 ELI5
Imagine you have a robot that can cook pasta (A), pasta (A), pasta (A), soup (B), soup (B), soup (B). But the pasta pot needs 2 minutes to cool before you use it again. The robot should always cook the dish it has the most of next — so it never wastes time waiting. That's the heap trick: always pick the most-needed dish that's cooled down enough!
