# 🏗️ 系统设计 / System Design — Day 23
**主题 / Topic:** Design a Web Crawler
**难度 / Difficulty:** Intermediate | **阶段 / Phase:** Growth

---

## 🌐 真实场景 / Real-World Scenario

想象你在谷歌工程团队——你需要构建一个爬虫，每天抓取数十亿个网页，为搜索引擎建立索引。如何在不压垮服务器、不陷入无限循环的情况下完成这个任务？

Imagine you're on the Google engineering team — you need to build a crawler that visits billions of pages every day to build a search index. How do you do this without overwhelming servers or getting stuck in infinite loops?

---

## 🗺️ 架构图 / Architecture Diagram

```
          ┌─────────────────────────────────────────────┐
          │              Seed URLs (种子 URL)            │
          └──────────────────┬──────────────────────────┘
                             │
                             ▼
          ┌─────────────────────────────────────────────┐
          │         URL Frontier (URL 队列)              │
          │   Priority Queue (优先级队列)                │
          │   [politeness delay per domain]             │
          └──────────┬──────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   DNS Resolver      │  ← DNS 解析缓存
          │   (with cache)      │
          └──────────┬──────────┘
                     │
     ┌───────────────▼──────────────────┐
     │        Downloader Workers        │  ← 并行抓取
     │   (async, N parallel threads)   │
     └─┬───────────────────────────────┘
       │
       ├──▶ robots.txt Checker ──▶ skip if disallowed
       │
       ├──▶ Content Parser (HTML/JS)
       │        │
       │        ├──▶ Extract new URLs ──▶ URL Deduplication
       │        │                              │
       │        │                    ┌─────────▼──────────┐
       │        │                    │  Bloom Filter /    │
       │        │                    │  Seen URL Store    │
       │        │                    └─────────┬──────────┘
       │        │                              │ (not seen)
       │        │                              ▼
       │        │                       URL Frontier
       │        │
       │        └──▶ Content Storage (S3 / HDFS)
       │                    │
       └────────────────────▼
                    Indexer (离线处理)
```

---

## ⚖️ 关键权衡 / Key Tradeoffs

### 为什么这样设计？ / Why design it this way?

**1. URL 去重 — Bloom Filter vs. Hash Set**

| 方案 | 优点 | 缺点 |
|------|------|------|
| Hash Set | 准确，无误报 | 内存占用大（1B URLs ≈ 数十 GB） |
| Bloom Filter | 极低内存（~1.2 GB for 1B URLs） | 有小概率误报（漏爬少量 URL） |

**对于搜索引擎，Bloom Filter 是赢家**——偶尔漏爬一个 URL 可接受。
For a search engine, Bloom Filter wins — occasionally missing a URL is acceptable.

**2. URL 优先级 / URL Prioritization**
- PageRank 高的页面 → 优先级高
- 更新频繁的网站（新闻站）→ 更高频率重爬
- 使用**优先级队列**（多个队列，按 tier 分）

**3. Politeness（礼貌性）**
同一个域名的请求间隔 ≥ 1 秒，防止对目标网站造成 DDoS。
Enforce ≥1s delay per domain to avoid accidentally DDoS-ing sites.

---

## ❌ 别踩这个坑 / Common Mistakes

**坑 1: 忘记处理 Spider Trap（蜘蛛陷阱）**
```
example.com/page?color=red&sort=asc&page=1
example.com/page?color=red&sort=asc&page=2
... (infinite)
```
修复：URL 规范化 + 最大深度限制（e.g., depth ≤ 10）
Fix: URL normalization + max depth limit

**坑 2: 爬取重复内容**
不同 URL 可能指向相同内容（www vs non-www, http vs https）。
Use **content hash** (MD5/SHA1) to detect duplicate content even at different URLs.

**坑 3: 忽略 robots.txt**
合法爬虫必须遵守 robots.txt 协议，否则可能面临法律风险和 IP 封禁。
Legitimate crawlers MUST respect robots.txt — legal liability + IP bans otherwise.

**坑 4: 单点故障**
URL Frontier 和存储层都需要分布式、高可用设计（Kafka + distributed DB）。

---

## 📊 规模估算 / Scale Estimation

- 目标：15 亿网页 in 4 weeks
- 每秒需爬取：~6,200 pages/sec
- 存储：平均 100KB/page → **150 TB total**
- 带宽：6,200 × 100KB = **620 MB/s**

---

## 📚 References

- https://web.stanford.edu/class/cs276/handouts/lecture22-crawling.pdf
- https://www.cs.cornell.edu/courses/cs6125/2015sp/slides/crawling.pdf
- https://www.youtube.com/watch?v=BKZxZwUgL3Y (System Design Interview — Web Crawler)

---

## 🧒 ELI5

爬虫就像一个图书馆员，从一本书开始，读完后抄下所有书里提到的其他书名，然后去找那些书来读。为了不重复，他有一个小本子记下所有读过的书。为了礼貌，他每次只借一本，不一次性抢光所有书。

A web crawler is like a librarian who starts with one book, notes down all the other books it references, then goes to read those — and so on. To avoid repeats, she keeps a notebook of everything she's already read. To be polite, she only borrows one book at a time and doesn't rush the library.
