# 🐍 Python Craft — concurrent.futures: ThreadPool vs ProcessPool
*Day 52 · Expert Phase · Week 2 Concurrency · ~2 min read*

---

## 场景 / Scenario

你需要并发处理 100 个任务 — 可能是爬取 100 个网页，或者并行处理 100 个图片。Python 给了你两个工具：`ThreadPoolExecutor` 和 `ProcessPoolExecutor`。选错了，要么没效果，要么程序崩溃。

*You need to run 100 tasks concurrently — maybe scraping 100 URLs, or processing 100 images. Python offers two tools: `ThreadPoolExecutor` and `ProcessPoolExecutor`. Pick wrong and you either get no speedup or a crash.*

---

## 核心区别 / Core Difference

```
ThreadPoolExecutor          ProcessPoolExecutor
───────────────────         ──────────────────────
同一个进程，多个线程          多个进程，各自独立
受 GIL 限制                  绕过 GIL
适合 I/O 密集型               适合 CPU 密集型
内存共享（注意竞争）           内存隔离（需序列化传输）
启动快                        启动慢（fork overhead）
```

---

## 代码对比 / Code Comparison

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
import requests

# ─── I/O Bound: Use ThreadPoolExecutor ───
# Fetching URLs — most time is waiting for network
def fetch_url(url: str) -> str:
    response = requests.get(url, timeout=5)
    return f"{url}: {response.status_code}"

urls = ["https://httpbin.org/delay/1"] * 10

# Sequential: ~10s
# Threaded: ~1s (all wait in parallel)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_url, url) for url in urls]
    for future in as_completed(futures):
        print(future.result())

# ─── CPU Bound: Use ProcessPoolExecutor ───
# Number crunching — GIL blocks threads from real parallelism
def compute_heavy(n: int) -> int:
    # Simulate CPU work: count primes up to n
    return sum(1 for i in range(2, n) if all(i % j != 0 for j in range(2, i)))

numbers = [50000] * 8

# Threads: no speedup (GIL)
# Processes: near-linear speedup with CPU cores
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute_heavy, numbers))
    print(f"Results: {results}")

# ─── map() vs submit() ───
# map(): simpler, blocks until all done, results in order
results = list(executor.map(compute_heavy, numbers))

# submit(): more control, get results as they complete
futures = {executor.submit(compute_heavy, n): n for n in numbers}
for future in as_completed(futures):
    n = futures[future]
    print(f"compute_heavy({n}) = {future.result()}")
```

---

## 实际决策框架 / Decision Framework

```
任务类型判断:
├── 等网络/文件/数据库响应? → ThreadPoolExecutor
│   ├── max_workers: 10-50 (I/O 等待时间越长，可以更多)
│   └── 例: requests, boto3, sqlalchemy queries
│
└── 计算密集型 (数学/图像处理/解析)? → ProcessPoolExecutor
    ├── max_workers: os.cpu_count() 或更少
    ├── 注意: 传入参数必须可 pickle（不能是 lambda、本地函数）
    └── 例: PIL image processing, numpy heavy math, parsing
```

**常见陷阱：**

❌ 对 CPU 密集任务用 ThreadPoolExecutor → GIL 导致完全没有加速
❌ ProcessPoolExecutor 传入不可序列化对象 → `PicklingError`
❌ 忘记处理 `future.exception()` → 静默失败

```python
# ✅ Always handle exceptions
for future in as_completed(futures):
    try:
        result = future.result()
    except Exception as e:
        print(f"Task failed: {e}")
```

---

## 与前几天的关联 / Connection to Previous Days

| Day | 主题 | 关系 |
|-----|------|------|
| Day 50 | threading — GIL, Lock | concurrent.futures 的 Thread 底层是 threading |
| Day 51 | multiprocessing | concurrent.futures Process 底层是 multiprocessing |
| Day 52 (今天) | concurrent.futures | 高层抽象，两者统一接口 |
| 下一步 | asyncio | 单线程并发，另一条路 |

---

## 📚 参考资料 / References

- [Python docs — concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [Real Python — ThreadPoolExecutor tutorial](https://realpython.com/python-concurrency/)
- [Python GIL explained — David Beazley](https://dabeaz.com/python/GIL.pdf)

---

## 🧒 ELI5

ThreadPool 像一个餐厅服务员团队：多个服务员同时服务多桌，大部分时间都在等客人点单（I/O等待），所以多人有用。ProcessPool 像开了多个独立的餐厅分店：每家店完全独立运营，适合每家店都需要大量准备工作（CPU计算）的情况。

*ThreadPool is like a restaurant with multiple waiters: they serve multiple tables at once, spending most time waiting for customers (I/O). ProcessPool is like opening multiple independent restaurant locations: each runs completely independently, good when each needs heavy prep work (CPU computation).*
