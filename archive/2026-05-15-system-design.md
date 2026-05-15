# 🏗️ 系统设计 / System Design — Day 44
## Design a Content Moderation System (内容审核系统)

> **难度 / Difficulty:** Advanced · **阶段 / Phase:** Mastery

---

### 场景 / Scenario

想象你在 Meta 工作，每天有 **5亿条** 帖子、图片、视频被上传。你需要构建一个系统，在内容展示给用户之前，自动检测并过滤违规内容（仇恨言论、色情、暴力、虚假信息）。

You're at Meta. 500M pieces of content uploaded daily. Build a system that detects and filters violating content before it reaches users — hate speech, nudity, violence, misinformation.

---

### 架构图 / Architecture

```
Producers
  [Mobile/Web App]
        │
        ▼
  [API Gateway]
        │
    ┌───┴────┐
    │ Upload │ ──────────► [Object Storage: S3/GCS]
    │ Service│                     │
    └────────┘              [Content Event Bus: Kafka]
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
      [Text Classifier]   [Image/Video ML]    [Graph Signals]
      (BERT/LLM-based)    (CNN/Vision model)  (user history, reports)
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   ▼
                         [Score Aggregator]
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼               ▼
              [Auto-Approve]  [Human Queue]  [Auto-Remove]
              score < 0.2    0.2 < s < 0.8  score > 0.8
                                   │
                          [Moderation Dashboard]
                          (human reviewers)
                                   │
                          [Feedback Loop]
                          (labels → retrain)
```

---

### 核心设计决策 / Key Design Decisions

**1. 异步 vs 同步处理 / Async vs Sync**
- 视频不能同步审核（太慢）→ **乐观发布 + 后置过滤**
- 文本可以同步（< 100ms） → **发布前拦截**
- Trade-off: 延迟展示 vs 允许短暂可见

**2. 多模型流水线 / Multi-model pipeline**
- 不同内容类型用不同模型（文本/图像/视频/音频）
- 集成上下文信号：用户举报数、账号年龄、历史违规
- 模型投票 + 加权分数 → 最终判决

**3. 人工审核队列 / Human-in-the-loop**
- 灰色地带内容（score 0.2–0.8）发给人工审核员
- 目标：每个案例审核时间 < 24h
- 人工标注数据回流 → 定期重训练模型

**4. 上诉机制 / Appeals**
- 被误删内容可申诉 → 触发二次人工审核
- 降低误杀率(False Positive)对用户信任的损害

---

### 为什么这样设计？/ Why This Design?

| 问题 | 决策 | 原因 |
|------|------|------|
| 5亿/天吞吐量 | Kafka 异步 | 解耦上传和审核，削峰 |
| 高准确性需求 | 多模型融合 | 单一模型误判率高 |
| 上下文感知 | 图谱信号 | 同一词在不同用户/背景下含义不同 |
| 监管合规 | 可审计日志 | GDPR/DSA 要求保存决策记录 |

---

### 别踩这个坑 / Common Mistakes

❌ **单模型打天下** — 文本模型看不懂图，图像模型看不懂上下文  
❌ **全量同步审核** — 视频审核可能要30秒，用户不会等  
❌ **忽略误报(False Positive)** — 过度审核会赶走正常用户，比漏审代价更大  
❌ **冷启动无数据** — 新平台没有标注数据？用迁移学习 + 小批量人工标注  
❌ **不设置上诉通道** — 监管机构（DSA/GDPR）要求平台必须提供申诉机制  

---

### 关键指标 / Key Metrics

- **Precision/Recall** — 误杀率 vs 漏审率（需要业务决定取舍点）
- **Review queue latency** — 人工审核积压时间
- **Appeals rate** — 用户申诉率（高了说明误判多）
- **Model drift** — 定期监控分布漂移（新梗、新表情包）

---

### 🧒 ELI5

想象学校里有个自动"坏话检测仪"。它先快速扫一眼所有内容，明显坏的直接删，明显好的直接放，看不准的交给老师手动检查。老师的判断结果再教"检测仪"变聪明。

---

### 📚 References
- https://engineering.fb.com/2020/08/07/ml-applications/hate-speech/
- https://transparency.fb.com/enforcement/
- https://blog.youtube/inside-youtube/youtube-content-id/
- https://aws.amazon.com/rekognition/content-moderation/
