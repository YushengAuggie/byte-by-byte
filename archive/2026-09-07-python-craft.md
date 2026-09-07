# 🐍 Python Craft — Day 128 (Synthesis: Expert)

> **合成模式** — 50个精选主题已全部覆盖。今天深度合成：Python 性能优化全景——从 profiling 到生产。

---

## Python 性能优化全景 / Python Performance Optimization: End-to-End

---

### 🎯 系统性思维：先测量，再优化

**The #1 rule: Profile before you optimize.**

```
过早优化 → 浪费时间优化不重要的路径
正确流程: Measure → Identify bottleneck → Fix → Re-measure
```

---

### 第一层：找到瓶颈 / Layer 1: Find the Bottleneck

我们在 Day 97 覆盖了 profiling，今天把它和后续所有优化工具串联起来：

```python
# 1. cProfile — CPU 耗时 (Day 97)
import cProfile
cProfile.run('my_function()')

# 2. line_profiler — 行级分析
# pip install line-profiler
# @profile 装饰器 + kernprof -l -v script.py

# 3. memory_profiler — 内存耗用
# pip install memory-profiler
# @profile 装饰器 + python -m memory_profiler script.py

# 快速判断: CPU-bound 还是 I/O-bound?
import time
start = time.perf_counter()
result = your_function()
elapsed = time.perf_counter() - start
# CPU-bound: 优化算法/并行; I/O-bound: 异步/连接池
```

---

### 第二层：算法与数据结构 / Layer 2: Algorithms & Data Structures

最大的性能提升往往来自算法改进，而非底层优化：

```python
# ❌ O(n²) 查找
def has_duplicate_slow(lst):
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]: return True
    return False

# ✅ O(n) 使用 set
def has_duplicate_fast(lst):
    return len(lst) != len(set(lst))

# 关键数据结构选择:
# list.append O(1), list.insert(0,x) O(n)
# dict/set lookup O(1), list lookup O(n)
# collections.deque popleft() O(1), list.pop(0) O(n)
# heapq for top-K, sorted() for full sort
```

---

### 第三层：Python 内置优化 / Layer 3: Python Built-ins

```python
# ✅ 列表推导式 vs 循环 (~2x faster)
squares = [x*x for x in range(10000)]  # faster
squares = list(map(lambda x: x*x, range(10000)))  # comparable

# ✅ join vs += for strings (O(n) vs O(n²))
result = ''.join(parts)  # ✅
result = ''
for p in parts: result += p  # ❌ O(n²)

# ✅ lru_cache for memoization (Day 101 caching)
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)

# ✅ slots for memory-heavy objects
class Point:
    __slots__ = ['x', 'y']  # 40-50% less memory than dict
    def __init__(self, x, y): self.x, self.y = x, y
```

---

### 第四层：并发策略 (综合 Day 46-49) / Layer 4: Concurrency

```
任务类型         最佳方案
────────────────────────────────
CPU-bound       multiprocessing.Pool (绕过 GIL)
I/O-bound多任务  asyncio (协程，低开销)
I/O-bound线程   threading (简单 I/O，如文件读写)
混合            ProcessPoolExecutor + asyncio

# 黄金法则: 不要在 async 函数里调用阻塞 I/O
# ❌ async def fetch(): time.sleep(1)
# ✅ async def fetch(): await asyncio.sleep(1)
```

---

### 第五层：生产级优化 / Layer 5: Production

```python
# 1. 连接池 (Day 78) — 避免每次请求重建连接
from sqlalchemy import create_engine
engine = create_engine(url, pool_size=10, max_overflow=20)

# 2. 序列化选型 (Day 102)
# JSON: 通用，慢 | msgpack: 快2-10x | protobuf: schema强
import msgpack
data = msgpack.packb({'key': 'value'})  # faster than json

# 3. 生成器节省内存 (Day 98)
def read_large_file(path):
    with open(path) as f:
        for line in f: yield line.strip()
# 不会把整个文件读入内存

# 4. NumPy 向量化 (如适用)
import numpy as np
a = np.array([1,2,3,4,5])
result = a * 2 + 1  # 比 Python loop 快 100x
```

---

### 🔑 优化决策树 / Optimization Decision Tree

```
性能问题
    ↓
先 profile (cProfile/line_profiler)
    ↓
CPU-bound?
    ├─ Yes → 算法优化 → multiprocessing → NumPy/Cython
    └─ No (I/O-bound?)
           ├─ Yes → asyncio / 连接池 / 批量请求
           └─ Memory? → 生成器 / __slots__ / 更好的数据结构
```

---

## 📚 References
- https://docs.python.org/3/library/profile.html — cProfile 官方文档
- https://pymotw.com/3/concurrency.html — Python 并发全览
- https://wiki.python.org/moin/PythonSpeed/PerformanceTips — Python 性能 Tips 官方

## 🧒 ELI5
优化代码就像整理你的房间。第一步是找出最乱的地方（profiling），而不是随便整理。然后优先整理最影响你的区域（算法）。最后才是买更好的收纳盒（底层工具）。先找问题，再找解法。
