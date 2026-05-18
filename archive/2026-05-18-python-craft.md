# 🐍 Python Craft — threading：GIL、Thread、Lock

> 📅 Day 46 | ⏱️ 2 min read | 🔴 Mastery | Week 1: Concurrency & Parallelism

---

## 🎯 真实场景 / Real Scenario

你在构建一个爬虫，需要同时抓取 50 个 URL。单线程要 50 秒，你想并行跑完。但同事警告你："Python 有 GIL，多线程没用！"

这是真的吗？答案是：**取决于你的任务类型**。

*You're building a scraper to fetch 50 URLs concurrently. Single-threaded takes 50 seconds. Your colleague warns: "Python has the GIL, threads are useless!" Is that true? The answer: it depends on your workload type.*

---

## 🔑 核心概念 / Core Concepts

### GIL — 全局解释器锁 / Global Interpreter Lock

```
GIL 的本质：同一时刻，只有一个 Python 线程在执行 Python 字节码

┌─────────────────────────────────────────────────────────┐
│                Python Process                           │
│                                                         │
│  Thread 1 ──▶ [Running Python code]  ←── GIL held      │
│  Thread 2 ──▶ [Waiting for GIL]                        │
│  Thread 3 ──▶ [Waiting for GIL]                        │
│                                                         │
│  BUT: When Thread 1 does I/O → it RELEASES the GIL     │
│  Thread 2 or 3 can then acquire GIL and run!           │
└─────────────────────────────────────────────────────────┘
```

**结论 / The key insight:**
- **I/O-bound tasks** (网络请求、文件读写): `threading` ✅ 有效，线程等 I/O 时释放 GIL
- **CPU-bound tasks** (数值计算、图像处理): `threading` ❌ 无效，用 `multiprocessing` 或 NumPy/C 扩展

---

## 💻 代码示例 / Code Examples

### 基础多线程 / Basic Threading

```python
import threading
import time
import requests  # pip install requests

results = {}

def fetch_url(url: str, thread_id: int):
    """I/O-bound task — benefits from threading despite GIL."""
    # GIL is released during the actual network I/O
    response = requests.get(url, timeout=5)
    results[thread_id] = response.status_code
    print(f"Thread {thread_id}: {url} → {response.status_code}")

urls = [
    "https://httpbin.org/delay/1",  # Each takes ~1 second
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]

# Sequential: ~3 seconds
start = time.time()
for i, url in enumerate(urls):
    fetch_url(url, i)
print(f"Sequential: {time.time() - start:.1f}s")  # ~3.0s

# Threaded: ~1 second (I/O overlap)
threads = []
start = time.time()
for i, url in enumerate(urls):
    t = threading.Thread(target=fetch_url, args=(url, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()  # Wait for all threads to complete
print(f"Threaded: {time.time() - start:.1f}s")  # ~1.0s ✓
```

### Lock — 防止竞态条件 / Preventing Race Conditions

```python
import threading

# ❌ Race condition — without lock
counter = 0

def increment_unsafe():
    global counter
    for _ in range(100_000):
        counter += 1  # Read-modify-write: NOT atomic!

threads = [threading.Thread(target=increment_unsafe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Expected 500000, got: {counter}")  # ❌ Often < 500000

# ✅ Thread-safe — with Lock
counter = 0
lock = threading.Lock()

def increment_safe():
    global counter
    for _ in range(100_000):
        with lock:  # Context manager: acquires and releases automatically
            counter += 1  # Only one thread at a time

threads = [threading.Thread(target=increment_safe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Expected 500000, got: {counter}")  # ✅ Always 500000
```

---

## ⚡ 常见模式 / Common Patterns

```python
# Pattern: Thread with daemon=True (exits when main thread exits)
t = threading.Thread(target=background_task, daemon=True)
t.start()
# No need to join — dies with main process

# Pattern: threading.Event for signaling
stop_event = threading.Event()

def worker():
    while not stop_event.is_set():
        do_work()
        time.sleep(1)

t = threading.Thread(target=worker)
t.start()
time.sleep(5)
stop_event.set()  # Signal thread to stop
t.join()
```

---

## ❌ vs ✅ 决策框架 / When to Use What

| Task Type | Example | Use |
|-----------|---------|-----|
| Network I/O | Web scraping, API calls | `threading` or `asyncio` |
| File I/O | Reading many files | `threading` |
| CPU-intensive | Image processing, ML | `multiprocessing` |
| Many concurrent I/O | High-concurrency server | `asyncio` (next week) |

---

## 🧒 ELI5

GIL 就像一个会议室只有一把椅子。CPU 密集型工作（比如算数学题）需要一直坐着，所以轮流坐没意义。但 I/O 工作（比如等快递）的时候，你可以站起来出去，别人就可以坐进来——这样多线程就有用了！

*The GIL is like a meeting room with only one chair. CPU work (doing math) means you must always be seated — taking turns is pointless. But I/O work (waiting for delivery) means you leave the chair empty, so others can sit — that's when threading helps!*

---

## 📚 References

- [Python docs — threading module](https://docs.python.org/3/library/threading.html)
- [Real Python — An Intro to Threading in Python](https://realpython.com/intro-to-python-threading/)
- [Python GIL Explained — David Beazley](https://www.dabeaz.com/python/UnderstandingGIL.pdf)
