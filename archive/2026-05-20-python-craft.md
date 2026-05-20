# 🐍 Python Craft — Day 2

**主题 / Topic:** multiprocessing — Pool, Process, Shared Memory
**类别 / Category:** 并发与并行 / Concurrency & Parallelism
**阶段 / Phase:** Mastery

---

## 为什么你需要 multiprocessing？/ Why Do You Need multiprocessing?

上一节我们学了 `threading`，它有一个大问题：**GIL（全局解释器锁）**。
Python 的 GIL 确保同一时刻只有一个线程执行 Python 字节码，这意味着多线程**无法真正并行执行 CPU 密集型任务**。

**解决方案：multiprocessing** — 每个进程有独立的 Python 解释器和内存空间，绕过 GIL，实现真正的 CPU 并行。

Last session: `threading` has a big problem — the **GIL** (Global Interpreter Lock). Python ensures only one thread executes Python bytecode at a time, meaning threads *cannot truly parallelize CPU-bound work*. **Solution: multiprocessing** — each process has its own interpreter and memory, bypassing the GIL for real CPU parallelism.

```
threading: Thread1 ─┐
                    ├── GIL ──► Only 1 runs at a time (I/O-bound OK)
           Thread2 ─┘

multiprocessing: Process1 ──► CPU Core 1 ┐
                 Process2 ──► CPU Core 2 ├── True parallelism
                 Process3 ──► CPU Core 3 ┘
```

---

## 真实场景 / Real Scenario

你有 1000 张图片需要调整大小，每张需要 200ms CPU 时间。单线程需要 200 秒。用 4 核 multiprocessing Pool，约 50 秒。

1000 images to resize, 200ms CPU each. Single-threaded: 200 seconds. 4-core Pool: ~50 seconds.

---

## Process — 最基本的方式 / Basic: Process

```python
from multiprocessing import Process
import os

def worker(task_id):
    print(f"Task {task_id} running in PID {os.getpid()}")
    # CPU-intensive work here
    result = sum(i * i for i in range(10_000_000))
    print(f"Task {task_id} done: {result}")

if __name__ == "__main__":  # REQUIRED on Windows/macOS!
    processes = []
    for i in range(4):
        p = Process(target=worker, args=(i,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()  # wait for all to finish
    
    print("All done!")
```

⚠️ **`if __name__ == "__main__":`** 在 macOS/Windows 上是必须的，否则 spawn 新进程时会无限递归。

---

## Pool — 推荐方式 / Recommended: Pool

Pool 管理一个工作进程池，自动分配任务。

```python
from multiprocessing import Pool
import time

def cpu_bound_task(n):
    """Simulate CPU-intensive work"""
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    numbers = [1_000_000, 2_000_000, 3_000_000, 4_000_000]
    
    # map: blocking, returns results in order
    with Pool(processes=4) as pool:
        results = pool.map(cpu_bound_task, numbers)
    print(f"map results: {results}")
    
    # imap: lazy iterator, memory-efficient for large inputs
    with Pool(processes=4) as pool:
        for result in pool.imap(cpu_bound_task, numbers):
            print(f"Got: {result}")
    
    # map_async: non-blocking
    with Pool(processes=4) as pool:
        async_result = pool.map_async(cpu_bound_task, numbers)
        # do other work...
        results = async_result.get(timeout=30)
```

**Pool API 速查 / Quick Reference:**
| 方法 | 特点 |
|------|------|
| `pool.map(f, iterable)` | 阻塞，结果有序 |
| `pool.imap(f, iterable)` | 懒惰迭代，省内存 |
| `pool.starmap(f, [(a,b), ...])` | 多参数版 map |
| `pool.map_async(f, iterable)` | 非阻塞，返回 AsyncResult |
| `pool.apply(f, args)` | 单任务，阻塞 |

---

## Shared Memory — 进程间共享数据 / Shared Memory

进程间不共享内存！需要显式共享。

```python
from multiprocessing import Process, Value, Array, Manager
import ctypes

def increment(counter, lock_needed=False):
    for _ in range(100):
        counter.value += 1  # NOT thread-safe without lock!

def safe_increment(counter, lock):
    for _ in range(100):
        with lock:
            counter.value += 1

if __name__ == "__main__":
    # Value: single shared value
    counter = Value(ctypes.c_int, 0)  # c_int type, initial value 0
    
    # Array: shared array
    shared_arr = Array(ctypes.c_double, [1.0, 2.0, 3.0])
    
    # Manager: more flexible but slower (uses socket communication)
    with Manager() as manager:
        shared_dict = manager.dict()
        shared_list = manager.list()
        
        def worker(d, l, key):
            d[key] = key * 2
            l.append(key)
        
        procs = [Process(target=worker, args=(shared_dict, shared_list, i)) for i in range(5)]
        for p in procs: p.start()
        for p in procs: p.join()
        print(dict(shared_dict))  # {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}
```

---

## threading vs multiprocessing 选择指南 / When to Use What

```
任务类型                    推荐
──────────────────────────────────────────────
I/O 密集（网络请求、文件）  → threading 或 asyncio
CPU 密集（计算、图像处理）  → multiprocessing
混合任务                    → ProcessPool + ThreadPool
简单并发                    → concurrent.futures (统一 API)
```

```python
# concurrent.futures — 统一接口，推荐！/ Unified interface, recommended!
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def task(n): return n * n

# CPU-bound: ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task, i) for i in range(10)]
    results = [f.result() for f in futures]

# I/O-bound: ThreadPoolExecutor  
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(task, range(10)))
```

---

## 常见陷阱 / Common Pitfalls

❌ **忘记 `if __name__ == "__main__":`** — 进程 spawn 时会 import 主模块，导致无限循环创建进程。

❌ **共享大量数据** — 进程间通信（pickle 序列化）有开销。数据量大时用 `shared_memory`（Python 3.8+）或 `numpy` + `mmap`。

❌ **在 lambda 或局部函数上用 Pool** — Pool 用 pickle 序列化函数，lambda 不可序列化。

```python
# ❌ Wrong
pool.map(lambda x: x*2, [1,2,3])  # PicklingError!

# ✅ Correct
def double(x): return x * 2
pool.map(double, [1,2,3])
```

---

## 📚 参考资料 / References

1. [Python multiprocessing 官方文档](https://docs.python.org/3/library/multiprocessing.html)
2. [Python Concurrency: threading vs multiprocessing vs asyncio — Real Python](https://realpython.com/python-concurrency/)
3. [concurrent.futures — Higher-level interface](https://docs.python.org/3/library/concurrent.futures.html)

---

## 🧒 ELI5

想象你要解 1000 道数学题。
- **单线程**：你一道一道解，200 分钟。
- **threading**：你和朋友们在同一张桌子用同一支笔轮流写（GIL），一样慢。
- **multiprocessing**：你的 4 个朋友各自拿一张独立的桌子和笔，同时解，50 分钟！

Imagine solving 1000 math problems. Single-threaded: you do them one by one, 200 min. Threading: you and friends share one pen at one table (GIL) — still slow. Multiprocessing: 4 friends each have their own table and pen, working truly in parallel — 50 min!
