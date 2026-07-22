# 🎨 Python Craft — Day 97
**Profiling — cProfile, line_profiler, memory_profiler**
*Category: Data & Performance · Week 10*

## 真实场景

你在做一个 dashboard，API 响应时间从 200ms 爬升到 2 秒。老板问你：「哪里慢？」你能马上回答吗？

Python 有三把剖析刀：**cProfile**（函数级）、**line_profiler**（行级）、**memory_profiler**（内存级）。

---

## 1. cProfile — 找慢函数（30 秒入门）

```python
import cProfile
import pstats
import io

def slow_function():
    total = 0
    for i in range(1_000_000):
        total += i ** 2
    return total

def main():
    result = slow_function()
    return result

# Method 1: command line
# python -m cProfile -s cumtime my_script.py

# Method 2: programmatic (better for production diagnosis)
pr = cProfile.Profile()
pr.enable()
main()
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(10)  # top 10 functions
print(s.getvalue())
```

**输出解读**：
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.142    0.142    0.142    0.142 script.py:4(slow_function)
```
- `tottime`：函数自身耗时（不含子调用）
- `cumtime`：累计耗时（含子调用）← 通常先看这个

---

## 2. line_profiler — 找慢行（精确到代码行）

```python
# pip install line_profiler

from line_profiler import LineProfiler

def process_data(items: list) -> list:
    result = []
    for item in items:
        # 哪一行最慢？
        cleaned = item.strip().lower()
        if len(cleaned) > 3:
            result.append(cleaned * 2)
    return result

# Profile specific function
lp = LineProfiler()
lp.add_function(process_data)
lp_wrapper = lp(process_data)
lp_wrapper(["Hello ", "World", "AI", "Python Performance"])
lp.print_stats()

# Or use decorator (cleaner)
@lp
def process_data_v2(items):
    ...
```

**输出**：
```
Line #  Hits    Time  Per Hit   % Time  Line Contents
     5  10000   0.02     0.00      5.0  cleaned = item.strip().lower()
     6  10000   0.35     0.04     88.0  if len(cleaned) > 3:    ← 这行！
```

---

## 3. memory_profiler — 找内存泄漏

```python
# pip install memory_profiler

from memory_profiler import profile

@profile
def load_large_dataset(path: str) -> list:
    # Line-by-line memory tracking
    data = []
    with open(path) as f:
        for line in f:
            data.append(line.strip())  # Incremental: good
    
    # 危险：一次性加载所有内容
    # content = f.read()  # Could OOM on large files
    
    return data

# Run: python -m memory_profiler script.py
```

**输出**：
```
Line #    Mem usage    Increment  Line Contents
     7   45.2 MiB     45.2 MiB   data = []
     9   89.4 MiB     44.2 MiB   data.append(...)  ← 内存增长在这里
```

---

## 实战：快速诊断流程

```python
# Step 1: 先用 cProfile 找热点函数（30秒）
python -m cProfile -s cumtime your_script.py | head -20

# Step 2: 对热点函数用 line_profiler（精确）
# kernprof -l -v your_script.py  (需要 @profile 装饰器)

# Step 3: 如果是内存问题
python -m memory_profiler your_script.py

# Step 4: 可视化（推荐）
pip install snakeviz
python -m cProfile -o output.prof your_script.py
snakeviz output.prof  # 浏览器可视化
```

---

## 常见陷阱

❌ **过早优化**：没 profiling 就猜瓶颈，90% 的时间猜错。
✅ 永远先 measure，再 optimize。

❌ **在生产直接开 profiler**：cProfile 有 ~10-30% 开销。
✅ 用采样 profiler（如 `py-spy`）做生产诊断，几乎零开销。

```bash
# py-spy: 生产安全，无需修改代码
pip install py-spy
py-spy top --pid 12345          # 实时 top-like 视图
py-spy record -o profile.svg --pid 12345  # Flamegraph
```

---

## 猜猜这段代码哪里慢？

```python
def find_duplicates(items):
    seen = []          # A: 用 list
    duplicates = []
    for item in items:
        if item in seen:  # O(n) lookup!
            duplicates.append(item)
        seen.append(item)
    return duplicates
```

**A. 正确，没有性能问题**
**B. `item in seen` 是 O(n)，应该用 set**
**C. `append` 太慢**
**D. for 循环应该用 map**

<details><summary>显示答案 / Show Answer</summary>
**B**。`list` 的 `in` 操作是 O(n)，对 n 个元素就是 O(n²)。用 `set` 把 `in` 变成 O(1)，整体降为 O(n)。这是最常见的 Python 性能陷阱之一。
</details>

---

## 📚 References
- [Python cProfile docs](https://docs.python.org/3/library/profile.html)
- [line_profiler GitHub](https://github.com/pyutils/line_profiler)
- [memory_profiler docs](https://pypi.org/project/memory-profiler/)
- [py-spy: sampling profiler for production](https://github.com/benfred/py-spy)

## 🧒 ELI5
就像医院做体检：cProfile 是全身扫描（找哪个器官有问题），line_profiler 是局部精密检查（具体哪条血管堵了），memory_profiler 是量体重变化（哪里在积累脂肪）。先扫再查，不要乱猜。
