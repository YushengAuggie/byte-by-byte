# 🎨 前端 / Python Craft — Day 12 (Section 4)
## Decorator Pattern (OOP) — 对象包装，不是语法糖
> ⏱️ 预计阅读时间 / Est. read time: 2 min | Design Patterns Week 3

---

## 真实场景 / Real Scenario

你在做一个日志系统：基础 Logger 只写文件，但某些场景需要同时加时间戳、加调用者信息、加颜色。你不想修改 Logger 类，也不想为每种组合创建子类。

You have a base Logger that writes to file. Some cases need timestamps, caller info, and colors added. You don't want to modify Logger or create 12 subclass combinations.

**Decorator Pattern** 的核心：**动态地给对象添加职责，而不修改类本身。**

The core idea: **attach new responsibilities to an object dynamically, without modifying its class.**

---

## 代码示例 / Code

```python
from abc import ABC, abstractmethod

# Component interface — 所有对象共享的接口
class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass

# Concrete component — 最简单的实现
class FileLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[FILE] {message}")

# Base decorator — 持有被包装的对象
class LoggerDecorator(Logger):
    def __init__(self, logger: Logger):
        self._logger = logger  # wrap the inner logger

    def log(self, message: str) -> None:
        self._logger.log(message)  # delegate by default

# Concrete decorator 1: adds timestamp
class TimestampDecorator(LoggerDecorator):
    def log(self, message: str) -> None:
        from datetime import datetime
        timestamped = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self._logger.log(timestamped)

# Concrete decorator 2: adds log level
class LevelDecorator(LoggerDecorator):
    def __init__(self, logger: Logger, level: str = "INFO"):
        super().__init__(logger)
        self.level = level

    def log(self, message: str) -> None:
        self._logger.log(f"[{self.level}] {message}")

# --- Usage ---
# Simple logger
logger = FileLogger()
logger.log("Server started")
# → [FILE] Server started

# Wrap with timestamp
logger = TimestampDecorator(FileLogger())
logger.log("Server started")
# → [FILE] [14:30:05] Server started

# Stack multiple decorators (order matters!)
logger = LevelDecorator(TimestampDecorator(FileLogger()), level="ERROR")
logger.log("Server crashed")
# → [FILE] [14:30:05] [ERROR] Server crashed
```

---

## ❌ vs ✅ 对比 / Common Mistake

❌ **用继承解决组合问题**:
```python
class TimestampFileLogger(FileLogger): ...
class LevelTimestampFileLogger(TimestampFileLogger): ...
# 3 种特性 = 7 个子类！
```

✅ **用 Decorator 自由组合**:
```python
logger = LevelDecorator(TimestampDecorator(FileLogger()))
# n 种特性 = n 个 decorator，可任意组合
```

---

## 什么时候用 / When to Use

✅ 需要**动态**给对象添加职责（非编译时继承）
✅ 特性可以**任意组合**（N 种组合用继承会爆炸）
✅ 不想修改原始类（开闭原则）

❌ 如果只有 1-2 种固定组合，直接子类更简单
❌ 过度嵌套会让调试栈很深（每层都是包装）

---

## Python 标准库中的 Decorator Pattern
- `io.BufferedWriter(io.FileIO(...))` — IO 流包装
- `functools.lru_cache` — 虽然是语法糖，本质也是 wrapper
- `logging.Handler` — 可以叠加 Formatter、Filter

---

## 📚 References
- [Refactoring.Guru - Decorator](https://refactoring.guru/design-patterns/decorator)
- [Python io module](https://docs.python.org/3/library/io.html) — real-world example
- [Design Patterns: Elements of Reusable OO Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)

## 🧒 ELI5

Decorator 就像俄罗斯套娃：外层娃娃（Decorator）把内层娃娃（Component）包住，在传球之前加点料。可以套很多层，每层加不同功能。

Decorator is like Russian dolls: the outer doll wraps the inner one, adds something before passing the message through. You can stack as many layers as you want, each adding a different feature.
