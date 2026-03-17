# 引入小于 case 的 retrieval unit，同时保留 case-level replay

英文版本：[PlugMem Follow-Up: Smaller Retrieval Units Without Losing Replay](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem-fine-grained-retrieval-units.md)

主分析文档：[PlugMem 与 OpenPrecedent 对照分析](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-openprecedent-analysis.md)

## 目的

评估 OpenPrecedent 是否应该在 runtime retrieval 时引入“小于 case 的检索单位”，同时保留 case 作为 replay 与 audit 的核心对象。

## 为什么重要

OpenPrecedent 现在的 precedent model 仍然明显偏 case-centered。
这对 explanation 很有帮助，但对 live reuse 来说可能偏粗。

PlugMem 的启发是：
如果 retrieval unit 更接近 reusable knowledge，而不是整段历史 episode，memory 往往会更有用。

## OpenPrecedent 当前的张力

OpenPrecedent 现在同时承担两个任务：

1. replay 一个决策的完整历史
2. 在 live task 中返回足够紧凑的 guidance

这两个任务不一定应该共享完全相同的 retrieval unit。

- case 很适合第一个任务
- 但未必最适合第二个任务

## 可能的更小单位

比较合理的小单位可能包括：

- 一条 reusable constraint
- 一条 reusable rejected option
- 一条 authority boundary
- 一条 distilled decision judgment
- 一条 stable factual statement

这些单位不是拿来替代 case，而是为 case 的可复用部分提供更细粒度的访问路径。

## 为什么更小单位可能更好

更小的 retrieval unit 可能带来这些好处：

- 减少无关叙事负担
- 提高 retrieval precision
- 让 runtime brief 更紧凑
- 让排序问题从“哪个 case 最像”转向“哪个具体知识单位最有用”

此外，它还可以更自然地把多个历史 case 的证据组合起来。

## 主要风险

- 单位太小，导致上下文丢失过多
- 返回的碎片单独看成立，但脱离原始边界条件后容易误导
- 把产品做成 generic vector store，而弱化 evidence-grounded precedent system 的边界

## 值得继续研究的问题

- 检索单位要小到什么程度才有用，但又不至于失真
- 小单位排序是否真的比 case-centered 排序更有帮助
- runtime 应返回“单位本身”，还是“单位 + supporting case reference”
- 在压缩 retrieval 的同时，如何保住 replayability 与 auditability

## 更合理的下一步

- 先在 retrieval / brief-construction 层做实验，而不是一下子改整个产品模型
- 在同一类任务上比较 case-centered brief 和 unit-centered brief
- 要求每个返回单位都保留 supporting case reference，避免 replay 断裂

## 结论

OpenPrecedent 很可能应继续保留 case 作为 replay 单位，但不应默认 case 也必须永远是 runtime retrieval 的唯一单位。
这是 PlugMem 对 OpenPrecedent 下一阶段设计提出的最直接问题之一。
