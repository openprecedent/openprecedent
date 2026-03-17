# 引入记忆效用与上下文成本（memory utility / context cost）评价视角

日期：2026-03-17

英文版本：[引入记忆效用与上下文成本评价视角（英文）](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem/plugmem-memory-utility-evaluation.md)

主分析文档：[PlugMem 与 OpenPrecedent 对照分析](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem/plugmem-openprecedent-analysis.md)

## 目的

研究 OpenPrecedent 是否应该把运行时记忆（runtime memory）的评价，从“有没有命中 / 有没有起作用”进一步扩展为：

- 它提供了多少真正有用的决策价值
- 它为此消耗了多少上下文成本

## 为什么重要

PlugMem 很强调一个很实际的原则：

- 好记忆（memory）不是“存得最多”的记忆（memory）
- 好记忆（memory）是“每单位上下文成本能提供更多决策价值”的记忆（memory）

这对 OpenPrecedent 很重要，因为运行时摘要（runtime brief）本身就在争夺有限的上下文预算（context budget）。

## OpenPrecedent 当前的位置

OpenPrecedent 现在主要看的指标是：

- 有没有触发决策脉络查询（lineage）
- 命中是不是空
- 当前任务有没有受到影响
- 有没有污染（contamination）

这些都很重要，但还少一个维度：

- 检索（retrieval）到底高不高效

## 更强的效用视角（utility 视角）会问什么

如果真的引入效用视角（utility lens），评价会变成：

- 摘要（brief）里的哪些内容后来真的被采用了
- 哪些内容其实是冗余的
- 摘要（brief）消耗了多少上下文
- 最终判断里有多少可以追溯到摘要（brief）
- 一个更短的摘要（brief）是否也能产生相同效果

## 为什么这件事难

这件事比看命中率（hit rate）难，因为：

- 有些摘要（brief）会改变问题框架（framing），但不会被显式引用
- 有些记忆（memory）的价值在于避免错误，而不是直接生成新内容
- 有些长摘要（brief）即使很长，也可能因为避免了高成本错误而仍然值得

所以，这个方向很可能需要混合评价方式：

- 结构化字段
- 人工判断
- 下游结果对比

## 可能的指标方向

可以先从这些方向尝试：

- 摘要（brief）中有多少项后来进入了最终改动或最终判断
- 返回项里有多少被人类评估为与决策相关（decision-relevant）
- 摘要（brief）的 token 数量与最终采用约束数、采用判断数的比例
- 成功轮次（round）中平均有多少无关或未使用项（irrelevant / unused item）

## 与当前研究的关系

这其实是当前第二阶段研究的自然延伸。
OpenPrecedent 现在已经在问：

- 有没有触发
- 有没有用
- 有没有污染

效用视角（utility lens）新增的问题是：

- 它值不值得这份上下文成本

如果未来 OpenPrecedent 转向更细粒度的知识单元检索（knowledge unit retrieval），这个问题会更重要。

## 更合理的下一步

- 先用真实运行时摘要（runtime brief）做轻量人工评分
- 比较几个成功和失败轮次（round）的上下文效率（context efficiency）
- 在真实例子不够多前，不要过早做过度形式化的公式

## 结论

OpenPrecedent 最终应该评价记忆效用（memory utility），而不只是评价检索（retrieval）是否发生、匹配（match）是否非空。
这是 PlugMem 给出的一个非常关键的升级方向，因为它把问题从“记忆（memory）有没有出现”推进到了“记忆（memory）值不值得它占用的上下文成本”。
