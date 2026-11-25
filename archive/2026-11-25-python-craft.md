# Day 157 — Python Craft Expert Synthesis
## Python 内存模型深挖：对象、引用与 CPython 内部
### Python Memory Model Deep Dive: Objects, References & CPython Internals

---

🐍 **Python Craft 综合 / Python Craft — Expert Synthesis**

*50 个 Python 话题走完，今天穿透表面，直击 CPython 内存模型——理解这个，你才真正懂 Python 为什么这样工作。*

---

## 想象你在调试一个神秘的内存泄漏...

```python
import gc

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

# 创建循环引用
a = Node(1)
b = Node(2)
a.next = b
b.next = a  # 循环！

del a
del b
# 问题：内存释放了吗？
print(gc.collect())  # 输出什么？为什么？
```

答案：`gc.collect()` 会返回 2（收集到了 2 个对象）——因为 CPython 的引用计数无法处理循环引用，需要靠**循环垃圾收集器**。

---

## 核心概念 1：一切皆对象，引用计数是第一道防线

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # 2（x + getrefcount参数）

y = x
print(sys.getrefcount(x))  # 3

del y
print(sys.getrefcount(x))  # 2（回到2）
```

**CPython 对象头（C struct 视角）：**
```c
typedef struct _object {
    Py_ssize_t ob_refcnt;    // 引用计数
    PyTypeObject *ob_type;   // 类型指针
} PyObject;
```

每次赋值 `y = x` → `ob_refcnt++`
每次 `del y` 或超出作用域 → `ob_refcnt--`
当 `ob_refcnt == 0` → 立即释放内存

---

## 核心概念 2：小整数缓存（让你的面试官眼前一亮）

```python
a = 256
b = 256
print(a is b)  # True — 同一对象！

a = 257
b = 257
print(a is b)  # False — 不同对象！（通常情况下）

# 为什么？CPython 预分配 -5 到 256 的整数对象
# 节省频繁创建小整数的开销
```

**字符串驻留（String Interning）：**
```python
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True — 驻留！

s1 = "hello world"
s2 = "hello world"  
print(s1 is s2)  # 可能 False — 含空格的字符串不自动驻留

# 显式驻留
import sys
s1 = sys.intern("hello world")
s2 = sys.intern("hello world")
print(s1 is s2)  # True
```

---

## 核心概念 3：分代垃圾收集器

```
Generation 0（新生代） → Generation 1 → Generation 2（老生代）

新创建对象进 Gen 0
Gen 0 满了触发 GC → 存活者晋升到 Gen 1
Gen 1 满了触发 GC → 存活者晋升到 Gen 2
Gen 2 是完整 GC（最慢，最少触发）
```

```python
import gc

# 查看各代阈值
print(gc.get_threshold())   # (700, 10, 10) 默认值
# Gen0: 700次分配触发；Gen1: Gen0收集10次触发；Gen2同理

# 查看各代当前对象数
print(gc.get_count())       # (当前gen0, gen1, gen2)

# 手动触发（生产代码里几乎不需要）
collected = gc.collect(0)   # 只收集gen0
collected = gc.collect()    # 完整收集
```

**实战应用 — 处理大量临时对象时：**
```python
import gc

def process_large_dataset(items):
    results = []
    for i, item in enumerate(items):
        result = expensive_transform(item)
        results.append(result)
        
        # 每 10000 个触发一次 GC，防止内存峰值过高
        if i % 10000 == 0:
            gc.collect(0)  # 只收年轻代，开销小
    
    return results
```

---

## 核心概念 4：`__slots__` — 节省 40-50% 内存

```python
# 普通 class：每个实例有个 __dict__（哈希表）
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 百万个 Point 对象 → 大量 __dict__ 开销

# __slots__：用固定内存布局替代 __dict__
class PointSlotted:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
p1 = Point(1, 2)
p2 = PointSlotted(1, 2)
print(sys.getsizeof(p1))  # ~56 bytes（不含 __dict__ 本身）
print(sys.getsizeof(p2))  # ~48 bytes

# __dict__ 额外占用约 232 bytes！
print(sys.getsizeof(p1.__dict__))  # 232 bytes
# p2 没有 __dict__
```

**什么时候用 `__slots__`：**
- ✅ 创建大量（>10万）的简单数据对象
- ✅ 属性固定，不需要动态添加
- ❌ 需要多重继承（会让 slots 变复杂）
- ❌ 需要 `__dict__`（pickling、动态属性等）

---

## 核心概念 5：弱引用 — 打破循环，不阻止 GC

```python
import weakref

class Cache:
    def __init__(self):
        # 普通 dict：强引用，对象不会被 GC
        # self._cache = {}
        
        # WeakValueDictionary：弱引用，对象没有其他引用时会被 GC
        self._cache = weakref.WeakValueDictionary()
    
    def get(self, key, factory):
        if key not in self._cache:
            obj = factory()
            self._cache[key] = obj
        return self._cache[key]

# 实践：监听器/回调注册，避免 observer 阻止 被观察对象 GC
class EventEmitter:
    def __init__(self):
        self._listeners = weakref.WeakSet()
    
    def add_listener(self, listener):
        self._listeners.add(listener)
    
    def emit(self, event):
        # 已 GC 的 listener 自动从 WeakSet 消失
        for listener in self._listeners:
            listener.on_event(event)
```

---

## 🔧 实用诊断工具

```python
# 查找内存泄漏
import tracemalloc

tracemalloc.start()

# ... 你的代码 ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:5]:
    print(stat)
# 输出：哪些行分配了最多内存

# 查找循环引用
import gc
gc.set_debug(gc.DEBUG_LEAK)
gc.collect()
# 有循环引用会打印到 stderr
```

---

## 📚 References
- [CPython Source — Objects/object.c](https://github.com/python/cpython/blob/main/Objects/object.c)
- [Python Memory Management — Real Python](https://realpython.com/python-memory-management/)
- [Python `gc` module docs](https://docs.python.org/3/library/gc.html)
- [Python `weakref` module docs](https://docs.python.org/3/library/weakref.html)

## 🧒 ELI5
Python 给每个对象贴一个小标签，记录有多少人"指着"它。没人指了就扔掉。但如果两个玩具互相拿着对方，计数永远不会到零——这时候 Python 会派一个"特别清洁队"（GC）去找这种互相拿着的东西，一起扔掉。`__slots__` 就像给每个玩具分配一个固定大小的抽屉，比每个玩具都有一个无限大的背包更省地方。
