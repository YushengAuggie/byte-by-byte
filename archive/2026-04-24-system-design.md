# 🏗️ 系统设计 / System Design — Day 26: Design YouTube / Netflix (Video Streaming)

> **阶段 / Phase:** Mastery | **难度 / Difficulty:** Advanced | **阅读时间 / Read time:** ~3 min

---

## 场景 / Scenario

想象你在设计 YouTube。每天有 500 小时的视频被上传，20 亿用户在观看。你如何让全球每个人都能流畅播放一段 4K 视频，而不是等 buffering 圈圈转个不停？

You're designing YouTube. 500 hours of video uploaded every minute, 2 billion users watching. How does every person on earth get buttery-smooth 4K playback without staring at a buffering spinner?

---

## 架构图 / Architecture Diagram

```
                    ┌────────────────────────────────────┐
                    │         Content Creator             │
                    └───────────────┬────────────────────┘
                                    │ Upload (raw video)
                                    ▼
                    ┌────────────────────────────────────┐
                    │    Upload Service (chunked HTTP)    │
                    │    → Object Storage (raw: S3/GCS)   │
                    └───────────────┬────────────────────┘
                                    │ trigger
                                    ▼
            ┌────────────────────────────────────────────────┐
            │         Transcoding Pipeline (async)            │
            │  • Split → Transcode (360p/720p/1080p/4K)       │
            │  • Audio normalization                          │
            │  • Thumbnail generation                         │
            │  → CDN-ready segments (HLS/DASH chunks)         │
            └───────────────────┬────────────────────────────┘
                                │ writes
                                ▼
                   ┌─────────────────────────┐
                   │    CDN (Cloudflare/      │
                   │    Akamai/AWS CloudFront)│
                   │    Edge nodes worldwide  │
                   └────────────┬────────────┘
                                │ streams
                                ▼
                   ┌─────────────────────────┐
                   │       Video Player       │
                   │  ABR (Adaptive Bitrate) │
                   │  Switches quality auto  │
                   └─────────────────────────┘

   ┌──────────────────────────────────────────────────────┐
   │                 Metadata Service                      │
   │  • PostgreSQL: video metadata, user data             │
   │  • Elasticsearch: full-text search                   │
   │  • Redis: view counts, trending, recommendations     │
   └──────────────────────────────────────────────────────┘
```

---

## 关键设计决策 / Key Design Decisions

### 1. 上传流程 — 分块上传 / Chunked Upload
- **为什么？/ Why?** 视频文件可能有 10GB+。断点续传（resumable upload）避免网络中断前功尽弃。
- 每个 chunk 独立上传 → 并行传输 → 服务端拼接
- YouTube / GCS 都用 resumable upload API

### 2. 转码管道 / Transcoding Pipeline
- **ABR (Adaptive Bitrate Rate)**：同一视频存 5 种分辨率（240p/480p/720p/1080p/4K）
- **HLS vs DASH**：HLS (Apple) / DASH (Android+Web)，现代平台同时支持两者
- 转码是 CPU 密集型 → 用**消息队列** (Kafka/SQS) 异步解耦，水平扩展 worker

### 3. CDN 分发 / CDN Distribution
- **为什么不直接读 S3？/ Why not S3?** 延迟太高，S3 按请求收费，全球用户体验差
- CDN 将视频 segment 缓存在距用户最近的边缘节点
- Cache key = `{video_id}/{quality}/{segment_number}.ts`

### 4. 视频格式 — HLS 分片 / HLS Segmentation
```
video.m3u8  (playlist file — tells player which segments exist)
├── seg_0000.ts  (2-10 second chunks)
├── seg_0001.ts
├── seg_0002.ts
└── ...
```
播放器只下载**当前 + 预读几个**片段，不需要下载整个视频文件。

---

## 核心权衡 / Key Tradeoffs

| 决策 | 方案 A | 方案 B | 选择 |
|------|--------|--------|------|
| 转码 | 同步（阻塞上传） | 异步（消息队列） | ✅ 异步 |
| 存储 | 一种质量 | 多种质量（ABR） | ✅ ABR |
| 分发 | 源站直接服务 | CDN 边缘缓存 | ✅ CDN |
| 计数 | 强一致（写 DB）| 最终一致（Redis + 批量写）| ✅ 最终一致 |

---

## ⚠️ 常见错误 / Common Mistakes

**坑 1：把转码做成同步的**
上传后立即返回 URL，但转码需要 5-10 分钟 → 用异步队列 + 状态轮询

**坑 2：忘了视频 seek（跳转）问题**
用户跳到视频 50 分钟处 → 需要 CDN 缓存那个 segment，不能只缓存开头

**坑 3：view count 用强一致数据库**
每秒百万次观看，直接写 DB 会打死数据库 → Redis incr + 定时批量刷新到 DB

**坑 4：不考虑版权检测**
YouTube 有 Content ID 系统，上传后异步扫描比对 audio/video fingerprint

---

## 📊 数量估算 / Scale Estimation

```
上传: 500 min of video/min → ~1GB raw video/min → ~500 MB/min after compression
存储: 1 video × 5 qualities × avg 500MB = 2.5GB per video
CDN reads: 2B users × 1 video/day × 500MB = 10^18 bytes/day (1 EB/day)
```

---

## 📚 References

1. [YouTube Architecture — High Scalability](http://highscalability.com/youtube-architecture)
2. [HLS Specification (Apple Developer)](https://developer.apple.com/documentation/http-live-streaming)
3. [DASH-IF Industry Forum](https://dashif.org/about/)

---

## 🧒 ELI5 / 小孩版解释

想象你录了一段乐高搭建视频想分享给全世界。你先把视频寄给一个大仓库（S3），仓库的工人把它剪成小片段，做出清晰版和模糊版备用。然后在全球各个城市的小仓库（CDN）都放上一份。当你的朋友在北京看视频，他从北京仓库取片段，快得很！他的网速好就看清晰版，网速差就自动换成模糊版——这就是 Netflix 和 YouTube 背后的秘密。

Think of it like sharing a Lego video worldwide: you send it to a big warehouse, workers cut it into small clips and make both HD and low-quality versions. Then mini-warehouses in cities worldwide get a copy. Viewers get clips from their nearest warehouse — good internet = HD, bad internet = auto-switches to lower quality. That's ABR + CDN!
