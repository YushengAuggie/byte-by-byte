# 🏗️ 系统设计 / System Design — Day 47
**设计地理空间系统 / Design a Geospatial System (Yelp / Nearby Friends)**
*2026-06-02 | Expert Phase*

---

## 场景 / Scenario

想象你在设计 Yelp 的"附近餐厅"功能，或者 Facebook 的"附近朋友"。用户打开 App，瞬间看到 5km 范围内的所有餐厅——背后是什么魔法？

*Imagine you're building Yelp's "nearby restaurants" feature or Facebook's "Nearby Friends." The user opens the app and instantly sees all restaurants within 5km. What's the magic behind it?*

---

## 架构图 / Architecture

```
Client (Mobile)
       │
       ▼
  API Gateway
       │
  ┌────┴────┐
  │ Location │
  │ Service │
  └────┬────┘
       │ Query: (lat, lng, radius)
       │
  ┌────▼──────────────────────────┐
  │        Geo Index Layer        │
  │                               │
  │  ┌──────────┐  ┌───────────┐  │
  │  │ Geohash  │  │  Quadtree │  │
  │  │  Index   │  │  (memory) │  │
  │  └────┬─────┘  └─────┬─────┘  │
  │       └──────┬────────┘        │
  │          Redis / PostGIS       │
  └────────────────────────────────┘
       │
  ┌────▼────┐
  │  Place   │  ← metadata (name, rating, hours)
  │    DB    │
  │(Postgres)│
  └──────────┘

[Nearby Friends variant]
  User Location → Write path:
  Client → Location Service → Redis GeoSet (GEOADD)
  
  Read path:
  Client → Location Service → GEORADIUS → User IDs → Profile Service
```

---

## 核心算法 / Core Algorithms

### 方案 1：Geohash（静态 POI，如 Yelp）
- 将地球表面编码成层级网格字符串：`9q8yy` → `9q8yy4` → `9q8yy4j`
- 精度 6 = ~1.2km 格子；精度 7 = ~150m
- **查询**：取当前 geohash + 8 个邻格，IN 查询
- **优点**：可存 DB/Redis，水平扩展容易
- **坑**：边界问题！两个相邻点可能 geohash 完全不同

```python
# Using geohash2 library
import geohash2

def nearby_places(lat, lng, radius_km, precision=6):
    center = geohash2.encode(lat, lng, precision)
    neighbors = geohash2.neighbors(center)  # 8 neighbors
    search_cells = [center] + neighbors
    
    # Query DB: SELECT * FROM places WHERE geohash LIKE ANY(search_cells)
    return search_cells
```

### 方案 2：Redis GEO（实时位置，如 Nearby Friends）
```bash
# Write: user updates location
GEOADD user_locations 116.3974 39.9093 "user:1234"

# Read: find users within 5km
GEORADIUS user_locations 116.3974 39.9093 5 km WITHCOORD COUNT 100
```
Redis 底层用 **52-bit Geohash** 存储，O(N+log(M)) 查询复杂度。

### 方案 3：Quadtree（高密度区域）
- 递归四分空间，叶节点存 POI 列表
- 适合密度不均匀（城区 vs 郊区）
- 通常 in-memory，需要 periodic rebuild

---

## 关键权衡 / Key Tradeoffs

| 维度 | Geohash + DB | Redis GEORADIUS | Quadtree |
|------|-------------|----------------|----------|
| 适合场景 | 静态 POI | 实时位置 | 复杂多边形 |
| 写频率 | 低 | 高（每隔 30s 更新） | 低 |
| 精度控制 | 通过精度位数 | 半径参数 | 递归深度 |
| 扩展性 | 水平分片 | Redis Cluster | 难分片 |

---

## 别踩这个坑 / Common Mistakes

❌ **直接用经纬度算距离**：`sqrt((lat1-lat2)² + (lng1-lng2)²)` — 经纬度不是欧氏空间，赤道 1° ≠ 极地 1°
✅ 用 **Haversine 公式** 或数据库内置 ST_Distance

❌ **不考虑边界情况**：geohash 精度 6 的格子，用户在边缘可能漏掉 50m 外的餐厅
✅ 查询中心格子 + 8 个邻格

❌ **Nearby Friends 每次全量查询所有用户**
✅ 只查询 **active users**（最近 5min 有位置更新的）+ Redis TTL 自动清理离线用户

❌ **实时位置写入过于频繁**
✅ 客户端：移动超过 50m 才上报；后端：写 Redis 而非 DB（DB 异步存历史轨迹）

---

## 📚 References
- [Geohash Wikipedia](https://en.wikipedia.org/wiki/Geohash)
- [Redis GEO Commands](https://redis.io/docs/data-types/geo/)
- [System Design: Proximity Service — Alex Xu](https://bytebytego.com/courses/system-design-interview/proximity-service)

## 🧒 ELI5

把城市地图分成很多个小格子，给每个格子取一个名字（geohash）。找附近餐厅就是：先找你所在的格子和旁边 8 个格子，然后在这 9 个格子里找餐厅——比扫描整张地图快多了！

*Imagine dividing a city map into little squares, each with a name (geohash). Finding nearby restaurants means: look in your square and the 8 squares around it. Much faster than checking the whole map!*
