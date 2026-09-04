# Python Craft 合成 / Python Craft Synthesis — Day 126

🐍 **Python Craft 合成 / Python Craft Synthesis**
**第 126 天 · Expert 阶段 · 内存与对象系统深度合成**

---

## Python 对象内存全景——__slots__、weakref、对象布局
## Python Object Memory: __slots__, weakref, and Layout Deep Dive

你在做一个 dashboard，需要在内存中维持 100 万个 DataPoint 对象。Python 的默认对象有多重？怎么让它们变轻？

*You're building a dashboard that holds 1 million DataPoint objects in memory. How heavy is a default Python object? How do you make it lighter?*

---

### Python 对象的默认内存布局 / Default Object Layout

```python
import sys

class DataPoint:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

p = DataPoint(1.0, 2.0, 3.14)
print(sys.getsizeof(p))          # ~48 bytes (object shell)
print(sys.getsizeof(p.__dict__)) # ~232 bytes (the real cost!)
# Total: ~280 bytes per instance
```

**为什么 `__dict__` 这么重？**
每个实例的 `__dict__` 是一个完整的 Python dict：初始分配 8 个槽位，每个槽位 24 bytes。即使你只存 3 个属性，也要为未来的动态属性预留空间。

---

### `__slots__` — 消除 `__dict__`

```python
class DataPointSlots:
    __slots__ = ('x', 'y', 'value')  # declare allowed attributes
    
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

p2 = DataPointSlots(1.0, 2.0, 3.14)
print(sys.getsizeof(p2))  # ~72 bytes — no __dict__!
# hasattr(p2, '__dict__')  → False
# p2.new_attr = 42         → AttributeError!
```

**内存对比 (1,000,000 个对象):**
| 方式 | 单对象大小 | 100万对象总内存 |
|------|-----------|---------------|
| 普通 class | ~280 bytes | ~267 MB |
| `__slots__` | ~72 bytes | ~69 MB |
| **节省** | — | **~74%** |

---

### weakref — 引用不阻止垃圾回收

```python
import weakref
import gc

class Cache:
    pass

obj = Cache()
weak = weakref.ref(obj)   # weak reference — doesn't increment refcount

print(weak())             # <__main__.Cache object>
del obj
gc.collect()
print(weak())             # None — object was collected!
```

**适用场景：**
- 观察者模式：listener 持有 weak ref，防止因订阅而泄漏对象
- 缓存：`weakref.WeakValueDictionary` — 值被删除时 key 自动消失
- 双向引用：父对象持强引用子对象，子对象用 weakref 指回父对象，打破循环

```python
from weakref import WeakValueDictionary

# Cache that doesn't prevent GC
cache: WeakValueDictionary[str, Cache] = WeakValueDictionary()
obj = Cache()
cache['key'] = obj
print(dict(cache))   # {'key': <Cache>}
del obj
print(dict(cache))   # {} — auto-cleaned!
```

---

### 综合应用：高性能对象池

```python
import weakref
from typing import Optional

class PooledObject:
    __slots__ = ('_id', '_data', '__weakref__')  # __weakref__ needed for weakref support!
    
    def __init__(self, id: int):
        self._id = id
        self._data: dict = {}
    
    @property
    def id(self) -> int:
        return self._id

class ObjectPool:
    def __init__(self, max_size: int = 1000):
        self._pool: weakref.WeakValueDictionary[int, PooledObject] = weakref.WeakValueDictionary()
        self._max = max_size
    
    def get(self, id: int) -> Optional[PooledObject]:
        return self._pool.get(id)
    
    def register(self, obj: PooledObject) -> None:
        self._pool[obj.id] = obj  # GC can reclaim when no strong refs remain
```

注意：`__slots__` + `weakref` 需要显式把 `'__weakref__'` 加入 `__slots__`，否则 `weakref.ref()` 会报错。

---

### 猜猜输出什么？/ Quiz

```python
class A:
    __slots__ = ('x',)

class B(A):
    pass  # No __slots__ defined!

b = B()
b.x = 1
b.y = 2   # What happens?
print(hasattr(b, '__dict__'))
```

**A)** AttributeError on `b.y`
**B)** Works fine, b has both `__slots__` x and `__dict__`
**C)** Works fine, but `__dict__` is empty
**D)** Works fine, but x is not accessible

**答案 / Answer: B** — 子类没定义 `__slots__` 时，继承会重新引入 `__dict__`。只有整个继承链都定义 `__slots__` 才能完全消除 `__dict__`。

---

### 整合三个概念 / Synthesis

| 技术 | 核心用途 | 成本 |
|------|---------|------|
| `__slots__` | 减少每实例内存，固化 API | 失去动态属性，weakref 需要显式声明 |
| `weakref` | 打破循环引用，实现 ephemeral cache | 不能用于内置类型（int, str 等） |
| `__dict__` | 灵活性，动态属性 | 每实例 ~200+ bytes overhead |

**黄金原则：**
- 高频创建的值对象（DataPoint, Event, Record）→ 用 `__slots__`
- 观察者、缓存、双向关联 → 考虑 `weakref`
- 灵活配置对象、原型阶段 → 默认 `__dict__` 即可

---

📚 **References:**
- https://docs.python.org/3/reference/datamodel.html#slots — 官方 __slots__ 文档
- https://docs.python.org/3/library/weakref.html — weakref 模块文档
- https://realpython.com/python-slots/ — Real Python: __slots__ 详解

🧒 **ELI5:** 默认 Python 对象像带很多抽屉的柜子（__dict__）。`__slots__` 说"我只需要 3 个固定格子"，省掉了柜子框架。`weakref` 是"便利贴"——别人看到对象，但你把便利贴扔掉后对象还是会消失。
