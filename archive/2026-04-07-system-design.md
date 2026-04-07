# 🏗️ 系统设计 / System Design — Day 19
**Topic:** Design a URL Shortener (TinyURL)
**Date:** 2026-04-07

---

🏗️ **系统设计 / System Design**

**设计一个短链接服务（TinyURL）**
**Design a URL Shortener (TinyURL)**

---

### 🌍 真实场景 / Real-World Scenario

想象你在 Twitter（现 X）工作。每条推文最多 280 字，但一个普通的 YouTube 链接就能占掉 60 个字符。你的任务：把 `https://www.youtube.com/watch?v=dQw4w9WgXcQ` 变成 `https://tinyurl.com/abc123`。

*Imagine you're at Twitter (now X). Tweets are 280 chars, but a YouTube URL alone takes 60. Your job: turn `https://www.youtube.com/watch?v=dQw4w9WgXcQ` into `https://tinyurl.com/abc123`.*

**功能需求 / Functional Requirements:**
- 给一个长 URL，生成唯一短链接
- 访问短链接，重定向到原始 URL
- 短链接可配置过期时间（可选）

**非功能需求 / Non-Functional:**
- 100M 短链/天（写操作）
- 读写比约 10:1（10亿次重定向/天）
- 链接可用 5 年（可用 → 高可用）
- P99 重定向延迟 < 50ms

---

### 🏛️ 架构图 / Architecture Diagram

```
Client
  │
  ▼
[Load Balancer]
  │              │
  ▼              ▼
[App Server]  [App Server]   ← stateless, horizontally scalable
  │
  ├──► [Cache (Redis)]  ← 短链 → 长链，命中率 ~95%
  │          │ miss
  ▼          ▼
[Primary DB (PostgreSQL)] ──► [Read Replicas × 3]
  │
  ▼
[ID Generator Service]   ← 独立发号器（雪花算法 or 自增）
```

**核心表结构 / Core Schema:**
```sql
CREATE TABLE url_mappings (
  short_code  VARCHAR(7) PRIMARY KEY,   -- e.g. "abc123f"
  long_url    TEXT NOT NULL,
  created_at  TIMESTAMP DEFAULT NOW(),
  expires_at  TIMESTAMP,
  user_id     BIGINT
);
CREATE INDEX idx_short_code ON url_mappings(short_code);
```

---

### ⚙️ 关键设计决策 / Key Design Decisions

**1. 如何生成短码？ / How to generate short codes?**

方案A — **Base62 编码**（推荐）：
```
62^7 = 3.5 万亿种组合 ≈ 足够用 100 年
```
- 用自增 ID（如 `1234567`) → Base62 编码 → `"b8Xk2mP"`
- 优点：无碰撞，ID 顺序保证短码唯一
- 缺点：短码可预测（可加随机盐）

方案B — **MD5 哈希截取**：
- 取 URL 的 MD5 前 7 位
- 问题：**哈希碰撞**，不同 URL 可能得到相同短码

```python
import base62  # pip install pybase62

def shorten(long_url: str, auto_increment_id: int) -> str:
    # Convert unique auto-increment ID to base62
    return base62.encodebytes(auto_increment_id.to_bytes(8, 'big')).decode()[-7:]

# Example: ID 1000000 → "4c92"... → take last 7 chars
```

**2. 重定向类型 / Redirect Type:**
- `301 Permanent`：浏览器缓存，减服务器压力，但无法统计点击数
- `302 Temporary`：每次必过服务器，可精确统计 → **大多数短链服务用 302**

**3. 缓存策略 / Caching:**
- Redis 存储 `shortCode → longURL`，TTL = 24h
- 读写比 10:1，缓存命中率可达 95%+
- LRU 策略驱逐不热门的链接

---

### ⚠️ 别踩这个坑 / Common Mistakes

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| 用 MD5 哈希直接截取，不处理碰撞 | 用自增 ID + Base62，或哈希时加碰撞检测 |
| 短码暴露自增 ID（可遍历所有链接） | Base62 编码后加随机偏移或加盐 |
| 重定向用 301（无法统计点击） | 根据需求选 301/302；统计场景用 302 |
| 单点 ID 生成器（性能瓶颈） | 用 Snowflake 分布式 ID 或数据库自增分段 |
| 忘记过期清理（磁盘无限增长） | 定时任务 + TTL 字段清理过期链接 |

---

### 📊 容量估算 / Capacity Estimation

```
写：100M 短链/天 ÷ 86400s ≈ 1160 QPS
读：1B 重定向/天 ÷ 86400s ≈ 11600 QPS
存储：每条记录约 500 bytes × 100M/天 × 365天 × 5年 ≈ 91 TB
```

---

### 📚 参考资料 / References

1. [System Design Interview: URL Shortener — Alex Xu](https://bytebytego.com/courses/system-design-interview/design-a-url-shortener)
2. [How TinyURL Works — High Scalability](http://highscalability.com/blog/2021/4/27/how-should-i-store-the-short-links-in-the-database.html)
3. [Base62 Encoding Explained — GeeksForGeeks](https://www.geeksforgeeks.org/url-shortening-service-using-base62-encoding/)

---

### 🧒 ELI5（用小学生能懂的方式解释）

想象你有一本很厚的字典，每本字典有一个编号。你把网址存进字典，给它一个编号（比如第 12345 条）。然后你把 12345 翻译成一串奇怪的字母（比如 "abcXY"）。别人访问 "abcXY" 时，你查字典找到 12345，再找到原来的网址，带他过去。这就是短链接！

*Imagine a big dictionary. Every URL gets a unique page number (12345). You translate that number into a short code ("abcXY"). When someone visits "abcXY", you look up 12345 in your dictionary, find the original URL, and send them there. That's it!*
