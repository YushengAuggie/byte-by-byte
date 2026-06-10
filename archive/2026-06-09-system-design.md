# 🏗️ 系统设计 / System Design — Day 61
**Topic:** Design a Live Streaming System (Twitch)
**Date:** 2026-06-09 | **Phase:** Expert

---

## 🏗️ 系统设计 / System Design
### 设计直播系统 / Design a Live Streaming System (Twitch)

**想象你在设计 Twitch...**

每天有数百万主播同时开播，每位主播的视频流需要被数千甚至数十万观众实时观看。你需要处理极低延迟、海量并发、全球分发，还要支持聊天、订阅、打赏。这是一个真正复杂的实时系统。

**Imagine you're designing Twitch...**

Millions of streamers go live daily. Each stream needs to reach thousands to hundreds of thousands of viewers in real time. You must handle ultra-low latency, massive concurrency, global distribution, plus chat, subscriptions, and donations.

---

## 🏛️ 架构图 / Architecture

```
                         ┌─────────────────────────────────┐
                         │         Streamer Client         │
                         │  OBS / Browser / Mobile App     │
                         └──────────────┬──────────────────┘
                                        │  RTMP (push)
                                        ▼
                         ┌─────────────────────────────────┐
                         │    Ingest Servers (Edge PoPs)   │
                         │  - Receive RTMP stream          │
                         │  - Authenticate streamer        │
                         └──────────────┬──────────────────┘
                                        │  Raw video segments
                                        ▼
                         ┌─────────────────────────────────┐
                         │     Transcoding Cluster         │
                         │  - 1080p / 720p / 480p / 360p   │
                         │  - HLS / DASH segmentation      │
                         │  - ~2-5 sec segments            │
                         └──────────────┬──────────────────┘
                                        │  Segmented chunks
                                        ▼
          ┌─────────────────────────────────────────────────────┐
          │               Origin Storage / CDN                   │
          │   S3 / GCS  ──────────► CDN Edge Nodes (global)     │
          │   .m3u8 manifests     Akamai / CloudFront / Fastly   │
          └─────────────────────────────────────────────────────┘
                                        │  HLS pull
                                        ▼
                         ┌─────────────────────────────────┐
                         │       Viewer Clients            │
                         │  - Pull segments via CDN        │
                         │  - ABR (Adaptive Bitrate)       │
                         └─────────────────────────────────┘

          ┌─────────────────────────────────────────────────────┐
          │               Chat / Realtime Layer                  │
          │   WebSocket Servers → Kafka → Chat Storage          │
          │   PubSub (Redis) for fan-out per channel            │
          └─────────────────────────────────────────────────────┘
```

---

## ⚡ 核心流程 / Core Flow

**推流 (Streaming In):**
1. 主播用 OBS 通过 RTMP 推流到最近的 Ingest 节点
2. Ingest 节点验证 stream key，转发到 Transcoding 集群
3. Transcoder 生成多码率 HLS 分片（每段约 2-6 秒）
4. 分片上传到 Origin Storage，CDN 立即缓存

**拉流 (Watching):**
1. 观众请求频道 URL → 获取 .m3u8 playlist
2. 客户端 ABR 算法根据网络选择码率
3. 每 2-6 秒拉取最新分片，实现 "实时" 播放

---

## ⚖️ 关键权衡 / Key Tradeoffs

| 决策 | 选项 | Why |
|------|------|-----|
| 传输协议 | RTMP(推) + HLS(拉) | RTMP 低延迟推流；HLS CDN 友好 |
| 延迟 vs 稳定性 | 6s 缓冲 vs 1s LL-HLS | 传统 HLS 稳定但 6s 延迟；LL-HLS 降到 ~1-2s 但更复杂 |
| 转码 | 实时 vs 离线 | 直播必须实时；使用 GPU 集群并行转码 |
| CDN | 自建 vs 第三方 | Twitch 体量需自建部分 PoP；早期用 Akamai/Cloudfront |
| 聊天 | WebSocket vs SSE | 聊天双向需要 WebSocket；每频道独立 pubsub 防止热点 |

---

## 🔢 容量估算 / Capacity Estimation

```
假设:
- 100K 并发主播，平均 1000 观众/主播
- 每路推流: ~6 Mbps (1080p)
- 转码输出: 3个码率 × 6 Mbps = ~18 Mbps/主播

推流带宽: 100K × 6 Mbps = 600 Gbps ingest
输出带宽: 100K × 1000 观众 × 3 Mbps avg = 300 Tbps CDN
存储: 100K 主播 × 6 MB/s × 3600s = ~2 PB/hour (VOD)
```

这就是为什么 Twitch 的 CDN 费用是天文数字。

---

## ❌ 常见错误 / Common Mistakes

**别踩这个坑:**

1. **忘记 Transcoding 是瓶颈** — 一路 1080p 流需要大量 CPU/GPU。不要设计单机转码，必须水平扩展 + 任务队列。

2. **忽视 CDN 缓存策略** — HLS 分片是内容可寻址的，可以强缓存。但 .m3u8 manifest 是动态的，缓存时间要短（~1-3秒）否则观众看不到新分片。

3. **聊天设计的 fan-out 问题** — 1 个频道 10 万人同时发消息，不能 1:1 推送。需要 pubsub + 客户端拉取，或限速 + 采样（Twitch 真的会在高热时丢弃聊天消息）。

4. **低估 Low-Latency 复杂性** — LL-HLS 需要 HTTP/2 push 和 chunked transfer encoding，实现复杂，慎重选择。

---

## 📚 References

- [HLS Specification — Apple Developer](https://developer.apple.com/streaming/)
- [How Twitch's Video Ingestion Works — Twitch Engineering Blog](https://blog.twitch.tv/en/2022/04/26/ingesting-live-video-streams-at-global-scale/)
- [Low-Latency HLS — WWDC](https://developer.apple.com/videos/play/wwdc2019/502/)

---

## 🧒 ELI5

直播就像一个超级快的外卖系统：厨师（主播）做好菜后，配送员（CDN）把菜分发到全国各地的分拣站，你去最近的站取菜。厨师一直在做新菜，你每隔几秒就去取一次，所以看起来是"实时"的。

Live streaming is like a super-fast food delivery: the chef (streamer) keeps cooking dishes, delivery hubs (CDN) store copies near you, and you pick up the latest dish every few seconds. It feels "live" because the chef never stops cooking and you never stop picking up.
