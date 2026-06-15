# 🐍 Python Craft — Day 66
## State Machine — Explicit State Transitions

**⏱️ 阅读时间：约2分钟 / Reading time: ~2 min**
**Pattern: Design Patterns | Week 5**

---

### 🌏 真实场景 / Real Scenario

你在做一个订单系统：订单可以是 `pending → paid → shipped → delivered`，也可以 `canceled`。随着业务复杂度增加，你开始在代码里到处写 `if order.status == "paid" and ...`——这就是状态机失控的信号。

You're building an order system: `pending → paid → shipped → delivered`, or `canceled`. As complexity grows, you get `if status == "paid" and ...` scattered everywhere. Time for an explicit state machine.

---

### ❌ 没有状态机时 / Without State Machine

```python
class Order:
    def __init__(self):
        self.status = "pending"
    
    def pay(self):
        if self.status == "pending":
            self.status = "paid"
        elif self.status == "paid":
            raise Exception("Already paid")
        elif self.status == "shipped":
            raise Exception("Can't pay after shipping")
        # ... 到处都是 if/elif，容易漏状态

    def ship(self):
        if self.status == "paid":  # what about canceled?
            self.status = "shipped"
        # 谁来保证这里的逻辑完整？
```

❌ 问题：状态转换逻辑散落在每个方法里，难以追踪合法路径。

---

### ✅ 显式状态机 / Explicit State Machine

```python
from enum import Enum, auto
from typing import Dict, Set

class OrderStatus(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELED = auto()

class StateMachine:
    """
    Generic state machine: declare transitions, enforce them.
    """
    def __init__(self, initial: OrderStatus, transitions: Dict[OrderStatus, Set[OrderStatus]]):
        self.state = initial
        self.transitions = transitions
    
    def transition(self, new_state: OrderStatus) -> None:
        allowed = self.transitions.get(self.state, set())
        if new_state not in allowed:
            raise ValueError(
                f"Invalid transition: {self.state.name} → {new_state.name}. "
                f"Allowed: {[s.name for s in allowed]}"
            )
        self.state = new_state


class Order:
    TRANSITIONS = {
        OrderStatus.PENDING:   {OrderStatus.PAID, OrderStatus.CANCELED},
        OrderStatus.PAID:      {OrderStatus.SHIPPED, OrderStatus.CANCELED},
        OrderStatus.SHIPPED:   {OrderStatus.DELIVERED},
        OrderStatus.DELIVERED: set(),   # terminal state
        OrderStatus.CANCELED:  set(),   # terminal state
    }
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        self._sm = StateMachine(OrderStatus.PENDING, self.TRANSITIONS)
    
    @property
    def status(self) -> OrderStatus:
        return self._sm.state
    
    def pay(self):
        self._sm.transition(OrderStatus.PAID)
        print(f"Order {self.order_id}: payment confirmed ✅")
    
    def ship(self):
        self._sm.transition(OrderStatus.SHIPPED)
        print(f"Order {self.order_id}: shipped 📦")
    
    def deliver(self):
        self._sm.transition(OrderStatus.DELIVERED)
        print(f"Order {self.order_id}: delivered 🎉")
    
    def cancel(self):
        self._sm.transition(OrderStatus.CANCELED)
        print(f"Order {self.order_id}: canceled ❌")


# Usage
order = Order("ORD-001")
order.pay()     # PENDING → PAID ✅
order.ship()    # PAID → SHIPPED ✅
order.cancel()  # SHIPPED → CANCELED ❌ raises ValueError!
```

---

### 🔑 核心洞察 / Key Insights

1. **转换表是单一事实来源**：所有合法状态转换都在 `TRANSITIONS` 字典里，一目了然
2. **无效转换立即报错**：不会静默地进入非法状态
3. **状态机可复用**：`StateMachine` 类与业务逻辑解耦，可以用在任何场景

*The transition table is the single source of truth. Invalid transitions fail loudly. The machine is reusable.*

---

### 🔁 何时用状态机 / When to Use

**✅ 用状态机：**
- 对象有明确的生命周期（订单、任务、连接、审批流）
- 你发现代码里有很多 `if status == X and status == Y`
- 需要记录状态转换历史（审计日志）

**❌ 不必用：**
- 状态只有2-3个且逻辑简单
- 状态之间不互相约束

---

### 📈 进阶：带回调的状态机 / Advanced: Hooks on Transition

```python
def transition(self, new_state, on_enter=None):
    # ... validate ...
    old_state = self.state
    self.state = new_state
    if on_enter:
        on_enter(old_state, new_state)  # trigger side effects

# Example: log every transition
order._sm.transition(
    OrderStatus.PAID,
    on_enter=lambda old, new: audit_log.write(old, new)
)
```

---

### 🧒 ELI5

就像地铁闸机：只有在"关闭"状态投币才能开门；已经"开着"的时候不能再投币。状态机就是这个"只允许合法操作"的逻辑。

Like a subway turnstile: you can only insert a coin when it's "locked." The state machine enforces what actions are legal in each state.

---

### 📚 References
- 🔗 https://python-statemachine.readthedocs.io/en/latest/ (python-statemachine library)
- 🔗 https://realpython.com/python-finite-state-machine/
- 🔗 https://gameprogrammingpatterns.com/state.html (classic State pattern explanation)
