# 🏗️ 系统设计 / System Design — Day 29: Design a File Storage System (Google Drive/Dropbox)

> **难度 / Difficulty:** Advanced · **阶段 / Phase:** Mastery · **预计阅读时间 / Read time:** ~3 min

---

## 想象这个场景 / Imagine This

你在设计 Google Drive —— 全球 10 亿用户存储文件、照片、视频，随时随地同步，多设备实时协作编辑。

You're designing Google Drive — 1B users storing files, photos, videos; syncing across devices; real-time collaborative editing.

核心挑战：**任意大小的文件、版本管理、冲突解决、大规模扩展**。

Core challenges: **arbitrary file sizes, version control, conflict resolution, massive scale**.

---

## 核心需求 / Requirements

**功能性需求 / Functional:**
- 上传、下载、删除文件 / Upload, download, delete files
- 文件夹层级结构 / Folder hierarchy
- 文件共享与权限管理 / Sharing & permissions
- 版本历史 / Version history (last N versions)
- 增量同步（只传改变的部分）/ Delta sync (only changed chunks)

**非功能性需求 / Non-functional:**
- 可用性 99.999% / 99.999% availability
- 文件一致性（跨设备）/ Cross-device consistency
- 存储 PB 级数据 / PB-scale storage

---

## 架构图 / Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Clients                              │
│         Web / Desktop App / Mobile App                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
              ┌────────▼────────┐
              │   API Gateway   │
              │  (Rate Limit,   │
              │   Auth, Route)  │
              └──┬──────────┬───┘
                 │          │
        ┌────────▼──┐  ┌────▼───────────┐
        │  Metadata  │  │  Upload Service │
        │  Service   │  │  (Chunking)     │
        │ (Files DB) │  └────┬────────────┘
        └────────────┘       │ chunks
                       ┌─────▼──────────┐
                       │  Chunk Store   │
                       │  (Object Store │
                       │   e.g. S3)     │
                       └────────────────┘
                              │
              ┌───────────────▼──────────────┐
              │       Sync Service           │
              │  (Delta detection, Notify)   │
              │  WebSocket / SSE to clients  │
              └──────────────────────────────┘

 Metadata DB: PostgreSQL (file tree, versions, chunks list)
 Object Store: S3 / GCS (immutable chunk blobs, content-addressed)
 Cache: Redis (session, file metadata hot path)
 Queue: Kafka (async chunk processing, notifications)
```

---

## 关键设计决策 / Key Design Decisions

### 1. 分块上传 / Chunked Upload
把大文件切成 **4–8MB 的块（chunk）**，每块独立上传。

Split files into **4–8MB chunks**; upload each independently.

- **Why:** 断点续传、重传只补缺块、去重（相同内容不重复存储）
- **Why:** Resume on failure, only retry failed chunks, deduplication across users

```
文件 → 计算每块 SHA-256 → 查询哪些块已存在 → 只上传缺失块
File → compute SHA-256 per chunk → query which exist → upload only missing
```

### 2. 内容寻址存储 / Content-Addressed Storage
块用 SHA-256 命名，相同内容 = 相同 key。

Chunks keyed by SHA-256 — identical content → same key.

- 自动去重：如果你和同事上传同一个 PDF，只存一份
- Auto-dedup: if you and a colleague upload the same PDF, stored once

### 3. 元数据与数据分离 / Metadata vs. Data Separation
```
Metadata DB stores:
  - file_id, name, parent_folder_id, owner_id
  - version_id, chunk_list (ordered SHA-256s)
  - created_at, modified_at, permissions

Chunk Store: immutable blobs in S3
```

### 4. 冲突解决 / Conflict Resolution
- 乐观锁：版本号 CAS（Compare-And-Swap）
- Optimistic locking: version CAS
- 冲突时：创建"副本（conflict copy）"，用户手动合并
- On conflict: create a "conflict copy", let user merge
- Google Docs 用 OT（Operational Transform）实现实时协作
- Google Docs uses OT for real-time co-editing

---

## 增量同步 / Delta Sync

```
Client sends: {file_id, chunks_hash_list}
Server responds: {missing_chunks: [...], obsolete_chunks: [...]}
Client uploads only missing chunks → Server assembles new version
```

客户端只传改变的块 → 大文件小改动 = 极少流量。

Client only sends changed chunks → small changes to big files = tiny bandwidth.

---

## ⚠️ 别踩这个坑 / Common Mistakes

| 错误 / Mistake | 正确做法 / Correct |
|---|---|
| 整个文件一次传 / Upload whole file | 分块 + 断点续传 / Chunked + resumable |
| 用 DB 存文件内容 / Store file blobs in DB | 只存元数据，文件放对象存储 / Metadata in DB, blobs in object store |
| 同步操作堵塞请求 / Sync ops blocking requests | Kafka 队列异步处理 / Async via Kafka |
| 每次修改整个文件重传 / Re-upload whole file on change | Delta sync，只传改变块 / Delta sync, send only changed chunks |
| 权限检查在客户端 / Client-side permission checks | 永远在服务端验证 / Always server-side |

---

## 容量估算 / Capacity Estimation

```
1B users × avg 10GB storage = 10 EB total
Daily uploads: 100M files/day × avg 1MB = 100TB/day
Chunk size: 4MB → 25 chunks per 100MB file
Dedup ratio: ~20% storage saved across users
```

---

## 📚 参考资料 / References

- [System Design Interview – Alex Xu: Google Drive](https://bytebytego.com/courses/system-design-interview/design-google-drive)(https://bytebytego.com/courses/system-design-interview/design-google-drive)
- [Dropbox Tech Blog – How we optimized our sync algorithm](https://dropbox.tech/infrastructure/streaming-file-synchronization)(https://dropbox.tech/infrastructure/how-we-optimized-magic-pocket-for-performance)
- [Google Drive API Documentation](https://developers.google.com/drive/api/guides/manage-uploads)(https://developers.google.com/drive/api/guides/about-files)

---

## 🧒 ELI5

想象你要邮寄一本很厚的书给朋友。你不是把整本书一起寄，而是把每一页撕下来，分别用不同的信封寄（分块）。如果某封信丢了，只重寄那一页（断点续传）。而且如果两本书有相同的几页，只需要寄一次（去重）。

*Imagine mailing a thick book to a friend. Instead of mailing the whole book at once, you tear out each page and mail them in separate envelopes (chunking). If one gets lost, you only resend that page (resume). And if two books share identical pages, you only mail them once (dedup).*
