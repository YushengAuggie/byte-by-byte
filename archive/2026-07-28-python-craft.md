# 🎨 Python Craft — Day 42: Serialization — JSON, msgpack, pickle, protobuf

**Category:** Data & Performance | **Week 11** | **Phase:** Expert

---

## 为什么序列化很重要 / Why Serialization Matters

你在构建一个微服务平台，服务间需要传递复杂的 Python 对象。选错序列化方案会导致：
- 性能瓶颈（高吞吐场景慢 10x）
- 跨语言兼容问题
- 安全漏洞（pickle 反序列化攻击）
- 版本兼容噩梦

You're building a microservices platform. Choosing the wrong serialization can create 10x performance bottlenecks, security vulnerabilities, or versioning nightmares.

---

## 四种方案对比 / Four Approaches

```python
import json
import pickle
import msgpack
# pip install msgpack protobuf

data = {
    "user_id": 12345,
    "name": "Yusheng",
    "scores": [98, 87, 95, 100],
    "active": True
}

# ─── 1. JSON ───────────────────────────────────────
# Human-readable, universal, but slow and verbose
json_bytes = json.dumps(data).encode("utf-8")
# Size: ~80 bytes, any language can read it

# ─── 2. msgpack ────────────────────────────────────
# pip install msgpack
# Binary JSON — 2-4x faster, 20-40% smaller
msgpack_bytes = msgpack.packb(data, use_bin_type=True)
# Size: ~50 bytes, still schema-less

# ─── 3. pickle ─────────────────────────────────────
# Python-native, can serialize ANYTHING
# ⚠️ NEVER unpickle untrusted data (code execution)
pickle_bytes = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
# Size: ~100 bytes, Python-only

# ─── 4. protobuf ───────────────────────────────────
# Schema-first, strongly typed, fastest at scale
# Define schema in .proto file, generate Python classes
# Size: ~30 bytes, any language, schema enforced

# Quick benchmark comparison:
import timeit
import sys

print(f"JSON size:    {len(json_bytes)} bytes")
print(f"msgpack size: {len(msgpack_bytes)} bytes")
print(f"pickle size:  {sys.getsizeof(pickle_bytes)} bytes")
```

---

## 性能实测 / Performance Benchmark

```python
import timeit

n = 100_000

json_time = timeit.timeit(
    lambda: json.dumps(data), number=n
)
msgpack_time = timeit.timeit(
    lambda: msgpack.packb(data, use_bin_type=True), number=n
)

print(f"JSON:    {json_time:.3f}s for {n} ops")
print(f"msgpack: {msgpack_time:.3f}s for {n} ops")
# Typical: msgpack is 2-3x faster than json
```

---

## 决策框架 / When to Use What

```
需要人类可读 / debugging / REST API?
  → JSON ✅

跨语言通信，需要 schema 验证，高吞吐？
  → Protobuf ✅ (gRPC 默认)

Python 内部缓存 / 短期任务队列？
  → msgpack (安全) 或 pickle (仅限受信任数据)

⚠️ 危险区 / NEVER DO:
  - unpickle(redis.get("user_data"))  # 如果 Redis 被攻破
  - pickle.loads(request.body)        # RCE 漏洞！
```

---

## ❌ 常见错误 vs ✅ 正确做法

```python
# ❌ 错误：pickle 序列化用户输入的数据存到 Redis
import redis
r = redis.Redis()
user_object = get_user_from_request()
r.set("user:123", pickle.dumps(user_object))  # 危险！

# ✅ 正确：JSON 或 msgpack 用于外部数据
import json
r.set("user:123", json.dumps(user_object.__dict__))

# ✅ 高性能内部服务用 msgpack
r.set("user:123", msgpack.packb(user_object.__dict__, use_bin_type=True))
```

---

## Protobuf 快速入门 / Protobuf Quickstart

```protobuf
// user.proto
syntax = "proto3";
message User {
  int32 user_id = 1;
  string name = 2;
  repeated int32 scores = 3;
  bool active = 4;
}
```

```python
# After: protoc --python_out=. user.proto
from user_pb2 import User

user = User(user_id=12345, name="Yusheng", 
            scores=[98, 87, 95], active=True)
proto_bytes = user.SerializeToString()
# ~30 bytes, strongly typed, backward compatible
```

---

## 总结 / Summary

| 方案 | 速度 | 大小 | 跨语言 | 安全 | 使用场景 |
|------|------|------|--------|------|---------|
| JSON | ⭐⭐ | ⭐⭐ | ✅ | ✅ | REST API, 调试 |
| msgpack | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ | 内部服务, 缓存 |
| pickle | ⭐⭐⭐ | ⭐⭐⭐ | ❌ | ⚠️ | Python 任务队列 |
| protobuf | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ | gRPC, 高吞吐 |

---

## 📚 References

- [Python msgpack docs](https://msgpack-python.readthedocs.io/)
- [Protocol Buffers Python Tutorial](https://protobuf.dev/getting-started/pythontutorial/)
- [Python pickle security warning](https://docs.python.org/3/library/pickle.html#restricting-globals)

## 🧒 ELI5

序列化就是把 Python 字典"打包"成快递箱，发给另一台服务器。  
- JSON = 用纸盒，人人都能开  
- msgpack = 用泡沫箱，更小更快  
- pickle = 用魔法箱，只有 Python 能开，如果邮差是坏人会爆炸  
- protobuf = 用定制模具，最紧凑，但要先定义模具形状

Serialization is packing your Python objects into a box to ship across the network. JSON is a cardboard box (universal), msgpack is a foam box (smaller, faster), pickle is a magic box (Python-only, dangerous from strangers), and protobuf is a custom mold (smallest, fastest, but needs a schema first).
