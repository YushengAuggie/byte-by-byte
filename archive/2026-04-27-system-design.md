# 🏗️ 系统设计 / System Design — Day 32

**主题 / Topic:** Design Google Maps  
**难度 / Difficulty:** Advanced | **阶段 / Phase:** Mastery  
**预计阅读 / Read time:** ~3 分钟

---

## 🌍 想象你在设计 Google Maps...

你需要支持 **10亿用户** 实时导航、路线规划、地图渲染，还要处理交通状况更新。  
You need to support **1B users** doing real-time navigation, route planning, map rendering, and live traffic updates.

这不只是"存地图数据"那么简单——挑战在于数据量庞大、实时性要求高、以及地理空间查询的复杂性。  
It's not just "store map data" — the challenge is massive data volume, real-time requirements, and complex geospatial queries.

---

## 🏛️ 架构图 / Architecture

```
[Mobile/Web Client]
        |
   [CDN / Tile Cache]   ← 静态地图瓦片 / Static map tiles
        |
   [API Gateway]
   /     |      \
[Route  ] [Search] [Traffic]
[Service] [Service] [Service]
   |         |          |
[Graph DB] [Geo Index] [Stream]
[Roads]   [POI/Places] [Kafka]
              |              |
         [PostGIS]    [Real-time
        [S3 Tiles]    Aggregator]
              |
         [Data Lake]
         (OpenStreetMap
          + fleet GPS)
```

---

## 🔑 核心设计决策 / Key Design Decisions

### 1. 地图瓦片系统 / Map Tile System

地图按 **Mercator 投影** 切割为 256×256 瓦片，按 zoom level (0-20) 分层存储。  
Maps are sliced into 256×256 tiles using Mercator projection, stored per zoom level.

```
Zoom 0 = 1 tile (whole world)
Zoom 10 = 1M tiles (city level)
Zoom 18 = 68B tiles (street level)
```

**存储策略 / Storage:** S3 + CloudFront CDN  
瓦片是静态资源，CDN 命中率 >95%，极大减少源服务器压力。  
Tiles are static assets — >95% CDN hit rate massively reduces origin load.

### 2. 路线规划 / Routing Engine

使用 **Dijkstra / A\*** 算法，但直接跑整个地图不现实（节点太多）。  
Pure Dijkstra on the full map is infeasible (too many nodes).

**解决方案 / Solution: Hierarchical Routing (CH — Contraction Hierarchies)**

```
Level 3: Highways (interstate)     ← 长途优先走这层
Level 2: Major roads (city)         ← 城际
Level 1: Local streets              ← 最后一公里
```

先在高层图快速找大方向，再在低层补充细节——搜索空间缩小 1000x。  
Search at high levels for direction, detail at low levels — 1000x smaller search space.

### 3. 实时交通 / Real-Time Traffic

**数据来源 / Sources:**
- 匿名 GPS 轨迹（手机上报）/ Anonymous GPS traces from phones
- 事故/施工报告 / Incident reports
- 历史交通模式 / Historical traffic patterns

**架构:**
```
GPS probes → Kafka → Stream Processor → Edge Weight Updates
                                      → Route Re-calculation
```

每条路的"边权重"代表当前行驶时间，每 1-5 分钟更新一次。  
Each road edge weight = current travel time, updated every 1-5 min.

### 4. 地理索引 / Geo-Spatial Indexing

搜索"附近的星巴克"需要高效的地理查询。  
"Find Starbucks nearby" needs efficient geo queries.

**方案 / Approach: Geohash + R-Tree (PostGIS)**

```python
# Geohash: encode lat/lng as string prefix
# "9q8yy..." = San Francisco downtown
# Nearby = same prefix → O(1) bucket lookup
import geohash
loc = geohash.encode(37.7749, -122.4194, precision=6)
# "9q8yy4" → search "9q8yy*" for neighbors
```

---

## ⚖️ 权衡 / Key Tradeoffs

| 决策 / Decision | 方案 A | 方案 B | 选择理由 / Why |
|---|---|---|---|
| 路线算法 | Dijkstra (simple) | Contraction Hierarchies | 性能 / Performance |
| 地图存储 | 矢量 Vector | 栅格瓦片 Raster | CDN 可缓存 / Cacheable |
| 交通更新 | Pull (客户端轮询) | Push (WebSocket) | 节省带宽 / Bandwidth |
| 地理索引 | PostGIS | Custom Quadtree | 成熟度 / Maturity |

---

## ⚠️ 别踩这个坑 / Common Mistakes

**❌ 坑 1:** 把路线规划做成单体服务  
路线计算 CPU 密集，必须独立扩展。  
Route computation is CPU-heavy — must scale independently.

**❌ 坑 2:** 忽略地图数据更新  
路网每天都在变（新路、施工），需要 ETL pipeline 定期从 OpenStreetMap 导入。  
Road networks change daily — need ETL from OpenStreetMap.

**❌ 坑 3:** 以为实时交通只需要快速存储  
真正的挑战是 **数据新鲜度 vs 系统负载** 的权衡——更新太频繁会压垮路由服务。  
Real challenge is freshness vs load — too-frequent updates overwhelm routing.

---

## 📊 容量估算 / Capacity Estimates

```
DAU: 1B users
Requests: ~10B/day (navigation + search + tile loads)
Map tile storage: ~100TB (all zoom levels, global)
GPS traces ingest: ~5M events/second peak
Route cache: Redis, 15-min TTL, ~1TB hot data
```

---

## 📚 References

- https://www.uber.com/blog/engineering/h3/ — Uber H3 hexagonal geo-indexing
- https://www.openstreetmap.org/ — OpenStreetMap (the data behind many map services)
- https://docs.mapbox.com/help/glossary/vector-tiles/ — Mapbox vector tiles explained
- https://en.wikipedia.org/wiki/Contraction_hierarchies — Contraction Hierarchies routing

---

## 🧒 ELI5

想象地图是一本超大的图画书，按放大倍数分成很多小页（瓦片）。你想要什么页，服务器就给你发什么页——大部分页都缓存好了，超级快。找路就像在地铁图上先找大站，再找小站，而不是一步一步数路口。  
Imagine the map is a huge picture book split into tiny pages (tiles) by zoom level. You ask for the page you need, and the server sends it — most pages are already cached, so it's super fast. Finding a route is like finding big subway stations first, then small stops — not counting every intersection one by one.
