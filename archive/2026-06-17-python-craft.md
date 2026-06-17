# 🐍 Python Craft — Descriptors: @property 的底层原理

> **Day 68 · Expert Phase · Python Internals · ~2 min read**

---

## 场景 / Real Scenario

你用过 `@property` 无数次，但它**是什么**？当你写 `obj.name`，Python 怎么决定是直接返回属性还是调用方法？答案：**Descriptor Protocol（描述符协议）**。

You've used `@property` many times — but *what is it*? When you access `obj.name`, how does Python decide whether to return a value or call a method? The answer: the **Descriptor Protocol**.

---

## 核心概念 / Core Concept

任何实现了 `__get__`, `__set__`, `__delete__` 之一的类，就是一个 **描述符**。
Any class implementing `__get__`, `__set__`, or `__delete__` is a **descriptor**.

```python
# @property 是语法糖，等价于用 property 类（本身就是描述符）
# @property is syntactic sugar for the property class (which IS a descriptor)

class Celsius:
    def __init__(self):
        self._temp = 0

    @property
    def temperature(self):
        print("Getting temperature")
        return self._temp

    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError("Too cold!")
        self._temp = value

c = Celsius()
c.temperature = 25   # calls __set__
print(c.temperature) # calls __get__
```

---

## 自定义描述符 / Build Your Own Descriptor

```python
class ValidatedFloat:
    """A descriptor that validates float values with min/max bounds."""

    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None  # set by __set_name__

    def __set_name__(self, owner, name):
        # Called when class is defined — gives descriptor its attribute name
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # class-level access returns descriptor itself
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value):
        if not self.min_val <= value <= self.max_val:
            raise ValueError(
                f"{self.name} must be between {self.min_val} and {self.max_val}"
            )
        setattr(obj, f"_{self.name}", value)


class Product:
    price = ValidatedFloat(0.0, 99999.99)   # descriptor instance
    rating = ValidatedFloat(0.0, 5.0)

    def __init__(self, price, rating):
        self.price = price    # triggers ValidatedFloat.__set__
        self.rating = rating


p = Product(29.99, 4.5)
print(p.price)    # 29.99 — triggers __get__
p.price = -10     # ValueError: price must be between 0.0 and 99999.99
```

---

## 工作原理 / How It Works

```
obj.attr 的查找顺序 (attribute lookup order):
1. type(obj).__mro__ 中找 attr → 如果是 data descriptor → 优先返回
2. obj.__dict__ 中找 attr → 返回
3. type(obj).__mro__ 中找 attr → 如果是 non-data descriptor → 返回
4. AttributeError

Data Descriptor = 同时有 __get__ + __set__ (e.g., property, ValidatedFloat)
Non-data Descriptor = 只有 __get__ (e.g., functions/methods)
```

这就是为什么 `@property` 能**覆盖** instance dict — 它是 data descriptor，优先级更高。
This is why `@property` overrides instance dict — it's a data descriptor with higher priority.

---

## @property vs 描述符对比 / When to Use Which

| | `@property` | Custom Descriptor |
|--|--|--|
| 适用场景 | 单个类的属性验证/计算 | 多个类复用同一验证逻辑 |
| 代码位置 | 在类内部 | 在类外部，可复用 |
| 例子 | `temperature` getter/setter | `ValidatedFloat` 跨类复用 |

**规则:** 逻辑只在一个类用 → `@property`；多个类复用 → 自定义描述符。

---

## 实际应用 / Real-World Uses

- **Django ORM Fields:** `CharField`, `IntegerField` 都是描述符
- **SQLAlchemy:** Column 映射通过描述符协议实现
- **dataclasses with validation:** `__post_init__` + property 组合

---

## 📚 References

- [Python Docs: Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [Fluent Python Ch.23 — Descriptors](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)
- [Real Python: Python Descriptors](https://realpython.com/python-descriptors/)

---

## 🧒 ELI5

普通属性就像一个盒子，你往里放东西，拿出来就是原样。描述符就像一个有内置规则的盒子：放进去时会检查，拿出来时会加工。`@property` 就是 Python 自带的最常用描述符盒子。

A normal attribute is like a plain box — put something in, get the same thing out. A descriptor is a box with built-in rules: it checks when you put things in and transforms when you take them out. `@property` is just Python's most popular pre-made descriptor box.
