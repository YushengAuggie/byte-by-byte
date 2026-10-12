# Python Craft — Day 137 (Synthesis)
## 深入 Python 内存模型：对象、引用、GC 三位一体

🎨 **Python Craft — Expert Synthesis**
**综合主题：Python 内存模型全景 — 从对象到 GC**

> 综合覆盖：引用计数（Day 73）、GC（Day 54）、描述符（Day 68）、生成器（Day 98）

---

### 真实场景 / Real Scenario

你在做性能分析，发现一个 FastAPI 服务的内存持续增长但不触发 GC。你需要理解 Python 内存模型才能找到根因。

You're profiling a FastAPI service with creeping memory growth that doesn't trigger GC. Understanding Python's memory model is key to debugging.

---

### Python 对象内存布局 / Object Memory Layout

```python
import sys

# Every Python object has a header:
# ob_refcnt (reference count) + ob_type (type pointer)
x = [1, 2, 3]
print(sys.getsizeof(x))   # 88 bytes (list header + 3 pointers)
print(sys.getsizeof(1))   # 28 bytes (int object)

# Small ints [-5, 256] are cached — same object!
a = 256; b = 256
print(a is b)  # True  — same object
a = 257; b = 257
print(a is b)  # True in a script (CPython const-folding); False in interactive REPL
```

---

### 引用计数 + 循环引用 / Refcount + Cycles

```python
import gc
import ctypes

def show_refcount(obj):
    return ctypes.c_long.from_address(id(obj)).value

class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

# Create a reference cycle
a = Node("A")
b = Node("B")
a.next = b
b.next = a  # cycle!

# refcount never drops to 0 → CPython's cyclic GC must intervene
del a, b
# Objects are NOT freed yet — they're in gc's "unreachable" set
count = gc.collect()  # Now they're freed
print("Collected:", count)  # e.g. 4 (Node A, B + their __dict__)
```

**关键洞察：** CPython 的分代 GC（generation 0/1/2）专门处理循环引用。无循环引用的对象由引用计数立即释放，无需 GC 介入。

---

### 内存泄漏常见模式 / Common Leak Patterns

```python
# Pattern 1: Global cache without eviction ← 最常见
_cache = {}
def process(key, data):
    _cache[key] = data  # grows forever!
    # Fix: use functools.lru_cache or limit size

# Pattern 2: Closure capturing large objects
def make_handler(large_df):
    def handler(request):
        return large_df.shape  # large_df lives as long as handler!
    return handler
# Fix: capture only what you need
def make_handler(shape):
    def handler(request):
        return shape
    return handler

# Pattern 3: __del__ with cycles → prevents GC
class Bad:
    def __del__(self):
        pass  # Having __del__ + cycle = uncollectable in Python <3.4!
# Python 3.4+ fixed this, but still a smell
```

---

### 实用诊断工具 / Diagnostic Tools

```python
import tracemalloc
import linecache

# Trace top 10 memory allocations
tracemalloc.start()

# ... your code here ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
# Output: file.py:42: size=1.5 MiB, count=20000, average=78 B
```

```bash
# External tools
pip install memory-profiler
python -m memory_profiler your_script.py

# For heap dumps
pip install objgraph
python -c "import objgraph; objgraph.show_most_common_types(limit=10)"
```

---

### 📚 References
- https://realpython.com/python-memory-management/
- https://docs.python.org/3/library/gc.html
- https://pythonspeed.com/articles/python-memory-leaks/

### 🧒 ELI5
Python 给每个对象贴一个"被用了几次"的标签（引用计数）。标签归零就立刻删除。但如果 A 指着 B、B 指着 A，两个标签永远不归零——这时候需要 GC "垃圾侦探"来找出这些互相指的死循环，强制清理。
Python puts a "used N times" sticker on every object. Hit zero — deleted immediately. But if A points to B and B points to A, both stickers never hit zero. That's where Python's garbage collector acts as a detective, finding those loops and force-cleaning them.
