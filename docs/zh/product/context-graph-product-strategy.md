# Context Graph 产品战略工作文档

## 文档信息

- 文档类型：产品战略工作文档
- 主题：Context Graph 决策图谱基础设施
- 版本：v1
- 日期：2026-03-08
- 状态：Active
- 归档材料：
  - 原始研究材料：[/workspace/01-product/99-archive/context-graph/source-materials](/workspace/01-product/99-archive/context-graph/source-materials)
  - 中间分析材料：[/workspace/01-product/99-archive/context-graph/working-materials](/workspace/01-product/99-archive/context-graph/working-materials)
  - 汇报与导出材料：[/workspace/01-product/99-archive/context-graph/review-materials](/workspace/01-product/99-archive/context-graph/review-materials)

## 维护说明

这份文档是 Context Graph 方向唯一持续维护的工作文档。

- 后续讨论、判断和结论只更新这一个文件
- 原始研究材料归档保存，不作为持续维护对象
- 中间分析稿、MVP 草稿、汇报稿和导出件统一归档，不再同步更新
- 如需追溯来源或旧稿，只查看本节列出的归档目录

## 一句话定义

Context Graph 是一层位于 Agent 执行路径上的决策记录与复用基础设施，用来把“为什么这样决策”沉淀成可追溯、可审计、可复用的组织资产。

## 执行摘要

2025 到 2026 年的官方产品动态已经足够清楚地表明一件事：Agent 观测、Tracing、Memory、Graph RAG 和治理能力正在快速进入主流产品栈，但这些能力仍然被分散在不同层中。[S1][S2][S3][S4][S5][S6][S7][S8][S9]

基于现有证据，可以做出三个判断：

1. 事实层面：Agent observability 已成为基础能力，而不是差异化能力。OpenAI、AWS、Microsoft、IBM、LangChain、Braintrust 都已经公开提供 tracing、监控或治理能力。[S1][S2][S3][S4][S5][S6]
2. 事实层面：Graph / temporal memory 已经证明对长期记忆和复杂检索有价值，但主流方案仍主要服务于 memory 或 RAG，而不是企业级决策谱系。[S7][S8][S9]
3. 推断层面：真正的产品空白不在“再做一个 observability 平台”或“再做一个 graph store”，而在把跨系统决策过程以可编辑、可复用、可审计的图谱形式沉淀下来，并直接服务未来决策。

因此，本产品第一阶段不应以“通用图数据库”或“通用可观测性”定位进入市场，而应以“决策可见性 + 决策审计 + 历史先例复用”切入高价值垂直场景。

## 1. 背景与 Why Now

### 1.1 已经被市场验证的方向

根据截至 2026-03-08 可公开访问的官方资料：

- OpenAI Agents SDK 已把“保留完整 trace”作为 agentic application 的基础能力来表述。[S1]
- AWS Bedrock AgentCore 已提供内建 metrics、spans、logs，并要求通过 ADOT / OpenTelemetry 补充更完整观测数据。[S2][S3]
- Microsoft Foundry 已支持对 Microsoft Agent Framework、Semantic Kernel、LangChain、LangGraph、OpenAI Agent SDK 做 tracing 集成，并在界面中展示 ordered run steps、tool calls、inputs/outputs。[S4]
- IBM watsonx Orchestrate 已把 agent governance 和 observability 作为独立产品价值来销售，并强调 metrics、policy controls、monitoring、latency、drift、OpenTelemetry 接入。[S5]
- LangSmith 和 Braintrust 都把 tracing、monitoring、dashboards、alerts、feedback、evaluation 作为一体化工作流的一部分。[S6][S10]

这说明一件事：行业已经接受“Agent 必须可观测”，但行业尚未完成“决策过程必须可沉淀和可复用”这一步。

### 1.2 当前方案的结构性缺口

官方资料同样显示：

- OpenTelemetry 把 trace 定义为事件集合，并把 trace 建模为 span 的 DAG。这适合表达执行过程，但不足以直接表达业务语义、规则冲突、例外审批和长期可复用先例。[S11]
- GraphRAG 的官方文档强调其核心是从文本构建知识图谱、社区层次和摘要，用于增强复杂问答；对应论文也将其表述为 query-focused summarization 路线。官方文档同时明确提示 indexing 可能很昂贵，且需要 prompt tuning。[S8][S9][S13]
- Zep 的官方文档和论文强调 temporal knowledge graph、历史关系维护和长期记忆能力，证明“时间感知图谱”对 agent memory 有价值，但产品心智仍更偏 memory / context engineering，而非通用决策谱系系统。[S7][S12]

据此可以推断：

- Observability 平台擅长回答“系统做了什么”
- Graph / memory 平台擅长回答“系统记住了什么”
- 市场仍缺少一类产品，专门回答“系统为什么这么决策，以及以后如何复用这个决策”

## 2. 产品判断

### 2.1 产品定位

本产品定位为：

- AI 时代的决策图谱基础设施
- Agent 编排层上的决策谱系层
- 面向高监管与高复杂流程的决策审计与先例复用平台

本产品不定位为：

- 通用图数据库
- 通用知识图谱平台
- 通用 RAG 平台
- 通用 observability 平台
- 仅面向开发调试的 trace viewer

### 2.2 核心产品主张

分享的不是运行日志，也不是单轮上下文，而是“一个决策是如何形成的结构化历史”。

这份历史至少应包含：

- 决策触发条件
- 参与的系统状态
- 调用过的工具和规则
- 冲突与例外
- 最终动作
- 后续反馈
- 可被未来类似场景检索到的先例指纹

### 2.3 场景选择原则

作为基础设施产品，Context Graph 不应脱离公司真实业务闭门造车，也不应先假想一个抽象市场需求再反推产品形态。更合理的生长方式是：

- 紧贴公司内部强相关、强使用、强数据密度的 agent 业务生长
- 在真实场景中抽取共性能力，而不是先定义一套过度抽象的平台
- 先证明内部高频场景成立，再向外部相邻场景扩展

这意味着，第一阶段的场景选择本身就是产品方法论的一部分，而不只是资源分配问题。

### 2.4 为什么同时选择两个差异较大的场景

同时选择销售数字人 agent 和编码 agent，并不是为了分散焦点，而是为了更早识别“哪些能力是真正的基础设施能力”。

如果只做一个场景，团队很容易把某个垂直业务中的特殊流程误判为通用基础设施能力；而两个差异较大的场景并行验证，反而更有利于把真正共通的能力沉淀下来，例如：

- 决策事件采集
- 多来源上下文挂载
- 例外与人工覆盖记录
- 历史先例检索
- 回放与审计导出
- 人工修正闭环

可以把这理解为一个三步验证路径：

1. 用两个差异较大的核心场景抽取共性能力
2. 把共性能力沉淀为一套基础设施产品
3. 再从第三个新场景中验证这套基础设施能否合理复现和扩展

如果第三个场景可以在有限扩展下被支持，说明我们沉淀的是基础设施；如果每进一个新场景都要重写核心模型，说明当前抽出来的仍然只是场景化方案。

### 2.5 第三个场景的选择原则

第三个场景不应该只是“再找一个新行业”，而应承担基础设施验证职责。更合理的选择原则是：

- 既包含明确的技术决策链条
- 又包含大量人的判断、协作、升级和接管过程
- 能同时复用前两个场景沉淀下来的部分能力
- 但又足够不同，能暴露现有抽象的边界

按照这个标准，第三个场景的高度优先候选应进一步收敛为：

- 面向公司已有项目私有化云虚拟化承载平台的一线工单技术支持 agent

这里不建议把第三场景拆成“故障恢复”“升级”“转人工”等孤立子任务单独验证，因为技术支持面向一线时本质上是混合任务流。真正需要被验证的不是某个单点能力，而是围绕工单生命周期的一整套综合决策能力。

## 3. 目标用户与核心场景

### 3.1 第一阶段核心用户

- 公司内部建设和运营销售数字人 agent 的产品、运营与平台团队
- 公司内部建设编码 agent，尤其服务老旧项目持续迭代的研发与工程效率团队
- 需要审计、复盘和解释 AI 决策过程的业务和技术负责人

### 3.2 关键利益相关者

- 平台工程
- AI / Agent 应用团队
- 业务负责人
- 风控 / 合规 / 内审
- 安全团队

### 3.3 第一阶段优先场景

当前阶段明确只做两个场景，不再泛化铺开：

- 销售数字人 agent
- 编码 agent，尤其是老旧项目在 agent 模式下的未来迭代

选择这两个场景，不是因为它们是最通用的行业范式，而是因为它们与公司当前能力和资产最匹配：

- 它们是公司最核心、与 agent 最深度耦合的两个垂直方向
- 公司在这两个方向上已有最多真实运行数据、上下文数据和历史操作痕迹
- 它们都天然存在“多步决策 + 多来源上下文 + 高频例外处理”的特征，适合沉淀 Context Graph
- 一旦形成高质量先例库，后续复用价值和产品壁垒都会明显高于通用场景
- 它们既能服务内部产品迭代，也更可能沉淀成对外可复制的方法论

这两个场景各自承载的 Context Graph 价值不同：

- 销售数字人 agent：核心在于记录客户理解、话术选择、异议处理、线索推进、转化判断和人工接管时机
- 编码 agent：核心在于记录任务拆解、代码理解、历史约束、修改理由、测试结果、回滚判断和跨版本演化逻辑

其中，编码 agent 下的老旧项目迭代尤其重要，因为老系统通常具有：

- 隐含约束多
- 文档缺失严重
- 历史决策散落在代码、提交、Issue、聊天和口头经验中
- 每次修改都高度依赖上下文和“不要破坏已有系统”的经验判断

这类场景比绿地项目更能体现 Context Graph 对“组织记忆”和“历史先例复用”的核心价值。

同时，这两个场景的组合还有一个基础设施层面的意义：

- 销售数字人 agent 更偏实时互动、上下文切换和策略推进
- 编码 agent 更偏长期约束、复杂依赖和多轮演化

如果一套能力同时能支撑这两类差异明显的决策过程，那么它更有可能具备跨场景的基础设施属性，而不是某个单一业务的定制工具。

## 4. 问题陈述

当前企业在 Agent 落地中存在四类实际问题：

1. 只能看到 trace，无法看到业务决策语义
2. 只能回放步骤，无法回答为什么通过了某个例外
3. 历史轨迹很多，但无法形成“类似情境下的先例库”
4. 合规、风控、业务和工程团队看到的是不同视图，缺少统一决策对象

归根结底，今天缺少的是“决策作为可查询对象”的基础设施。

## 5. 产品目标

### 5.1 总目标

把跨系统、跨工具、跨角色发生的 Agent 决策过程沉淀为统一的 Context Graph，使企业能对决策进行查看、解释、审计和复用。

### 5.2 第一阶段目标

- 能实时捕获决策过程中的关键事件，而不是只做事后 ETL
- 能把线性 trace 转成面向决策语义的 graph 结构
- 能对单次决策提供回溯和解释视图
- 能检索相似历史决策并输出先例
- 能支持人工修正和审计导出
- 能在销售数字人 agent 和编码 agent 两个场景中分别形成可用的场景模板

### 5.3 非目标

- 不做通用 workflow 编排平台
- 不做通用 observability 替代品
- 不做开放式知识图谱平台
- 不做面向大众的 AI agent 市场
- 不在第一阶段做全自动决策优化引擎

## 6. 竞争格局与机会判断

### 6.1 竞争图谱

#### A. Agent Observability

- LangSmith：支持 tracing、view traces、monitoring、alerts、feedback、evaluation，适合开发与生产观察。[S6]
- Braintrust：强调 tracing 捕获每一步执行细节，并提供 observe / dashboards / scoring 工作流。[S10]
- Microsoft Foundry：支持多框架 tracing 与 thread logs，可查看 ordered run steps 和 tool calls。[S4]
- AWS AgentCore：提供 built-in metrics、spans、logs 和 OTEL / ADOT 集成。[S2][S3]

结论：这类产品证明“execution visibility”是刚需，但并未原生回答“business decision lineage”。

#### B. Graph / Memory / Graph RAG

- Zep：自动构建 temporal knowledge graph，处理关系变化和历史上下文。[S7]
- Zep 论文：在 DMR benchmark 上 94.8% 对 93.4%，在 LongMemEval 上最高提升 18.5%，延迟最多下降 90%。[S12]
- GraphRAG：把原始文本转成 knowledge graph、community hierarchy 和 summaries，用于复杂问答；但官方也明确指出 indexing 成本高，且需要 prompt tuning。[S8][S9]

结论：这类产品证明“graphified context”有价值，但仍偏检索、记忆和知识增强。

#### C. Governance / Enterprise Control

- IBM watsonx Orchestrate：把 observability、policy controls、monitoring、drift、latency 和 OpenTelemetry 接入打包为治理能力。[S5]

结论：企业购买意愿首先来自可控、可审计、可治理，而不是技术名词本身。

### 6.2 本产品的白区

基于上述证据，白区可以概括为：

- 从 trace 到 decision object 的结构升级
- 从 memory 到 precedent 的可复用升级
- 从 observability 到 auditability 的业务升级
- 从单次 replay 到跨案例检索和解释的产品升级

这不是某一个现有类别的小补丁，而是跨 observability、memory、governance 三个类别的组合产品。

## 7. 方案概述

### 7.1 核心对象模型

第一阶段定义 6 个核心对象：

- Decision Event：一次决策链中的原子事件
- Decision Node：关键判断节点
- Context Snapshot：决策时刻的外部状态快照
- Policy / Rule Reference：参与判断的规则和约束
- Exception / Override：例外路径和人工覆盖
- Precedent Link：与历史决策的相似关系

### 7.2 系统架构

建议架构分为五层：

1. Capture Layer
   - SDK
   - OTel adapters
   - middleware / sidecar hooks

2. Decision Modeling Layer
   - trace to decision graph mapping
   - event schema normalization
   - dual-timeline support

3. Graph Store Layer
   - entity / edge / episode storage
   - temporal validity
   - correction history

4. Retrieval and Reasoning Layer
   - similar decision retrieval
   - precedent ranking
   - risk markers
   - rule gap detection

5. Governance and UX Layer
   - decision replay
   - audit export
   - human correction UI
   - approval and access control

### 7.3 关键设计原则

- 优先执行路径捕获，不依赖事后拼装
- 优先决策语义建模，不停留在 span DAG
- 优先人机共建，不假设全自动提取可靠
- 优先垂直模板，不追求第一天就通用
- 优先审计与复盘价值，再扩到优化价值

## 8. MVP 定义

### 8.1 MVP 范围

第一阶段建议只做五个模块：

#### 模块一：采集与接入

- 支持 OpenTelemetry 兼容接入
- 支持 SDK / API 方式上报决策事件
- 支持从 LangChain / OpenAI Agents SDK / custom runtime 映射到统一 schema

#### 模块二：决策图谱构建

- 将 trace、tool calls、inputs / outputs、business metadata 映射为决策节点与边
- 支持事件时间和摄入时间双时间轴
- 支持规则引用和例外路径记录

#### 模块三：决策回放与解释

- 展示单次决策链
- 展示每个关键节点的依据、输入、规则、动作
- 展示人工覆盖与异常点

#### 模块四：先例检索

- 对当前决策检索最近 N 条相似案例
- 返回相似原因、结果和差异点
- 支持按规则、角色、对象、风险标签过滤

#### 模块五：治理与导出

- 人工修正节点关系
- 审计导出
- 权限控制和访问记录

并要求所有模块都同时支持两个场景模板：

- `sales-digital-human`
- `coding-agent-legacy-iteration`

### 8.2 明确不进 MVP 的能力

- 自动生成通用策略建议
- 多跳反事实推理
- 自动规则学习闭环
- 面向所有业务系统的深度连接器覆盖
- 完整 BI / analytics 平台能力

## 9. 功能需求

### 9.1 功能需求

1. 系统必须支持接收 trace、steps、tool calls、inputs / outputs 及业务 metadata。
2. 系统必须把线性事件转换为决策图谱对象。
3. 系统必须允许绑定规则、例外、审批理由和人工覆盖。
4. 系统必须支持单次决策回放。
5. 系统必须支持相似案例检索。
6. 系统必须支持人工修正节点与边，并保留修正历史。
7. 系统必须支持审计导出。
8. 系统必须支持多租户访问控制与基础权限隔离。

### 9.2 非功能需求

- 性能：单条决策事件写入 p95 小于 500ms；单次决策回放页面首屏小于 3s
- 可靠性：图谱写入成功率大于 99.9%
- 安全：默认最小权限；敏感字段脱敏；审计日志完整
- 合规：支持数据保留策略、删除策略与导出记录
- 可扩展性：支持通过 OTel 或统一 ingestion API 扩展新 Agent 框架

## 10. 成功指标

### 10.1 北极星指标

- 被系统成功结构化为 decision graph 的关键决策占比

### 10.2 第一阶段核心指标

- 决策解释覆盖率：有完整“输入 + 规则 + 动作 + 结果”链路的决策比例
- 相似案例命中率：用户认为“有帮助”的 precedent 检索占比
- 复盘效率提升：完成一次决策复盘所需时间下降比例
- 审计准备时间下降：生成可用审计材料的平均时间下降比例
- 人工修正接受率：被确认有效的系统关系提取比例

### 10.3 业务验证指标

- 试点场景中人工复核时间下降
- 例外决策争议减少
- 合规 / 风控团队对证据链完整性的满意度

## 11. 商业化与 GTM 假设

### 11.1 初始销售叙事

第一阶段最容易成交的叙事不是“更先进的图谱”，而是：

- 让 AI 决策可审计
- 让高风险流程可解释
- 让历史案例可复用
- 让平台团队知道 agent 到底为什么这么做

### 11.2 初始定价假设

可优先验证三段式：

- 平台年费
- 按关键决策事件量计费
- 行业模板 / 合规模块增购

### 11.3 目标客户顺序

1. 先服务公司内部销售数字人 agent 与编码 agent 团队
2. 再验证与这两个场景相邻的外部客户或合作场景
3. 再选择第三个新场景验证基础设施的可复现性和可扩展性
   当前优先候选：面向公司已有项目私有化云虚拟化承载平台的一线工单技术支持 agent
4. 之后再考虑更广义的高复杂流程企业团队

## 12. 风险与应对

### 12.1 主要风险

- 用户未必会为“Context Graph”这个词买单
- 自动提取质量不够时，信任会迅速下降
- 图谱构建和检索容易做得很重，导致试点周期过长
- 早期没有足够历史数据时，precedent 功能价值有限
- 大厂可能用 observability + memory + governance 组合快速逼近

### 12.2 应对策略

- 对外卖点优先用“决策审计 / 决策复盘 / 历史先例”
- 第一阶段保留人工修正环节
- 只聚焦少数高价值场景
- 用模板和 schema 降低冷启动成本
- 与 OTel 生态兼容，减少接入阻力

## 13. 开放问题

- 销售数字人 agent 中，precedent 的最小单位应该是单轮对话动作、单次线索推进，还是完整销售会话
- 编码 agent 中，precedent 的最小单位应该是单次代码变更、单个任务，还是跨多个迭代的演化链
- 老旧项目里最关键的上下文对象应优先抽取哪些：模块边界、历史缺陷、隐含约束、评审意见还是回滚记录
- 技术支持 agent 的“case”边界应如何定义：以单张工单为单位，还是以一次完整支持会话 / 问题生命周期为单位
- 在私有化云虚拟化承载平台场景里，哪些对象应作为优先上下文：集群、宿主机、虚机、网络、存储、版本、租户、工单历史，还是知识库条目
- 技术支持 agent 中，哪些混合决策最值得优先结构化：受理、分诊、排查、升级、转人工、恢复确认、结单，还是 postmortem 归因
- precedent 的相似度应优先基于语义、规则标签还是结构模式
- 决策图谱底层是否需要独立图数据库，还是先用事件存储加派生索引
- human-in-the-loop 的最小交互单位是节点修正、边修正还是案例标注
- 对客户来说，最先愿意付费的是 replay、audit export 还是 precedent retrieval

## 14. 当前结论

截至 2026-03-08，基于官方资料和论文证据，比较稳妥的结论是：

1. Agent observability 已经成为主流平台的基础配置。[S1][S2][S3][S4][S5][S6][S10]
2. Temporal graph memory 和 Graph RAG 已经证明图结构对长期上下文与复杂检索有效。[S7][S8][S9][S12][S13]
3. 市场仍缺少“面向决策对象”的统一产品层，这是本项目最值得验证的白区。[Inference]
4. 第一阶段必须从高价值垂直场景切入，并用 auditability 和 precedent value 而不是 graph 技术叙事来验证需求。[Inference]

## 15. 参考来源

- [S1] OpenAI Agents SDK, OpenAI Developers, accessed 2026-03-08
  - https://developers.openai.com/api/docs/guides/agents-sdk
- [S2] Add observability to your Amazon Bedrock AgentCore resources, AWS Docs, accessed 2026-03-08
  - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html
- [S3] AgentCore generate memory observability data, AWS Docs, accessed 2026-03-08
  - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-memory-metrics.html
- [S4] Trace and Observe AI Agents in Microsoft Foundry, Microsoft Learn, accessed 2026-03-08
  - https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/develop/trace-agents-sdk
- [S5] Governance and observability, IBM watsonx Orchestrate, accessed 2026-03-08
  - https://www.ibm.com/products/watsonx-orchestrate/governance-and-observability
- [S6] LangSmith Observability, LangChain Docs, accessed 2026-03-08
  - https://docs.langchain.com/langsmith/observability
- [S7] Graph Overview, Zep Documentation, accessed 2026-03-08
  - https://help.getzep.com/graph-overview
- [S8] GraphRAG documentation, Microsoft, accessed 2026-03-08
  - https://microsoft.github.io/graphrag/
- [S9] microsoft/graphrag README, GitHub, accessed 2026-03-08
  - https://github.com/microsoft/graphrag
- [S10] Braintrust Observability, accessed 2026-03-08
  - https://www.braintrust.dev/docs/observability
- [S11] OpenTelemetry Overview, OpenTelemetry, accessed 2026-03-08
  - https://opentelemetry.io/docs/specs/otel/overview/
- [S12] Zep: A Temporal Knowledge Graph Architecture for Agent Memory, arXiv:2501.13956, 2025-01-20
  - https://arxiv.org/abs/2501.13956
- [S13] From Local to Global: A Graph RAG Approach to Query-Focused Summarization, arXiv:2404.16130, revised 2025-02-19
  - https://arxiv.org/abs/2404.16130

## 16. 决策记录

- `2026-03-08`: v1 采用“产品战略 + PRD”合并写法，先验证垂直场景与价值叙事，再决定是否拆分为独立 PRD / GTM / 技术方案文档。
- `2026-03-08`: 第一阶段场景明确收敛为“销售数字人 agent”和“编码 agent（尤其老旧项目迭代）”。这是一条基于公司现有资产和数据密度的产品决策，不再优先验证通用客服、采购或广义运维场景。
- `2026-03-08`: 场景策略采用“三步法”：先用两个差异较大的内部核心场景抽共性，再沉淀基础设施，随后用第三个场景验证可扩展性，避免闭门造车式的平台设计。
- `2026-03-08`: 第三个场景的优先候选收敛为“面向公司已有项目私有化云虚拟化承载平台的一线工单技术支持 agent”。原因是它同时包含技术决策链条与高密度人工协作决策，并且必须以混合任务流整体验证，不能拆成若干孤立子任务分别看待。
