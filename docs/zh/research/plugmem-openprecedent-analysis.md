# PlugMem 与 OpenPrecedent 对照分析

英文版本：[PlugMem And OpenPrecedent](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem-openprecedent-analysis.md)

## 目的

本文将论文 [PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents](https://arxiv.org/abs/2603.03296) 与微软研究博客 [From raw interaction to reusable knowledge: Rethinking memory for AI agents](https://www.microsoft.com/en-us/research/blog/from-raw-interaction-to-reusable-knowledge-rethinking-memory-for-ai-agents/) 放到 OpenPrecedent 当前的产品和研究背景里进行对照分析。

目的不是单独复述论文，而是判断这项外部研究对 OpenPrecedent 当前这些核心对象意味着什么：

- 原始事件捕获
- 蒸馏后的 decision lineage
- replay 与 explanation
- precedent retrieval
- runtime decision-lineage brief

## 外部研究的核心主张

PlugMem 的核心观点很明确：

- 原始交互历史不适合作为长期记忆的直接检索对象
- 更适合作为长期记忆的是可复用知识，而不是冗长轨迹
- memory 的任务应是为决策提供紧凑、结构化、可复用的知识
- 如果结构、检索和推理方式设计得好，一个通用 memory 模块可以优于 raw retrieval baseline，甚至优于某些 task-specific memory system

微软研究博客对同一观点的表达更直接：

- 事件本身不是最好的复用单位
- 事实与可复用技能比原始轨迹更适合作为记忆单位
- 更重要的问题不是 memory 的体量，而是它以多少上下文成本提供了多少决策价值

这与 OpenPrecedent 当前的问题高度相关，因为 OpenPrecedent 已经开始主动区分：

- 过程证据
- 可复用判断

## 与 OpenPrecedent 的强一致点

### 1. 原始历史是必要层，但不是最终记忆层

OpenPrecedent 已经把 raw history 视为 evidence layer，而不是最终 memory product。

当前方向已经很清楚：

- `event` 记录过程证据
- `decision` 记录可复用判断

这与 PlugMem 的主张一致：原始 episodic trace 必须先被转换成可复用知识，才更适合作为长期记忆。

### 2. 复用应服务于判断，而不是服务于机械 replay

OpenPrecedent 当前已经排除了这些内容进入 decision：

- tool choice
- file writes
- command execution
- retry mechanics

这与 PlugMem 从 raw trajectory 转向 compact reusable knowledge 的方向是一致的。两者都强调：

- 记忆单位要紧凑
- 记忆单位要与判断相关
- evidence 与 reusable knowledge 要分层

### 3. 检索质量比存量大小更关键

PlugMem 强调：如果检索出来的是冗长、低价值、弱相关内容，memory 越大反而可能越差。

OpenPrecedent 最近的真实项目研究也看到类似现象：

- 问题不只是历史太少
- 更关键的是返回内容是否相关、可复用、不过度污染

所以，PlugMem 对 utility 而不是 volume 的强调，强化了 OpenPrecedent 当前的 post-MVP 研究方向。

### 4. Runtime memory 必须足够紧凑，才能真正影响行动

PlugMem 检索的是压缩后的知识，再交给 agent 使用。

OpenPrecedent 当前 runtime brief 的作用也类似，返回的是：

- accepted constraints
- cautions
- rejected options
- authority signals
- task frame

这些都不是 transcript replay，而是用于收窄当前行动空间的紧凑输出。

## 它对 OpenPrecedent 的挑战

### 1. OpenPrecedent 目前仍以 case 作为主要检索单位

现在 OpenPrecedent 的 precedent retrieval 仍主要从 historical case 出发，再从 case 中提炼 decision-lineage summary。

这对 replay 和 explanation 有帮助，但相比 PlugMem，粒度仍偏粗。PlugMem 更强调 memory 应围绕 reusable knowledge unit，而不是整条历史 episode 来组织。

因此这里出现了一个真实张力：

- replay 需要 case-centered narrative
- runtime reuse 可能更需要 finer-grained knowledge-centered access path

### 2. OpenPrecedent 还没有明确区分 fact-like knowledge 与 prescriptive knowledge

PlugMem 明确区分：

- propositional knowledge
- prescriptive knowledge

而 OpenPrecedent 当前的 semantic decision taxonomy 还没有清楚地区分：

- 稳定的事实性知识
- 可迁移的处方式判断

这个区分会直接影响 extraction 和 retrieval 的质量。

### 3. OpenPrecedent 还没有系统评估 utility 与 context cost 的关系

现在 OpenPrecedent 主要看的是：

- 有没有触发 retrieval
- 命中是不是空
- 当前工作有没有受到影响
- 是否出现 contamination

这些已经有研究价值，但还不足以回答：

- 每一单位 runtime context 到底贡献了多少真正有用的决策信号

### 4. PlugMem 的 task-agnostic generality 比 OpenPrecedent 当前应采取的姿态更激进

PlugMem 把自己定义成 task-agnostic plugin memory module。

OpenPrecedent 到目前为止一直有意避免过早走向这种泛化 platform abstraction，这个克制仍然是对的。当前产品价值仍来自：

- local-first development
- issue-scoped research
- repository-grounded evidence
- concrete runtime validation

## 最重要的产品含义

这篇论文给 OpenPrecedent 最重要的启发是：

OpenPrecedent 应继续坚持把 raw event capture 与 reusable memory 当作两个不同层，但 reusable layer 不应只被理解为 case summary，而应更明确地被设计成一个 knowledge substrate。

这并不意味着放弃 case。
更准确地说，OpenPrecedent 现在其实有两个不同的产品任务：

1. 通过 case 与 event 保留可审计的 replay 能力
2. 通过更紧凑、更可复用的知识单位支撑 runtime reuse

PlugMem 强化了一个观点：
这两个任务可以共享 evidence，但不一定必须共享完全相同的 retrieval unit。

## OpenPrecedent 现在应继续保留的东西

### 1. 保留 replayability 与 evidence lineage

PlugMem 的 knowledge-first framing 很强，但 OpenPrecedent 的 case + replay 模型也是非常重要的优势。

研究、审查和调试仍然需要回答：

- 结论从哪里来
- 依据了哪些 evidence events
- 当时的完整上下文是什么

因此，即便未来转向更知识化的 retrieval，case 与 event 仍应是 audit substrate。

### 2. 保留对 operational behavior 进入 precedent 的限制

这篇论文不是在削弱 OpenPrecedent 当前的 semantic decision refocus，反而是在强化它：

- operational trace 应是 evidence
- reusable judgment 才应成为 precedent

### 3. 保持 issue-scoped、repository-grounded 的研究方式

PlugMem 的 task-agnostic 成功是强烈的研究信号，但 OpenPrecedent 仍应通过 issue-scoped、repository-grounded 的方式继续验证，而不是直接跳成泛化 memory platform。

## OpenPrecedent 可能应新增的方向

### 1. 在 case 之上增加更明确的 reusable-knowledge layer

OpenPrecedent 可以考虑显式建模一个不等同于 case 的 reusable knowledge layer。

可能方向包括：

- 从重复 case 中抽出的 fact-like repository / environment knowledge
- 从成功决策模式中蒸馏出的 prescriptive guidance unit
- 与 supporting case / event evidence 的 typed link

### 2. 在 decision lineage 内部增加事实与处方的区分

当前 decision taxonomy 已经比旧模型更强，但还没有显式区分：

- stable factual knowledge
- reusable prescriptive judgment

### 3. 把 evaluation 从 hit rate 扩展到 information density

OpenPrecedent 可以逐步补充这些问题：

- runtime brief 的哪些内容真正被使用了
- 返回内容里哪些是 decision-relevant，哪些是冗余
- brief 消耗的上下文成本与其决策价值是否匹配

### 4. 引入小于 case 的 retrieval unit，同时保留 case-level replay

OpenPrecedent 不需要一下子抛弃 case retrieval。
但可以逐步考虑让 runtime retrieval 更多返回：

- specific distilled decision unit
- reusable constraint
- reusable rejected option
- stable authority boundary

而不是每次都把 case 作为默认最高层 memory object。

## 论文没有替我们解决的问题

PlugMem 并没有替 OpenPrecedent 解决这些关键问题：

- 如何让 reusable knowledge 继续可追溯到具体 event evidence
- 如何控制 partially related prior cases 带来的 contamination
- 如何表达 repository-specific knowledge，而不伪装成“普遍 task-agnostic”
- 如何在 aggressive compression 的同时保住 replay 与 explanation 的价值

因此，OpenPrecedent 应把 PlugMem 当成强研究信号，而不是现成替代方案。

## 相关 follow-up 文档

四个最值得继续拆开的方向，已经分别整理成独立说明文档：

1. [在 case 之上增加更明确的 reusable-knowledge layer](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-reusable-knowledge-layer.md)
2. [在 decision lineage 中区分事实型知识与处方式知识](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-fact-vs-prescription.md)
3. [引入 memory utility / context cost 评价视角](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-memory-utility-evaluation.md)
4. [引入小于 case 的 retrieval unit，同时保留 case-level replay](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-fine-grained-retrieval-units.md)

## 总结

PlugMem 并没有推翻 OpenPrecedent 当前的方向，反而在很大程度上确认了我们已经做出的关键修正：

- raw trace 是 evidence
- reusable memory 应该是紧凑、结构化、与判断相关的知识

但它也明显提高了标准。
如果 OpenPrecedent 想真正把 post-MVP research phase 做深，就不能只停留在 case-centered precedent lookup，而需要把 reusable knowledge unit 作为一等设计问题来对待，同时保留自身在 replay 与 evidence lineage 上的优势。
