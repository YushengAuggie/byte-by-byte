# 🎨 Python Craft — Day 20
**主题 / Topic:** Metaclasses — When and Why (ORM Example)
**类别 / Category:** Python Internals
**日期 / Date:** 2026-06-18

---

## 🎨 Python Craft

**Metaclasses（元类）— 控制"类"本身的创建**

---

### 🔥 真实场景 / Real Scenario

你在构建一个 mini ORM（像 Django Models 那样）。你希望用户写：

```python
class User(Model):
    name = CharField(max_length=100)
    age  = IntField()
```

然后 `User.objects.filter(name="Alice")` 就能自动生成 SQL。  
问题是：`name` 和 `age` 在类定义时只是**类属性**，ORM 怎么知道它们是数据库字段？

You're building a mini ORM (like Django Models). The user writes a class with field descriptors. How does the ORM auto-detect which attributes are fields vs regular class attributes?

**答案：Metaclass。** 元类在类被**创建时**拦截，可以检查、修改、注册任何类属性。

---

### 🤔 先理解：类也是对象 / Classes Are Objects

```python
# 普通对象的创建
obj = MyClass()   # MyClass() 调用 MyClass.__init__

# 类本身的创建（你平时看不见的）
MyClass = type('MyClass', (object,), {'method': ...})
#             ^^^名字      ^^^父类       ^^^属性字典
```

`type` 就是所有类的默认**元类**。自定义 metaclass = 自定义"类的工厂"。

---

### 💻 Mini ORM 实现 / Implementation

```python
# Field descriptors (simplified)
class Field:
    def __init__(self, column_type):
        self.column_type = column_type
        self.name = None  # set by metaclass

class CharField(Field):
    def __init__(self, max_length=255):
        super().__init__('VARCHAR')
        self.max_length = max_length

class IntField(Field):
    def __init__(self):
        super().__init__('INTEGER')


# THE METACLASS — intercepts class creation
class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Collect all Field instances from class body
        fields = {}
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, Field):
                attr_value.name = attr_name  # inject field name
                fields[attr_name] = attr_value

        # Inject metadata onto the class
        namespace['_fields'] = fields
        namespace['_table'] = name.lower() + 's'  # User → users

        return super().__new__(mcs, name, bases, namespace)


# Base Model uses the metaclass
class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @classmethod
    def create_table_sql(cls):
        cols = []
        for name, field in cls._fields.items():
            cols.append(f"  {name} {field.column_type}")
        return f"CREATE TABLE {cls._table} (\n" + ",\n".join(cols) + "\n);"

    def insert_sql(self):
        fields = list(self._fields.keys())
        values = [repr(getattr(self, f, None)) for f in fields]
        return (f"INSERT INTO {self._table} ({', '.join(fields)}) "
                f"VALUES ({', '.join(values)});")


# User just declares fields — metaclass does the rest
class User(Model):
    name = CharField(max_length=100)
    age  = IntField()


# Usage
print(User._fields)         # {'name': CharField, 'age': IntField}
print(User._table)          # 'users'
print(User.create_table_sql())
# CREATE TABLE users (
#   name VARCHAR,
#   age INTEGER
# );

u = User(name="Alice", age=30)
print(u.insert_sql())
# INSERT INTO users (name, age) VALUES ('Alice', 30);
```

---

### 猜猜输出什么 / Quiz

```python
class Meta(type):
    def __new__(mcs, name, bases, ns):
        ns['_created_by'] = 'metaclass'
        return super().__new__(mcs, name, bases, ns)

class Foo(metaclass=Meta):
    pass

print(Foo._created_by)
print(type(Foo))
```

A) `'metaclass'` 和 `<class '__main__.Meta'>`  
B) `AttributeError` — Foo 没有 `_created_by`  
C) `'metaclass'` 和 `<class 'type'>`  
D) `None` 和 `<class 'type'>`

<details><summary>显示答案 / Show Answer</summary>
**A** — 元类的 `__new__` 在类创建时运行，自动注入 `_created_by`。`type(Foo)` 返回的是元类本身 `Meta`，不是 `type`。
</details>

---

### ❌ 误用 vs ✅ 正确用法

❌ **Bad:** 什么都用 metaclass  
```python
# DON'T: 用 metaclass 只是加一个方法
class MyMeta(type):
    def __new__(mcs, name, bases, ns):
        ns['greet'] = lambda self: "hello"
        return super().__new__(mcs, name, bases, ns)
```

✅ **Good:** 用 `__init_subclass__` 或 class decorator 替代简单场景  
```python
# BETTER for simple injection:
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.greet = lambda self: "hello"

# OR: use a decorator
def add_greet(cls):
    cls.greet = lambda self: "hello"
    return cls
```

**何时真正需要 metaclass / When You Actually Need It:**
- 框架级别的类注册（Django Models, SQLAlchemy）
- 需要在类创建时（非实例化时）修改类结构
- 跨继承链的 API 强制约束（如 ABC）

---

### 📚 References

- [Python Data Model — Metaclasses](https://docs.python.org/3/reference/datamodel.html#metaclasses)
- [Understanding Python Metaclasses](https://realpython.com/python-metaclasses/)
- [Django ORM Source — ModelBase metaclass](https://github.com/django/django/blob/main/django/db/models/base.py)

### 🧒 ELI5

普通类是"蓝图"，用来造对象。元类是"造蓝图的工厂"——它控制蓝图本身是怎么被创建的。Django 的 `Model` 就用了元类：当你写 `class User(Model): name = CharField()` 时，元类自动扫描所有字段、创建数据库映射，你什么都不用手动做。

A regular class is a "blueprint" for making objects. A metaclass is a "factory for blueprints" — it controls how the blueprint itself is created. Django's `Model` uses a metaclass: when you write `class User(Model): name = CharField()`, the metaclass auto-scans all fields and creates DB mappings. You do nothing manually.
