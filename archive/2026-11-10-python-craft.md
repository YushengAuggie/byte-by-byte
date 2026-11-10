# Python 内存模型深度解析 — 对象、引用、垃圾回收的完整图景

> Day 152 | Python Craft Synthesis | 2026-11-10

---

🐍 **Python 工坊 / Python Craft** *(2 min)*

**综合主题：Python 对象模型 + 垃圾回收 + 内存陷阱**
**Synthesis: Python Object Model + GC + Memory Gotchas**

---

### 一切皆对象，但不是你想的那样 / Everything Is an Object, But Not How You Think

```python
import sys
import gc

# --- 1. Reference Counting (Day 73 revisit) ---
a = [1, 2, 3]
b = a          # refcount = 2
print(sys.getrefcount(a))  # 3 (getrefcount itself holds a temp ref)

del b          # refcount → 2 (getrefcount arg + a)
del a          # refcount → 0 → CPython frees immediately

# --- 2. Circular Reference — Where refcount FAILS ---
class Node:
    def __init__(self):
        self.ref = None

x = Node()
y = Node()
x.ref = y     # y refcount = 2
y.ref = x     # x refcount = 2

del x         # x refcount = 1, NOT 0 — leaked!
del y         # y refcount = 1, NOT 0 — leaked!
# CPython's generational GC (Day 73) detects this cycle
gc.collect()  # force cycle collection
print(gc.garbage)  # [] if __del__ not defined

# --- 3. Small Integer Interning ---
a = 256
b = 256
print(a is b)  # True — CPython caches -5..256

a = 257
b = 257
print(a is b)  # False in most cases (implementation-dependent)
# ✅ Always use == for value comparison, never `is` for non-singletons

# --- 4. String Interning (関键面试坑) ---
s1 = "hello"
s2 = "hello"
print(s1 is s2)   # True — compile-time interning

s3 = "hello world"
s4 = "hello world"
print(s3 is s4)   # True if compile-time constant, False at runtime

s5 = "hello" + " world"
s6 = "hello" + " world"
print(s5 is s6)   # True — CPython constant-folds literal concatenation at compile time!

# ⚠️ Only truly dynamic (runtime) concat avoids interning:
def concat(a, b): return a + b
s7, s8 = concat("hello", " world"), concat("hello", " world")
print(s7 is s8)   # False — genuinely runtime, no interning

# --- 5. __slots__ — Eliminating __dict__ Overhead ---
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

import tracemalloc
tracemalloc.start()
points_regular = [RegularPoint(i, i) for i in range(100_000)]
snap1 = tracemalloc.take_snapshot()

tracemalloc.clear_traces()
points_slotted = [SlottedPoint(i, i) for i in range(100_000)]
snap2 = tracemalloc.take_snapshot()

# Slotted uses ~3x less memory — critical for large data structures
```

---

### 知识综合 / Synthesis Map

| 主题 | 今天的连接 |
|------|-----------|
| 引用计数 (Day 73) | 循环引用如何绕过它 |
| 垃圾回收 (Day 73) | 分代 GC 填补引用计数的漏洞 |
| dataclasses (Day 99) | `__slots__` + dataclass = 内存高效的数据容器 |
| 序列化 (Day 102) | 内存模型决定 pickle 能/不能序列化什么 |
| GIL (Day 54) | GIL 与引用计数的关系：保护 refcount 操作原子性 |

---

### 常见坑 / Common Gotchas

```python
# ❌ Mutable default argument — classic Python gotcha
def append_to(element, to=[]):  # `to` created ONCE at function definition
    to.append(element)
    return to

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] ← NOT [2]!

# ✅ Correct: use None sentinel
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```

---

### 🧒 ELI5

Python 变量不是盒子，是便利贴。每个对象是一个盒子，变量是贴在盒子上的标签。`del x` 只是撕掉标签，不是砸碎盒子。当一个盒子上没有任何标签，Python 才回收它。

*Python variables aren't boxes, they're sticky notes. Objects are boxes; variables are labels attached to them. `del x` removes the label, not the box. Python recycles the box only when it has zero labels.*

---

### 📚 References

- https://docs.python.org/3/c-api/refcounts.html — CPython reference counting internals
- https://devguide.python.org/internals/garbage-collector/ — Python GC deep dive
- https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Use___slots__ — __slots__ performance
