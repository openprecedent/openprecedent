# 在 case 之上增加更明确的 reusable-knowledge layer

英文版本：[PlugMem Follow-Up: A Reusable-Knowledge Layer Above Cases](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem-reusable-knowledge-layer.md)

主分析文档：[PlugMem 与 OpenPrecedent 对照分析](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-openprecedent-analysis.md)

## 目的

聚焦 PlugMem 提出的一个核心设计问题：

OpenPrecedent 是否应该在 raw event history 之上、case 对象之外，再显式增加一层 reusable knowledge layer？

## 为什么重要

OpenPrecedent 目前以 case 作为主要对象，有几个明显优点：

- 便于 replay
- 便于 explanation
- 便于 evidence lineage
- 便于保留完整历史叙事

但 case 同时也是一个比较大、比较混杂的单位。
对于 runtime reuse 来说，它可能太粗了。

PlugMem 的启发是：长期可复用 memory 更应围绕紧凑知识单位来组织，而不是围绕完整历史 episode 来组织。

## OpenPrecedent 当前的位置

OpenPrecedent 其实已经完成了第一步分层：

- `event` 是过程证据
- `decision` 是可复用判断

但它还没有真正把“可复用知识层”作为一个显式对象建模出来。
当前 runtime retrieval 仍然主要从 case 出发。

## 可能的对象形态

如果要加这层 reusable knowledge，最合理的形态不应是抽象 memory blob，而更像这些东西：

- 从重复 case 中抽出的稳定事实知识
- 经常重复出现的 reusable constraint
- 值得重复继承的 rejected option
- 可复用的 authority boundary
- 从成功决策模式中蒸馏出来的 prescriptive guidance

这些单位都应该继续能追溯到：

- supporting decision
- supporting case
- supporting event

这样才不会把 replay 和 audit 能力丢掉。

## 为什么它优于直接复用 case

直接用 case 检索仍然有价值，但它的问题是 runtime retrieval 为了拿到一点有用 guidance，往往要同时携带：

- 很多叙事性上下文
- 混杂的证据类型
- 对 replay 有价值、但对当前行动未必有价值的背景信息

如果增加 reusable-knowledge layer，OpenPrecedent 就有机会做到：

- case 继续负责 replay
- knowledge unit 负责 runtime reuse

## 主要风险

这里最大的风险有：

- 抽象过头，导致 knowledge unit 失去可审计性
- 和现有 decision 结构重复，但没有增加真实 retrieval 价值
- 过早脱离 repository-specific / case-specific 上下文
- 走成一个泛化 memory store，而不是继续服务当前产品边界

## 值得继续研究的问题

- 哪些知识单位足够稳定，值得跨 case 复用
- 哪些单位应该显式物化，哪些应在 retrieval 时动态生成
- 这层知识应来自重复 case 归纳，还是来自单 case 高质量蒸馏
- 如何保持每个 knowledge unit 与 evidence 的强连接

## 更合理的下一步

- 先把它当成 research design question，而不是马上做 schema 重构
- 先用少量真实 retrieval 案例测试几种知识单位形状
- 再评估它是否真的比 case-centered retrieval 更紧凑、更有用

## 结论

OpenPrecedent 很可能应该继续保留 case 作为 replay 单位，但认真研究在 case 之上增加 reusable-knowledge layer，作为 runtime reuse 的主要对象。
这是 PlugMem 给 OpenPrecedent 最强、也最可操作的启发之一。
