# 🎨 前端 / Python Craft — Day 107

> gRPC Basics — Protobuf, Streaming, vs REST

---

## 场景 / Real Scenario

你在设计一个微服务架构：订单服务需要实时推送库存更新给前端，同时服务间调用需要强类型契约。产品说 REST 够用，但 SRE 说 10K QPS 下 JSON 序列化是瓶颈。你怎么看？

You're building a microservices system: the order service needs to stream inventory updates, and inter-service calls need a typed contract. The PM says REST is fine, but SRE flags JSON serialization as a bottleneck at 10K QPS. What's your call?

---

## gRPC 是什么 / What is gRPC

gRPC 是 Google 开发的高性能 RPC 框架，基于：
- **HTTP/2**（多路复用，头部压缩）
- **Protocol Buffers**（二进制序列化，比 JSON 小 3-10x）
- **强类型 schema**（.proto 文件定义接口）

```protobuf
// inventory.proto
syntax = "proto3";

service InventoryService {
  rpc GetStock (StockRequest) returns (StockResponse);           // Unary
  rpc WatchStock (StockRequest) returns (stream StockUpdate);    // Server streaming
  rpc BatchUpdate (stream StockUpdate) returns (SummaryResponse); // Client streaming
  rpc LiveSync (stream StockUpdate) returns (stream StockUpdate); // Bidirectional
}

message StockRequest {
  string product_id = 1;
}

message StockResponse {
  string product_id = 1;
  int32 quantity = 2;
  int64 updated_at = 3;
}

message StockUpdate {
  string product_id = 1;
  int32 delta = 2;
}
```

---

## Python 实现 / Python Implementation

```python
# pip install grpcio grpcio-tools

# 生成代码: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. inventory.proto

# server.py
import grpc
from concurrent import futures
import inventory_pb2, inventory_pb2_grpc

class InventoryServicer(inventory_pb2_grpc.InventoryServiceServicer):
    def GetStock(self, request, context):
        # Unary: one request, one response
        return inventory_pb2.StockResponse(
            product_id=request.product_id,
            quantity=42,
            updated_at=1722700000
        )

    def WatchStock(self, request, context):
        # Server streaming: one request, many responses
        import time
        for i in range(5):
            yield inventory_pb2.StockUpdate(
                product_id=request.product_id,
                delta=-1
            )
            time.sleep(1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(
        InventoryServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

# client.py
def get_stock(product_id: str):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        response = stub.GetStock(
            inventory_pb2.StockRequest(product_id=product_id)
        )
        print(f"Stock: {response.quantity}")

    # Server streaming
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        for update in stub.WatchStock(
            inventory_pb2.StockRequest(product_id=product_id)
        ):
            print(f"Delta: {update.delta}")
```

---

## gRPC vs REST 决策框架 / When to Use Each

| 维度 | REST | gRPC |
|------|------|------|
| 序列化 | JSON（可读，大） | Protobuf（二进制，小3-10x） |
| 类型安全 | 无（需手动校验） | 强类型（proto 定义即契约） |
| Streaming | 有限（SSE/WebSocket） | 原生支持（4种模式） |
| 浏览器支持 | ✅ 原生 | ❌ 需 grpc-web 代理 |
| 调试 | ✅ curl/Postman | ❌ 需专用工具（grpcurl） |
| 适合场景 | 公开 API、前后端通信 | 服务间通信、高吞吐内部 API |

---

## ❌ 常见错误 vs ✅ 正确做法

❌ 对外部客户端（移动端、第三方）暴露 gRPC
```python
# 外部 API 用 gRPC = 增加客户端复杂度
```

✅ 内部微服务用 gRPC，对外 REST + gRPC-Gateway 转换
```python
# BFF 层做协议转换：外部 REST → 内部 gRPC
# grpc-gateway 可以从 proto 自动生成 REST 网关
```

---

## 🧒 ELI5

REST 就像发短信（文字，人人都懂），gRPC 就像发摩尔斯电码（更快更小，但需要解码器）。服务之间内部通话用摩尔斯电码更高效；对外跟用户说话还是用短信。

---

## 📚 References
- https://grpc.io/docs/languages/python/quickstart/
- https://protobuf.dev/programming-guides/proto3/
- https://github.com/grpc/grpc/blob/master/examples/python/
- https://grpc-ecosystem.github.io/grpc-gateway/
