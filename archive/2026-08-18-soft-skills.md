# 🗣️ 软技能 / Soft Skills — 综合题：当你同时是技术专家和团队领导

*综合主题：技术影响力 × 跨团队协作 × 工程文化*

---

## 场景题 (Staff+ 级别)

> "You're a senior/staff engineer. A junior team has shipped a service you'll need to integrate with. The API design is poor — inconsistent naming, no versioning, missing error codes. They've already deployed it to prod and have customers. How do you handle this?"

这题考察的不是对错，而是你如何在**不打击积极性、不造成冲突**的前提下推动改进。

---

## STAR 拆解

**Situation**: 外部团队已上线，API 质量有问题，但他们有用户。

**Task**: 作为集成方，你需要既能短期解决问题，又要长期推动改善。

**Action**:
1. **先建关系，再提问题** — 约 1:1，以"我想更好地理解你们的设计决策"开场，不要直接指出错误
2. **用数据说话** — "我在集成时遇到这些具体问题，影响了 X"
3. **提供方案，而非只有批评** — 准备一个 API 改进草稿，主动说"我可以帮忙写文档/设计新版本"
4. **提议增量路径** — 建议引入 `/v2` 端点，保持向后兼容，给老用户迁移时间

**Result**: 团队愿意接受，因为你给的是**帮助**，不是评判。新版本在下个季度上线。

---

## ❌ Bad vs ✅ Good

❌ "这个 API 设计得很差，需要重新设计。"  
✅ "我发现集成时有几个摩擦点，我整理了一个建议清单——你觉得哪些可以优先考虑？"

❌ 在工程全组会议上提 → 让对方当众难堪  
✅ 先私下沟通，达成共识后再拉更多人

---

## Senior/Staff 级别额外考虑

- **技术标准 vs 人际关系**：你的工作是提升整个组织的工程质量，但方式决定结果
- **时间跨度**：短期 → 在自己这侧写 adapter 层屏蔽问题；长期 → 推动团队建立 API Review 流程
- **向上管理**：如果对方团队不配合，何时应该升级？（答：只在有业务风险时）

---

## Key Takeaways

1. 技术问题 + 人际问题要分开处理，先解决人际
2. 带着方案去，不要只带问题
3. Staff 的杠杆在于影响力，不在于权威

---

## 📚 References
- https://staffeng.com/guides/work-on-what-matters
- https://www.amazon.com/Staff-Engineer-Leadership-beyond-management/dp/1736417916

## 🧒 ELI5
就像新同学搭的积木城堡有点歪，你不能直接推倒，而是笑着说"我们一起让它更稳固吧"，然后帮他一起加固。这样城堡变好了，友谊也在。
