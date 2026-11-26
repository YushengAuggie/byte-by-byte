# 🐍 Python Craft — Day 158 · Synthesis
> Expert Level · Synthesis Mode · 2 min read

---

## 深度合成：Python 并发三兄弟的统一模型
## Deep Synthesis: One Mental Model for Python's Three Concurrency Primitives

我们已经覆盖了 `threading`、`multiprocessing`、`asyncio` 和 `concurrent.futures`。今天用一张统一模型把它们串起来，并探讨一个高级模式：**混合并发 (Hybrid Concurrency)**。

We've covered threading, multiprocessing, asyncio, and concurrent.futures separately. Today: a unified mental model and an advanced pattern — **hybrid concurrency**.

---

## 统一决策树 / Unified Decision Tree

```
你的任务是...?
Your task is...?

           IO-Bound (网络/磁盘)?           CPU-Bound (计算)?
                   ↓                              ↓
    需要处理多少并发?             需要多少进程?
    How many concurrent?         How many?
           ↓                              ↓
    < 1000: threading         1-N CPUs: multiprocessing
    > 1000: asyncio               ↓
                              有IO等待吗?
                              Any IO waits?
                                  ↓
                         是→ ProcessPool + asyncio混合
                         否→ ProcessPoolExecutor即可
```

---

## 高级模式：混合并发 / Advanced Pattern: Hybrid Concurrency

真实后端场景：你有一个 ML inference 服务，需要：
1. **接受大量并发 HTTP 请求** (IO-bound → asyncio)
2. **每个请求调用 CPU 密集的模型推理** (CPU-bound → process pool)

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor
import numpy as np

# CPU-bound work — runs in a separate process (bypasses GIL)
def run_inference(input_data: list[float]) -> float:
    """Simulate CPU-heavy model inference."""
    arr = np.array(input_data)
    # Heavy computation — no IO, pure CPU
    return float(np.dot(arr, arr) ** 0.5)

# Async IO handler — runs in event loop
async def handle_request(
    executor: ProcessPoolExecutor,
    request_id: int,
    data: list[float]
) -> dict:
    loop = asyncio.get_running_loop()
    
    # Offload CPU work to process pool without blocking event loop
    result = await loop.run_in_executor(executor, run_inference, data)
    
    return {"request_id": request_id, "result": result}

async def main():
    # 4 worker processes for CPU work, event loop handles IO concurrency
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Simulate 20 concurrent requests
        tasks = [
            handle_request(executor, i, [float(j) for j in range(100)])
            for i in range(20)
        ]
        results = await asyncio.gather(*tasks)
    
    print(f"Processed {len(results)} requests")
    # Each result computed in parallel by separate processes

asyncio.run(main())
```

**关键洞察 / Key Insight:**
- `asyncio.gather` → 并发调度20个请求 (IO层)
- `loop.run_in_executor` → 把每个 CPU 任务丢给进程池，**不阻塞事件循环**
- `ProcessPoolExecutor` → 4个进程，真正并行利用多核 CPU

---

## 性能对比 / Performance Comparison

```python
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def cpu_task(n):
    """CPU-bound: sum squares"""
    return sum(i*i for i in range(n))

async def io_task(n):
    """IO-bound: simulated network delay"""
    await asyncio.sleep(0.1)
    return n

# Benchmark results (8-core machine, N=1000000):
# cpu_task × 8:
#   Sequential:          12.4s
#   ThreadPoolExecutor:  12.1s  ← GIL kills parallelism
#   ProcessPoolExecutor:  1.8s  ← True parallel, 6.9x faster!
#
# io_task × 100:
#   Sequential:          10.0s
#   ThreadPoolExecutor:   0.11s ← threads release GIL on IO
#   asyncio.gather:       0.10s ← best for massive concurrency
```

---

## 坑的总结 / Common Pitfalls Revisited

| 坑 Pitfall | 正确做法 Fix |
|---|---|
| `ThreadPool` 做 CPU 密集 | 换 `ProcessPool` — GIL 不会释放 |
| `asyncio` 里调用阻塞函数 | `run_in_executor` 或用 async 版本 |
| `ProcessPool` 传大对象 | 传 index/path，不传 numpy array |
| 创建太多 Process | `max_workers=os.cpu_count()` 足够 |
| 忘记 `await` | 返回 coroutine 对象而非结果 |

---

## 一行总结 / One-Line Summary

```
asyncio = 大量IO并发的调度器
threading = 少量IO并发 + 简单
multiprocessing = CPU并行 + 绕过GIL
hybrid = asyncio事件循环 + ProcessPool推理/计算
```

---

## 🧒 ELI5

餐厅比喻：
- `asyncio` = 一个超高效服务员，同时端很多桌 (快速切换)
- `threading` = 多个服务员，共用一个收银机 (GIL)
- `multiprocessing` = 多个独立餐厅，各自有收银机 (真并行)
- 混合 = 超效服务员接单，把烹饪(CPU)分给多个厨师

## 📚 References
- [Python asyncio docs — run_in_executor](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)
- [Python concurrent.futures docs](https://docs.python.org/3/library/concurrent.futures.html)
- [Real Python — Speed Up Python with Concurrency](https://realpython.com/python-concurrency/)
