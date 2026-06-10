# 🐍 Python Craft — Day 61
**Topic:** Singleton Pattern — And Why You Usually Shouldn't
**Date:** 2026-06-09 | **Phase:** Expert | **Week:** 4 — Design Patterns

---

## 🐍 Python Craft
### Singleton 模式 — 以及为什么你通常不应该用它
### Singleton Pattern — And Why You Usually Shouldn't

---

## 🎯 真实场景 / Real Scenario

你在做一个 backend service，需要一个全局配置对象。你听说用 Singleton 可以保证只有一个实例。听起来很合理对吧？

You're building a backend service and need a single global config object. Someone says "use a Singleton." Sounds reasonable... until it isn't.

---

## 📖 什么是 Singleton / What Is a Singleton

Singleton 保证一个类 **只有一个实例**，并提供全局访问点。

```python
# 最简单的 Python Singleton: 用 __new__ 控制实例化
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # 注意: __init__ 会被多次调用! 用 hasattr 防止重复初始化
        if not hasattr(self, '_initialized'):
            self.value = 42
            self._initialized = True

# Usage
a = Singleton()
b = Singleton()
print(a is b)  # True — 同一个对象
```

---

## 🏭 更 Pythonic 的实现 / More Pythonic Approaches

```python
# 方式 1: Module-level singleton (最 Pythonic)
# config.py
class _Config:
    def __init__(self):
        self.debug = False
        self.db_url = "postgres://localhost/mydb"

config = _Config()  # 模块只加载一次，天然单例

# 其他模块:
from config import config
print(config.debug)

# -------------------------

# 方式 2: 用 @classmethod + class variable
class DatabasePool:
    _pool = None
    
    @classmethod
    def get_instance(cls):
        if cls._pool is None:
            cls._pool = cls._create_pool()
        return cls._pool
    
    @classmethod
    def _create_pool(cls):
        print("Creating connection pool...")
        return {"connections": []}

pool1 = DatabasePool.get_instance()
pool2 = DatabasePool.get_instance()
print(pool1 is pool2)  # True

# -------------------------

# 方式 3: Metaclass (最"正规"但最复杂)
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logs = []
```

---

## ⚠️ 为什么你通常不应该用 Singleton / Why You Usually Shouldn't

```python
# ❌ 问题 1: 测试困难 — 全局状态污染测试
class UserService:
    def get_user(self, user_id):
        return Database.get_instance().query(f"SELECT * FROM users WHERE id={user_id}")

# 你怎么在测试里替换 Database？很难！

# ✅ 更好的做法: 依赖注入
class UserService:
    def __init__(self, db):  # 注入依赖
        self.db = db
    
    def get_user(self, user_id):
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")

# 测试里:
mock_db = MockDatabase()
service = UserService(db=mock_db)  # 轻松 mock!

# -------------------------

# ❌ 问题 2: 并发问题 — 线程不安全的懒初始化
import threading

class UnsafeSingleton:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:  # 两个线程可能同时通过这里!
            cls._instance = cls()
        return cls._instance

# ✅ 线程安全版本:
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # 双重检查锁
                    cls._instance = cls()
        return cls._instance
```

---

## ✅ 何时应该用 Singleton / When to Actually Use It

| 场景 | 理由 |
|------|------|
| 连接池 (DB, Redis) | 连接是昂贵的全局资源 |
| 日志器 | 全局写入点，可接受 |
| 配置对象 | 只读，没有状态变更问题 |
| 缓存 | 全局共享缓存合理 |

**何时绝对不用:**
- 业务逻辑对象（User, Order, Product）
- 任何需要在测试中 mock 的对象
- 多进程环境（每个进程有自己的内存空间，Singleton 不跨进程）

---

## 📚 References

- [Python Design Patterns — Singleton](https://python-patterns.guide/gang-of-four/singleton/)
- [Why Singleton is Considered Anti-Pattern](https://stackoverflow.com/questions/137975/what-are-drawbacks-or-disadvantages-of-singleton-pattern)
- [Python Docs — Metaclasses](https://docs.python.org/3/reference/datamodel.html#metaclasses)

---

## 🧒 ELI5

Singleton 就像学校里只有一个校长办公室——不管谁去问，都去同一间办公室找同一个人。这听起来很方便，但问题是：如果你在做作业测验，你没办法假装一个"假校长"来测试不同情况。真正好的设计是把校长作为参数传入，这样测验时可以用"模拟校长"。

Singleton is like a school with one principal's office — everyone goes to the same place to get the same person. Sounds convenient, but the problem is: when testing, you can't swap in a "fake principal." Better design passes the principal as a parameter, so tests can use a mock one.
