📊 NeetCode: 23/150 · SysDesign: 22/40 · Behavioral: 22/40 · Frontend: 22/50 · AI: 11/30
🔥 1-day streak!

🏗️ **系统设计 / System Design**
# 设计新闻流（Twitter / Facebook）/ Design a News Feed

## 1) 场景 / Scenario
想象你在做一个社交 App：
- 用户关注很多人
- 打开首页要看到“关注的人最新动态”（按时间倒序）
- 需要：快速打开、可无限下拉、支持发帖/删帖、支持隐私（拉黑/仅好友）

You’re building a social app:
- Users follow many accounts
- Home timeline shows recent posts from followees (reverse chronological)
- Requirements: fast load, infinite scroll, post/delete, privacy (blocks / friends-only)

---

## 2) 关键 API / Core APIs
- `POST /posts` 创建动态 / create post
- `POST /follow` 关注 / follow
- `GET /feed?cursor=...` 拉取首页流 / fetch feed
- `DELETE /posts/{id}` 删除动态 / delete

---

## 3) 两种主流方案 / Two common approaches
### A. Fanout-on-write（写入时推送）
发帖时把这条 post “复制/投递”到所有粉丝的 inbox/feed 存储。

Pros:
- 读快：`GET /feed` 只扫自己的 inbox

Cons:
- 写放大：大 V 发帖会写爆
- 需要异步队列 + 回压

### B. Fanout-on-read（读取时拉取）
读首页时：查自己关注列表 → 拉取每个关注者的最近 posts → 合并排序（k-way merge）。

Pros:
- 写轻：发帖只写一份

Cons:
- 读慢：关注很多人时合并开销大
- 需要缓存/预计算

现实里通常是 **混合**：普通用户 fanout-on-write；大 V / 名人用 fanout-on-read 或“部分推送”。

In practice it’s hybrid: push for normal users; pull (or partial push) for celebrities.

---

## 4) 推荐架构（混合）/ Suggested architecture (Hybrid)

```
          +-------------------+
Client -->|  API Gateway      |
          +---------+---------+
                    |
          +---------v---------+
          |  Feed Service     |<-------------------+
          +----+---------+----+                    |
               |         |                         |
   (read path) |         | (write path)            |
               |         v                         |
        +------v--+   +--+----------------+        |
        |  Cache  |   |  Post Service     |        |
        | (Redis) |   +--+----------------+        |
        +----+----+      |                         |
             |           v                         |
             |     +-----+------+                  |
             |     |  Post Store | (Cassandra/LSM)  |
             |     +-----+------+                  |
             |           |                         |
             |           v                         |
             |     +-----+------+      +-----------+--------+
             |     |  MQ / Log  |----->| Fanout Workers     |
             |     | (Kafka)    |      | (async push)       |
             |     +------------+      +-----------+--------+
             |                                     |
             |                                     v
             |                           +---------+--------+
             +-------------------------->|  Inbox Store      |
                                         | (per user feed)   |
                                         +------------------+
```

关键点 / Key ideas:
- **Post Store**：存权威 post（可按 authorId + time 索引）
- **Inbox Store**：每个用户一个“收件箱时间线”（只存 postId + ts + authorId）
- **MQ**：解耦发帖与推送；可重放、可扩容
- **Cache**：热点用户首页、关注列表、作者最新 posts

---

## 5) 读路径 / Read path (GET /feed)
1. 先查 Redis：是否有缓存的第一页（或 cursor 对应页）
2. 没命中：从 Inbox Store 取 `N` 条（按时间倒序），拿到 postIds
3. 批量去 Post Store / Cache 取 post 内容（MGET / batch)
4. 过滤隐私（block / friends-only）并返回

Cursor 设计：用 `(lastTimestamp, lastPostId)` 做稳定翻页，避免 offset 分页在插入/删除时乱跳。

---

## 6) 写路径 / Write path (POST /posts)
1. 写入 Post Store（生成 snowflake/UUID）
2. 投递事件到 Kafka：`PostCreated(postId, authorId, ts)`
3. Fanout worker：
   - 取 author 的 followers
   - 对普通作者：批量写入 followers 的 Inbox Store
   - 对大 V：不 fanout（只写作者自己的 “author timeline”）

---

## 7) 关键取舍 / Key tradeoffs
- **读延迟 vs 写放大**：push 读快但写爆；pull 写轻但读慢
- **一致性**：首页允许 eventual consistency（秒级延迟可接受）
- **存储成本**：inbox 只存指针（postId），否则成本爆炸
- **名人策略**：按 follower 数阈值切换策略（并动态调整）

---

## 8) 常见坑 / Common mistakes
- 只做 fanout-on-write：遇到“大 V”直接写入风暴
- Inbox 存全量 post 内容：重复数据导致存储/回填困难
- 用 offset 分页：新帖插入后翻页错乱、重复/漏读
- 忽视隐私与删除：需要支持“撤回/删除”传播（tombstone + read-time filter）

---

## 🧒 ELI5
把新闻流想成“报纸投递”：
- **推送**：作者一发文章，就把报纸送到每个订阅者门口（读很快，但送货很累）。
- **拉取**：你想看时自己去每个作者家门口拿最新报纸，再拼成一份（写很轻，但你得跑很多家）。
所以现实里：普通作者直接投递；大明星让你来取。

---

## 📚 References
- https://www.hellointerview.com/learn/system-design/answer-keys/design-twitter
- https://www.hellointerview.com/learn/system-design/answer-keys/design-facebook-news-feed
- https://kafka.apache.org/documentation/
