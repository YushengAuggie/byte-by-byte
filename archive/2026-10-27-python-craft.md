# 🐍 Python Craft — Day 143 | Expert Synthesis: Python Memory Model Deep Dive

**Python 内存模型与对象生命周期 — 从引用计数到 GC**
**Python Memory Model & Object Lifecycle — From Refcount to GC**

---

## 真实场景 / Real Scenario

你在做一个长跑 Python 服务（Celery worker / FastAPI），上线几小时后内存稳步上涨。你打开 `top`，发现 RSS 只增不减。**内存泄漏，还是正常的？**

You deploy a long-running Python service. Hours later, memory steadily climbs. Is it a leak — or just Python being Python?

---

## Python 内存的三层模型 / Three-Layer Model

```
Layer 1: Python 对象层 (PyObject)
  └─ 每个对象有 ob_refcnt (引用计数)
  └─ refcnt = 0 → 立即释放

Layer 2: Python 内存分配器 (pymalloc)
  └─ 小对象 (≤512B) → pymalloc arena
  └─ 大对象 → malloc → OS

Layer 3: OS 层
  └─ Python 向 OS 申请内存 → 可能不归还
  └─ RSS 上涨不代表泄漏！
```

**关键洞察**：Python 释放了对象，但 pymalloc arena 不一定还给 OS。RSS 上升 ≠ 内存泄漏。

---

## 引用计数 + 循环 GC / Refcount + Cyclic GC

```python
import gc
import sys

# 引用计数示例
a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount 临时引用)

b = a
print(sys.getrefcount(a))  # 3

del b
print(sys.getrefcount(a))  # 2

# 循环引用 — refcount 永不归零
class Node:
    def __init__(self):
        self.next = None

n1 = Node()
n2 = Node()
n1.next = n2
n2.next = n1  # 循环引用！
del n1, n2    # refcount 仍 > 0，靠 GC 清理

# 手动触发 GC
gc.collect()  # 清理循环引用
print(gc.get_count())  # (gen0, gen1, gen2) 各代计数
```

---

## 内存泄漏的真实原因 / Real Causes of Memory Leaks

```python
# ❌ 常见泄漏 1: 全局缓存无上限
_cache = {}
def get_user(user_id):
    if user_id not in _cache:
        _cache[user_id] = fetch_from_db(user_id)  # 永远增长！
    return _cache[user_id]

# ✅ 修复: 使用 LRU Cache
from functools import lru_cache
@lru_cache(maxsize=1000)
def get_user(user_id):
    return fetch_from_db(user_id)

# ❌ 常见泄漏 2: 未关闭的资源
def bad():
    f = open("large_file.txt")
    data = f.read()
    # f 没关，但文件描述符泄漏
    return data

# ✅ 修复: context manager
def good():
    with open("large_file.txt") as f:
        return f.read()

# ❌ 常见泄漏 3: 线程局部变量
import threading
local = threading.local()
def handler():
    local.big_object = [0] * 10_000_000  # 每个线程都持有，不清理
```

---

## 诊断工具 / Diagnostic Tools

```python
# tracemalloc — 追踪内存分配来源
import tracemalloc

tracemalloc.start()
# ... 运行你的代码 ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:3]:
    print(stat)

# objgraph — 可视化对象引用
# pip install objgraph
import objgraph
objgraph.show_growth(limit=5)       # 增长最快的对象类型
objgraph.show_backrefs(some_obj)    # 谁引用了这个对象
```

---

## Senior 级别总结 / Senior Takeaways

| 现象 | 原因 | 解决 |
|------|------|------|
| RSS 缓慢增长 | pymalloc 持有 arena | 正常，用 `MALLOC_TRIM_THRESHOLD_` 调优 |
| RSS 持续增长 | 真正的对象泄漏 | tracemalloc + objgraph 定位 |
| CPU GC pause | 循环引用太多 | 减少循环引用，用 weakref |
| 多进程内存高 | 每个进程有独立堆 | 用 copy-on-write 友好的数据结构 |

---

## 📚 References
- [Python Docs: gc module](https://docs.python.org/3/library/gc.html)
- [Python Docs: tracemalloc](https://docs.python.org/3/library/tracemalloc.html)
- [Real Python: Memory Management in Python](https://realpython.com/python-memory-management/)

## 🧒 ELI5
Python 就像一个仓库工人，用完的箱子（对象）他会数有多少人还要用。没人要了就扔掉。但有时候两个箱子互相说"我要等你"，死锁了 — GC 是专门来解决这种死锁的清洁工。
