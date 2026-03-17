# 在决策脉络（decision lineage）中区分事实型知识与处方式知识

日期：2026-03-17

英文版本：[在决策脉络中区分事实型知识与处方式知识（英文）](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem/plugmem-fact-vs-prescription.md)

主分析文档：[PlugMem 与 OpenPrecedent 对照分析](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem/plugmem-openprecedent-analysis.md)

## 目的

评估 OpenPrecedent 是否应该在语义决策模型（semantic decision model）内部显式区分：

- 事实型可复用知识（fact-like reusable knowledge）
- 处方式可复用知识（prescriptive reusable knowledge）

## 为什么重要

PlugMem 明确区分：

- 命题性知识（propositional knowledge）
- 处方式知识（prescriptive knowledge）

这个区分的重要性在于，很多记忆系统（memory system）的失败，正是因为它混淆了：

- 什么是真的
- 什么是应该做的

两者都重要，但它们不是同一种可复用资产。

## OpenPrecedent 当前的位置

OpenPrecedent 已经有语义决策分类（semantic decision taxonomy），但它还没有明确地区分：

- 关于仓库、环境、上下文的稳定事实
- 在类似情境下推荐采取的判断或行动方式

这会让检索结果（retrieval result）更容易混在一起，比如一个摘要（brief）同时携带：

- 事实（facts）
- 约束（constraints）
- 规范（norms）
- 建议（advice）

但内部没有清晰边界。

## 为什么这个区分可能有帮助

显式区分之后，可能会改善：

- 抽取质量（extraction quality）
- 检索精度（retrieval precision）
- 运行时摘要（runtime brief）的组织方式
- 污染控制（contamination control）

原因是：

- 事实型知识（fact-like knowledge）的迁移风险通常更低
- 处方式知识（prescriptive knowledge）的误迁移风险通常更高

## 一个简单例子

事实型知识（fact-like knowledge）：

- 仓库采用单议题单分支（one issue per branch）
- 某个运行时路径（runtime path）共享在固定目录（home）下
- 某个清单字段（manifest field）有稳定语义

处方式知识（prescriptive knowledge）：

- 在重大实现前先做 `initial_planning`
- 不要把当前任务扩大成大规模架构重写
- 把已合并分支复用（merged branch reuse）视为护栏违规（guardrail violation）

这两类信息都可能来自同一个案例（case），但它们不一定应该用相同方式存储、排序、呈现。

## 风险

- 过早建模，导致分类法（taxonomy）复杂度上升
- 某些边界项很难强行归类
- 抽取（extraction）复杂度提高，但评估（evaluation）还没跟上

## 值得继续研究的问题

- 这个区分应该体现在分类法（taxonomy）、元数据（metadata），还是只体现在检索（retrieval）时
- 现有语义决策类型（semantic decision type）里哪些更偏事实，哪些更偏处方
- 事实/处方拆分（fact/prescription split）是否真能降低运行时摘要（runtime brief）的污染（contamination）

## 更合理的下一步

- 先在分析和评估（evaluation）层测试这个区分，而不是马上改模式（schema）
- 在真实摘要（brief）上做人类分类，看看当前检索（retrieval）内容天然会不会分成这两类
- 再决定是否要上升为正式分类法（taxonomy）变化

## 结论

这是 PlugMem 给出的一个非常高杠杆启发。
它比“全面重构记忆模型（memory 模型）”更窄，但可能对抽取（extraction）、检索（retrieval）和污染控制（contamination control）都有直接帮助。
