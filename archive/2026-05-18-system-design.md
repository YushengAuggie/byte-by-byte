# 🏗️ 系统设计 / System Design — 推荐系统 / Design a Recommendation System

> 📅 Day 46 | ⏱️ 3 min read | 🔴 Advanced

---

## 想象你在设计... / Imagine You're Designing...

你加入了一家类似 Netflix 的公司，PM 找你说："用户流失率太高了，我们要给每个用户推荐他们真正想看的内容。" 每天有 2 亿活跃用户，内容库有 1500 万个视频。你怎么设计？

*You join a Netflix-like company. The PM says: "Churn is too high — we need to recommend content users actually want to watch." 200M DAU, 15M videos in the catalog. How do you design this?*

---

## 🏛️ Architecture Diagram

```
User Request
     │
     ▼
┌─────────────────┐
│   API Gateway   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│            Recommendation Service           │
│                                             │
│  ┌─────────────┐    ┌──────────────────┐   │
│  │  Candidate  │    │   Ranking Layer  │   │
│  │ Generation  │───▶│  (ML Ranker +    │   │
│  │             │    │   Business Rules)│   │
│  └─────────────┘    └──────────────────┘   │
│         │                    │             │
│    ┌────▼────┐        ┌──────▼─────┐      │
│    │ Multiple│        │ Feature    │      │
│    │ Sources │        │ Store      │      │
│    └─────────┘        └────────────┘      │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│             Candidate Sources               │
│                                             │
│  ┌──────────────┐  ┌──────────────────┐    │
│  │ Collaborative│  │Content-Based     │    │
│  │  Filtering   │  │Filtering         │    │
│  │ (user-item   │  │(item embeddings) │    │
│  │  matrix)     │  │                  │    │
│  └──────────────┘  └──────────────────┘    │
│                                             │
│  ┌──────────────┐  ┌──────────────────┐    │
│  │   Trending   │  │ Contextual       │    │
│  │   / Popular  │  │ (time, device,   │    │
│  │              │  │  location)       │    │
│  └──────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│             Data Infrastructure             │
│                                             │
│  User Events ──▶ Kafka ──▶ Feature Store   │
│  (clicks, watch    │       (Redis online    │
│   time, skips)     │        features)      │
│                    │                       │
│                    ▼                       │
│             Spark / Flink                  │
│             (batch + stream)               │
│                    │                       │
│                    ▼                       │
│          Embedding Store (FAISS/           │
│          Pinecone for ANN search)          │
└─────────────────────────────────────────────┘
```

---

## 🔑 关键设计决策 / Key Design Decisions

### 两阶段架构 / Two-Stage Architecture

推荐系统的标准做法是**候选生成 → 精排**，这不是偶然的：

*The industry-standard two-stage approach—candidate generation → ranking—exists for good reason:*

| Stage | Input | Output | Latency Budget |
|-------|-------|--------|----------------|
| Candidate Generation | User ID | 100-500 items | 50ms |
| Ranking | 500 items + features | Top 20 | 100ms |
| Business Filters | Top 20 | Final list | 10ms |

**候选生成** 追求召回（recall），用轻量模型快速从百万候选里找到相关的。  
**精排** 追求精度（precision），用复杂模型在少量候选里找最好的。

### 协同过滤 vs 内容过滤 / Collaborative vs Content-Based

```
Collaborative Filtering:
"和你相似的用户喜欢 X"
User A watched: [Movie1, Movie2, Movie3]
User B watched: [Movie1, Movie2, ?]
→ Recommend Movie3 to User B

Content-Based:
"你看过的东西和 X 相似"
User watched: Action movies with Tom Hanks
→ Recommend similar action/Tom Hanks movies

Hybrid (Netflix/Spotify approach):
Combine both + context signals
```

### 冷启动问题 / Cold Start Problem

| 场景 | 策略 |
|------|------|
| 新用户 | 推热门内容 + 引导填写偏好 |
| 新内容 | 用内容特征（genres, actors）+ 曝光池 |
| 新平台 | 先热门，再逐渐收集数据 |

---

## ⚖️ 关键权衡 / Key Tradeoffs

**实时 vs 批量特征** / Real-time vs Batch Features

```
批量 (Hadoop/Spark, 每小时更新):
✅ 历史偏好、长期兴趣模型
❌ 无法捕捉用户刚才的行为

实时 (Flink, 秒级更新):
✅ 当前 session 的行为（刚搜了什么）
❌ 计算昂贵、延迟要求高
```

实践中：**Lambda 架构** — 批量做基础，实时做修正。

**精确推荐 vs 多样性** / Accuracy vs Diversity

如果只推用户最喜欢的类型，他们会陷入信息茧房。Netflix 有明确的 **diversity budget**：每20个推荐里，强制包含至少3个用户不常看的类型。

---

## ☠️ 别踩这个坑 / Common Mistakes

**坑1：忘记 Feedback Loop（反馈循环）**  
推荐系统会自我强化。只推热门 → 热门更热门 → 新内容永远没机会。必须加 **exploration factor**（比如 ε-greedy 或 UCB）。

**坑2：混淆 Offline 和 Online 指标**  
离线 A/B 测试 CTR 很好，不代表线上用户满意。Netflix 发现，用户满意度更好的指标是 **watch time after click**，而不是 CTR 本身。

**坑3：忽略延迟**  
推荐要在 <200ms 内返回（含网络）。重模型必须离线预计算，用 cache 存结果。

---

## 🧒 ELI5

推荐系统就像一个超级聪明的图书馆员。她记得你借过什么书，知道和你品味相似的人喜欢什么，还会把最新上架的热门书放在你面前——但不会每次都给你一样的书，不然你会无聊的！

*A recommendation system is like a super-smart librarian. She remembers what you've borrowed, knows what people with similar tastes enjoy, and shows you popular new books — but she makes sure to occasionally surprise you so you don't get stuck in a rut.*

---

## 📚 References

- [Netflix Tech Blog — How Netflix's Recommendations Work](https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429)
- [Spotify Engineering — Collaborative Filtering at Scale](https://engineering.atspotify.com/2021/12/how-spotify-uses-ml-to-create-the-future-of-personalization/)
- [Meta Engineering — Deep Learning Recommendation Model (DLRM)](https://ai.facebook.com/blog/dlrm-an-advanced-open-source-deep-learning-recommendation-model/)
