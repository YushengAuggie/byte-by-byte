# 🐍 Python Craft — Day 156 (Synthesis)
## 深度综合: Python 内存模型全景 — 对象、引用、GC、__slots__ 的统一视角
## Deep Synthesis: Python Memory Model — Objects, References, GC, and __slots__ Unified

> 综合回顾: GC (Day 73), Metaclasses (Day 69), dataclasses (Day 99), Descriptors (Day 68)

---

### 🧠 Python 对象的内存代价 / Memory Cost of a Python Object

很多人不知道：**Python 中每个对象都是一个 C 结构体，最小开销约 56 字节**（64位系统）。

```python
import sys

x = 42          # int
print(sys.getsizeof(x))   # 28 bytes

y = "hello"
print(sys.getsizeof(y))   # 54 bytes

z = []
print(sys.getsizeof(z))   # 56 bytes (empty list!)

# A simple instance
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(sys.getsizeof(p))           # ~48 bytes (just the shell)
print(sys.getsizeof(p.__dict__))  # ~232 bytes (the dict!)
# Total: ~280 bytes for two integers!
```

**结论**：普通类实例用 `__dict__` 存属性，字典开销巨大。

---

### ⚡ __slots__ 的威力 / The Power of __slots__

```python
from dataclasses import dataclass

# Regular class: uses __dict__
class PointDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With __slots__: no __dict__, uses fixed offsets
class PointSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

# dataclass with slots (Python 3.10+)
@dataclass(slots=True)
class PointDC:
    x: float
    y: float

import tracemalloc
tracemalloc.start()

# Create 1 million points
points_dict  = [PointDict(i, i)  for i in range(1_000_000)]
points_slots = [PointSlots(i, i) for i in range(1_000_000)]

# PointDict:  ~280 MB
# PointSlots: ~56 MB  (5x smaller!)
# Attribute access is also faster (no dict lookup)
```

---

### 🔄 引用计数 + 循环 GC / RefCount + Cyclic GC

```python
import gc
import ctypes

# Python uses reference counting as primary GC
a = [1, 2, 3]
# refcount = 1

b = a
# refcount = 2

del a
# refcount = 1 (b still holds reference)

del b
# refcount = 0 → immediately deallocated (no GC needed!)

# Problem: circular references
class Node:
    def __init__(self):
        self.ref = None

x = Node()
y = Node()
x.ref = y   # x → y
y.ref = x   # y → x  (cycle!)

del x, y
# refcount never hits 0!
# Python's cyclic GC (gc module) handles this in generation sweeps

gc.collect()  # Force a cycle collection
print(gc.get_count())  # (gen0, gen1, gen2) object counts
```

---

### 🎯 实战决策 / When to Use What

```
大量小对象 (坐标、事件、消息)?
  → __slots__ 或 dataclass(slots=True)
  → 节省 60-80% 内存

需要动态属性 (__dict__)?
  → 普通类，接受内存开销

不可变数据?
  → NamedTuple (C struct 级别, 比 slots 还快)

性能极限?
  → numpy arrays / ctypes structs / array.array
```

---

### 📊 对比总结 / Comparison

| 方式 | 内存/实例 | 属性访问速度 | 动态属性 | 推荐场景 |
|---|---|---|---|---|
| 普通类 | ~280B | 中 | ✅ | 通用 |
| `__slots__` | ~56B | 快 | ❌ | 大量小对象 |
| `dataclass(slots=True)` | ~56B | 快 | ❌ | 数据容器 |
| `NamedTuple` | ~72B | 最快 | ❌ | 不可变数据 |
| `numpy` array | 8B/元素 | 极快 | ❌ | 数值计算 |

---

### 🧒 ELI5

Python 对象就像酒店房间：普通类是套房，有个大衣柜（`__dict__`），可以放任何东西，但很贵。`__slots__` 是标准间，只有固定数量的抽屉，住1000人省很多钱。

---

### 📚 References
- https://docs.python.org/3/reference/datamodel.html#slots
- https://realpython.com/python-slots/
- https://rushter.com/blog/python-memory-and-ref-counting/
