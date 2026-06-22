# 🎨 Python Craft — Day 22
**Topic:** Garbage Collection — Reference Counting + Generational GC
**Category:** Python Internals
**Date:** 2026-06-22

---

## 真实场景 / Real Scenario

你在做一个高并发的 web 服务，发现内存随时间线性增长，重启后才恢复正常。是内存泄漏？还是 GC 没回收？这道题就是要搞清楚 CPython 的内存管理机制。

You're running a high-traffic web service and notice memory grows linearly over time, only recovering after restarts. Is it a leak, or GC not collecting? This is exactly why you need to understand CPython's memory model.

---

## 核心概念 / Core Concepts

### 1. 引用计数 / Reference Counting (Primary GC)

CPython 的核心机制：每个对象维护一个 `ob_refcnt`。引用增加 +1，引用消失 -1，归零立即释放。

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2: 'a' + getrefcount's temp ref

b = a
print(sys.getrefcount(a))  # 3: 'a', 'b', + temp ref

del b
print(sys.getrefcount(a))  # 2: back to 'a' + temp ref

# When refcount hits 0 → __del__ called → memory freed immediately
```

**优点：** 确定性（立即释放），低 overhead
**缺点：** 无法处理循环引用！

### 2. 循环引用问题 / Circular Reference Problem

```python
import gc

# Create a reference cycle
a = {}
b = {}
a['b'] = b  # a → b
b['a'] = a  # b → a  ← cycle!

# Delete our references
del a, b
# Neither object's refcount hits 0!
# a.refcnt = 1 (b still points to it)
# b.refcnt = 1 (a still points to it)
# Both are leaked... until the cycle collector runs

gc.collect()  # Manually trigger cycle collection
print(gc.garbage)  # Objects that couldn't be freed (if they have __del__)
```

### 3. 分代垃圾回收 / Generational GC (Cycle Collector)

CPython 用三代（generation 0, 1, 2）来管理循环引用：

```
Generation 0: 新创建的对象 → 最频繁回收 (threshold: 700 new objects)
Generation 1: 在 gen0 中存活的 → 每 10次 gen0 回收触发一次
Generation 2: 长寿对象 → 每 10次 gen1 回收触发一次

"年轻人死得快，老人活得久" — 统计规律
```

```python
import gc

# Check current thresholds
print(gc.get_threshold())   # (700, 10, 10) — default

# Check object counts per generation
print(gc.get_count())       # (current_gen0, current_gen1, current_gen2)

# Tune for high-throughput servers
gc.set_threshold(10000, 10, 10)  # Reduce gen0 frequency → less GC pause

# Disable GC entirely (Instagram/Pinterest pattern for batch jobs)
gc.disable()
# ... do batch work ...
gc.collect()  # One big collection at the end
gc.enable()
```

---

## ❌ 常见内存泄漏 / Common Leak Patterns

```python
# ❌ Pattern 1: Unbounded cache
_cache = {}
def get_data(key):
    if key not in _cache:
        _cache[key] = fetch_expensive(key)  # Never evicted!
    return _cache[key]

# ✅ Fix: Use weakref or functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_data(key):
    return fetch_expensive(key)

# ❌ Pattern 2: Event listener not removed
class Widget:
    def __init__(self, event_bus):
        event_bus.subscribe('click', self.on_click)  # Strong ref!
    # Widget deleted, but event_bus still holds reference → leak

# ✅ Fix: Use weakref
import weakref
event_bus.subscribe('click', weakref.ref(self.on_click))
```

---

## 实用调试 / Debug in Practice

```python
# Find what's holding a reference
import gc
import sys

obj = [1, 2, 3]
referrers = gc.get_referrers(obj)
print(f"Object has {sys.getrefcount(obj)} refs")
print(f"Referred to by: {len(referrers)} objects")

# Track object counts over time (memory profiling)
import tracemalloc
tracemalloc.start()

# ... do work ...

snapshot = tracemalloc.take_snapshot()
stats = snapshot.statistics('lineno')
for stat in stats[:5]:
    print(stat)  # Top memory consumers by line
```

---

## 🧒 ELI5

想象每个对象是一个气球，上面绑着绳子。有几根绳子就是引用计数。所有绳子都断了，气球飘走（内存释放）。但如果两个气球互相绑在一起，就算你放开了，它们还在相互牵扯 — 这就是循环引用。分代 GC 是个清洁工，专门去找这种互相牵扯的气球群，剪断它们。

---

## 📚 References
- CPython Memory Management: https://docs.python.org/3/c-api/memory.html
- gc module docs: https://docs.python.org/3/library/gc.html
- Instagram's GC trick: https://instagram-engineering.com/dismissing-python-garbage-collection-at-instagram-4dca40b29172
- tracemalloc docs: https://docs.python.org/3/library/tracemalloc.html
