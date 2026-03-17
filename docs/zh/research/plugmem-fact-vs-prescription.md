# 在 decision lineage 中区分事实型知识与处方式知识

英文版本：[PlugMem Follow-Up: Fact-Like Versus Prescriptive Knowledge](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem-fact-vs-prescription.md)

主分析文档：[PlugMem 与 OpenPrecedent 对照分析](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-openprecedent-analysis.md)

## 目的

评估 OpenPrecedent 是否应该在 semantic decision model 内部显式区分：

- fact-like reusable knowledge
- prescriptive reusable knowledge

## 为什么重要

PlugMem 明确区分：

- propositional knowledge
- prescriptive knowledge

这个区分的重要性在于，很多 memory system 的失败，正是因为它混淆了：

- 什么是真的
- 什么是应该做的

两者都重要，但它们不是同一种可复用资产。

## OpenPrecedent 当前的位置

OpenPrecedent 已经有 semantic decision taxonomy，但它还没有明确地区分：

- 关于仓库、环境、上下文的稳定事实
- 在类似情境下推荐采取的判断或行动方式

这会让 retrieval 结果更容易混在一起，比如一个 brief 同时携带：

- facts
- constraints
- norms
- advice

但内部没有清晰边界。

## 为什么这个区分可能有帮助

显式区分之后，可能会改善：

- extraction quality
- retrieval precision
- runtime brief 的组织方式
- contamination control

原因是：

- fact-like knowledge 的迁移风险通常更低
- prescriptive knowledge 的误迁移风险通常更高

## 一个简单例子

事实型知识：

- 仓库采用 one issue per branch
- 某个 runtime path 共享在固定 home 下
- 某个 manifest field 有稳定语义

处方式知识：

- 在重大实现前先做 `initial_planning`
- 不要把当前任务扩大成大规模架构重写
- 把 merged branch reuse 视为 guardrail violation

这两类信息都可能来自同一个 case，但它们不一定应该用相同方式存储、排序、呈现。

## 风险

- 过早建模，导致 taxonomy 复杂度上升
- 某些边界项很难强行归类
- extraction 复杂度提高，但 evaluation 还没跟上

## 值得继续研究的问题

- 这个区分应该体现在 taxonomy、metadata，还是只体现在 retrieval 时
- 现有 semantic decision type 里哪些更偏事实，哪些更偏处方
- fact/prescription split 是否真能降低 runtime brief 的 contamination

## 更合理的下一步

- 先在分析和 evaluation 层测试这个区分，而不是马上改 schema
- 在真实 brief 上做人类分类，看看当前 retrieval 内容天然会不会分成这两类
- 再决定是否要上升为正式 taxonomy 变化

## 结论

这是 PlugMem 给出的一个非常高杠杆启发。
它比“全面重构 memory 模型”更窄，但可能对 extraction、retrieval 和 contamination control 都有直接帮助。
