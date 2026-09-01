# 🐍 Python Craft — Day 123 (Expert Synthesis)

> **合成模式** — 所有 50 个 Python Craft 主题已完成。今日深度合成：Python 内存模型与对象生命周期。

---

## 深度合成：你真的理解 Python 怎么管理内存吗？
## Deep Synthesis: Do You Really Understand Python's Memory Model?

综合 Day 48 (asyncio)、Day 54 (GIL)、Day 73 (GC) 的底层视角。

---

### 三层内存管理架构

```
┌─────────────────────────────────────────┐
│  Layer 3: Object-specific allocators    │
│  (int cache, list free list, etc.)      │
├─────────────────────────────────────────┤
│  Layer 2: pymalloc (Python's allocator) │
│  Manages 8-512 byte objects in arenas   │
├─────────────────────────────────────────┤
│  Layer 1: malloc / OS allocator         │
│  Large objects (>512 bytes) go here     │
└─────────────────────────────────────────┘
```

---

### 对象缓存：Python 偷偷帮你做的优化

```python
# Small integers are CACHED (-5 to 256)
a = 100; b = 100
print(a is b)   # True — same object!

a = 1000; b = 1000
print(a is b)   # False — different objects

# Interned strings (compile-time constants)
a = "hello"; b = "hello"
print(a is b)   # True — interned

a = "hello world"; b = "hello world"
print(a is b)   # True in CPython (often)

# But:
a = "hello" + " world"  # runtime concat
b = "hello world"
print(a is b)   # Depends on implementation! Never rely on this
```

**关键：用 `==` 比较值，用 `is` 比较身份（只用于 None/True/False）**

---

### 引用计数 + 循环垃圾回收

```python
import gc
import sys

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

# Reference counting: works for acyclic graphs
a = Node(1)      # refcount(a) = 1
b = a            # refcount(a) = 2
del a            # refcount = 1, NOT freed yet
del b            # refcount = 0, freed immediately ← CPython

# PROBLEM: Circular references leak with ref counting alone
a = Node(1)
b = Node(2)
a.next = b
b.next = a       # cycle: a → b → a
del a, b         # refcounts both = 1, NOT 0! Memory leak!

# Solution: gc module handles cycles
gc.collect()     # force cycle collection
print(sys.getrefcount(None))  # always huge — None is everywhere
```

**三代 GC：** 新对象在 Generation 0。存活过几次 GC → 升代。Generation 2 很少被扫（开销最小）。

---

### 实战：用 `__slots__` 节省大量内存

```python
import sys

class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

d = WithDict(1, 2)
s = WithSlots(1, 2)

print(sys.getsizeof(d))           # ~56 bytes
print(sys.getsizeof(d.__dict__))  # ~112 bytes — hidden cost!
print(sys.getsizeof(s))           # ~56 bytes (no __dict__)

# For 1 million objects:
# WithDict:   ~168 MB (56 + 112)
# WithSlots:  ~56 MB
# Savings: ~67%!
```

**何时用 `__slots__`：** 大量同类型对象（如图节点、数据行）。代价：不能动态添加属性，不能多继承 slots 类。

---

### weakref：打破循环引用的利器

```python
import weakref

class Cache:
    def __init__(self):
        self._cache = {}  # strong refs — objects never freed!
    
class BetterCache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()  # weak refs
        # When the object has no other refs, it's freed automatically
        # AND removed from the dict

obj = SomeExpensiveObject()
cache = BetterCache()
cache._cache['key'] = obj
del obj  # freed immediately; cache auto-cleans
```

**应用：** LRU cache eviction、事件系统（观察者不应持有 subject 的强引用）、Django ORM 的 model registry。

---

### 🧒 ELI5

Python 给每个东西贴一个"有几个人在用我"的标签。没人用了就扔掉。但两个东西互相指着对方，标签永远不会变 0——所以 Python 还有个清洁工（GC）专门找这种"死循环"扔掉。`__slots__` 就是告诉 Python"这个对象只有这几个属性"，省掉了一个隐藏的字典，内存更省。

---

### 📚 References
- https://docs.python.org/3/c-api/memory.html (CPython memory management)
- https://docs.python.org/3/library/gc.html (gc module)
- https://docs.python.org/3/reference/datamodel.html#slots (__slots__)
- https://pympler.readthedocs.io/en/stable/ (memory profiling tool)
