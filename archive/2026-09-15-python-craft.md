# Python Craft — Day 133
**日期 / Date:** 2026-09-15 | **阶段 / Phase:** Expert | **模式 / Mode:** Synthesis

---

## 🐍 Python Craft — 深入 Python 字节码与 `dis` 模块
### Bytecode Internals: What CPython Actually Executes

---

### 🌏 为什么这个值得深入？/ Why Go Deeper Here?

我们覆盖了 50 个 Python 工艺话题——从 GIL、asyncio 到设计模式。今天去一个极少数工程师真正理解的地方：**Python 字节码**。当你写 `x = a + b`，CPython 实际执行的是什么？

We've covered 50 Python Craft topics. Today: somewhere few engineers actually go — **Python bytecode**. When you write `x = a + b`, what does CPython *actually* run?

---

### 🔬 `dis` 模块实战 / dis Module in Action

```python
import dis

def add_numbers(a, b):
    x = a + b
    return x

dis.dis(add_numbers)
# Output:
#   2           0 RESUME                   0
#   3           2 LOAD_FAST                0 (a)
#               4 LOAD_FAST                1 (b)
#               6 BINARY_OP               0 (+)
#              10 STORE_FAST               2 (x)
#   4          12 LOAD_FAST                2 (x)
#              14 RETURN_VALUE
```

**字节码指令解析 / Bytecode breakdown:**
- `LOAD_FAST` — 从局部变量表加载（比 `LOAD_GLOBAL` 快 ~3x）
- `BINARY_OP` — 调用 `a.__add__(b)`，走类型调度
- `STORE_FAST` — 写回局部变量表
- `RETURN_VALUE` — 弹出栈顶返回

---

### ⚡ 为什么局部变量比全局变量快？/ Why Locals Beat Globals

```python
import timeit

x = 10  # global

def use_global():
    return x + 1      # LOAD_GLOBAL → dict lookup

def use_local():
    x = 10
    return x + 1      # LOAD_FAST → array index lookup

# Local is ~3x faster because:
# LOAD_GLOBAL → hash lookup in __dict__
# LOAD_FAST   → direct array[index] access in frame

print(timeit.timeit(use_global, number=10_000_000))  # ~0.8s
print(timeit.timeit(use_local,  number=10_000_000))  # ~0.3s
```

> 这就是为什么 CPython 高性能代码常见技巧：把频繁访问的全局函数先赋给局部变量
> `_append = list.append` — saves repeated LOAD_GLOBAL in tight loops

---

### 🏗️ 代码对象 / Code Objects

```python
def outer():
    x = 1
    def inner():
        return x
    return inner

fn = outer()
code = fn.__code__

print(code.co_varnames)    # ('x',) — local variable names
print(code.co_freevars)    # ('x',) — variables from closure
print(code.co_consts)      # constants embedded in bytecode
print(code.co_stacksize)   # max stack depth needed

# 每个函数都有自己的 code object
# Code objects are IMMUTABLE and SHARED across calls
# The frame (execution context) is created fresh per call
```

---

### 🔍 实战应用：Profile 热点前先看字节码 / Practical: Read Bytecode Before Profiling

```python
# 为什么这段代码慢？先 dis 看看
def slow_concat(items):
    result = ""
    for item in items:
        result = result + str(item)  # 每次 BINARY_OP + 创建新字符串对象
    return result

# dis 揭示每次循环都有 BINARY_OP (string concat = O(n²))

def fast_concat(items):
    parts = []
    for item in items:
        parts.append(str(item))  # LOAD_ATTR + CALL (amortized O(1))
    return "".join(parts)        # 一次性分配

# 或者更 Pythonic:
def fastest_concat(items):
    return "".join(str(i) for i in items)
```

---

### 🧠 CPython 执行模型速览 / CPython Execution Model

```
Python source (.py)
        ↓ compile()
Bytecode (.pyc) — code object with opcodes
        ↓ eval loop (ceval.c)
CPython interpreter — stack-based VM
        ↓
C-level operations (list.append, int.__add__, etc.)
```

- Python 是**栈式虚拟机** (stack-based VM)，不是寄存器 VM
- 每次函数调用创建一个新的 **PyFrameObject**（持有局部变量、字节码指针、栈）
- `sys._getframe()` 可以在运行时获取当前帧

---

### 🎯 面试加分项 / Interview Extra Credit

当面试官问"Python 为什么慢"，大多数人说"GIL"。但更深层的原因：
1. **动态类型 + BINARY_OP 要走类型调度**，每次 `a + b` 都要查 `type(a).__add__`
2. **栈式 VM overhead**，每个操作都是函数调用
3. **对象模型**，所有 int 都是堆分配的 PyObject（Rust/C 的 int 是栈上原始值）

这也是为什么 Cython、Numba、PyPy 能大幅提速的根本原因。

---

### 📚 References
- https://docs.python.org/3/library/dis.html — Official dis module docs
- https://realpython.com/cpython-source-code-guide/ — CPython source code guide
- https://leanpub.com/insidethepythonvirtualmachine — Inside the Python Virtual Machine

### 🧒 ELI5
你写的 Python 代码就像食谱（高层语言），CPython 先把食谱翻译成"烹饪步骤卡片"（字节码），再按顺序执行每张卡片。`dis` 模块让你能直接看到这些步骤卡片，帮你理解为什么有些写法比另一些慢。

Your Python code is a recipe. CPython translates it into step-by-step instruction cards (bytecode), then executes them one by one. The `dis` module lets you peek at those cards, explaining why some code is faster than others.
