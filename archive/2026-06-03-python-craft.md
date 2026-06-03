# 🎨 Python Craft — Factory & Abstract Factory: Object Creation Patterns

> Day 58 · Expert Phase · Design Patterns Week 3 · ~2 min read

---

## 场景 / Scenario

你在构建一个数据管道，需要根据配置文件创建不同类型的数据库连接：PostgreSQL、MySQL、SQLite。调用方不应该知道具体类怎么初始化，只需要说"给我一个数据库连接"。

You're building a data pipeline that creates different DB connections based on config: PostgreSQL, MySQL, SQLite. Callers shouldn't know initialization details — just say "give me a database connection."

---

## 问题 / The Problem

```python
# ❌ Without factory — caller knows too much
if config["type"] == "postgres":
    db = PostgresDB(host=..., port=5432, ssl=True)
elif config["type"] == "mysql":
    db = MySQLDB(host=..., charset="utf8mb4")
# This if-else is scattered EVERYWHERE in the codebase
```

散落在各处的 `if-else` 是维护噩梦。每次加新数据库类型，你要搜索整个代码库。

---

## Factory Pattern (工厂模式)

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

# Abstract product
class Database(ABC):
    @abstractmethod
    def connect(self) -> None: ...
    
    @abstractmethod
    def query(self, sql: str) -> list: ...

# Concrete products
class PostgresDB(Database):
    def __init__(self, host: str, port: int = 5432):
        self.host = host
        self.port = port
    
    def connect(self) -> None:
        print(f"Connecting to Postgres at {self.host}:{self.port}")
    
    def query(self, sql: str) -> list:
        return [{"postgres": True}]

class SQLiteDB(Database):
    def __init__(self, path: str):
        self.path = path
    
    def connect(self) -> None:
        print(f"Opening SQLite at {self.path}")
    
    def query(self, sql: str) -> list:
        return [{"sqlite": True}]

# Simple Factory (not GoF, but very practical)
class DatabaseFactory:
    _registry: Dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str, klass: type) -> None:
        cls._registry[name] = klass
    
    @classmethod
    def create(cls, config: Dict[str, Any]) -> Database:
        db_type = config.pop("type")
        klass = cls._registry.get(db_type)
        if not klass:
            raise ValueError(f"Unknown DB type: {db_type}")
        return klass(**config)

# Register once at startup
DatabaseFactory.register("postgres", PostgresDB)
DatabaseFactory.register("sqlite", SQLiteDB)

# Usage — caller is clean
config = {"type": "postgres", "host": "prod.db.internal", "port": 5432}
db = DatabaseFactory.create(config)
db.connect()
# → "Connecting to Postgres at prod.db.internal:5432"
```

---

## Abstract Factory (抽象工厂) — 当产品有"家族"

适用于需要创建**一组相关对象**的场景，比如"AWS 套件" vs "GCP 套件"。

```python
# Abstract Factory — creates families of related objects
class CloudFactory(ABC):
    @abstractmethod
    def create_storage(self) -> "Storage": ...
    
    @abstractmethod
    def create_queue(self) -> "Queue": ...

class AWSFactory(CloudFactory):
    def create_storage(self) -> "Storage":
        return S3Storage()
    
    def create_queue(self) -> "Queue":
        return SQSQueue()

class GCPFactory(CloudFactory):
    def create_storage(self) -> "Storage":
        return GCSStorage()
    
    def create_queue(self) -> "Queue":
        return PubSubQueue()

# Client code — doesn't know if it's AWS or GCP
def deploy_pipeline(factory: CloudFactory):
    storage = factory.create_storage()
    queue = factory.create_queue()
    # Works with any cloud provider
```

---

## ❌ vs ✅ 对比

| 方式 | 问题 |
|------|------|
| ❌ `if/elif` everywhere | 散落在各处，新类型 = 全局搜索改动 |
| ❌ Direct `new` in caller | 调用方和具体实现紧耦合 |
| ✅ Factory + registry | 新类型只需 `register()` 一行，调用方无需改动 |
| ✅ Abstract Factory | 整个"产品家族"可以一键切换 |

---

## 什么时候用 / When to Use

**用 Factory 当 / Use Factory when:**
- 对象创建逻辑复杂，或类型由配置/运行时决定
- 想要用字符串标识来选择实现类
- 测试时需要换掉真实实现 (inject mock)

**用 Abstract Factory 当 / Use Abstract Factory when:**
- 产品有多个"家族"(AWS/GCP, Light/Dark theme)
- 需要保证同一家族的对象一起被创建
- 切换家族时不想改调用代码

**不要过度使用 / Don't overuse:**
- 2-3 个实现？直接 `if/else` 更清晰
- 工厂本身只适合当需求明确要扩展时

---

## 📚 References

- [Factory Method - Refactoring.Guru](https://refactoring.guru/design-patterns/factory-method)
- [Abstract Factory - Refactoring.Guru](https://refactoring.guru/design-patterns/abstract-factory)
- [Python Patterns - Factory](https://python-patterns.guide/gang-of-four/factory-method/)

---

## 🧒 ELI5

工厂模式就像麦当劳 🍔。你说"给我一个汉堡"，不用知道后厨怎么做。工厂决定用什么原料、怎么组装。抽象工厂是"给我一整套麦当劳套餐"——汉堡+薯条+可乐都来自同一个"家族"，换成肯德基套餐时，三样都会换。

Factory is like McDonald's 🍔. You say "give me a burger" without knowing how the kitchen works. Abstract Factory is "give me a full combo meal" — burger + fries + drink all from the same "family." Switch to KFC, and all three switch together.
