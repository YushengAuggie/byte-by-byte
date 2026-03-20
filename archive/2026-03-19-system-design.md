🏗️ **系统设计 Day 6 / System Design Day 6**
**CDN (Content Delivery Network) — 内容分发网络**

---

**想象你在设计... / Imagine You're Building...**

你在上海开了一家咖啡豆网店，客户遍布全球。每次有人从纽约访问你的网站，请求要飞越太平洋到上海服务器取图片、CSS、JS，再飞回去。往返 200ms+，用户等得花都谢了 🌸。

解决方案？在纽约、伦敦、东京都放一份你网站的静态资源副本。用户访问时，就近取货。

这就是 **CDN（内容分发网络）**。

You run a coffee bean shop in Shanghai with global customers. Every request from NYC flies across the Pacific and back — 200ms+ round trip. Solution? Cache copies of your static assets in NYC, London, Tokyo. Users get served from the nearest copy. That's a **CDN**.

---

**架构图 / Architecture Diagram**

```
                     用户请求 User Request
                           │
                     ┌──────┴──────┐
                     │  DNS 解析    │
                     │ (返回最近的  │
                     │  CDN 节点)   │
                     └──────┬──────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌──────────┐       ┌──────────┐       ┌──────────┐
  │ CDN Edge │       │ CDN Edge │       │ CDN Edge │
  │  纽约    │       │  伦敦    │       │  东京    │
  │ ████████ │       │ ████     │       │ ██████   │
  │ (cached) │       │ (cached) │       │ (cached) │
  └────┬─────┘       └────┬─────┘       └────┬─────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │ cache miss 时回源
                           ▼
                    ┌──────────────┐
                    │ Origin Server│
                    │  源站 (上海)  │
                    └──────────────┘
```

---

**核心概念 / Key Concepts**

**1. Cache Hit vs Cache Miss**
- **Hit（命中）：** CDN 节点有缓存 → 直接返回，超快（< 50ms）
- **Miss（未命中）：** CDN 没有 → 回源站取，存一份，下次就 Hit 了

**2. TTL (Time To Live)**
- 缓存过期时间。太短 → 频繁回源；太长 → 用户看到旧内容
- 静态资源（图片/CSS/JS）：TTL 长（1天-1年），文件名带 hash（`app.a3f2b1.js`）
- API 响应：TTL 短（几秒-几分钟）或不缓存

**3. Cache Invalidation（缓存失效）**
- 发布新版本时需要清除旧缓存
- 方法 1：Purge API（主动清除指定 URL）
- 方法 2：文件名 hash（新版本 = 新文件名 = 自动绕过旧缓存）✅ 推荐

**4. Push vs Pull CDN**
- **Pull：** CDN 节点在第一次请求时从源站拉取（大多数 CDN 默认行为）
- **Push：** 你主动上传内容到 CDN（适合大文件、已知内容）

---

**别踩这个坑 / Don't Fall Into This Trap**

❌ 把带用户个人信息的 API 响应（如 `/api/me`）也放 CDN 缓存
→ 用户 A 看到用户 B 的数据！

✅ 只缓存公开、不含个人信息的内容。私有内容设 `Cache-Control: private, no-store`。

⚠️ CDN 缓存了错误的 response（比如 500 错误页面）
→ 设置：只缓存 2xx 响应，或设置很短的负缓存 TTL

⚠️ 源站宕机时 CDN 还能服务（这是优点！）但如果 TTL 过了且源站还没恢复 → "stale-while-revalidate" 策略可以继续用旧缓存

---

**面试要点 / Interview Key Points**

1. CDN 降低延迟（地理距离）+ 减轻源站压力
2. 适合静态资源；动态内容需要谨慎（考虑 Edge Computing）
3. 常见 CDN：CloudFront (AWS), Cloudflare, Akamai, Fastly
4. CDN + Load Balancer + Cache = 高性能系统的三驾马车

---

*Day 6 / 150 — 系统设计基础系列*
