# Python Craft: 策略模式 / Strategy Pattern — Pluggable Algorithms

> 📅 Day 56 · 🐍 Python Craft · Design Patterns Week 3 · Expert Phase

---

## 🎨 前端 / Python Craft

**今日话题:** 策略模式 — 让算法可插拔
**Topic:** Strategy Pattern — Making Algorithms Swappable at Runtime

---

### 真实场景 / Real Scenario

你在做一个电商平台，需要支持多种**支付方式**（信用卡、PayPal、加密货币），多种**运费计算方式**（标准、快递、免邮），以及多种**折扣策略**（VIP折扣、季节折扣、批量折扣）。

最烂的做法：一个巨大的 `if/elif/else` 链。策略模式让你**把算法封装成可互换的对象**。

*You're building an e-commerce platform supporting multiple payment methods, shipping calculations, and discount strategies. The worst approach: a giant if/elif/else chain. Strategy Pattern lets you encapsulate algorithms as interchangeable objects.*

---

### 代码示例 / Code Example

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

# ── Approach 1: ABC (classic OOP) ────────────────────────────
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        ...

class NoDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price

class VIPDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 0.20):
        self.percentage = percentage
    
    def apply(self, price: float) -> float:
        return price * (1 - self.percentage)

class BulkDiscount(DiscountStrategy):
    """10% off for orders over $100"""
    def apply(self, price: float) -> float:
        return price * 0.90 if price > 100 else price

# ── Approach 2: Protocol (duck typing, more Pythonic) ─────────
class Discountable(Protocol):
    def apply(self, price: float) -> float:
        ...

# Any callable with the right signature works — no inheritance needed
def seasonal_discount(price: float) -> float:
    return price * 0.85  # 15% off

# ── Context: The object that USES a strategy ──────────────────
@dataclass
class ShoppingCart:
    items: list[tuple[str, float]]  # (name, price)
    discount_strategy: DiscountStrategy = None
    
    def total(self) -> float:
        raw_total = sum(price for _, price in self.items)
        if self.discount_strategy:
            return self.discount_strategy.apply(raw_total)
        return raw_total
    
    def checkout_with(self, strategy: DiscountStrategy) -> float:
        """Swap strategy at runtime — the key power of this pattern"""
        self.discount_strategy = strategy
        return self.total()

# ── Usage ─────────────────────────────────────────────────────
cart = ShoppingCart(items=[("Laptop", 999), ("Mouse", 29)])

print(cart.total())                              # 1028.0 (no discount)
print(cart.checkout_with(VIPDiscount(0.20)))     # 822.4
print(cart.checkout_with(BulkDiscount()))        # 925.2
print(cart.checkout_with(NoDiscount()))          # 1028.0

# Even simpler: use a plain function as strategy (duck typing)
cart.discount_strategy = seasonal_discount  # type: ignore
print(cart.total())                              # 873.8
```

---

### 猜猜输出 / Guess the Output

```python
strategies = [NoDiscount(), VIPDiscount(0.10), BulkDiscount()]
cart = ShoppingCart(items=[("Item", 120)])

results = [cart.checkout_with(s) for s in strategies]
print(results)
```

**A)** `[120.0, 108.0, 108.0]`  
**B)** `[120.0, 108.0, 120.0]`  
**C)** `[120.0, 120.0, 108.0]`  
**D)** 报错 — 无法重用同一个 cart

<details><summary>查看答案</summary>

**A) `[120.0, 108.0, 108.0]`**

- NoDiscount: 120 → 120.0
- VIPDiscount(0.10): 120 × 0.90 = 108.0  
- BulkDiscount: 120 > 100, so 120 × 0.90 = 108.0

</details>

---

### ❌ vs ✅ 对比

```python
# ❌ Bad: Giant if/elif — hard to test, extend, or swap at runtime
def calculate_total(price, discount_type):
    if discount_type == "vip":
        return price * 0.80
    elif discount_type == "bulk":
        return price * 0.90 if price > 100 else price
    elif discount_type == "seasonal":
        return price * 0.85
    else:
        return price

# ✅ Good: Strategy Pattern — each strategy independently testable
# Adding a new strategy = new class, zero changes to existing code
class FlashSaleDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price * 0.50  # 50% off — hot!
```

---

### 何时用 / 何时不用 / When to Use / Avoid

**✅ 用 (Use when):**
- 同一操作有多种变体，且变体可能在运行时切换
- 想对每种变体独立测试
- 算法变体会频繁增减（开放-封闭原则）

**❌ 不用 (Avoid when):**
- 只有 2-3 种固定变体，且不会扩展 → 简单 if/else 更清晰
- 算法变体只在初始化时确定，且永不改变 → 工厂模式更合适

---

### 📚 References
- [Refactoring Guru: Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- [Python Patterns - Strategy](https://python-patterns.guide/gang-of-four/strategy/)
- [Real Python - Duck Typing](https://realpython.com/duck-typing-python/)

### 🧒 ELI5

就像去餐厅，你可以选择"筷子"、"叉子"或"汤匙"——都是吃东西的工具，随时可以换，但餐厅本身不需要改变。策略模式就是把"怎么做"和"做什么"分开。

*Like choosing chopsticks, fork, or spoon at a restaurant — they're all eating tools, swappable anytime, but the restaurant itself doesn't change. Strategy Pattern separates "how to do" from "what to do."*
