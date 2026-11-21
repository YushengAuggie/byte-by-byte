# 🐍 Python Craft — Day 153 (Synthesis)
**深度：Python 内存模型 + 对象生命周期全景图**

---

## 综合主题

我们覆盖过 GIL（Day 54）、垃圾回收（Day 73）、描述符（Day 68）、元类（Day 69）。今天串联成一张完整的**对象生命周期地图**：从创建到销毁，Python 在内存里做了什么？

---

## Python 对象生命周期全景

```
创建阶段:
  MyClass()
    → type.__call__()
    → MyClass.__new__()   ← 分配内存 (PyObject_Malloc)
    → MyClass.__init__()  ← 初始化状态
    → 引用计数 refcount = 1

存活阶段:
  x = obj    → refcount = 2
  del x      → refcount = 1
  func(obj)  → refcount 临时 +1，调用结束 -1

销毁阶段:
  refcount → 0
    → __del__() 调用 (finalizer)
    → PyObject_Free() 释放内存
  
  循环引用:
    a.ref = b; b.ref = a → 两个 refcount 永远 ≥ 1
    → 分代 GC (gc module) 检测并清理
```

---

## 运行示例：追踪对象生命

```python
import sys
import gc

class Tracked:
    def __init__(self, name):
        self.name = name
        print(f"[CREATE] {name}")
    
    def __del__(self):
        # Note: __del__ not guaranteed to be called on interpreter shutdown
        print(f"[DESTROY] {self.name}")

# --- 引用计数演示 ---
a = Tracked("Alpha")           # refcount = 1
print(sys.getrefcount(a))      # 2 (getrefcount itself adds 1 temp ref)

b = a                          # refcount = 2
del a                          # refcount = 1, NOT destroyed yet
del b                          # refcount = 0, DESTROY now

# --- 循环引用演示 ---
class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

n1 = Node("n1")
n2 = Node("n2")
n1.next = n2   # n2 refcount = 2
n2.next = n1   # n1 refcount = 2
del n1         # n1 refcount = 1 (still alive via n2.next)
del n2         # n2 refcount = 1 (still alive via n1.next)
# Both are leaked! Manual GC:
collected = gc.collect()
print(f"GC collected {collected} objects")  # GC collected 2 objects

# --- 分代 GC 参数 ---
# gc.get_threshold() → (700, 10, 10)
# Gen 0: 新对象，每 700 次分配触发一次
# Gen 1: Gen 0 幸存者，每 10 次 Gen 0 触发一次
# Gen 2: 长期对象，每 10 次 Gen 1 触发一次
print(gc.get_threshold())  # (700, 10, 10)
```

---

## 实战：weakref 打破循环引用

```python
import weakref

class Cache:
    def __init__(self):
        # Strong ref: prevents GC
        # self._items = {}
        
        # Weak ref: allows GC when no other references exist
        self._items = weakref.WeakValueDictionary()
    
    def set(self, key, value):
        self._items[key] = value
    
    def get(self, key):
        return self._items.get(key)  # Returns None if GC'd

cache = Cache()
obj = SomeExpensiveObject()
cache.set("key", obj)
del obj  # Cache doesn't prevent GC → memory freed
```

---

## 性能陷阱 + 最佳实践

| 场景 | ❌ 问题 | ✅ 修复 |
|------|---------|---------|
| 大量临时对象 | GC 压力大，STW pause | 用对象池 / `__slots__` |
| 循环引用 | 内存泄漏 | weakref 或重构依赖方向 |
| `__del__` 依赖顺序 | 不可靠（解释器退出时顺序无保证） | 用 `contextlib.closing` 或 with 语句 |
| 长期运行服务 | Gen 2 积累，GC pause 变长 | `gc.freeze()` 冻结稳定对象到 Gen 2 |

```python
# Production tip: freeze long-lived objects to avoid GC overhead
# (Used by Instagram to reduce GC pause by ~10%)
import gc
gc.collect()   # Force collect before freeze
gc.freeze()    # Move all current objects to permanent generation
```

---

## 连接之前的知识

- **GIL（Day 54）**：GIL 保护引用计数操作是原子的，refcount++ 不会 race condition
- **垃圾回收（Day 73）**：分代 GC 只处理循环引用，refcount 处理其余
- **描述符（Day 68）**：`__get__/__set__` 触发时对象已经存活（refcount ≥ 1）
- **元类（Day 69）**：`type.__call__` 控制 `__new__` + `__init__` 的调用顺序

---

## 📚 References
- https://devguide.python.org/internals/garbage-collector/
- https://instagram-engineering.com/dismissing-python-garbage-collection-at-instagram-4dca40b29172
- https://docs.python.org/3/library/gc.html

## 🧒 ELI5
Python 追踪每个对象被多少个变量"指向"。指向数变成 0，对象立刻被删除——就像一个蜡烛，所有人都松手它就熄灭。但如果两个蜡烛互相抓住对方，就算没人拿着它们也不会熄灭——这就是循环引用，需要专门的"循环检测员"（GC）来打破。
