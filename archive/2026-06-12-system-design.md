# Day 64 — System Design: Design a CDN from Scratch

🏗️ **系统设计 / System Design** — Design a CDN from Scratch

---

## 真实场景 / Real-World Scenario

想象你在构建一个视频平台，用户遍布全球。一个视频文件 5GB 存储在你的纽约数据中心——东京的用户每次播放都要跨越 14,000 公里的海底光纤，延迟高达 200ms+，缓冲不断。

Imagine you're building a video platform with global users. A 5GB video stored in your NYC datacenter means Tokyo users cross 14,000km of undersea fiber cables — 200ms+ latency, constant buffering.

**解决方案：内容分发网络 (CDN)**。把内容推近用户，而不是把用户拉向内容。
**Solution: Content Delivery Network (CDN)**. Push content close to users, not the other way around.

---

## 架构图 / Architecture Diagram

```
                    ┌─────────────────────────────────┐
                    │         Origin Server           │
                    │    (NYC — Source of Truth)      │
                    └──────────────┬──────────────────┘
                                   │ Cache Miss → Pull
                    ┌──────────────▼──────────────────┐
                    │      CDN Control Plane          │
                    │  (DNS routing, cache policies,  │
                    │   purge API, analytics)         │
                    └───┬─────────────┬───────────────┘
                        │             │
          ┌─────────────▼──┐    ┌─────▼──────────────┐
          │  Edge PoP: LAX │    │  Edge PoP: NRT(Tokyo)│
          │  ┌──────────┐  │    │  ┌──────────────┐   │
          │  │L1 Cache  │  │    │  │ L1 Cache     │   │
          │  │(SSD,hot) │  │    │  │(SSD, hot)    │   │
          │  └──────────┘  │    │  └──────────────┘   │
          │  ┌──────────┐  │    │  ┌──────────────┐   │
          │  │L2 Cache  │  │    │  │ L2 Cache     │   │
          │  │(HDD,warm)│  │    │  │(HDD, warm)   │   │
          │  └──────────┘  │    │  └──────────────┘   │
          └────────────────┘    └────────────────────┘
                 ▲                       ▲
           US West users           Asia-Pacific users
           ~5ms latency              ~8ms latency
```

---

## 核心组件 / Core Components

### 1. DNS 路由 / DNS Routing
当用户访问 `cdn.example.com/video.mp4`：
1. DNS 返回距离用户最近的 PoP (Point of Presence) IP
2. 基于 **Anycast** 或 GeoDNS 实现就近路由
3. TTL 设置短 (30-60s) 以支持快速故障转移

When a user requests `cdn.example.com/video.mp4`:
1. DNS returns the IP of the nearest PoP
2. Routing via **Anycast** or GeoDNS
3. Short TTL (30-60s) enables fast failover

### 2. 缓存策略 / Cache Strategy
```
Cache-Control: public, max-age=86400, stale-while-revalidate=3600
```
- **静态资源** (JS/CSS/images): 长 TTL + 内容哈希命名 (`app.a3f2bc.js`)
- **视频内容**: 按块缓存 (HLS segments, 2-10s each)
- **动态内容** (API 响应): 短 TTL 或 bypass CDN
- **Cache Key**: URL + 重要请求头 (Accept-Encoding, Accept-Language)

### 3. 缓存填充 / Cache Population
```
两种模式 / Two modes:

Pull Model (Lazy):  User Request → Cache Miss → Fetch from Origin → Cache → Serve
Push Model (Eager): Upload → CDN API → Pre-populate all edges → Serve instantly
```
- **Pull**: 适合长尾内容，按需缓存 / Good for long-tail content
- **Push**: 适合热门发布 (新专辑、大型活动) / Good for hot launches

### 4. 缓存失效 / Cache Invalidation
```bash
# Purge by URL
curl -X DELETE https://api.cdn.com/cache?url=https://cdn.example.com/image.png

# Purge by tag (bulk)
curl -X DELETE https://api.cdn.com/cache?tag=product-123
```
挑战：全球 200+ PoP，purge 传播延迟 5-30s。  
Challenge: 200+ PoPs globally, purge propagation takes 5-30s.

---

## 关键权衡 / Key Tradeoffs

| 决策 | 选项A | 选项B | 如何选 |
|------|-------|-------|--------|
| 缓存 TTL | 长 (高命中率) | 短 (内容新鲜) | 静态用长+内容哈希；动态用短 |
| Pull vs Push | 按需填充 | 预热所有边缘 | 热门内容 Push；长尾 Pull |
| 边缘计算 | 在 PoP 运行逻辑 | 回源运行逻辑 | 认证/个性化放 Edge |
| HTTPS 终止 | 在 Edge 终止 | 透传到 Origin | 在 Edge 终止：降延迟 |

---

## 别踩这个坑 / Common Mistakes

**❌ 忘记 Vary 头**
```http
# 没有 Vary: Accept-Encoding
# 压缩版本和非压缩版本共用同一缓存 key → 部分用户收到乱码
Vary: Accept-Encoding
```

**❌ 缓存含用户数据的 API 响应**
```
# 错误：用户特定数据被公开缓存
Cache-Control: public, max-age=300  ← 危险！包含用户 ID

# 正确：
Cache-Control: private, max-age=60   ← 只在用户浏览器缓存
```

**❌ 单点 Origin 导致 CDN 全量回源时雪崩**  
解法：Origin 也要部署在多个区域，CDN 回源时就近选择。

---

## 📚 References
- https://www.cloudflare.com/learning/cdn/what-is-a-cdn/
- https://aws.amazon.com/cloudfront/features/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control

## 🧒 ELI5
CDN 就像麦当劳的供应链：总部 (Origin) 做好配方，全球门店 (Edge PoP) 就近备好食材。北京的顾客不用飞到美国总部点汉堡——最近的门店直接出餐。

CDN is like McDonald's supply chain: HQ (Origin) creates the recipe, local franchises (Edge PoPs) stock the ingredients nearby. Beijing customers don't fly to US HQ for a burger — the nearest store serves them instantly.
