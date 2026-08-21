# 🎨 Day 116 — Python Craft Synthesis
> Expert Level | Deep Dive: Python Memory Model & Object Internals

---

# 🎨 Python Craft — 对象内存模型深度解析

## 你真的理解 Python 对象吗？

---

### 场景 / Scenario

你在做 code review，同事写了这段代码：

```python
# 同事的代码
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item(1))  # [1]
print(add_item(2))  # 你猜？
```

**猜猜输出什么？**

答案：`[1, 2]` — 默认参数是**对象**，函数定义时创建一次，复用！

---

### Python 对象内存模型 / The PyObject Model

每个 Python 对象本质上是 C 结构体 `PyObject`：

```c
// CPython internals (simplified)
typedef struct _object {
    Py_ssize_t ob_refcnt;   // 引用计数
    PyTypeObject *ob_type;  // 类型指针
} PyObject;
```

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))   # 引用计数（含临时引用）
print(id(x))                # 内存地址

# 小整数缓存 (-5 to 256)
a = 256; b = 256
print(a is b)   # True — same object!

a = 257; b = 257
print(a is b)   # False — different objects
```

---

### 可变 vs 不可变的内存影响 / Mutable vs Immutable

```python
# 不可变：每次"修改"都创建新对象
s = "hello"
print(id(s))
s += " world"
print(id(s))   # Different! New string object

# 可变：原地修改，id 不变
lst = [1, 2, 3]
print(id(lst))
lst.append(4)
print(id(lst))  # Same! Same object

# 陷阱：tuple 中含可变对象
t = ([1, 2], [3, 4])
t[0].append(99)  # Works! tuple is immutable, but its list element isn't
print(t)  # ([1, 2, 99], [3, 4])
```

---

### __slots__ — 内存优化利器 / Memory Optimization

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

a = WithDict(1, 2)
b = WithSlots(1, 2)

print(sys.getsizeof(a.__dict__))  # ~232 bytes (dict overhead)
print(sys.getsizeof(b))           # ~56 bytes (no __dict__)
# ~4x memory reduction with __slots__!
```

**何时用 `__slots__`：** 百万级实例、数据类、性能关键路径
**何时不用：** 需要动态属性、继承复杂时

---

### 深拷贝 vs 浅拷贝 vs 引用 / Copy Semantics

```python
import copy

original = [[1, 2], [3, 4]]

# 引用：完全共享
ref = original
ref[0].append(99)
print(original)  # [[1, 2, 99], [3, 4]] — mutated!

# 浅拷贝：顶层新建，内部共享
shallow = copy.copy(original)
shallow[0].append(88)
print(original)  # [[1, 2, 99, 88], [3, 4]] — inner list still shared!

# 深拷贝：完全独立
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0].append(77)
print(original)  # [[1, 2], [3, 4]] — unchanged ✅
```

---

### 📚 References

- [Python Memory Management — Real Python](https://realpython.com/python-memory-management/)
- [CPython Internals Book — Anthony Shaw](https://realpython.com/products/cpython-internals-book/)
- [__slots__ Magic — Python Docs](https://docs.python.org/3/reference/datamodel.html#slots)

### 🧒 ELI5

Python 里每个变量都是便利贴（引用），贴在真正的盒子（对象）上。不可变对象像冰块 — 要"修改"就造新冰块。可变对象像黏土 — 可以直接捏。`__slots__` 是给对象换个更小的收纳盒。
