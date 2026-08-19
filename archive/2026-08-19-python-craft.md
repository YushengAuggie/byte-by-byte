# Python Craft 综合 — CPython 字节码深度解析
# Python Craft Synthesis — CPython Bytecode Deep Dive

> Day 114 · Synthesis Mode · Expert Phase

---

## 🐍 Python Craft

**你写的 Python 到底变成了什么？CPython 字节码实战**
**What Does Your Python Actually Become? CPython Bytecode in Action**

---

### 🎯 为什么要懂字节码？/ Why Care About Bytecode?

你优化了算法，换了数据结构，但函数还是慢。真正的瓶颈往往藏在 CPython 的执行层：字节码指令数、LOAD/STORE 开销、循环展开。懂字节码，才能做最后一公里优化。

You've optimized the algorithm, changed data structures, but the function is still slow. Real bottlenecks often hide in CPython's execution layer: bytecode instruction count, LOAD/STORE overhead, loop unwinding. Understanding bytecode unlocks last-mile optimization.

---

### 🔬 反汇编实战 / Disassembly in Action

```python
import dis

# Example 1: 简单函数 / Simple function
def add(a, b):
    return a + b

dis.dis(add)
# Output:
#   2           0 RESUME          0
#   3           2 LOAD_FAST       0 (a)
#               4 LOAD_FAST       1 (b)
#               6 BINARY_OP      0 (+)
#              10 RETURN_VALUE

# Example 2: 列表推导 vs 循环 / List comprehension vs loop
def loop_append(n):
    result = []
    for i in range(n):
        result.append(i * 2)
    return result

def list_comp(n):
    return [i * 2 for i in range(n)]

# List comprehension generates a dedicated LIST_APPEND opcode
# and avoids repeated LOAD_ATTR for "append" — that's why it's faster!

# Example 3: 揭秘 global 为何比 local 慢
x = 10  # global

def use_global():
    return x      # LOAD_GLOBAL (slower: dict lookup)

def use_local():
    x = 10
    return x      # LOAD_FAST (faster: array index)

# LOAD_FAST: index into frame's local array — O(1)
# LOAD_GLOBAL: dict lookup in globals() — O(1) but higher constant

import timeit
print(timeit.timeit(use_global, number=10_000_000))  # ~0.6s
print(timeit.timeit(use_local,  number=10_000_000))  # ~0.4s

# 🚀 Optimization trick: cache globals as locals in hot loops
def fast_math(data):
    _sqrt = __import__('math').sqrt  # local binding = LOAD_FAST
    return [_sqrt(x) for x in data]
```

---

### 🧠 关键字节码指令速查 / Key Opcodes Reference

```
LOAD_FAST    → local variable (fastest)
LOAD_DEREF   → closure variable (medium)  
LOAD_GLOBAL  → global/builtin (slower)
LOAD_ATTR    → object attribute (slowest: __getattribute__)

CALL_FUNCTION     → positional args only
CALL_FUNCTION_KW  → with keyword args (extra overhead!)
BUILD_LIST        → literal []  
LIST_APPEND       → inside list comprehension (optimized)
GET_ITER / FOR_ITER → for loop machinery
```

---

### 📊 性能洞察 / Performance Insights

```python
# Why "x in set" is faster than "x in list"
# set:  LOAD_FAST + CONTAINS_OP (hash lookup O(1))
# list: LOAD_FAST + CONTAINS_OP (linear scan O(n))

# Why f-strings beat % formatting and .format()
# f-string: FORMAT_VALUE + BUILD_STRING (single pass)
# %:        binary operation + string parsing
# .format(): CALL_FUNCTION overhead

# Checking bytecode count as a proxy for speed:
import dis
f1 = lambda x: f"hello {x}"
f2 = lambda x: "hello %s" % x
print(len(list(dis.get_instructions(f1))))  # fewer instructions
print(len(list(dis.get_instructions(f2))))  # more instructions
```

---

### 🔗 综合联系 / Synthesis Connections

| 已学概念 | 字节码联系 |
|---------|-----------|
| GIL (Day 46) | GIL 在字节码执行边界释放 (每 sys.getswitchinterval() 次) |
| asyncio (Day 48) | SEND opcode + coroutine frame suspension |
| generators (Day 98) | YIELD_VALUE + frame state saved on heap |
| lru_cache (Day 101) | 绕过 Python 字节码，C 级别缓存 |

---

### 📚 References
- https://docs.python.org/3/library/dis.html
- https://devguide.python.org/internals/compiler/
- https://realpython.com/cpython-source-code-guide/
- https://github.com/python/cpython/blob/main/Python/ceval.c

### 🧒 ELI5
你写的 Python 代码就像乐谱。CPython 是乐手，会先把乐谱翻译成简单的"字节码音符"，然后一个个演奏。懂了这些音符，你就知道哪些写法让乐手演奏得更顺畅。
Your Python is like sheet music. CPython translates it into simple "bytecode notes" then plays them one by one. Understanding these notes tells you which code makes the musician play faster.
