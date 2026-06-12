# Day 64 — Python Craft: Adapter Pattern — Wrapping Incompatible Interfaces

🎨 **前端 / Python Craft** — Adapter Pattern: Wrapping Incompatible Interfaces

> 注：本 Phase 的 Section 4 为 Python 设计模式（Python Craft），非前端内容。

---

## 真实场景 / Real-World Scenario

你在做一个 dashboard，需要展示来自三个不同数据源的日志：AWS CloudWatch、DataDog、和你自己的 MySQL。每个 SDK 的接口都不一样——你不可能统一修改它们的源码。适配器模式 (Adapter Pattern) 就是为此而生的。

You're building a monitoring dashboard that aggregates logs from three different sources: AWS CloudWatch, DataDog, and your own MySQL. Each SDK has a completely different interface — you can't modify their source code. The Adapter Pattern exists exactly for this.

---

## 问题 / The Problem

```python
# Three incompatible 3rd-party interfaces
class CloudWatchClient:
    def get_log_events(self, log_group: str, start_time: int) -> dict:
        return {"events": [{"message": "...", "timestamp": 1234567890}]}

class DatadogClient:
    def query_logs(self, service: str, from_ts: float, to_ts: float) -> list:
        return [{"text": "...", "date": 1234567890000}]

class MySQLLogger:
    def fetch_records(self, table: str, since: str) -> list[tuple]:
        return [("2026-06-12 10:00:00", "User logged in")]
```

你的 dashboard 代码不想关心数据来自哪里——它只想调用统一的 `get_logs(source, start_time) → list[LogEntry]`。

Your dashboard shouldn't care where data comes from — it just wants a unified `get_logs(source, start_time) → list[LogEntry]`.

---

## 解法：适配器 / Solution: Adapters

```python
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod

@dataclass
class LogEntry:
    """Unified log entry — what our app speaks."""
    timestamp: datetime
    message: str
    source: str

# Abstract target interface
class LogProvider(ABC):
    @abstractmethod
    def get_logs(self, start_time: datetime) -> list[LogEntry]:
        pass

# Adapter 1: Wrap CloudWatch
class CloudWatchAdapter(LogProvider):
    def __init__(self, client: CloudWatchClient, log_group: str):
        self._client = client
        self._log_group = log_group
    
    def get_logs(self, start_time: datetime) -> list[LogEntry]:
        raw = self._client.get_log_events(
            log_group=self._log_group,
            start_time=int(start_time.timestamp())
        )
        return [
            LogEntry(
                timestamp=datetime.fromtimestamp(e["timestamp"]),
                message=e["message"],
                source="cloudwatch"
            )
            for e in raw["events"]
        ]

# Adapter 2: Wrap DataDog
class DatadogAdapter(LogProvider):
    def __init__(self, client: DatadogClient, service: str):
        self._client = client
        self._service = service
    
    def get_logs(self, start_time: datetime) -> list[LogEntry]:
        now = datetime.now().timestamp()
        raw = self._client.query_logs(
            service=self._service,
            from_ts=start_time.timestamp(),
            to_ts=now
        )
        return [
            LogEntry(
                timestamp=datetime.fromtimestamp(e["date"] / 1000),  # ms → s
                message=e["text"],
                source="datadog"
            )
            for e in raw
        ]

# Adapter 3: Wrap MySQL
class MySQLAdapter(LogProvider):
    def __init__(self, logger: MySQLLogger, table: str):
        self._logger = logger
        self._table = table
    
    def get_logs(self, start_time: datetime) -> list[LogEntry]:
        raw = self._logger.fetch_records(
            table=self._table,
            since=start_time.strftime("%Y-%m-%d %H:%M:%S")
        )
        return [
            LogEntry(
                timestamp=datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"),
                message=row[1],
                source="mysql"
            )
            for row in raw
        ]
```

---

## 统一调用 / Unified Usage

```python
# Dashboard code — completely unaware of underlying SDKs
def aggregate_logs(providers: list[LogProvider], since: datetime) -> list[LogEntry]:
    all_logs = []
    for provider in providers:
        all_logs.extend(provider.get_logs(since))
    
    return sorted(all_logs, key=lambda x: x.timestamp)

# Setup — only done once at startup
providers = [
    CloudWatchAdapter(CloudWatchClient(), log_group="/app/prod"),
    DatadogAdapter(DatadogClient(), service="payment-service"),
    MySQLAdapter(MySQLLogger(), table="app_logs"),
]

# Use — dashboard just calls this
logs = aggregate_logs(providers, since=datetime(2026, 6, 12, 8, 0))
```

---

## 核心结构 / Core Structure

```
Your App Code
     │  calls
     ▼
LogProvider (abstract interface)
     │  implements
     ├── CloudWatchAdapter ──wraps──► CloudWatchClient (3rd party)
     ├── DatadogAdapter    ──wraps──► DatadogClient    (3rd party)
     └── MySQLAdapter      ──wraps──► MySQLLogger      (3rd party)
```

---

## ❌ 常见误用 / Common Mistakes

**❌ 让适配器做业务逻辑**  
适配器只负责接口转换，不应该包含过滤、聚合、业务规则。
```python
# 错误 ❌
class CloudWatchAdapter(LogProvider):
    def get_logs(self, start_time):
        logs = ...
        return [l for l in logs if "ERROR" in l.message]  # 业务过滤放这里！

# 正确 ✅ — 过滤留给调用方
logs = [l for l in provider.get_logs(since) if "ERROR" in l.message]
```

**❌ 适配器包含状态**  
适配器应该是无状态的包装器，状态属于底层客户端。

---

## 适配器 vs 外观 / Adapter vs Facade

| | 适配器 Adapter | 外观 Facade |
|---|---|---|
| 目的 | 接口不兼容 → 转换 | 多个接口 → 简化 |
| 被包装数量 | 一个类 | 多个类 |
| 场景 | 第三方 SDK 接入 | 子系统简化 |

---

## 📚 References
- https://refactoring.guru/design-patterns/adapter
- https://refactoring.guru/design-patterns/adapter/python/example
- https://docs.python.org/3/library/abc.html

## 🧒 ELI5
适配器就像电源插头转换器。你从中国带来一个两脚插头的笔记本，到美国发现插座是三孔的。转换器不改变笔记本，也不改变插座——它中间做一个「翻译」，让不兼容的东西能一起工作。

Adapter is like a power plug converter. You bring a Chinese laptop with a two-prong plug to the US with three-prong outlets. The converter doesn't change your laptop or the outlet — it translates in the middle so incompatible things work together.
