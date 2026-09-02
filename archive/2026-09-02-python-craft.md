# 🎨 Python Craft — Day 124 (Synthesis)
**生产 Python 系统的 10 个隐藏性能杀手**
*10 Hidden Performance Killers in Production Python Systems*

---

## 🎯 场景 / Scenario

你的 Python API 在 load test 里 P99 突然飙到 2 秒，CPU 正常、内存正常、DB 也没慢。你知道是 Python 本身的问题，但不知道从哪下手。

*Your Python API's P99 latency spikes to 2s under load. CPU/memory/DB all look fine. Where do you start?*

---

## 🔬 深度合成：10 个生产级性能陷阱

### 1. 字典查找 vs 列表扫描 (Dict Lookup vs List Scan)

```python
# ❌ O(n) 每次查找
valid_status = ["active", "inactive", "pending", "deleted"]
if user.status in valid_status:  # scans whole list

# ✅ O(1) 哈希查找
valid_status = {"active", "inactive", "pending", "deleted"}  # set!
if user.status in valid_status:
```
**影响**: 1000 次/s 的请求 × 列表长度 50 = 明显 CPU 浪费

---

### 2. 字符串拼接 O(n²) 陷阱 (String Concatenation)

```python
# ❌ 每次 + 都创建新字符串对象，O(n²)
result = ""
for item in large_list:
    result += str(item)

# ✅ join 一次性分配，O(n)
result = "".join(str(item) for item in large_list)
```

---

### 3. 未释放的数据库连接 (DB Connection Leaks)

```python
# ❌ 异常时连接泄漏
conn = db.get_connection()
result = conn.execute(query)  # 如果这里抛异常...
conn.close()  # 永远不会执行

# ✅ 用 context manager 保证释放
with db.get_connection() as conn:
    result = conn.execute(query)
# 无论异常与否，连接都会归还到连接池
```

---

### 4. N+1 查询 (ORM N+1)

```python
# ❌ 每个 user 都触发一次额外 SQL
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # SELECT * FROM profile WHERE user_id=?  × N

# ✅ 一次 JOIN 拿所有数据
users = User.objects.select_related('profile').all()
```

---

### 5. Global 变量与 GIL 争抢 (GIL Contention)

```python
# ❌ 纯 CPU 密集任务用 ThreadPoolExecutor 无效
# GIL 让多线程 CPU-bound 代码实际是串行的
with ThreadPoolExecutor(4) as pool:
    results = list(pool.map(cpu_heavy_fn, data))

# ✅ CPU-bound → ProcessPoolExecutor
# ✅ I/O-bound → ThreadPoolExecutor or asyncio
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor(4) as pool:
    results = list(pool.map(cpu_heavy_fn, data))
```

---

### 6. 未使用生成器导致内存爆炸 (No Generators)

```python
# ❌ 一次性加载 10M 行到内存
rows = list(db.execute("SELECT * FROM events"))  # OOM risk

# ✅ 流式处理，内存恒定
for row in db.execute("SELECT * FROM events"):  # iterator
    process(row)
```

---

### 7. Pickle 序列化用于大对象 (Pickle Overhead)

```python
# ❌ pickle 慢，且不安全
import pickle
cache.set(key, pickle.dumps(large_obj))

# ✅ msgpack / orjson for speed
import orjson
cache.set(key, orjson.dumps(obj))  # 5-10x faster than json
```

---

### 8. 忘记 `__slots__` 在高频对象上 (Missing __slots__)

```python
# ❌ 每个实例都有 __dict__ (额外内存)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y  # 每个对象 ~200 bytes overhead

# ✅ __slots__ 消除 __dict__ (~50% 内存节省)
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
```
**适用场景**: 大量小对象（坐标、事件记录、metric 点）

---

### 9. 同步代码阻塞 asyncio 事件循环 (Blocking in Async)

```python
# ❌ time.sleep 阻塞整个 event loop！
async def handler():
    time.sleep(1)  # kills concurrency

# ✅ await asyncio.sleep 让出控制权
async def handler():
    await asyncio.sleep(1)  # non-blocking
    
# ❌ 同步 requests 库
response = requests.get(url)  # blocks event loop

# ✅ httpx async
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

---

### 10. 生产环境忘开 `-O` 或关 debug (Missing Optimizations)

```bash
# 生产启动时
python -O app.py          # 关闭 assert + __debug__ blocks
PYTHONDONTWRITEBYTECODE=1  # 不写 .pyc (容器内有用)
PYTHONOPTIMIZE=2           # 同 -OO，去掉 docstrings

# uvicorn 生产配置
uvicorn app:app --workers 4 --loop uvloop  # uvloop 比默认快 2-4x
```

---

## 🧪 快速诊断工具

```python
# 找热点函数
python -m cProfile -s cumulative app.py

# 找内存泄漏
pip install memory_profiler
@profile  # decorator → line-by-line memory

# 找 N+1 查询 (Django)
pip install django-silk  # request-level SQL logging
```

---

## 📚 References
- https://docs.python.org/3/library/timeit.html — 精确计时
- https://github.com/joerick/pyinstrument — 采样型 profiler，生产友好
- https://orjson.readthedocs.io/en/latest/ — 最快 JSON 库

## 🧒 ELI5
Python 慢有时是因为你让它做了多余的工作：在 100 个苹果里一个一个找那个红的（列表），不如用标签本（集合/字典）直接翻到"红色"。每次路过都创建新便利贴（字符串拼接），不如最后一次性写好。这10个陷阱就是10种"在做多余的工作"的方式。
