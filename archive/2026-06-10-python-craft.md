# Day 62 — Python Craft / 前端 (Python Craft)

🎨 **Python Craft** · Day 62 · Design Patterns Week 4

---

## Command Pattern — Undo/Redo, Task Queues

> **命令模式 / Command Pattern** — 把操作封装成对象，让你能排队、记录、撤销、重放。

---

### 真实场景 / Real-World Scenario

你在做一个文本编辑器（或图像编辑器），需要：
- **Ctrl+Z** 撤销最后一步操作
- **Ctrl+Y** 重做
- **宏录制** — 把一系列操作保存为宏，一键重放
- **操作日志** — 记录用户做了什么，用于 audit 或 replay

*You're building a text editor. Users expect Undo, Redo, macro recording, and audit logs. All these features have one thing in common: treating operations as first-class objects.*

---

### 核心结构 / Core Structure

```python
from abc import ABC, abstractmethod
from typing import Optional
import copy

# ─── Command Interface ───────────────────────────────────────────
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        """执行操作 / Perform the operation"""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """撤销操作 / Reverse the operation"""
        pass
    
    def redo(self) -> None:
        """重做 = 再次执行 / Redo = re-execute (default)"""
        self.execute()

# ─── Receiver: The actual state being modified ──────────────────
class TextDocument:
    def __init__(self):
        self.content = ""
    
    def insert(self, pos: int, text: str) -> None:
        self.content = self.content[:pos] + text + self.content[pos:]
    
    def delete(self, pos: int, length: int) -> None:
        self.content = self.content[:pos] + self.content[pos + length:]
    
    def __repr__(self):
        return f'Document("{self.content}")'

# ─── Concrete Commands ───────────────────────────────────────────
class InsertCommand(Command):
    def __init__(self, doc: TextDocument, pos: int, text: str):
        self.doc = doc
        self.pos = pos
        self.text = text
    
    def execute(self) -> None:
        self.doc.insert(self.pos, self.text)
    
    def undo(self) -> None:
        self.doc.delete(self.pos, len(self.text))

class DeleteCommand(Command):
    def __init__(self, doc: TextDocument, pos: int, length: int):
        self.doc = doc
        self.pos = pos
        self.length = length
        self._deleted_text = ""  # Store for undo
    
    def execute(self) -> None:
        # Capture the text BEFORE deleting (needed for undo)
        self._deleted_text = self.doc.content[self.pos:self.pos + self.length]
        self.doc.delete(self.pos, self.length)
    
    def undo(self) -> None:
        self.doc.insert(self.pos, self._deleted_text)

# ─── Invoker: Manages command history ────────────────────────────
class CommandHistory:
    def __init__(self):
        self._history: list[Command] = []   # Undo stack
        self._redo_stack: list[Command] = []
    
    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # New action clears redo history
    
    def undo(self) -> bool:
        if not self._history:
            return False
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        return True
    
    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        command.redo()
        self._history.append(command)
        return True

# ─── Usage Demo ──────────────────────────────────────────────────
doc = TextDocument()
history = CommandHistory()

history.execute(InsertCommand(doc, 0, "Hello"))
print(doc)  # Document("Hello")

history.execute(InsertCommand(doc, 5, " World"))
print(doc)  # Document("Hello World")

history.execute(DeleteCommand(doc, 5, 6))
print(doc)  # Document("Hello")

history.undo()
print(doc)  # Document("Hello World")  ← undo delete

history.undo()
print(doc)  # Document("Hello")        ← undo insert

history.redo()
print(doc)  # Document("Hello World")  ← redo insert
```

---

### 进阶：Task Queue 应用 / Advanced: Task Queue Pattern

Command Pattern 非常适合**任务队列**——把操作序列化后存到 Redis，worker 异步执行：

```python
import json
from dataclasses import dataclass
from typing import Any

@dataclass
class SerializableCommand:
    """Commands that can be queued in Redis / Celery"""
    command_type: str
    payload: dict
    
    def to_json(self) -> str:
        return json.dumps({"type": self.command_type, "payload": self.payload})
    
    @classmethod
    def from_json(cls, data: str) -> "SerializableCommand":
        d = json.loads(data)
        return cls(d["type"], d["payload"])

# Queue a command
cmd = SerializableCommand("send_email", {"to": "user@example.com", "subject": "Hi"})
redis_client.lpush("task_queue", cmd.to_json())

# Worker pops and executes
raw = redis_client.brpop("task_queue", timeout=5)
if raw:
    cmd = SerializableCommand.from_json(raw[1])
    execute_command(cmd)  # dispatch by cmd.command_type
```

**真实世界用例 / Real-world uses:**
- Celery task serialization
- Event sourcing (每条命令 = 一个事件)
- Database migration rollback scripts
- Game engine (replay systems)

---

### ❌ vs ✅ 常见错误

**❌ 直接在 UI handler 里写逻辑:**
```python
# 耦合紧，无法 undo/redo
def on_click_delete():
    doc.delete(cursor_pos, selected_len)
```

**✅ 封装为 Command:**
```python
def on_click_delete():
    history.execute(DeleteCommand(doc, cursor_pos, selected_len))
```

---

### When to Use / When NOT to Use

**✅ 用 Command Pattern 当：**
- 需要 Undo/Redo
- 需要操作队列或延迟执行
- 需要 audit log / replay
- 操作需要参数化（不同配置执行同类操作）

**❌ 不用当：**
- 操作简单且一次性（过度设计）
- 操作不可逆且不需要撤销（比如发邮件，你不能"取消发送"）

---

### 📚 References

- [Refactoring Guru — Command Pattern](https://refactoring.guru/design-patterns/command)
- [Command Pattern in Python — Real Python](https://realpython.com/python-command-pattern/)
- [Event Sourcing + Command Pattern — Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)

---

### 🧒 ELI5

想象一个遥控器：每个按钮就是一个命令对象（InsertCommand、DeleteCommand）。遥控器（CommandHistory）记住你按过哪些按钮，按"返回"就能把最后一个操作倒放。这就是所有文字编辑器 Ctrl+Z 的工作原理！

*Think of a TV remote: each button is a Command object. The remote (history) remembers which buttons you pressed. Press "Back" to replay the last command in reverse. That's literally how Ctrl+Z works in every text editor!*
