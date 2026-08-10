# 🗣️ 软技能综合 / Soft Skills Synthesis — Day 111

## 场景：你的团队刚完成一次重大架构迁移，但上线后发现性能比预期差 30%。CEO 问你怎么回事。
## Scenario: Your team just completed a major architecture migration, but post-launch performance is 30% worse than expected. The CEO asks what happened.

---

## 为什么这个场景难 / Why This Is Hard

这不是普通的"tell me about a failure"——这需要你同时展示：
This isn't a standard "tell me about a failure" — you need to demonstrate:
1. 技术判断力 (technical judgment)
2. 透明度 + 不甩锅 (transparency without blame-shifting)
3. 向上沟通的能力 (executive communication under pressure)
4. 从数据出发的问题定位 (data-driven diagnosis)

---

## STAR 分解 / STAR Framework

**Situation (情境)**
> 我们迁移了核心订单服务从单体到微服务架构，上线后 P99 延迟从 200ms 升到 320ms。

**Task (任务)**
> 需要立刻向 CEO 解释，同时启动诊断并给出恢复计划。

**Action (行动)**
> 1. **先承认，不辩解：** "我们发现了一个预期外的性能问题，这是我们的责任。"
> 2. **提供数据，不猜测：** "我们看到的具体指标是...原因初步定位为网络跳数增加和 serialization overhead。"
> 3. **给出时间表：** "48小时内我们会有根因分析，72小时内会有修复方案。"
> 4. **回溯决策链：** 复盘我们的 load testing 在哪个阶段漏了这个场景

**Result (结果)**
> 3天内通过连接池复用和 gRPC 替换 REST 将延迟降至 190ms，比迁移前还快 5%。

---

## ❌ 别这样说 / What NOT to Say
- ❌ "这是因为 DevOps 没有配置好 k8s 参数" → 甩锅
- ❌ "当时我们时间不够，没法做更好的测试" → 找借口
- ❌ "这个性能问题不是很严重" → 淡化问题

## ✅ 这样更好 / What Works
- ✅ 用具体数字说话："P99 从 200ms 涨到 320ms，QPS 高峰期影响约 8% 的用户"
- ✅ 区分"已知/已做"和"漏掉了什么"："我们做了单服务压测，但漏了跨服务串联场景"
- ✅ 展示后续改进："我们在 post-mortem 中新增了跨服务集成压测环节"

---

## Staff+ 视角 / Senior/Staff Level Tips

**向上沟通的艺术：**
- CEO 不需要技术细节，需要：影响面 + 恢复时间 + 根因 + 你是否掌控了局面
- 永远先给结论，再给细节（Pyramid Principle）
- 承认不确定性，但承诺什么时候会有更多信息

**技术上的教训：**
- 微服务迁移必须做 **chaos engineering** 和 **end-to-end load test**，不只是单元/单服务压测
- 建立迁移 checklist：network hops、serialization format、connection pooling

---

## Key Takeaways
1. 危机时刻：先控制局面，给时间表，不找借口
2. 数据说话：永远有具体指标，不说"有点慢"
3. 后续提升比当时完美更重要：展示系统性改进，不是补丁式修复

---

## 📚 References
- https://sre.google/sre-book/postmortem-culture/
- https://www.kitchensoap.com/2012/10/25/on-being-a-senior-engineer/

## 🧒 ELI5
就像你打破了妈妈的花瓶：好的做法是马上说"我打破了，是我不小心，我来扫地，下次我会更注意"，而不是说"是风吹倒的"或者"花瓶本来就很脆"。
