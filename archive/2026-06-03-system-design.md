# 🏗️ 系统设计 / System Design — Design an Online Code Editor (Replit)

> Day 58 · Expert Phase · ~3 min read

---

## 场景 / Scenario

想象你在设计一个在线代码编辑器，就像 Replit 或 CodeSandbox。用户打开浏览器就能写 Python、运行 JavaScript、甚至协作调试。背后的系统需要支持实时执行、文件系统、多租户隔离、以及低延迟的编辑体验。

Imagine you're designing an online code editor like Replit or CodeSandbox. Users open a browser, write Python, run JavaScript, even collaborate on debugging — all without installing anything. Behind the scenes: real-time execution, file systems, multi-tenant isolation, and low-latency editing.

---

## 核心架构 / Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Browser)                      │
│  Monaco Editor (VSCode engine) + WebSocket + WebRTC (collab)│
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS + WebSocket
┌────────────────────────────▼────────────────────────────────┐
│                      API Gateway / BFF                       │
│            auth, routing, session mgmt                       │
└──────┬─────────────────────┬──────────────────┬─────────────┘
       │                     │                  │
┌──────▼──────┐    ┌─────────▼──────┐   ┌──────▼──────────┐
│ File Service │    │ Execution Svc  │   │ Collab Service  │
│ (S3 + local  │    │ (container per │   │ (CRDTs/OT +     │
│  FS cache)   │    │  session)       │   │  Redis pub/sub) │
└──────────────┘    └────────┬───────┘   └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Container Mgr  │  ← Kubernetes/Firecracker
                    │  (microVMs)     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
         ┌────▼────┐   ┌─────▼────┐   ┌─────▼────┐
         │ Python  │   │  Node.js │   │  Go Env  │
         │ Sandbox │   │  Sandbox │   │  Sandbox │
         └─────────┘   └──────────┘   └──────────┘
```

---

## 关键设计决策 / Key Design Decisions

### 1. 代码执行隔离 / Code Execution Isolation

**问题 / Problem:** 用户代码可能恶意 (`os.system("rm -rf /")`)。  
**方案 / Solution:** 每个用户 session 跑在独立的 microVM (Firecracker) 或 gVisor sandbox 里：
- **Firecracker:** AWS 开源的轻量 VMM，启动 <125ms，内存开销 ~5MB
- **gVisor:** Google 的用户态内核，拦截 syscall，比完整 VM 轻量

```
microVM per session:
  - CPU: 0.5 vCPU (burstable)
  - Memory: 256MB–2GB (configurable)
  - Network: egress whitelist only
  - Filesystem: overlay FS (read-only base + copy-on-write layer)
  - Timeout: 30s default, 5min for paid
```

### 2. 文件持久化 / File Persistence

```
写路径 / Write Path:
  Browser → API → File Service → 
    ├── Local tmpfs (fast, per-container)
    └── S3 (durable, async flush every 5s)

读路径 / Read Path:
  New session → S3 fetch → mount into container tmpfs
```

Trade-off: tmpfs 读写极快 (μs)，但容器崩溃会丢最近 5 秒改动。可接受。

### 3. 实时协作 / Real-Time Collaboration

用 **OT (Operational Transformation)** 或 **CRDT (Conflict-free Replicated Data Types)**：
- OT: 经典方案 (Google Docs)，服务端需要序列化操作
- CRDT: 去中心化，Yjs 库，peer-to-peer 友好

Replit 实际用 **Yjs (CRDT)** + WebRTC for P2P + WebSocket fallback。

### 4. 输出流式传输 / Output Streaming

```
Container stdout/stderr → Unix pipe → 
  Execution Service → WebSocket → Browser
```

用 **Server-Sent Events (SSE)** 或 **WebSocket**，按行 flush，不等代码跑完再返回。

---

## 关键权衡 / Key Tradeoffs

| 维度 | 选择 | 原因 |
|------|------|------|
| VM vs Container | microVM (Firecracker) | 安全隔离 > 启动速度 |
| OT vs CRDT | CRDT (Yjs) | 离线支持，无需中心化排序 |
| Local FS vs S3-only | Local tmpfs + async S3 | 延迟 vs 持久性平衡 |
| 1 VM per user vs pool | Per-session VM | 隔离 > 资源效率 |

---

## 别踩这个坑 / Common Mistakes

❌ **用 Docker 做隔离** — Docker 共享 Linux kernel，namespace 逃逸有历史漏洞  
✅ microVM / gVisor 提供硬件级隔离

❌ **同步写 S3** — 每次击键都同步写 S3，延迟几百毫秒  
✅ 本地 tmpfs 写，后台定期 flush

❌ **不限制资源** — 恶意用户 `while True: pass` 耗尽 CPU  
✅ cgroups 限制 CPU/内存，watchdog 超时杀进程

❌ **单点 WebSocket 服务器** — 协作服务无法水平扩展  
✅ Redis pub/sub 或 Kafka 做消息广播，WebSocket server 无状态

---

## 📚 References

- [Firecracker: Lightweight Virtualization for Serverless - AWS](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/)
- [How Replit Works - Replit Blog](https://blog.replit.com/killing-containers-at-scale)
- [Yjs CRDT Documentation](https://docs.yjs.dev/)
- [gVisor: Container Security Sandbox - Google](https://gvisor.dev/docs/)

---

## 🧒 ELI5

就像图书馆给每个读者一个独立的小房间 📚，你可以在里面做任何事，但你出去了房间就会被清空。图书馆 (S3) 会帮你保存笔记。如果你和朋友一起在同一份文档里写东西，就像用同一块白板，两个人的涂改不会互相覆盖。

It's like a library that gives each reader their own little room. You can do anything inside, but when you leave, the room resets. The library (S3) saves your notes. Real-time collaboration is like a magical whiteboard where two people can write simultaneously without overwriting each other.
