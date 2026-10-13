🐍 **Python Craft** — Synthesis: Python 3.13 的 Free-Threaded (No-GIL) 模式深潜 / Deep Dive on Free-Threaded Python

> 📊 Python Craft: 50/50 ✅ — 综合深潜 / Synthesis dive
> 结合 Day 46 (GIL)、Day 54 (GIL Deep Dive)、Day 48-49 (asyncio)、Day 52 (concurrent.futures)

---

### 为什么现在要讲这个？

PEP 703 (Making the GIL Optional in CPython) 已经被接受。Python 3.13 开始提供**可选的 free-threaded build**（`python3.13t`），Python 3.14 正式支持。这是过去 30 年 Python 并发模型最大的一次变化。你用 Day 46 学的 `threading.Lock` 和 Day 48 的 `asyncio` 决策**正在重新洗牌**。

PEP 703 was accepted. CPython 3.13 ships an **experimental free-threaded build** (`python3.13t`); 3.14 makes it officially supported. Everything you learned about `threading` and `asyncio` tradeoffs needs re-grounding.

---

### 关键问题：三种并发在 free-threaded 下如何变？

| 场景 | GIL build (3.12 及之前) | Free-threaded build |
|---|---|---|
| **CPU-bound 多线程** | ❌ 串行 (GIL serializes) | ✅ **真并行** |
| **CPU-bound multiprocessing** | ✅ 并行，但 IPC 开销大 | ⚠️ 还有用，但 thread 更便宜 |
| **I/O-bound asyncio** | ✅ 单线程事件循环 | ✅ **不变** — 仍然是首选 |
| **I/O-bound threading** | ✅ 可以（GIL 在 I/O 时释放） | ✅ 也可以 |

**核心变化：** `threading` 第一次在 CPU-bound 任务上**真正并行**。但代价是——**单线程性能下降约 10-15%**（因为引用计数需要原子操作），且**第三方 C 扩展必须显式适配**（numpy, pandas 等逐步迁移中）。

---

### 一段代码看懂差异 / The one benchmark that shows the shift

```python
# save as cpu_bench.py
# Run twice:
#   python3.13   cpu_bench.py       (with GIL)
#   python3.13t  cpu_bench.py       (free-threaded; needs --disable-gil build)
import sys, time, threading

def crunch(n: int) -> int:
    # Pure Python CPU work: forces GIL contention
    total = 0
    for i in range(n):
        total += (i * i) % 97
    return total

N = 20_000_000
THREADS = 4

# --- Serial baseline ---
t0 = time.perf_counter()
for _ in range(THREADS):
    crunch(N)
serial = time.perf_counter() - t0

# --- Parallel via threading ---
t0 = time.perf_counter()
threads = [threading.Thread(target=crunch, args=(N,)) for _ in range(THREADS)]
for t in threads: t.start()
for t in threads: t.join()
parallel = time.perf_counter() - t0

gil_status = "disabled" if not sys._is_gil_enabled() else "enabled"
print(f"GIL {gil_status}: serial={serial:.2f}s  parallel={parallel:.2f}s  speedup={serial/parallel:.2f}x")
```

**典型观测值（4-core Mac，示意，具体数值因机器而异）：**
```
GIL enabled:  serial=5.8s  parallel=6.1s  speedup=0.95x   ← GIL 让并行比串行还慢
GIL disabled: serial=6.4s  parallel=1.9s  speedup=3.4x    ← 真·并行
```

注意 **GIL disabled 下 serial 更慢** — 这是单线程 10-15% 税。

---

### 新的决策矩阵 / Updated decision matrix

```
任务类型?
├── I/O-bound (网络, 磁盘, DB) → asyncio (仍然是最优)
│      需要调用阻塞库?       → asyncio + run_in_executor(ThreadPool)
│
├── CPU-bound
│   ├── 用了成熟 C 扩展 (numpy)   → 直接 threading (扩展早已释放 GIL)
│   ├── 纯 Python CPU 密集
│   │   ├── 3.13t available?       → threading ✅ (真并行)
│   │   └── 3.12 or stable build?  → multiprocessing / Pool
│   └── 极端大数据 / 跨机器      → Ray / Dask
│
└── 混合 (CPU + I/O)   → asyncio + ThreadPoolExecutor (free-threaded 下性能大涨)
```

---

### 要小心的坑 / Gotchas

1. **你的 Python 代码并不自动线程安全。** `dict`、`list` 的操作在 3.13t 下**不保证**不坏（PEP 703 承诺 atomic read/write 单个 slot，但 `d[k] += 1` 仍然是 race）。该用 `Lock` 还是要用。
2. **C 扩展必须声明 free-threaded 兼容** (`Py_MOD_GIL_NOT_USED`)。老 C 扩展在 3.13t 下会**自动开启 GIL fallback** — 你以为并行实际上还在串行。用 `sys._is_gil_enabled()` 检查。
3. **引用计数现在是原子操作**：hot path 上疯狂创建小对象的代码会变慢。考虑 `__slots__`、复用对象、避免闭包。
4. **性能剖析工具** (cProfile, py-spy) 对 3.13t 的支持仍在跟进；对比测试一定要同一 Python 版本。
5. **asyncio 不会消失。** I/O-bound 场景下 asyncio 的 overhead 比 threading 小一个数量级，free-threaded 不改变这一点。

---

### 迁移建议 / Migration checklist

- 保持 **asyncio 的代码不动**。
- 把 **multiprocessing 用于纯 Python CPU 并行** 的地方评估是否可以换成 threading（代码简化、省掉 pickle 开销）。
- `pip install --only-binary=:all: --prefer-binary` 检查你的依赖是否有 free-threaded wheels。
- CI 上并行跑 `python3.13` 和 `python3.13t` 两套测试，暴露竞态。
- 别着急在生产切 — 2026 年底才算稳定；先 staging / batch 任务试点。

---

### 📚 References

- PEP 703 — Making the GIL Optional in CPython: https://peps.python.org/pep-0703/
- Python 3.13 What's New — Free-threaded CPython: https://docs.python.org/3/whatsnew/3.13.html#free-threaded-cpython
- Py-Free-Threading HOWTO: https://py-free-threading.github.io/

### 🧒 ELI5

Python 以前像一条**单车道马路**：开再多车（线程）也只能一辆一辆过。Free-threaded 把它改成**多车道**。好消息：真的更快。坏消息：以前你靠"反正只有一辆车"的默认约定，现在必须装红绿灯（锁），否则会追尾。
