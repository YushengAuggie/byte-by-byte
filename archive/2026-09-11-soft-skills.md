# 🗣️ 软技能 / Soft Skills — Day 132 (Synthesis)
**综合场景：你如何拆解并交付一个"没有明确终点"的平台项目？**
**Synthesis: How do you scope and ship a platform project with no clear end state?**

---

## 为什么这道题特别难 / Why This Is Hard

平台类项目（内部工具、开发者平台、基础设施重构）最大的挑战是：没有"完成"的定义。你既不能无休止地建设，也不能过早宣布完成后留下一堆未覆盖的用例。Senior/Staff 工程师在这里最容易暴雷。

Platform projects (internal tooling, dev platforms, infra rewrites) are uniquely hard: there's no natural "done." You can't build forever, and you can't declare victory too early. This is where senior engineers often stumble.

---

## STAR 框架 / STAR Breakdown

**场景设定 / Situation:**
> "我们的服务部署系统是一堆 bash 脚本，20+ 个团队各自维护自己的 fork，重复逻辑遍地都是。我被指派重建它，但没有截止日期，也没有明确的 scope。"

**任务 / Task:**
定义什么是"足够好"，在不阻塞其他团队的前提下交付，同时持续迭代。

**行动 / Action:**
1. **先做用户调研**——和 5 个团队各 30 分钟，找 pain points 的交集
2. **定义 v1 的 done criteria**——"80% 的团队能用，剩下 20% 有清晰 migration path"
3. **公开 roadmap**——让所有 stakeholders 知道 v1 包含什么、不包含什么，减少"为什么没有 X"的摩擦
4. **先迁移最大的 2 个团队**——快速建立信心和真实 feedback
5. **设置 sunset date 给旧系统**——没有截止日期，没人会迁移

**结果 / Result:**
6 个月内完成核心迁移，旧系统正式 deprecated，团队从平均 45min 部署时间降到 8min。

---

## ❌ 坏回答 vs ✅ 好回答

❌ "我们尽量覆盖所有用例，持续迭代改进。"
— 没有边界，听起来永远做不完，面试官不知道你会交付什么

✅ "我主动定义了 v1 的成功标准，明确了不在 scope 的内容，并设置了旧系统的 sunset date 来推动迁移。"
— 展示了 ownership + 清晰的 decision-making + 结果导向

---

## Senior/Staff 加分点

- **主动定义 done**，而不是等别人告诉你
- **公开不做什么**（explicit non-goals）和做什么同样重要
- **用 sunset date 制造urgency**——内部迁移没有外部压力，必须自己创造
- **把平台的成功与用户的成功绑定**——Deploy 时间减少 = 平台成功，而不是"我们上线了新系统"

---

## Key Takeaways

1. **没有截止日期的项目 = 最难管理的项目**，先定义 done criteria
2. **Migration 必须有 deadline**，否则旧系统永远死不了
3. **明确 non-goals**，减少 scope creep 和 stakeholder 摩擦
4. **先找 top pain points**，别从技术最有趣的地方开始

---

## 📚 References
- https://lethain.com/staff-engineer-archetypes/ — Will Larson 的 Staff Engineer 视角
- https://martinfowler.com/bliki/StranglerFigApplication.html — Martin Fowler 平台迁移模式
- https://increment.com/teams/the-epistemology-of-software-quality/

## 🧒 ELI5
如果你要重建乐高城，最怕的是没有"城建完了"的标准。聪明的做法是先定好"哪几栋楼建好了就算第一期完成"，再设个"旧城墙拆掉的日期"，不然大家都不搬新家。
Building a new city from scratch is hard when "done" is undefined. Smart engineers define what v1 looks like, announce when the old city gets torn down, and don't try to build everything at once.
