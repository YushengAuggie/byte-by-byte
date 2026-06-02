# 🐍 Python Craft — Day 10 (Week 3)
**Observer Pattern — Event Systems**
*2026-06-02 | Expert Phase | Design Patterns*

---

## 场景 / Scenario

你在构建一个监控系统：某个指标超过阈值，需要同时触发 Slack 通知、PagerDuty 报警、写入日志。如果用 if-else 硬编码，每加一个新的通知渠道都要改核心代码——这违反了开闭原则。

*You're building a monitoring system: when a metric exceeds a threshold, you need to trigger Slack, PagerDuty, and logging simultaneously. If you hard-code if-else, every new channel requires touching core logic — violating Open/Closed Principle.*

---

## Observer Pattern 核心思路 / Core Idea

**发布者（Subject）** 不知道谁在监听；**订阅者（Observer）** 不需要知道其他订阅者存在。解耦！

```
Subject → notify() → [Observer1, Observer2, Observer3]
          (broadcasts)
```

---

## Python 实现 / Implementation

### 方式 1：经典面向对象 / Classic OOP

```python
from abc import ABC, abstractmethod
from typing import Any

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: Any) -> None:
        pass

class EventBus:
    """Simple synchronous event bus."""
    
    def __init__(self):
        self._listeners: dict[str, list[Observer]] = {}
    
    def subscribe(self, event: str, observer: Observer) -> None:
        self._listeners.setdefault(event, []).append(observer)
    
    def unsubscribe(self, event: str, observer: Observer) -> None:
        self._listeners.get(event, []).remove(observer)
    
    def publish(self, event: str, data: Any = None) -> None:
        for observer in self._listeners.get(event, []):
            observer.update(event, data)

# Concrete observers
class SlackNotifier(Observer):
    def update(self, event: str, data: Any) -> None:
        print(f"[Slack] 🔔 {event}: {data}")

class PagerDutyNotifier(Observer):
    def update(self, event: str, data: Any) -> None:
        print(f"[PagerDuty] 🚨 ALERT {event}: {data}")

class AuditLogger(Observer):
    def update(self, event: str, data: Any) -> None:
        print(f"[Log] {event} | {data}")

# Usage
bus = EventBus()
bus.subscribe("metric.threshold.exceeded", SlackNotifier())
bus.subscribe("metric.threshold.exceeded", PagerDutyNotifier())
bus.subscribe("metric.threshold.exceeded", AuditLogger())

bus.publish("metric.threshold.exceeded", {"metric": "cpu", "value": 95, "threshold": 90})
# [Slack] 🔔 metric.threshold.exceeded: {'metric': 'cpu', ...}
# [PagerDuty] 🚨 ALERT ...
# [Log] ...
```

### 方式 2：函数式 / Functional (更 Pythonic)

```python
from collections import defaultdict
from typing import Callable

class EventEmitter:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
    
    def on(self, event: str, handler: Callable) -> None:
        self._handlers[event].append(handler)
    
    def off(self, event: str, handler: Callable) -> None:
        self._handlers[event].remove(handler)
    
    def emit(self, event: str, **kwargs) -> None:
        for handler in self._handlers[event]:
            handler(**kwargs)

# Cleaner usage with plain functions
emitter = EventEmitter()

# Register handlers
def send_welcome_email(user_id: str, email: str):
    print(f"Sending welcome email to {email}")

emitter.on("user.signup", send_welcome_email)  # emitter.on(event, handler)

def track_analytics(user_id: str, **kwargs):
    print(f"Tracking signup for {user_id}")

emitter.on("user.signup", track_analytics)
emitter.emit("user.signup", user_id="u123", email="alice@example.com")
```

---

## ❌ 常见坑 / Common Mistakes

**❌ 忘记取消订阅导致内存泄漏**
```python
# Bad: widget subscribes but never unsubscribes
class Widget:
    def __init__(self, bus):
        bus.subscribe("resize", self)  # Widget can't be GC'd!

# Good: implement __del__ or use weakref
import weakref

class WeakEventBus:
    def subscribe(self, event, observer):
        self._listeners.setdefault(event, []).append(weakref.ref(observer))
```

**❌ Observer 抛异常导致后续 Observer 不执行**
```python
# Good: wrap each handler
def publish(self, event, data):
    for observer in self._listeners.get(event, []):
        try:
            observer.update(event, data)
        except Exception as e:
            logging.error(f"Observer {observer} failed: {e}")
```

---

## 与 Strategy Pattern 的区别 / vs Strategy

- **Strategy**：封装**算法**，一次只用一个（换引擎）
- **Observer**：封装**反应**，一次触发多个（广播）

---

## 实战场景 / Real-World Usage

| 场景 | 框架实现 |
|------|---------|
| Django signals | `post_save.connect(handler, sender=MyModel)` |
| Vue 3 reactive | `watch(() => state.count, handler)` |
| Python logging | `logger.addHandler(handler)` |
| Node.js EventEmitter | `emitter.on('data', callback)` |

---

## 📚 References
- [Observer Pattern — Refactoring Guru](https://refactoring.guru/design-patterns/observer/python/example)
- [Django Signals Docs](https://docs.djangoproject.com/en/5.0/topics/signals/)
- [Python Design Patterns — Brandon Rhodes](https://python-patterns.guide/gang-of-four/observer/)

## 🧒 ELI5

观察者模式就像订报纸：你跟报社说"每天送报给我"，报社不用知道你是谁，有新报纸了就送；你也不用每天去问"今天有报纸吗？"。新增或取消订阅互不影响。

*Observer is like subscribing to a newspaper: you tell the publisher "deliver to me daily," the publisher doesn't need to know you personally, and every new subscriber just gets added to the list. Everyone gets notified automatically, no polling needed.*
