# 🎨 前端 / Python Craft — Day 98
**Generators & itertools — Memory-Efficient Processing**

---

## 真实场景 / Real Scenario

你在处理一个 10GB 的服务器日志文件，需要找出所有 5xx 错误并统计每分钟的错误数。用列表加载整个文件会 OOM（内存溢出）。你会怎么做？

答案：**Generator + itertools**。

---

## Generator 基础 / Generator Basics

```python
# ❌ 内存炸弹 — 一次性加载所有行
def read_errors_bad(filename: str) -> list:
    with open(filename) as f:
        return [line for line in f if "5xx" in line]  # 10GB → OOM

# ✅ Generator — 按需产出，内存只用一行
def read_errors(filename: str):
    with open(filename) as f:
        for line in f:
            if "5xx" in line:
                yield line  # 暂停，等待下一次 next() 调用

# 使用
for error_line in read_errors("access.log"):
    process(error_line)  # 同一时刻内存里只有一行
```

**Generator 工作原理 / How it Works:**
```
调用 read_errors() → 返回 generator 对象（不执行函数体）
next(gen)          → 执行到第一个 yield，返回值，暂停
next(gen)          → 从上次暂停处继续，执行到下一个 yield
StopIteration      → 函数体执行完毕
```

---

## Generator Expression vs List Comprehension

```python
import sys

# List comprehension — 全部在内存
squares_list = [x**2 for x in range(1_000_000)]
print(sys.getsizeof(squares_list))  # ~8MB

# Generator expression — 几乎不占内存
squares_gen = (x**2 for x in range(1_000_000))
print(sys.getsizeof(squares_gen))   # ~200 bytes

# 用法相同，但内存差异巨大！
total = sum(squares_gen)  # 懒计算
```

---

## itertools — 标准库的瑞士军刀

```python
import itertools

# islice — 取前 N 个（不加载整个迭代器）
from itertools import islice
first_100_errors = list(islice(read_errors("huge.log"), 100))

# chain — 合并多个迭代器
log_files = ["jan.log", "feb.log", "mar.log"]
all_errors = itertools.chain.from_iterable(
    read_errors(f) for f in log_files
)

# groupby — 按 key 分组（需要已排序！）
from itertools import groupby
import re

def parse_minute(line: str) -> str:
    # Extract "2026-07-23 08:01" from log line
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', line)
    return match.group(0) if match else "unknown"

# Count errors per minute
for minute, errors in groupby(read_errors("access.log"), key=parse_minute):
    count = sum(1 for _ in errors)
    print(f"{minute}: {count} errors")

# takewhile / dropwhile — 条件截断
from itertools import takewhile, dropwhile

lines = ["INFO start", "INFO running", "ERROR boom", "INFO recover"]
before_error = list(takewhile(lambda l: "ERROR" not in l, lines))
# ["INFO start", "INFO running"]

# batched (Python 3.12+) — 分批处理
from itertools import batched
for batch in batched(read_errors("huge.log"), 1000):
    bulk_insert(batch)  # 每次插入1000条
```

---

## 实战：流式处理管道 / Streaming Pipeline

```python
from itertools import islice, groupby
from collections import Counter

def pipeline(filename: str, top_n: int = 10):
    """
    Read logs → filter errors → parse → count → top N
    全程 O(1) 内存（除了最终的 Counter）
    """
    def read_lines(f):
        with open(f) as fh:
            yield from fh
    
    def filter_5xx(lines):
        return (line for line in lines if " 5" in line)
    
    def extract_path(lines):
        for line in lines:
            parts = line.split()
            yield parts[6] if len(parts) > 6 else "unknown"
    
    paths = extract_path(filter_5xx(read_lines(filename)))
    return Counter(paths).most_common(top_n)

# Usage:
top_errors = pipeline("access.log", top_n=10)
```

---

## 什么时候用 / When to Use

✅ 使用 Generator/itertools:
- 数据集大于可用内存
- 只需要遍历一次（日志、流数据、文件）
- 构建数据处理管道

❌ 不要用:
- 需要多次遍历同一个序列（generator 用完不能重置）
- 数据集小且需要随机访问
- 需要 len() 或索引操作

---

## 📚 References
- https://docs.python.org/3/library/itertools.html
- https://docs.python.org/3/glossary.html#term-generator
- https://realpython.com/introduction-to-python-generators/
- https://docs.python.org/3/library/itertools.html#itertools.batched

## 🧒 ELI5
想象你要数一整个海滩的沙子。普通方法：先把所有沙子装进口袋（内存炸）。Generator 方法：一粒一粒数，数完一粒再拿下一粒，你的口袋只需要装一粒沙子。
