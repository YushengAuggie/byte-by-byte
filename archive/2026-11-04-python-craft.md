# 🐍 Python Craft — Day 147

**综合深化：Python 性能分析与优化决策树**
**Synthesis: Python Performance Profiling & Optimization Decision Tree**

*综合日 — Expert Level | 跨越 asyncio、GIL、生成器、缓存等历史主题*

---

## 场景 / Scenario

你收到报警：某个 Python 微服务 p99 突然升到 3 秒，CPU 长期打满。作为 Staff，你不能随便乱改——先诊断，再手术。

---

## 诊断流程 / Diagnosis Flow

```
High Latency / High CPU?
        │
        ▼
  ① cProfile 找热点函数
        │
   CPU 密集？──────────► ② 检查 GIL (Day 54)
        │                    ├─ IO 密集 → asyncio / threads
        │                    └─ CPU 密集 → multiprocessing / C extension
        │
   内存暴涨？──────────► ③ memory_profiler + tracemalloc
        │                    ├─ 大列表 → 改生成器 (Day 98)
        │                    └─ 循环引用 → weakref / 手动 GC
        │
   DB / 外部 IO 慢？──► ④ 检查 N+1 (connection pooling, Day 78)
                             └─ 检查是否用了 lru_cache (Day 101)
```

---

## 实战示例：用 cProfile + line_profiler 找热点 / Finding Hotspots

```python
# ─── Step 1: cProfile — find which FUNCTIONS are slow ───
import cProfile
import pstats

with cProfile.Profile() as pr:
    result = slow_function()

stats = pstats.Stats(pr)
stats.sort_stats("cumulative")
stats.print_stats(10)  # top 10 slowest

# Output example:
# ncalls  tottime  percall  cumtime  percall  filename:lineno(function)
# 100000    2.100    0.000    2.100    0.000  models.py:42(get_user)
# ← N+1 query pattern: 100000 calls to get_user!
```

```python
# ─── Step 2: line_profiler — find which LINES are slow ───
# pip install line_profiler

@profile  # decorator added by kernprof
def process_users(user_ids: list[int]):
    results = []
    for uid in user_ids:
        user = db.get(uid)          # ← line 5: 95% time here (N+1!)
        results.append(user.name)
    return results

# Run: kernprof -l -v script.py
# Timer unit: 1e-06 s
# Line 5:  950000 µs  95.0%  ← obvious N+1
```

---

## 修复模式对照 / Fix Patterns

```python
# ❌ Before: N+1 query
def get_names_slow(user_ids):
    return [db.get_user(uid).name for uid in user_ids]  # 100K DB calls

# ✅ After: batch fetch
def get_names_fast(user_ids):
    users = db.get_users_bulk(user_ids)  # 1 DB call
    return [u.name for u in users]

# ─────────────────────────────────────────────────────────

# ❌ Before: redundant computation in hot loop
def compute_all(items):
    for item in items:
        threshold = expensive_config_load()  # called 10K times!
        if item > threshold:
            process(item)

# ✅ After: hoist out of loop + cache
threshold = expensive_config_load()  # once
for item in items:
    if item > threshold:
        process(item)

# ─────────────────────────────────────────────────────────

# ❌ Before: materializing large list
def get_all_events():
    return [parse(line) for line in open("huge.log")]  # 10GB in RAM

# ✅ After: generator (Day 98)
def get_all_events():
    for line in open("huge.log"):
        yield parse(line)  # constant memory
```

---

## 跨主题决策树 / Cross-Topic Decision Tree

```
问题类型              历史主题              解法方向
─────────────────────────────────────────────────────────
IO 并发太低     →  asyncio (Day 48)    →  async/await + gather
CPU 被 GIL 卡   →  GIL (Day 54)        →  multiprocessing
大数据集内存    →  generators (Day 98)  →  yield, itertools
重复计算        →  lru_cache (Day 101)  →  @cache, Redis
外部服务调用慢  →  Retry (Day 79)       →  tenacity + circuit breaker
N+1 DB 查询     →  Connection Pool (Day 78) → bulk fetch + eager load
```

---

## 一个容易忽略的性能陷阱 / Hidden Trap

```python
# Python 3.11+ 的 tracemalloc — 找内存泄漏
import tracemalloc

tracemalloc.start()

# ... run your code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:5]:
    print(stat)

# Output: path/to/file.py:42: size=84.3 MiB, count=1000000
# ← 某行创建了100万个对象没释放
```

---

## 📚 References
- https://docs.python.org/3/library/profile.html
- https://github.com/pyutils/line_profiler
- https://docs.python.org/3/library/tracemalloc.html

## 🧒 ELI5
代码跑慢就像厨房出菜慢：先看哪个厨师最忙（cProfile），再看他每个动作花多久（line_profiler），然后看看是不是一直重复拿同一个调料（N+1/缓存问题），还是锅太小装不下食材（内存不足）。找到根因再动手，别随便换厨房。
