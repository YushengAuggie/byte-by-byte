# 🎨 Python Craft — Day 77
## Context Managers — `__enter__`/`__exit__`, contextlib

> ⏱️ 阅读时间约 2 分钟 / ~2 min read | 分类 / Category: Python Internals

---

### 🎬 场景导入 / Real Scenario

你在写一个数据库批量写入服务，需要：打开连接 → 开事务 → 写数据 → 提交/回滚 → 关连接。任何一步出错都要保证资源被释放。如果没有 context manager，这是一堆 try/finally。有了它，一行 `with` 搞定。

You're writing a DB batch write service: open conn → begin txn → write → commit/rollback → close. Any failure must clean up. Without context managers: nested try/finally. With them: one clean `with`.

---

### 🔍 `with` 语句背后发生了什么 / What `with` Actually Does

```python
with open("file.txt") as f:
    data = f.read()

# Python 展开成 / Python expands this to:
mgr = open("file.txt")
f = mgr.__enter__()        # setup: returns the "as" value
try:
    data = f.read()
except Exception as e:
    if not mgr.__exit__(type(e), e, e.__traceback__):
        raise              # if __exit__ returns False, re-raise
else:
    mgr.__exit__(None, None, None)  # no exception path
```

**`__exit__` 签名 / signature:** `(exc_type, exc_val, exc_tb)`
- 返回 `True` → 吞掉异常（suppress）
- 返回 `False`/`None` → 让异常继续传播

---

### 💻 三种写法 / Three Ways to Write Context Managers

**方式 1：类 / Class-based**
```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self  # "as" value

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {elapsed:.3f}s")
        return False  # don't suppress exceptions

with Timer() as t:
    expensive_operation()
```

**方式 2：`@contextmanager` — 最简洁 / Cleanest**
```python
from contextlib import contextmanager

@contextmanager
def db_transaction(conn):
    try:
        yield conn        # everything before yield = __enter__
        conn.commit()     # success path
    except Exception:
        conn.rollback()   # failure path
        raise
    finally:
        conn.close()      # always runs = __exit__

with db_transaction(get_conn()) as conn:
    conn.execute("INSERT ...")
```

**方式 3：`contextlib.suppress` — 吞异常 / Suppress exceptions**
```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("temp.txt")   # silently skip if file doesn't exist
# equivalent to try/except FileNotFoundError: pass — but cleaner
```

---

### ❌ 常见错误 / Common Mistakes

```python
# ❌ WRONG: forgetting yield in @contextmanager
@contextmanager
def bad_mgr():
    setup()
    # forgot yield! → GeneratorExit, cleanup never runs

# ✅ RIGHT: always yield exactly once
@contextmanager
def good_mgr():
    setup()
    try:
        yield
    finally:
        cleanup()

# ❌ WRONG: __exit__ returns True accidentally
def __exit__(self, *args):
    self.cleanup()
    return True  # silently swallows ALL exceptions — hard to debug!

# ✅ RIGHT: only suppress specific exceptions you intend to
def __exit__(self, exc_type, *args):
    self.cleanup()
    return exc_type is KeyboardInterrupt  # only suppress Ctrl+C
```

---

### 🤔 用 / 不用 / When to Use vs Not Use

| 用 / Use | 不用 / Skip |
|---|---|
| 资源获取/释放（文件、锁、DB、网络） | 简单函数，不需要清理 |
| 需要 setup + guaranteed teardown | 用 `try/finally` 一次就够 |
| 多处复用同一个 setup/teardown | 只用一次的一次性代码 |
| 测试中 mock/patch | - |

---

### 📚 References

- [Python docs: contextlib](https://docs.python.org/3/library/contextlib.html)
- [Real Python: Context Managers](https://realpython.com/python-with-statement/)
- [PEP 343 — The "with" Statement](https://peps.python.org/pep-0343/)

---

### 🧒 ELI5

`with` 语句就像"用完归位"的承诺：不管中间出了什么事，最后一定会做清理。就像借了图书馆的书，不管你读没读完，到期了自动还——你不需要记得"哦我要还书"。

`with` is a "put it back when done" promise: no matter what happens inside, cleanup always runs. Like a library book return — automatic, unconditional, no matter what.
