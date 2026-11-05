# Day 148 — Python Craft Synthesis: CPython 对象模型深挖

> **综合深化 / Expert Synthesis** — Day 148

---

🐍 **Python Craft 综合 / Python Craft Synthesis**

## 主题：CPython 对象内存布局 — 你以为你懂 Python 对象，但你不一定真懂
### CPython Object Memory Layout: What's Actually in Memory

---

### 引子 / The Setup

```python
import sys
x = 1
print(sys.getsizeof(x))  # 28 bytes on 64-bit Python

# A C int is 4 bytes. Why does Python use 28 bytes for the number 1?
```

这不只是个趣味问题。理解这个，你就理解了 Python 的内存开销、GC 行为、和为什么某些优化有效。

---

### PyObject 结构 / The PyObject Struct

CPython 中每个 Python 对象在内存里都是一个 C struct：

```c
// Objects/object.h — simplified
typedef struct _object {
    Py_ssize_t ob_refcnt;   // 8 bytes — reference count for GC
    PyTypeObject *ob_type;  // 8 bytes — pointer to type object (e.g., <class 'int'>)
} PyObject;

// For integers (PyLongObject):
typedef struct {
    PyObject ob_base;       // 16 bytes header
    Py_ssize_t ob_size;     // 8 bytes — number of "digits" (for big ints)
    digit ob_digit[1];      // 4 bytes — actual value storage
    // + padding = 28 bytes total
} PyLongObject;
```

**可视化内存布局 / Memory Layout:**

```
Address  Content
──────────────────────────────────────────
0x1000   [refcnt: 8 bytes]   ← how many references point here
0x1008   [ob_type: 8 bytes]  ← pointer to int type object
0x1010   [ob_size: 8 bytes]  ← 1 (one 30-bit digit needed)
0x1018   [ob_digit: 4 bytes] ← actual value: 1
         [padding: 4 bytes]
──────────────────────────────────────────
Total: 28 bytes for the number 1
```

---

### 引用计数实战 / Reference Counting in Action

```python
import ctypes

def ref_count(obj):
    """Get reference count of an object."""
    return ctypes.c_long.from_address(id(obj)).value

x = [1, 2, 3]
print(ref_count(x))   # 1 (just x)

y = x
print(ref_count(x))   # 2 (x and y)

del y
print(ref_count(x))   # 1 (only x)

# When refcount hits 0, CPython immediately frees the memory
# (no waiting for GC cycle, unlike Java/Go)
```

---

### 小整数缓存 / Integer Interning

```python
# CPython pre-allocates integers from -5 to 256
a = 100
b = 100
print(a is b)  # True — same object in memory!

a = 1000
b = 1000
print(a is b)  # False — different objects

# Why -5 to 256? Historical accident + common use cases
# This is why you should use == not is for integer comparison
```

```python
# Visualize the cache
import sys
cached_ids = set()
for i in range(-5, 257):
    x = i
    y = i
    if id(x) == id(y):
        cached_ids.add(i)
        
print(f"Cached integers: {min(cached_ids)} to {max(cached_ids)}")
# Cached integers: -5 to 256
```

---

### 字符串驻留 / String Interning

```python
# CPython interns strings that look like identifiers
a = "hello"
b = "hello"
print(a is b)  # True (interned)

a = "hello world"  # has a space
b = "hello world"
print(a is b)  # False (not interned — depends on CPython version/context)

# Explicit interning
import sys
a = sys.intern("hello world")
b = sys.intern("hello world")
print(a is b)  # True — now same object
```

---

### 为什么这对你的代码有影响 / Why This Matters for Your Code

```python
# BAD: creating millions of Python int objects
def sum_squares_slow(n):
    result = 0
    for i in range(n):        # range() is lazy, OK
        result += i * i       # creates temp int objects constantly
    return result

# BETTER: use numpy — stores actual C integers, no PyObject overhead
import numpy as np
def sum_squares_fast(n):
    arr = np.arange(n, dtype=np.int64)  # 8 bytes/element, no refcount overhead
    return np.sum(arr * arr)

# Benchmark
import timeit
n = 1_000_000
slow = timeit.timeit(lambda: sum_squares_slow(n), number=10)
fast = timeit.timeit(lambda: sum_squares_fast(n), number=10)
print(f"Pure Python: {slow:.2f}s | NumPy: {fast:.2f}s")
# Pure Python: ~2.5s | NumPy: ~0.02s — 100x difference
```

---

### __slots__ — 砍掉 __dict__ 开销 / Eliminating __dict__ Overhead

```python
import sys

class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

d = WithDict(1, 2)
s = WithSlots(1, 2)

print(sys.getsizeof(d))              # ~56 bytes
print(sys.getsizeof(d.__dict__))     # ~296 bytes — the hidden cost!
print(sys.getsizeof(s))              # ~48 bytes — no __dict__, much smaller

# At 1M objects:
# WithDict:  ~336 MB
# WithSlots: ~46 MB — 7x smaller
```

---

### 深度总结 / Key Takeaways

1. **每个 Python 对象 = C struct header + 数据** — 开销远大于原始类型
2. **引用计数是主要 GC 机制** — 循环引用由 generational GC 处理
3. **小整数和某些字符串被缓存** — `is` 有时为 True 是实现细节，不要依赖
4. **性能关键路径:** 用 numpy/array/struct 代替 Python 对象列表
5. **内存关键路径:** 用 `__slots__` 消除 `__dict__` 开销

---

### 🧒 ELI5

Python 对象就像一张便利贴：正面写着"有几个人在用这张纸"（引用计数）和"这是什么类型"（类型指针），背面才是真正的数据（比如数字 1）。
所以存个数字 1，你需要一整张便利贴，而不只是写个"1"在纸上。这就是 Python 比 C 慢和占内存的根本原因。

---

### 📚 References
- https://realpython.com/python-memory-management/ — Python memory management deep dive
- https://docs.python.org/3/c-api/structures.html — CPython object structures (official)
- https://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/ — Why Python is slow (classic post)
- https://docs.python.org/3/reference/datamodel.html#slots — __slots__ documentation
