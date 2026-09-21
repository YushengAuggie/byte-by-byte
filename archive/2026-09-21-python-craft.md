# 🐍 Python 工匠综合 / Python Craft Synthesis — Day 134

**Python 内存模型深潜：引用、id()、可变性的底层真相**
**Python Memory Model Deep Dive: The Truth About References, id(), and Mutability**

> 你用了多年 Python，但你真的理解 `a = b` 发生了什么吗？
> You've used Python for years, but do you *really* know what `a = b` does?

---

## 核心概念 / Core Concepts

Python 中**一切都是对象，变量都是引用**。

```python
# 变量不是"盒子"，而是"标签"
a = [1, 2, 3]
b = a          # b 指向同一个列表，不是复制！
b.append(4)
print(a)       # [1, 2, 3, 4]  ← a 也变了！

# 用 id() 验证
print(id(a) == id(b))  # True — 同一内存地址
```

---

## 小整数缓存 / Small Integer Cache

```python
# CPython 缓存 -5 到 256 的整数
a = 100; b = 100
print(a is b)   # True  (缓存命中，同一对象)

a = 1000; b = 1000
print(a is b)   # False (超出缓存范围，不同对象)
print(a == b)   # True  (值相等)

# 结论：用 == 比较值，用 is 只比较 None/True/False/单例
```

---

## 字符串驻留 / String Interning

```python
import sys

a = "hello"
b = "hello"
print(a is b)        # True  — CPython 驻留短字符串

a = "hello world"
b = "hello world"
print(a is b)        # True  — 编译时字面量驻留

a = "hello" + " world"   # 运行时拼接
b = "hello world"
print(a is b)        # 可能 False！

# 手动驻留
a = sys.intern("hello world")
b = sys.intern("hello world")
print(a is b)        # True — 强制驻留
```

---

## 可变 vs 不可变的内存影响 / Mutable vs Immutable

```python
# 不可变对象：修改 = 创建新对象
a = "hello"
print(id(a))
a += " world"     # 创建了新字符串！
print(id(a))      # 不同 id

# 可变对象：修改 = 原地修改
lst = [1, 2, 3]
print(id(lst))
lst.append(4)     # 原地修改
print(id(lst))    # 相同 id！

# 元组的"可变"陷阱
t = ([1, 2], [3, 4])
t[0].append(99)   # 合法！元组不可变指的是引用，不是内容
print(t)          # ([1, 2, 99], [3, 4])
```

---

## 浅拷贝 vs 深拷贝 / Shallow vs Deep Copy

```python
import copy

original = [[1, 2], [3, 4]]

# 浅拷贝：外层新建，内层共享
shallow = copy.copy(original)
shallow[0].append(99)
print(original)   # [[1, 2, 99], [3, 4]]  ← 被影响了！

# 深拷贝：完全独立
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0].append(99)
print(original)   # [[1, 2], [3, 4]]  ← 安全！

# 实际场景：默认参数陷阱
def append_to(item, lst=[]):   # 危险！
    lst.append(item)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2]  ← 共享同一列表！

def append_to_safe(item, lst=None):  # 正确！
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---

## 引用计数与垃圾回收 / Reference Counting & GC

```python
import sys
import gc

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + 传入 getrefcount 的临时引用)

b = a
print(sys.getrefcount(a))  # 3

del b
print(sys.getrefcount(a))  # 2

# 循环引用 → 引用计数无法回收 → 需要 cyclic GC
class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()
a.ref = b   # a → b
b.ref = a   # b → a (循环！)
del a, b    # 引用计数不会降到0，但 gc.collect() 可以回收
gc.collect()
```

---

## 实战规则 / Production Rules

```
赋值         → 只是绑定标签，不复制
==           → 值相等
is           → 同一对象（只用于 None/True/False）
copy.copy()  → 浅拷贝（嵌套结构要小心）
copy.deepcopy() → 深拷贝（安全但慢）
默认参数      → 永远用 None，不用可变对象
循环引用      → gc 模块可处理，但最好设计时避免
```

---

## 📚 References
- https://docs.python.org/3/reference/datamodel.html — Python Data Model
- https://realpython.com/pointers-in-python/ — Pointers in Python
- https://docs.python.org/3/library/copy.html — copy module
- https://devguide.python.org/internals/garbage-collector/ — CPython GC internals

## 🧒 ELI5
Python 的变量就像便利贴（标签），不是盒子。`a = b` 是把两张便利贴贴在同一个东西上，不是复印了一个新东西。所以改了 b 指向的内容，a 也看到变化了！

Python variables are sticky notes, not boxes. `a = b` puts two notes on the same object — not a copy. That's why changing `b`'s contents also shows up in `a`!
