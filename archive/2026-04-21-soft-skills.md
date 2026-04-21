# 🗣️ 软技能 / Soft Skills — Day 28
## Build vs Buy Decision Making

> **难度 / Level:** Senior/Staff | **类别 / Category:** Decision Making | **预计阅读 / Read time:** 2 min

---

### 🎯 为什么这个问题很重要 / Why This Question Matters

Build vs buy是每个Senior/Staff工程师都会遇到的战略决策。面试官想看：你会不会权衡**短期成本 vs 长期维护**，**控制权 vs 速度**，**差异化价值 vs 通用功能**。这不只是技术问题，更是工程判断力的体现。

Build vs buy is a strategic decision every Senior/Staff engineer faces. Interviewers want to see: can you weigh **short-term cost vs long-term maintenance**, **control vs speed**, **differentiating value vs commodity functionality**? This tests engineering judgment, not just technical skills.

---

### ⭐ STAR Framework

**Situation / 背景:**
> "我们在构建实时数据管道，需要一个消息队列。团队有人提议自研，也有人提议用Kafka。这是个200万用户的产品，但消息队列不是我们的核心竞争力。"

> "We were building a real-time data pipeline and needed a message queue. Some wanted to build one; others wanted Kafka. 2M users, but messaging wasn't our core differentiator."

**Task / 任务:**
> 评估两个方案的真实成本，给出有数据支撑的建议。

**Action / 行动:**
> 我做了一个快速分析框架：
> 1. **核心 vs 非核心** — 消息队列是通用基础设施，不是我们的差异化竞争力
> 2. **总拥有成本 (TCO)** — 自研：3个工程师×6个月 + 永续维护。Kafka：2周集成 + 运维成本（~$500/月托管服务）
> 3. **风险矩阵** — 自研：稳定性风险、没有社区支持。Kafka：供应商依赖、少量定制限制
> 4. **团队能力** — 没有分布式系统专家，自研风险高

> I built a quick decision framework:
> 1. **Core vs commodity** — message queuing is generic infrastructure, not our differentiation
> 2. **TCO** — build: 3 engineers × 6 months + perpetual maintenance vs buy: 2-week integration + ~$500/month managed service
> 3. **Risk matrix** — build: stability risk, no community. Buy: vendor dependency, some customization limits
> 4. **Team capabilities** — no distributed systems experts on team

> 我建议采用托管Kafka（Confluent Cloud）。节省了约18个工程师月，让团队专注于产品功能。

**Result / 结果:**
> 集成用了两周，比预期早6个月上线。运行了1年没有重大故障。后来我把这个框架整理成团队的"Make vs Buy"决策模板，被多个团队复用。

> Integration took 2 weeks, shipped 6 months early. Zero major incidents in year one. I documented the framework as a team "Make vs Buy" template — adopted by 3 other teams.

---

### ❌ Bad Answer vs ✅ Good Answer

**❌ 踩坑回答:**
> "我们选择了Kafka因为它很流行，大家都在用。"

*问题: 没有展示决策过程，没有权衡，听起来像随大流。*

**✅ 高分回答:**
> "我建立了一个框架来分析核心竞争力、TCO和团队风险，然后带着数据向stakeholders推荐了Kafka。结果节省了18个工程师月，让我们更早交付了用户真正需要的功能。"

---

### 🚀 Senior/Staff级别加分点

1. **量化影响** — 不只说"省了时间"，要说"节省18个工程师月 = $X万美元"
2. **展示框架** — 面试官想看你有可复用的决策方法，不是ad-hoc
3. **考虑长期维护** — "我们今天能构建它，但谁来维护？"
4. **识别错误的build理由** — "我们想完全控制" → 通常是overengineering的信号
5. **何时应该build** — 当功能是核心差异化价值，或有严格合规要求（数据主权），或外部方案有根本性gap

**经典Build vs Buy框架:**
```
Build when:
✅ Core differentiator (your competitive moat)
✅ Existing solutions have fundamental gaps
✅ Compliance/data sovereignty requirements
✅ Team has the expertise + bandwidth

Buy when:
✅ Commodity functionality
✅ No differentiation value
✅ High quality options exist
✅ Speed to market matters
✅ Team lacks domain expertise
```

---

### 💡 Key Takeaways / 核心要点

- 🎯 **不要build ego trip** — "因为自己写的更好" 不是理由
- 📊 **TCO要算全** — 工程时间 + 机会成本 + 永续维护 + 招聘专才
- 🔑 **核心竞争力优先** — 只在用户愿意为之付钱的差异化功能上build
- 📝 **记录决策** — ADR (Architecture Decision Record) 让团队对齐，避免反复争论

---

### 📚 References
- [ADR (Architecture Decision Records) — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Build vs Buy Framework — a16z](https://a16z.com/build-vs-buy/)
- [Stop building commodity features — pragmatic engineering](https://newsletter.pragmaticengineer.com/)

---

### 🧒 ELI5

自己造汽车还是买车？你要上班，开车去。你是汽车专家吗？不是。造车需要多久？1年。买车需要多久？1周。除非你是赛车手（汽车是你的核心竞争力），否则就买！工程决策也一样——把精力放在你做得比别人更好的地方。

Build a car or buy one? You need to get to work. Are you a car expert? No. How long to build? 1 year. Buy? 1 week. Unless you're a race car driver (cars ARE your competitive edge), just buy! Engineering is the same — spend your energy where you're uniquely better than others.
