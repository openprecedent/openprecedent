# 在案例（case）之上增加更明确的可复用知识层（reusable-knowledge layer）

英文版本：[在案例之上增加更明确的可复用知识层（英文）](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem-reusable-knowledge-layer.md)

主分析文档：[PlugMem 与 OpenPrecedent 对照分析](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-openprecedent-analysis.md)

## 目的

聚焦 PlugMem 提出的一个核心设计问题：

OpenPrecedent 是否应该在原始事件历史（raw event history）之上、案例对象（case）之外，再显式增加一层可复用知识层（reusable knowledge layer）？

## 为什么重要

OpenPrecedent 目前以案例（case）作为主要对象，有几个明显优点：

- 便于回放（replay）
- 便于解释（explanation）
- 便于证据脉络追踪（evidence lineage）
- 便于保留完整历史叙事

但案例（case）同时也是一个比较大、比较混杂的单位。
对于运行时复用（runtime reuse）来说，它可能太粗了。

PlugMem 的启发是：长期可复用记忆（memory）更应围绕紧凑知识单位来组织，而不是围绕完整历史片段（episode）来组织。

## OpenPrecedent 当前的位置

OpenPrecedent 其实已经完成了第一步分层：

- 事件（`event`）是过程证据
- 决策（`decision`）是可复用判断

但它还没有真正把“可复用知识层”作为一个显式对象建模出来。
当前运行时检索（runtime retrieval）仍然主要从案例（case）出发。

## 可能的对象形态

如果要加这层可复用知识（reusable knowledge），最合理的形态不应是抽象记忆块（memory blob），而更像这些东西：

- 从重复案例（case）中抽出的稳定事实知识
- 经常重复出现的可复用约束（reusable constraint）
- 值得重复继承的被拒绝选项（rejected option）
- 可复用的权威边界（authority boundary）
- 从成功决策模式中蒸馏出来的处方式指导（prescriptive guidance）

这些单位都应该继续能追溯到：

- 支撑性决策（supporting decision）
- 支撑性案例（supporting case）
- 支撑性事件（supporting event）

这样才不会把回放（replay）和审计（audit）能力丢掉。

## 为什么它优于直接复用案例（case）

直接用案例（case）检索仍然有价值，但它的问题是运行时检索（runtime retrieval）为了拿到一点有用指导（guidance），往往要同时携带：

- 很多叙事性上下文
- 混杂的证据类型
- 对回放（replay）有价值、但对当前行动未必有价值的背景信息

如果增加可复用知识层（reusable-knowledge layer），OpenPrecedent 就有机会做到：

- 案例（case）继续负责回放（replay）
- 知识单元（knowledge unit）负责运行时复用（runtime reuse）

## 主要风险

这里最大的风险有：

- 抽象过头，导致知识单元（knowledge unit）失去可审计性
- 和现有决策（decision）结构重复，但没有增加真实检索（retrieval）价值
- 过早脱离仓库特定或案例特定上下文（repository-specific / case-specific）
- 走成一个泛化记忆存储（memory store），而不是继续服务当前产品边界

## 值得继续研究的问题

- 哪些知识单位足够稳定，值得跨案例（case）复用
- 哪些单位应该显式物化，哪些应在检索（retrieval）时动态生成
- 这层知识应来自重复案例（case）归纳，还是来自单案例（case）高质量蒸馏
- 如何保持每个知识单元（knowledge unit）与证据（evidence）的强连接

## 更合理的下一步

- 先把它当成研究设计问题（research design question），而不是马上做模式重构（schema 重构）
- 先用少量真实检索（retrieval）案例测试几种知识单位形状
- 再评估它是否真的比以案例为中心的检索（case-centered retrieval）更紧凑、更有用

## 结论

OpenPrecedent 很可能应该继续保留案例（case）作为回放单位（replay unit），但认真研究在案例（case）之上增加可复用知识层（reusable-knowledge layer），作为运行时复用（runtime reuse）的主要对象。
这是 PlugMem 给 OpenPrecedent 最强、也最可操作的启发之一。
