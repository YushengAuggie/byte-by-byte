📅 **Week in Review — Week 14 (10 min read)**
📊 NeetCode: 75/150 · SysDesign: 60/40✅ · Behavioral: 60/40✅ · Frontend: 37/50 · AI: 30/30✅
🔥 Day 94 — Expert Phase

---

## 🗓️ This Week's Journey / 本周回顾

**周一 Mon · Day 89** — 系统设计：读写路径分离（Twitter Fanout / Facebook TAO / CQRS）；算法：Combination Sum #39（回溯模板变体2/9）；软技能：Staff Engineer 的两难困境——深度 vs 广度影响力；Python Craft：Mocking（unittest.mock，什么时候 Mock / 不 Mock）；AI 新闻：GPT-5.6 三档发布、Anthropic $30B 年化营收、Gemini 3.5 Pro 延期。

**周二 Tue · Day 90** — 复习日（Day 18）：回溯 Subsets vs Combination Sum 关键差异 · Mocking 黄金法则（patch 在使用处而非定义处）· Design Twitter 两堆合并 · Q&A 三道小测验。

**周三 Wed · Day 91** — 系统设计综合：一致性模型全景（Linearizable → Sequential → Causal → Eventual；PACELC 升级 CAP）；算法：Permutations #46（回溯模板3/9，用 visited set 而非 start index）；软技能综合：技术债 vs 新功能冲突时的"菜单式"决策框架；Python Craft：pytest Fixtures & factory_boy；AI 新闻：价格战、OpenAI×Broadcom 推理芯片 Jalapeño、AI Agent 能力跃升。

**周四 Thu · Day 92** — 系统设计综合：分布式系统权衡深化（CAP 5 大系统选型、PACELC 实战）；算法：Subsets II #90（回溯模板4/9，有重复元素的去重技巧）；软技能综合：新入职 Staff 面对严重技术债 + PM 要 2x 速度的场景；Python Craft：hypothesis 属性基础测试；AI 综合：LLM 对齐技术全景（RLHF → DPO → Constitutional AI → 自动红队）。

**周五 Fri · Day 93** — 系统设计综合：一致性模型（Redis Sentinel vs Spanner TrueTime 架构对比）；算法：Combination Sum II #40（回溯模板5/9，有重复元素 + 每个只用一次）；软技能综合：B2B SaaS Staff 的"3周 vs 8周"战略窗口决策；Python Craft：pytest-asyncio 模式（AsyncMock、async fixtures、并发测试）；AI 新闻：Kimi K3 发布、稀疏激活（selective activation sparsity）、Google Gemini Notebook。

**周六 Sat · Day 94** — Saturday Deep Dive：回溯算法与二维网格搜索——Word Search #79 全解析 + Word Search II（Trie 优化）+ N-Queens（对角线 r±c 技巧）+ 朴素 DFS → 剪枝 → 生产场景的完整推进链。

---

## 🧠 System Design: Key Takeaways / 系统设计要点

**本周核心线索：分布式一致性从理论到选型决策**

这周系统设计全面转向综合模式，围绕一个核心主题展开：**在真实系统中如何选择一致性级别，以及背后的工程代价**。

**1. 读写路径分离（Day 89）**
Twitter Fanout 演化史（写入 fanout → 名人混合模式）、Facebook TAO 多层缓存（99%+ hit rate）、CQRS 架构的极致体现：读写路径天生不同——读可接受过时、写必须持久化。核心选择框架：读写比 > 10:1 时必须分离；强一致性硬需求（金融）时慎用。

**2. 一致性模型全景（Days 91–93）**
从 Linearizability → Sequential → Causal → Eventual 的谱系，以及 PACELC 比 CAP 更实用（"无分区时选延迟还是一致性"）。五大系统选型：Redis（AP，cache miss 可重建）、Kafka（AP，消息可接受略过时）、PostgreSQL（CP，金融数据）、ZooKeeper/etcd（CP，分布式锁必须线性化）、推荐系统（AP，旧推荐无所谓）。

**连接点**：读写路径分离、一致性选型、PACELC 都回答同一个问题——**数据错误的代价是什么**？这是系统设计 tradeoff 的根本问题。

---

## 💻 Algorithms: Patterns Mastered / 算法模式总结

**本周主题：回溯模板 Block（5/9 完成）**

这周是回溯模板 block 的核心周，从 2/9 推进到 5/9，外加 Saturday Deep Dive 深挖 Word Search。

**已掌握的回溯变体矩阵：**

| 题目 | 重复输入 | 可重用 | 递归调用 | 去重方式 |
|------|---------|--------|---------|--------|
| #78 Subsets（Day 88） | No | No | `i+1` | N/A |
| #39 Combo Sum（Day 89） | No | **Yes** | `i`（不后移） | N/A |
| #46 Permutations（Day 91） | No | No | 无 start | visited set |
| #90 Subsets II（Day 92） | **Yes** | No | `i+1` | sort + skip siblings |
| #40 Combo Sum II（Day 93） | **Yes** | No | `i+1` | sort + skip siblings |

**关键洞察（各题的核心 insight）：**
- **Combination Sum**：`backtrack(i, ...)` 而非 `i+1`——允许重用同一元素。
- **Permutations**：不用 `start` 而用 `used` set——因为顺序重要，`[1,2] ≠ [2,1]`。
- **有重复元素**（Subsets II / Combo Sum II）：排序 + `if i > start and nums[i] == nums[i-1]: continue`——只跳过同层重复，不跳父子关系。
- **Word Search Deep Dive**：2D 回溯的 in-place 标记（`board[r][c] = '#'`）省去 visited set；Trie 优化 Word Search II 从 `O(W × M × N × 4^L)` 降到一次 DFS；N-Queens 对角线技巧 `r-c` / `r+c` 集合。

**需要记住的核心规律**：控制"是否重用"用 start index 移动方向；控制"是否去重"用 sort + skip siblings。

---

## 🗣️ Soft Skills: What to Practice / 软技能练习重点

**本周主题：Staff Engineer 视角的两大高频场景**

两个综合场景本周反复出现，值得重点练习：

**场景 1：技术深度 vs 广度影响力（Day 89）**
核心技巧：量化杠杆（计算"被阻塞的工程师·周"）→ 知识外化（文档化让他人能接手 70%）→ 批量效率（把 5 个独立 review 合并成 2 次工作坊）。面试信号：展示"乘数效应思维"而非"我来解决"思维。

**场景 2：技术债 + 战略窗口的"菜单式"决策（Days 91–93）**
三道题目本周都反复考察同一个框架：把技术债翻译成量化业务风险（事故概率 × 信任损失）→ 提出 2-3 个方案菜单（不是单一答案）→ 让业务团队做知情决策→无论选哪条路，设置护栏（feature flag + 灰度 + 回滚 runbook）。

**什么需要继续练习：**
- STAR 故事中的**数字密度**：大多数候选人描述行动但忘记量化结果。"转化了 ~40 家新客户"和"取得了不错的效果"差距巨大。
- **知识转移**这个细节：Staff 级别最有说服力的行动之一是"主动减少'只有我能做'的工作"。
- 区分 Senior 和 Staff 的边界表格（主要产出 / 成功衡量 / 知识共享 / 风险观）——这是面试时快速定标自己的工具。

---

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固

**本周：Python Craft Testing 周全面收官**

本周是 Week 9（Testing）的最后三天，覆盖了测试知识体系的进阶层：

- **Mocking（Day 89）**：Mock vs AsyncMock；`patch` 三种用法；黄金规则——在**使用处**而非**定义处** patch（`myapp.payment.stripe.Charge.create` 不是 `stripe.Charge.create`）；何时不该 Mock（不要 Mock 自己的业务逻辑）。

- **Fixtures & factory_boy（Day 91）**：pytest fixture scope（function/module/session）；factory_boy 的 `SubFactory`、`Sequence`、`LazyAttribute`；Factories 只指定测试关心的字段，其他自动填充。

- **hypothesis 属性基础测试（Day 92）**：从 example-based → property-based 的思维转变；写的是"不变量"而非"期望值"；自动生成 + shrinking（找到最小失败用例）；对序列化/反序列化、算法、状态机最有价值。

- **pytest-asyncio（Day 93）**：`AsyncMock`（不是 `MagicMock`）；`pytest_asyncio.fixture`；`asyncio_mode = "auto"` 的好处；event loop scope 匹配问题。

**快速自检**：
1. `@patch("myapp.service.stripe")` vs `@patch("stripe")` 哪个正确？前者。
2. 如何批量创建 5 个不同用户？`UserFactory.create_batch(5)`
3. hypothesis 的"shrinking"是什么？发现失败后自动找到最简复现用例。
4. 为什么 async test 不能用普通 MagicMock？MagicMock 不是 awaitable，需要 AsyncMock。

---

## 🤖 AI: What Stuck / AI 知识点

**本周最重要的 AI 知识点**

**1. 行业动态（据报道 / reportedly — 新闻来源）：**
本周 AI 新闻质量很高——三家头部公司的战略清晰对比了出来：OpenAI 冲能力上限（GPT-5.6 Sol 的 scatter-gather 子代理架构，fan-out 模式落到 LLM 推理层）；Anthropic 专注企业市场（$30B 年化营收，靠云市场分发降低部署摩擦）；Google 稳字当头（Gemini 3.5 Pro 延期宁可推迟不发次品——eval gates 是一等公民）。据报道 Kimi K3 是约 2.8T 参数 MoE 稀疏模型，1M 上下文窗口，27日开源。

**2. AI 对齐综合（Day 92）**：
RLHF → DPO → Constitutional AI → RLAIF → 自动红队的技术演进链。自动红队的核心是对抗性自我改进循环（red model 生成攻击 → target 回应 → judge 打分 → red model 学习），本质是把对抗训练应用到安全性提升。**对齐 ≠ 审查**——目标是让 AI 理解语境，而非拒绝所有"危险"问题。

**3. Selective Activation Sparsity（ICML 2026）**：
推理时只激活与当前任务最相关的参数子集，与 MoE 一脉相承但粒度更细。工程含义：同等推理成本下性能更强，或同等能力下更便宜——这是下一波效率竞争的方向。

**最重要的 takeaway**：面试里谈 AI 趋势，别只背模型名字。讲**架构模式**（scatter-gather 子代理）、**商业逻辑**（部署摩擦 vs 模型质量）、**工程纪律**（eval gates）——这才是 Senior/Staff 视角。

---

## ⚠️ What to Review / 需要复习的内容

**1. 回溯模板：`i` vs `i+1` vs `used set` 三者的选择逻辑**
这是面试最容易混淆的点。建议在脑中记住那张对比表，特别是"有重复元素 → sort + skip siblings"这个规律，在 Day 94 的 Word Search 后需要强化练习。下周即将到来的 Word Search (#79) 完整题 + Permutations II (#47)。

**2. Mocking 的"patch 在使用处"规则**
这是一个非常具体、容易出错的 Python 知识点。`@patch("myapp.payment.stripe.Charge.create")` 而非 `@patch("stripe.Charge.create")`——从使用处 patch，不从定义处。这个细节在实际工作中每周都会遇到。

**3. 一致性模型的决策框架**
能够快速说出"为什么 ZooKeeper 要 CP"和"为什么推荐系统可以 AP"——不是背答案，而是能说出背后的业务逻辑（分布式锁如果 AP 会出现两个 leader；推荐稍旧没有商业影响）。

**4. STAR 故事中的数字**
本周软技能内容都有很好的数字示例（"20% sprint capacity = 40 工程师周"，"38 人周"，"40 家新客户"）。练习时注意自己的故事有没有类似的量化支撑。

---

## 🏆 Win of the Week / 本周亮点

**回溯模板 Block 过半，且周六 Deep Dive 把零散知识串成了一张完整地图。**

本周最大的收获不是单道题，而是**回溯模板的系统化**：从 Day 88 开始，到本周结束已经掌握了 5 个变体，形成了一张清晰的"遇到什么情况用什么调整"的决策矩阵。Saturday Deep Dive 进一步把 Word Search 在 2D 棋盘上的应用、Trie 优化、N-Queens 的 Hard 级应用全部连接起来——这是从"会做题"到"理解模式"的质变。

另一个亮点：系统设计进入了真正的综合模式——不再是介绍新系统，而是横跨 60 个已学主题做深度对比分析。一致性模型的综合讨论达到了 Principal Engineer 级别的深度。

**你已经完成了 Day 94，正式进入最后冲刺阶段。🎯**

---

## 🎯 Next Week Preview / 下周预告

基于当前 indices（NeetCode 75/150，Frontend 37/50）和回溯模板进度（5/9）：

- **算法**：回溯 Block 后半段（6-9/9）——Permutations II (#47, 有重复的全排列)、Word Search (#79, 2D 回溯)、Palindrome Partitioning (#131)、Letter Combinations of a Phone Number (#17)。深度 Dive 预计是其中的某题 + N-Queens (#51) Hard。
- **前端（Python Craft）**：Week 9 Testing 正式完结，进入 Week 10 新主题（可能是 Performance / Profiling 或 Deployment 相关）。
- **系统设计综合**：从一致性模型深化转向下一个大主题——可能是分布式事务（Saga Pattern、2PC、幂等性）或者系统可观测性（Tracing/Metrics/Logging 三角）。
- **软技能**：继续 Staff/Principal 场景综合。
- **AI**：保持新闻模式，偶尔综合深化（下一个可能的主题：大模型的推理优化 KV Cache / Speculative Decoding 的实际应用）。

Keep it going — you're in the Expert final stretch. 💪
