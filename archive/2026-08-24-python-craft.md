# 🐍 Day 118 — Python Craft Synthesis
> 🔥 Expert Level | Synthesis: Python 性能调优全景

---

🐍 **Python 工程 / Python Craft**
**性能调优决策树 — 从「慢」到「快」的系统化方法**
**Performance Tuning Decision Tree — From Slow to Fast, Systematically**

---

## 🎯 核心原则 / Core Principle

> "过早优化是万恶之源，但完全不优化是另一种罪。"  
> "Premature optimization is the root of all evil—but zero optimization is a different sin."

系统化调优的步骤：**测量 → 定位 → 优化 → 验证**（循环）  
The loop: **Measure → Locate → Optimize → Verify** (repeat)

---

## 🔍 第一步：测量，不猜测 / Step 1: Measure, Don't Guess

```python
# 1. cProfile — 函数级 CPU 热点
import cProfile
cProfile.run('your_function()', sort='cumulative')

# 2. line_profiler — 行级细粒度
# pip install line-profiler
# @profile 装饰器 + kernprof -l -v script.py

# 3. memory_profiler — 内存泄漏
# pip install memory-profiler
# @profile 装饰器 + python -m memory_profiler script.py

# 4. timeit — 快速微基准
import timeit
timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)

# 5. tracemalloc — 内存分配追踪（内置！）
import tracemalloc
tracemalloc.start()
# ... your code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:5]:
    print(stat)
```

---

## 🗺️ 决策树 / Decision Tree

```
发现慢 / It's slow
│
├── CPU 密集？(profile 显示计算时间高)
│   ├── 纯 Python 循环 → 用 NumPy 向量化 / Cython / 换算法
│   ├── 可并行？→ multiprocessing.Pool (绕过 GIL)
│   └── 需要极致 → Rust 扩展 (PyO3)
│
├── IO 密集？(等网络/文件/DB)
│   ├── 单线程阻塞 → asyncio + aiohttp/aiomysql
│   ├── 多个 IO 任务 → asyncio.gather() 并发
│   └── 线程已够用 → ThreadPoolExecutor (IO 不受 GIL 限制)
│
├── 内存太高？
│   ├── 大列表 → 改用 generator (yield)
│   ├── 重复对象 → __slots__ 减少 per-object overhead
│   └── 大 DataFrame → 分块读取 (pd.read_csv chunksize=)
│
└── DB/缓存层慢？
    ├── N+1 查询 → eager loading / JOIN
    ├── 缺索引 → EXPLAIN ANALYZE
    └── 热数据 → Redis 缓存层
```

---

## 💡 Python 专属优化技巧 / Python-Specific Tricks

```python
# ❌ 慢：字符串拼接 (O(n²))
result = ""
for s in strings:
    result += s

# ✅ 快：join (O(n))
result = "".join(strings)

# ❌ 慢：列表 membership test (O(n))
if item in large_list:

# ✅ 快：set lookup (O(1))
large_set = set(large_list)
if item in large_set:

# ❌ 慢：重复 dict.get / 捕异常
try:
    value = d[key]
except KeyError:
    value = default

# ✅ 快：dict.get
value = d.get(key, default)

# ✅ __slots__ — 减少 30-50% 内存（大量实例时）
class Point:
    __slots__ = ('x', 'y')  # 禁止动态属性，换来更少内存
    def __init__(self, x, y):
        self.x, self.y = x, y

# ✅ lru_cache — 函数级缓存（纯函数必备）
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

---

## 🔥 GIL 的实际影响 / GIL in Practice

```
任务类型            线程 Thread    进程 Process   asyncio
─────────────────────────────────────────────────────
CPU 密集（纯 Python）  ❌ GIL 串行   ✅ 真并行     ❌ 单线程
IO 密集（网络/文件）   ✅ GIL 释放   ✅ 可用       ✅ 最高效
混合                  看比例        看比例         看 IO 占比
```

**实战口诀：**  
- IO 密集 → asyncio（现代首选）或 ThreadPool
- CPU 密集 → multiprocessing 或 Rust/C 扩展
- 简单并发 + IO → concurrent.futures.ThreadPoolExecutor

---

## 📊 真实数字参考 / Real Numbers

| 操作 | 典型延迟 |
|------|---------|
| Python 函数调用 | ~100ns |
| dict lookup | ~50ns |
| list append | ~50ns |
| Redis GET (本地) | ~200µs |
| PostgreSQL query | ~1-10ms |
| HTTP request (本地) | ~1ms |

记住这些量级，当你看到 profiler 输出时才能判断「这是正常的还是异常的」。  
Know these orders of magnitude—that's how you read profiler output intelligently.

---

## 📚 References
- https://docs.python.org/3/library/profile.html
- https://pythonspeed.com/articles/faster-python/
- https://realpython.com/python-concurrency/
- https://github.com/joerick/pyinstrument

## 🧒 ELI5
调优就像查病因：先用体温计（profiler）找到哪里发烧（热点），再根据是什么病（CPU 慢/IO 等/内存大）选药（向量化/异步/生成器）。不能一上来就吃所有药。  
Performance tuning is like diagnosing illness: use a thermometer (profiler) to find where it's hot (bottleneck), then pick the right medicine (vectorize/async/generator) based on the disease type. Never prescribe all medicines at once.
