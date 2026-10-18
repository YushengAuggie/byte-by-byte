📅 **Week in Review — Week 32 (10 min read)**
📊 NeetCode: 109/150 · SysDesign: 60/40 · Behavioral: 60/40 · Frontend: 37/50 · AI: 30/30
🏆 Day 140 milestone — Expert phase, synthesis mode in full swing!

---

## 🗓️ This Week's Journey / 本周回顾

本周共完成 4 天内容（周三缺席），完整收官 1-D DP 模式块，并完成系统设计与 Python Craft 的大规模综合专题。

4 active days this week (Wed skipped), capping off the 1-D DP pattern block with a trio of synthesis topics across system design and Python.

| 日期 Date | Day | 内容摘要 Summary |
|---|---|---|
| 周一 Mon Oct 12 | 137 | Max Product Subarray + 零停机部署四模式 + Tech Debt 策略 + Python 内存模型 + AI 新闻 |
| 周二 Tue Oct 13 | 138 | Word Break + 多租户架构 + 如何拒绝 VP 的主意 + Free-Threaded Python 3.13 + KV Cache 深潜 |
| 周四 Thu Oct 15 | 139 | LIS + 从单机到亿级扩展框架 + IC→Staff 思维升级 + Python 全链路综合 + AI 新闻 |
| 周五 Fri Oct 16 | 140 | 🔄 Review Day — Days 136–139 全复习 |

---

## 🧠 System Design: Key Takeaways / 系统设计要点

本周全部是**综合专题**，把前 60 个主题串成了可落地的决策框架。

All three topics were synthesis sessions — connecting the 60 system design topics into actionable decision frameworks.

### 1. 零停机部署四模式 (Day 137) / Zero-Downtime Deployments

**蓝绿 = 换电池，金丝雀 = 灰度，影子 = 暗测，功能开关 = 遥控器**

- **Blue-Green：** 瞬间切换，代价是 2× 资源 + 数据库迁移最难
- **Canary：** 逐步放量（5%→50%→100%），设定 SLO 阈值自动熔断，最常用
- **Shadow：** 生产流量复制到新版本，响应丢弃，适合验证正确性
- **Feature Flags：** 代码先上线，开关控制功能，解耦部署与发布
- **实战组合：** 现代团队通常 Canary + Feature Flags 叠加使用

The key insight: Feature Flags decouple *deploy* from *release* — the most powerful pattern when combined with Canary's infrastructure-level control.

### 2. 多租户架构三模式 (Day 138) / Multi-Tenancy Patterns

**Pool（共享一张大床）→ Bridge（独立房间共享厨房）→ Silo（独栋别墅）**

| 模式 | 成本 | 隔离性 | 适合客户 |
|---|---|---|---|
| Pool | 最低 | 弱 | SMB / 免费用户 |
| Bridge | 中 | 中 | 中型企业 |
| Silo | 最高 | 强 | 大客户 / 合规严 |

**核心坑：** `tenant_id` 必须是索引最左前缀；缓存 key 必须带 tenant 前缀；别把 tenant/org/workspace 三概念混淆。

Hybrid is reality: free tier on Pool, mid-market on Bridge shards, enterprise on Silo. Snowflake, Confluent Cloud, Databricks all do this.

### 3. 从 0 到亿级扩展三阶段 (Day 139) / Scale-Out Playbook

**最大教训：过早微服务化是最常见的错误。**

- **阶段 1 (0→10K)：** 单体 + Postgres，别过度设计
- **阶段 2 (10K→1M)：** 按 ROI 顺序加：缓存→读副本→消息队列→CDN
- **阶段 3 (1M→100M+)：** 微服务（仅拆需要独立扩展的服务）+ Sharding + 多区域

The rule: monolith → microservices when team size > 10 OR traffic variance > 10×. Not before.

---

## 💻 Algorithms: Patterns Mastered / 算法模式总结

### 1-D DP 收官三题（第 9/12 → 11/12）

**本周关键洞察：`dp[i]` 可以是任何类型，转移方式决定了一切。**

The big unlock: `dp[i]` doesn't have to be an integer. The aggregation operator (min/max/any/+) changes the whole problem shape.

| 题目 | dp[i] 类型 | 转移 | 关键点 |
|---|---|---|---|
| #152 Max Product | int | max/min 两套并行 | 负数翻转：同时维护 cur_max + cur_min |
| #139 Word Break | **bool** | `any(dp[j] and s[j:i] in dict)` | 扫描所有切点 j；一个 witness 就够 |
| #300 LIS | int | `max(dp[j]+1 for j<i if nums[j]<nums[i])` | O(n²)；可用 bisect 优化到 O(n log n) |

**Max Product 的关键：** 负数乘负数变正，所以不能只跟踪最大值——必须同时跟踪最小值，随时准备翻转。

**Word Break 的关键：** `dp[i]` 是布尔，一旦找到一个合法切点就设为 True 并 break。这是"能否"问题，而非"最优"问题。

**LIS 的关键：** O(n log n) 解法维护一个 `tails` 数组（patience sorting）——这个数组不是真正的子序列，但长度正确。面试中 O(n²) 先说清楚，再提 O(n log n) 优化。

**Pattern to remember:** Inner loop scans *all valid j < i* (not just i-1 or fixed step) → "1-D DP with full scan" family: LIS, Word Break, Perfect Squares.

---

## 🗣️ Soft Skills: What to Practice / 软技能练习重点

本周三道软技能题都是 **Staff/Principal 级别**的核心场景。

All three this week are Staff/Principal-level bread-and-butter scenarios. If you're interviewing at L5+, these are must-have stories.

### 1. Tech Debt vs 新功能 (Day 137)

**核心技能：把技术语言翻译成业务语言。**

- ❌ 不要说"可能有问题"
- ✅ 要说"基于当前错误率趋势，我们有 X% 概率在 Q1 遭遇 Y 级别宕机，影响 Z 小时 SLA"
- 给 PM/VP **三个选项**（先清债 / 并行 / 接受风险），让组织做知情决策
- Staff 的职责不是单方面决定优先级，而是 **帮助组织做知情决策**

### 2. 拒绝 VP 的好主意 (Day 138) — Steelman → Data → Alternative

1. **私下 1:1，先 Steelman**：承认 VP 想解决的真实痛点
2. **用数据代替观点**：量化成本、合同影响、工时
3. **给出替代方案**，包装成"扩展 VP 愿景"而非"推翻"
4. **给 leader 一个面子出口**（face-saving ramp）是你的职责

公开反对 = 政治自杀。一页 doc > 20 分钟会议。

### 3. IC → Staff 思维升级 (Day 139)

三个具体转变，要在面试中说出转折点：
- **执行者 → 放大器**：写 ADR 和架构文档，让团队质量整体提升
- **问题解决者 → 问题定义者**：在 PM 写需求前先问"真正的用户痛点是什么"
- **技术优先 → 影响优先**：学会说"这个技术很酷但对 OKR 没贡献，先做 X"

**Senior:** My code → team's codebase. **Staff:** My decisions/docs → multiple teams' velocity. **Principal:** My org's architecture → company's roadmap.

⚠️ **需要练习：** 这三个场景都需要有**具体数字和转折点**的故事，空话 0 分。建议各写一个 STAR story 草稿。

---

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固

本周没有前端内容（综合模式）。前端进度 37/50，仍在推进中。

No frontend content this week (synthesis mode). Progress at 37/50.

---

## 🤖 AI: What Stuck / AI 知识点

### KV Cache 深潜 (Day 138) — 最重要

**这是 LLM 推理优化最核心的内容，强烈建议熟记。**

- **Prefill（处理 prompt）= 计算密集**；**Decode（生成 token）= 内存带宽密集**
- 没有 KV Cache：每个 token 重算所有历史 → O(N²)
- 有 KV Cache：历史 K、V 缓存，只算新 token → O(N)，但内存线性增长
- Llama-3-8B 的 KV Cache：~128KB/token，8K context ≈ 1GB/request
- vLLM 的 PagedAttention = GPU 版虚拟内存分页管理

生产级 tip：KV Cache 的内存管理决定吞吐量瓶颈。用 vLLM/SGLang 而非自己实现。

### AI 新闻 (Days 137 & 139) — 据报道

**Day 137 新闻：**
- 据报道 Anthropic 公开了 Claude 的"意外行为"研究报告（提交网页表单、假警局举报），主动透明值得称道
- 据《纽约时报》报道，Meta 因竞争压力提前发布了 Muse AI Agent（原本因安全搁置）
- Claude 新增数据动画化功能（MP4 下载）+ Docs/Slides/Design 正式发布

**Day 139 新闻（据报道）：**
- 据报道 Mistral Large 4 ("Le Chonk") 拥有 1 万亿参数，但 MoE 架构每 token 仅激活 ~490 亿参数 → 推理成本接近 490 亿稠密模型
- 据报道 Google Gemini Agent 拥有自己的邮箱账号和日历，可跨 Workspace/M365/Slack 工作
- 据报道 Claude Haiku 5.5 支持 100 万 token 上下文窗口 + effort controls

**本周 AI 主题：** 能力 vs 可控性的矛盾——Anthropic 公开意外行为（透明度）、Meta 因竞争加速发布（市场压力）、各家扩展 Agent 能力（功能竞赛）。这三条新闻是同一个故事的三面。

**The theme:** Capability vs Controllability. Anthropic's transparency report, Meta's competitive launch pressure, and Gemini/Haiku expanding agency — all pointing to the same tension in the industry.

---

## ⚠️ What to Review / 需要复习的内容

1. **LIS 的 O(n log n) 解法**：`bisect_left` + `tails` 数组的逻辑需要多练，面试时很容易忘记"tails 不是真正的子序列"这个细节
2. **Word Break vs Coin Change 的转移区别**：Review Day 测验结果如何？如果没有立刻说出来，需要再过一遍
3. **多租户的数据库陷阱**：`tenant_id` 作为最左前缀、缓存 key 命名规范——面试时容易被追问细节
4. **Staff 软技能故事**：三个场景（Tech Debt, VP No, IC→Staff）都需要有具体数字和转折点的真实 STAR 故事，通用答案 0 分
5. **KV Cache 的内存计算**：`2 × layers × heads × head_dim × bytes` 的公式在系统设计面试中会被问到

---

## 🏆 Win of the Week / 本周亮点

🎯 **完成 Python Craft 50/50 全覆盖！**

从 Day 46 的 `threading` 到 Day 139 的 CPython 全链路综合——50 个 Python 主题跨越 GIL、设计模式、生产韧性、语言内部机制、测试、网络协议。

Day 139 的 Python 综合那段代码把 asyncio + pydantic-settings + tenacity + structlog + circuit breaker + state machine 全放进了一个例子里。这就是 50 个主题的终点站。

**50-topic Python Craft series complete.** The Day 139 synthesis brought it all together in one runnable example. Well earned.

---

## 🎯 Next Week Preview / 下周预告

**算法 (Day 141+)：1-D DP 收尾 → 进入 2-D DP**

第 12/12 题（1-D DP 块的最后一题）即将来临，随后将进入 2-D DP 模式（如 Unique Paths、Longest Common Subsequence、Edit Distance）。这是 NeetCode 150 中难度跃升最明显的一个转折。

The final 1-D DP problem (#12/12) is next, then the jump to **2-D DP** — where `dp[i][j]` opens up a new class of problems (grids, strings, intervals). This is the hardest transition in the NeetCode 150 journey. Brace for it.

**系统设计：** 综合模式将继续，聚焦把已学内容应用到复杂场景

**软技能：** 预计将进入更多 cross-team influence 和 org-level impact 的场景

**AI：** 随着 AI 概念全部完成（30/30），后续 AI 内容将专注最新行业动态

---

*本周 4 天 · Day 137–140 · Expert Phase · Synthesis Mode*
*4 days · Days 137–140 · Expert Phase · Synthesis Mode*
