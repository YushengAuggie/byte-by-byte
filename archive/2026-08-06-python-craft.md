# 🎨 前端 / Python Craft — Day 109
## DNS Resolution in Python — socket.getaddrinfo

---

### 🌍 真实场景 / Real-World Scenario

你在做一个服务健康检查系统，需要验证域名是否能正确解析、解析到哪些 IP，以及同时支持 IPv4 和 IPv6。你的同事直接用 `socket.gethostbyname()`，但在生产环境遇到了只返回一个 IP、IPv6 不支持的问题。

*Building a service health checker: you need to verify domain resolution, which IPs it resolves to, and support both IPv4/IPv6. Your colleague used `socket.gethostbyname()` but hit production issues — only one IP returned, no IPv6 support.*

---

### 🐛 常见错误 → 正确做法 / Common Mistake → Correct Approach

```python
# ❌ Bad: gethostbyname only returns one IPv4 address
import socket
ip = socket.gethostbyname("google.com")
print(ip)  # "142.250.80.46" — misses ALL other IPs and IPv6

# ✅ Good: getaddrinfo returns all address info
import socket

results = socket.getaddrinfo(
    "google.com",  # host
    443,           # port (0 for any)
    socket.AF_UNSPEC,       # address family: both IPv4 and IPv6
    socket.SOCK_STREAM,     # socket type: TCP
)

for family, type_, proto, canonname, sockaddr in results:
    addr, port = sockaddr[0], sockaddr[1]
    family_name = "IPv4" if family == socket.AF_INET else "IPv6"
    print(f"{family_name}: {addr}:{port}")

# Output:
# IPv4: 142.250.80.46:443
# IPv4: 142.250.80.142:443
# IPv6: 2607:f8b0:4004:c08::8a:443
# IPv6: 2607:f8b0:4004:c08::66:443
```

---

### 🏗️ 实用封装 / Production-Ready Wrapper

```python
import socket
from dataclasses import dataclass
from typing import Literal

@dataclass
class DNSRecord:
    family: Literal["IPv4", "IPv6"]
    address: str
    port: int

def resolve_dns(
    hostname: str,
    port: int = 0,
    family: socket.AddressFamily = socket.AF_UNSPEC,
) -> list[DNSRecord]:
    """
    Resolve hostname to all matching addresses.
    
    Args:
        hostname: Domain name to resolve
        port: Port hint (0 = any)
        family: AF_INET (IPv4 only), AF_INET6 (IPv6 only), AF_UNSPEC (both)
    """
    try:
        results = socket.getaddrinfo(hostname, port, family, socket.SOCK_STREAM)
    except socket.gaierror as e:
        raise ValueError(f"DNS resolution failed for {hostname}: {e}")
    
    records = []
    seen = set()
    for af, *_, sockaddr in results:
        addr = sockaddr[0]
        if addr not in seen:
            seen.add(addr)
            records.append(DNSRecord(
                family="IPv4" if af == socket.AF_INET else "IPv6",
                address=addr,
                port=sockaddr[1],
            ))
    return records

# Usage:
records = resolve_dns("google.com", port=443)
for r in records:
    print(f"  {r.family}: {r.address}:{r.port}")
```

---

### 🔍 getaddrinfo 返回值解析 / Return Value Breakdown

```python
# socket.getaddrinfo returns list of 5-tuples:
# (family, type, proto, canonname, sockaddr)
#
# family:    AF_INET (2) = IPv4, AF_INET6 (10) = IPv6
# type:      SOCK_STREAM (TCP), SOCK_DGRAM (UDP)
# proto:     protocol number (usually 6=TCP, 17=UDP)
# canonname: canonical name (only when AI_CANONNAME flag set)
# sockaddr:  (address, port) for IPv4
#            (address, port, flowinfo, scopeid) for IPv6
```

---

### ⚡ 高级用法 / Advanced: DNS Round-Trip Time

```python
import socket
import time

def dns_latency(hostname: str, samples: int = 3) -> float:
    """Measure average DNS lookup time in milliseconds."""
    times = []
    for _ in range(samples):
        start = time.perf_counter()
        socket.getaddrinfo(hostname, 0)
        times.append((time.perf_counter() - start) * 1000)
    return sum(times) / len(times)

print(f"google.com DNS latency: {dns_latency('google.com'):.1f}ms")
```

---

### 📊 When to Use / When NOT to Use

| Use `getaddrinfo` | Use alternatives |
|-------------------|-----------------|
| Need both IPv4+IPv6 | Need async DNS → `aiodns` |
| Need all IPs for a domain | Need DNS record types (MX, TXT) → `dnspython` |
| Health checks | Need DNSSEC validation → `unbound` |
| Connecting to servers | Need DNS-over-HTTPS → `httpx` + DoH endpoint |

---

### 📚 References
- https://docs.python.org/3/library/socket.html#socket.getaddrinfo
- https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts
- https://pypi.org/project/dnspython/

### 🧒 ELI5
`gethostbyname` 就像问"google.com 住哪里？"，只给你一个地址。`getaddrinfo` 就像问"google.com 所有的门牌号都给我"，还告诉你哪些是普通地址(IPv4)，哪些是新式地址(IPv6)。
*`gethostbyname` = "where does google.com live?" (one answer). `getaddrinfo` = "give me ALL addresses for google.com" including both old-style (IPv4) and new-style (IPv6) addresses.*
