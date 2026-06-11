# Day 63 — Python Craft

🐍 **Python实战 / Python Craft** · Day 63 · Design Patterns Week 4

---

## Builder Pattern — 复杂对象的分步构造 / Complex Object Construction

> **建造者模式** — 当一个对象有很多可选参数时,用链式调用分步构造,避免"望远镜式构造函数"。

---

### 场景 / Scenario

你要构造一个 HTTP 请求 / 数据库连接 / 配置对象,它有 15 个可选参数 —— 用一个 `__init__(a, b, c, d, e, f, ...)` 会变成噩梦。

---

### 核心代码 / Core Snippet

```python
from dataclasses import dataclass, field

@dataclass
class HttpRequest:
    url: str
    method: str = "GET"
    headers: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    timeout: float = 30.0

class RequestBuilder:
    def __init__(self, url: str):
        self._req = HttpRequest(url=url)

    def method(self, m: str):
        self._req.method = m
        return self                      # 返回 self → 链式调用

    def header(self, k: str, v: str):
        self._req.headers[k] = v
        return self

    def timeout(self, t: float):
        self._req.timeout = t
        return self

    def build(self) -> HttpRequest:
        return self._req

# 用法 / Usage — 可读性极佳
req = (RequestBuilder("https://api.example.com")
       .method("POST")
       .header("Authorization", "Bearer xyz")
       .header("Content-Type", "application/json")
       .timeout(10.0)
       .build())
```

---

### 猜猜输出 / Guess the Output

```python
b = RequestBuilder("http://x")
b.method("POST")          # 注意:没接着 build,也没用返回值
req = b.build()
print(req.method)
```

A) `GET`  B) `POST`  C) `None`  D) 报错

<details><summary>答案 / Answer</summary>
<b>B) POST</b> — <code>method()</code> 直接修改了内部 <code>self._req</code> 的状态。链式调用返回 self 只是为了语法糖,即使你不接住返回值,内部对象也已经被改了。这也提醒:Builder 是<b>有状态的</b>,不要复用同一个 builder 实例构造多个对象。
</details>

---

### ❌ vs ✅

```python
# ❌ 望远镜构造函数 / Telescoping constructor — 谁记得第 7 个参数是啥?
HttpRequest("http://x", "POST", {...}, {...}, 10.0)

# ✅ Builder — 自解释,可选参数随意省略
RequestBuilder("http://x").method("POST").timeout(10.0).build()
```

---

### 何时用 / When to Use

- ✅ 对象有**很多可选参数**(>4 个),且组合多变
- ✅ 构造过程需要**校验**或**分步**(先设 A 才能设 B)
- ✅ 想要**不可变最终对象** + 可变构造过程

### 何时不用 / When NOT to Use

- ❌ 参数少(2-3 个)→ 直接用 dataclass 或关键字参数,别过度设计
- ❌ Python 有 **keyword arguments + dataclass defaults**,很多场景比 Java 式 Builder 更简洁。优先用 `@dataclass` + kwargs,只在需要校验/分步/链式 DSL 时才上 Builder。

---

### 📚 References
- [Python dataclasses docs](https://docs.python.org/3/library/dataclasses.html)
- [Refactoring Guru — Builder Pattern](https://refactoring.guru/design-patterns/builder/python/example)

🧒 **ELI5:** 点汉堡的时候不用一次说完所有配料,而是一步步加:"要牛肉……加芝士……不要洋葱……好了。" 最后才把汉堡递给你。
