# 🏗️ 系统设计 Day 2 / System Design Day 2
**Topic: DNS, IP, and TCP/UDP — 互联网的"电话本"与"快递公司"**

---

## 场景引入 / Scenario

想象你在设计一个全球用户访问的网站。你写了 `https://myblog.com`，浏览器是怎么找到你服务器的？从你按下 Enter 到页面出现，背后发生了什么魔法？

*Imagine you're building a website for global users. You type `https://myblog.com` — how does your browser find your server? What magic happens between pressing Enter and seeing the page?*

---

## DNS：互联网的电话本 / DNS: The Internet's Phone Book

人类记得 `google.com`，机器只认识 `142.250.80.46`。DNS（Domain Name System）就是把"人话"翻译成"机器话"的翻译官。

*Humans remember `google.com`, machines only understand `142.250.80.46`. DNS translates human-readable names into machine-readable IPs.*

### DNS 查询流程 / DNS Resolution Flow

```
你的浏览器
    │
    ▼
[1] 本地缓存 / Local Cache
    │  (找到了? 直接返回 / Found? Return immediately)
    │  (没找到? 继续 / Not found? Continue)
    ▼
[2] 操作系统 hosts 文件 / OS hosts file
    │  (/etc/hosts on Linux/Mac)
    ▼
[3] 递归解析器 / Recursive Resolver
    │  (通常是你的 ISP 或 8.8.8.8)
    │  (Usually your ISP or 8.8.8.8)
    ▼
[4] 根域名服务器 / Root Nameserver
    │  ("我不知道 myblog.com，但 .com 服务器知道")
    │  ("I don't know myblog.com, but .com nameserver does")
    ▼
[5] TLD 服务器 / TLD Nameserver (.com)
    │  ("myblog.com 的权威服务器在这里")
    │  ("myblog.com's authoritative server is here")
    ▼
[6] 权威 DNS 服务器 / Authoritative Nameserver
    │  "myblog.com → 203.0.113.42"
    ▼
IP 地址返回给浏览器 / IP returned to browser
```

**真实类比 / Real-world analogy:**
根服务器 = 全国电话总机 → TLD 服务器 = 城市区号本 → 权威服务器 = 某公司的直线
*Root server = National operator → TLD = City directory → Authoritative = Company's direct line*

---

## IP：你在网络上的"门牌号" / IP: Your Network "Address"

- **IPv4**: `203.0.113.42` — 32位，约43亿个地址，已经快用完了
- **IPv6**: `2001:0db8:85a3::8a2e:0370:7334` — 128位，几乎无限

*IPv4 is 32-bit (~4.3 billion addresses, nearly exhausted). IPv6 is 128-bit, essentially unlimited.*

**公网 vs 私网 / Public vs Private IP:**
```
家庭网络 / Home Network:
  你的电脑      → 192.168.1.100 (私网/Private)
  你的手机      → 192.168.1.101 (私网/Private)
  路由器对外    → 203.0.113.42  (公网/Public)  ← 互联网只看到这个
                                                  ← Internet only sees this
NAT（网络地址转换）帮你把私网地址映射到公网
NAT (Network Address Translation) maps private to public
```

---

## TCP vs UDP：快递公司 vs 广播电台

| 特性 / Feature | TCP | UDP |
|---|---|---|
| 连接方式 / Connection | 三次握手 / 3-way handshake | 无连接 / Connectionless |
| 可靠性 / Reliability | ✅ 保证送达 / Guaranteed | ❌ 尽力而为 / Best-effort |
| 顺序 / Order | ✅ 有序 / Ordered | ❌ 可能乱序 / May arrive out of order |
| 速度 / Speed | 较慢 / Slower | 更快 / Faster |
| 适用场景 / Use cases | HTTP, Email, File transfer | Video streaming, Gaming, DNS |

### TCP 三次握手 / TCP 3-Way Handshake

```
客户端 / Client          服务器 / Server
     │                        │
     │──── SYN ──────────────>│  "我想连接你 / I want to connect"
     │                        │
     │<─── SYN-ACK ───────────│  "好的，收到 / OK, received"
     │                        │
     │──── ACK ──────────────>│  "我也确认了 / Confirmed"
     │                        │
     │══════ 连接建立 / Connection Established ══════│
```

**为什么需要3次？/ Why 3 handshakes?**
2次不够——服务器无法确认客户端收到了回复。就像打电话："喂？" "喂，听到了吗？" "听到了，开始说吧。"
*2 isn't enough — the server can't confirm the client received its reply. Like a phone call: "Hello?" "Hello, can you hear me?" "Yes, go ahead."*

---

## 为什么这样设计？/ Why This Design?

**DNS 分层设计的好处 / Benefits of hierarchical DNS:**
- **可扩展性**: 根服务器只有13个，但全球有数十亿个域名
- **缓存**: 每层都可以缓存，减少重复查询
- **容错**: 多个根服务器，一个挂了其他继续工作

*Scalability (13 root servers handle billions of domains via delegation), caching at every layer, and fault tolerance through redundancy.*

---

## 别踩这个坑 / Don't Fall Into This Trap

**坑1: DNS 缓存污染面试题**
面试问："为什么我改了 DNS 记录，但用户还是访问旧服务器？"
答：TTL（Time To Live）没过期。DNS 记录有缓存时间，改了之后要等 TTL 归零才会全面生效。**上线前提前降低 TTL！**

*DNS cache: after changing DNS records, users still hit old servers until TTL expires. Best practice: lower TTL hours before a migration.*

**坑2: TCP 不等于安全**
TCP 保证送达，但不加密。`http://` 用 TCP，但数据是明文。需要加密要用 TLS（即 `https://`）。

*TCP guarantees delivery, not security. HTTP over TCP is plaintext. TLS (HTTPS) is needed for encryption.*

---

## 关键要点 / Key Takeaways

1. **DNS** = 域名 → IP 的翻译，分层设计，有缓存
2. **IPv4** 快用完了，**IPv6** 是未来
3. **TCP** = 可靠但慢（文件、网页）；**UDP** = 快但不可靠（直播、游戏）
4. 三次握手确保双向通信可靠建立

*DNS translates domains to IPs with hierarchical caching. IPv4 is nearly exhausted, IPv6 is the future. TCP = reliable but slower; UDP = fast but lossy. 3-way handshake ensures both ends can send and receive.*

---
*Day 2 of 100 | #ByteByByte | 系统设计基础系列*
