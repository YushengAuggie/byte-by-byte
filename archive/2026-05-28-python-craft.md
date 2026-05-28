# 🐍 Python Craft — Day 7
## Producer-Consumer with queue.Queue
**类别 / Category:** Concurrency & Parallelism — Week 2 | **阶段 / Phase:** Expert | **用时 / Time:** ~2 min

---

## 真实场景 / Real-World Scenario

你在构建一个**日志处理 pipeline**：
- 多个线程持续产生日志事件 (producers)
- 几个线程负责批量写入数据库 (consumers)

两者速度不匹配 — 生产者偶尔会爆发，消费者来不及处理。
`queue.Queue` 是这类问题的标准解：**线程安全的有界缓冲区**。

You're building a **log processing pipeline**:
- Multiple threads constantly produce log events (producers)
- A few threads batch-write them to the database (consumers)

They run at different speeds — producers sometimes burst, consumers can't keep up.
`queue.Queue` is the standard solution: **a thread-safe bounded buffer**.

---

## 核心 API / Core API

```python
import queue

q = queue.Queue(maxsize=100)  # bounded: blocks when full

# Producer side
q.put(item)           # block if full
q.put(item, block=False)  # raise queue.Full immediately
q.put_nowait(item)    # alias for put(block=False)

# Consumer side
item = q.get()        # block if empty
item = q.get(timeout=5)  # block up to 5s, then raise queue.Empty
q.task_done()         # signal this item is processed

# Coordination
q.join()              # block until all items have task_done() called
q.qsize()             # approximate size (not reliable for flow control!)
```

---

## 完整示例 / Full Example

```python
import queue
import threading
import time
import random

def producer(q: queue.Queue, name: str, count: int):
    for i in range(count):
        item = f"{name}-event-{i}"
        q.put(item)  # blocks if queue is full (backpressure!)
        print(f"[PRODUCE] {item}")
        time.sleep(random.uniform(0.01, 0.05))
    print(f"[PRODUCE] {name} done")


def consumer(q: queue.Queue, name: str):
    while True:
        try:
            item = q.get(timeout=2)  # wait up to 2s for new items
        except queue.Empty:
            print(f"[CONSUME] {name}: queue empty, exiting")
            break
        
        # Simulate processing
        time.sleep(random.uniform(0.05, 0.1))
        print(f"[CONSUME] {name} processed: {item}")
        q.task_done()  # IMPORTANT: signal completion


def main():
    q = queue.Queue(maxsize=20)  # bounded buffer — backpressure!
    
    # Start 3 producers
    producers = [
        threading.Thread(target=producer, args=(q, f"P{i}", 10))
        for i in range(3)
    ]
    
    # Start 2 consumers
    consumers = [
        threading.Thread(target=consumer, args=(q, f"C{i}"))
        for i in range(2)
    ]
    
    for t in producers + consumers:
        t.start()
    
    # Wait for all producers to finish
    for t in producers:
        t.join()
    
    # Wait for queue to drain
    q.join()
    print("All items processed!")
    
    for t in consumers:
        t.join()


if __name__ == "__main__":
    main()
```

---

## 关键机制 / Key Mechanisms

### 1. 背压 / Backpressure
`Queue(maxsize=20)` + `q.put(item)` 实现自动背压：
- 队列满 → producer 自动阻塞，不会把内存打爆
- 这比无限队列 `Queue()` 安全得多

`Queue(maxsize=20)` + `q.put(item)` = automatic backpressure:
- Queue full → producer automatically blocks, memory won't explode
- Much safer than unbounded `Queue()`

### 2. task_done + join 的配合 / task_done + join Pattern
```
生产者放入: unfinished_tasks += 1
消费者 task_done(): unfinished_tasks -= 1
q.join(): 阻塞直到 unfinished_tasks == 0
```
如果忘记调用 `task_done()`，`q.join()` 会永远卡住。

If you forget `task_done()`, `q.join()` hangs forever.

### 3. 毒丸模式 / Poison Pill Pattern (优雅退出)
比用 timeout 更优雅的消费者退出方式：

```python
SENTINEL = None  # poison pill

# Producer: after finishing, send one sentinel per consumer
for _ in range(num_consumers):
    q.put(SENTINEL)

# Consumer:
item = q.get()
if item is SENTINEL:
    q.task_done()
    break  # clean exit
```

---

## Queue 的变体 / Queue Variants

| 类型 | 行为 | 用途 |
|---|---|---|
| `Queue()` | FIFO | 标准 producer-consumer |
| `LifoQueue()` | LIFO (stack) | DFS、撤销历史 |
| `PriorityQueue()` | 最小堆 | 任务优先级调度 |
| `SimpleQueue()` | 无界 FIFO，无 task_done | 只需要简单传递 |

---

## ⚠️ 常见坑 / Common Gotchas

**坑 1:** 忘记 `task_done()` → `q.join()` 卡死
**坑 2:** 用 `q.qsize()` 做流量控制 → 不精确，有竞态
**坑 3:** consumer 数量太少 → 队列持续满，producers 全堵住
**坑 4:** 不设 timeout → consumer 线程永远不退出

---

## 📚 References
- [queue — Synchronized queue class (Python docs)](https://docs.python.org/3/library/queue.html)
- [Producer-Consumer Problem — Python threading patterns](https://realpython.com/intro-to-python-threading/#producer-consumer-threading)
- [Python Concurrency — queue.Queue vs asyncio.Queue](https://superfastpython.com/queue-in-python/)

## 🧒 ELI5
生产者-消费者就像一个传菜口：厨师（生产者）做好菜放进去，服务员（消费者）从另一头取走。`queue.Queue` 是那个传菜口——大小有限（防止堆满），线程安全（多个厨师/服务员同时用不会乱）。

Producer-consumer is like a restaurant pass-through window: chefs (producers) put plates in, servers (consumers) take them out. `queue.Queue` is that window — bounded (prevents overflow), thread-safe (multiple chefs/servers can use it simultaneously without chaos).
