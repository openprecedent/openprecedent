# Context Graph 竞品格局与横向分析

## 文档信息

- 文档类型：竞品研究
- 主题：Context Graph 赛道竞争格局与横向对比
- 版本：v1
- 日期：2026-03-09
- 状态：Draft
- 关联战略：[2026-03-context-graph-product-strategy.md](/workspace/01-product/01-strategy/2026-03-context-graph-product-strategy.md)
- 关联需求：[2026-03-context-graph-mvp-prd-v1.md](/workspace/01-product/04-requirements/2026-03-context-graph-mvp-prd-v1.md)

## 一句话结论

截至 2026-03-09，Context Graph 所在赛道已经出现明显玩家分层，但真正同时覆盖“决策上下文、执行边界、决策轨迹、先例复用”的公司仍然很少。当前最接近终局方向的直接玩家是 ElixirData；Zep、Letta、Mem0、Supermemory 等主要覆盖 memory / context 层；LangSmith、Braintrust、Phoenix、OpenLIT、Foundry、AWS、OpenAI Agents SDK 等主要覆盖 tracing / observability 层；IBM 更偏治理与企业控制层。

换句话说，赛道并不空白，但“以 decision object 为中心的完整产品层”仍未被广泛占据。

## 1. 研究范围与方法

本研究只纳入截至 2026-03-09 可公开访问的官方资料、官方文档、官方产品页。重点考察以下问题：

- 产品核心对象是什么
- 是否支持 agent 轨迹采集
- 是否支持决策过程解释
- 是否支持 precedent / 历史复用
- 是否强调 policy / authority / governance
- 是否更接近我们的 MVP 或终局方向

本次不重点评估：

- 纯向量数据库
- 传统 BI / APM 平台
- 通用 workflow 编排器
- 非官方第三方评测文章

## 2. 赛道分层

### 2.1 第一层：Agent Observability / Tracing

这类产品的核心价值是记录 agent 运行轨迹、调试问题、监控成本和性能。

代表玩家：

- LangSmith
- Langfuse
- Braintrust
- Arize Phoenix
- OpenLIT
- Microsoft Foundry Tracing
- AWS Bedrock AgentCore Observability
- OpenAI Agents SDK Tracing

### 2.2 第二层：Memory / Context Graph / Stateful Agent

这类产品的核心价值是给 agent 提供长期记忆、时序知识图谱、状态保持和上下文装配。

代表玩家：

- Zep
- Letta
- Mem0
- Supermemory
- MemLayer
- Ryumem
- Recallr
- Memgraph
- Mnemosyne

### 2.3 第三层：Decision / Governance / Control Plane

这类产品的核心价值是把 AI 执行过程放进治理边界内，强调 policy、authority、approval、evidence、auditability。

代表玩家：

- ElixirData
- IBM watsonx Orchestrate
- AI Agentree

### 2.4 第四层：混合型平台

这类产品横跨多层，但通常仍有明显主轴。

- ElixirData：context + control + decision traces
- IBM：governance + observability
- Letta：runtime + memory-first agent
- OpenAI Agents SDK：runtime + tracing

## 3. 竞品总表

| 厂商 / 产品 | 核心定位 | 主要层级 | 开源情况 | 轨迹采集 | 决策解释 | 先例 / 历史复用 | Policy / Authority | 与我们关系判断 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ElixirData | Context OS / Decision Infrastructure | 决策与治理 | 未见公开开源仓库，平台看起来闭源商业化 | 强 | 强 | 强 | 强 | 当前最接近终局直接竞品 |
| IBM watsonx Orchestrate | Agent governance and observability | 治理与观测 | 闭源商业产品 | 强 | 中 | 弱 | 强 | 企业治理型邻近竞品 |
| AI Agentree | Decision tracing & governance | 决策与治理 | 未见公开开源仓库，倾向闭源 SaaS | 中 | 中 | 未明显强调 | 强 | 概念接近的小型直接玩家 |
| LangSmith | Agent observability platform | 观测 | 平台闭源，可自托管但需企业许可 | 强 | 中 | 中，偏 conversation clustering | 弱 | 观测层强替代品 |
| Langfuse | Open source LLM engineering platform | 观测 | 核心平台开源，可自托管 | 强 | 中 | 中，偏 traces/evals/datasets | 弱 | 最强开源观测替代品之一 |
| Braintrust | Observability + eval | 观测 | 平台闭源，SDK/Proxy 等部分组件开源 | 强 | 中 | 中，偏日志分析与反馈闭环 | 弱 | 观测与评测替代品 |
| Arize Phoenix | OTEL-based tracing & eval | 观测 | 平台开源，可自托管，ELv2 | 强 | 中 | 弱 | 弱 | 开源观测替代品 |
| OpenLIT | Open-source AI engineering observability | 观测 | 平台开源，可自托管，Apache-2.0 | 强 | 弱 | 弱 | 弱 | 开源工程平台替代品 |
| Microsoft Foundry | Agent tracing in platform | 观测 | 闭源平台能力 | 强 | 中 | 弱 | 中 | 平台原生观测能力 |
| AWS AgentCore | Built-in observability | 观测 | 闭源云平台能力 | 强 | 弱 | 弱 | 弱 | 云厂商基础能力 |
| OpenAI Agents SDK | Built-in tracing in runtime | 运行时观测 | SDK 开源，平台服务非完全开源产品 | 强 | 弱 | 弱 | 中，guardrails 但非治理平台 | 基础设施底座，不是完整竞品 |
| Zep | Context engineering / temporal graph memory | memory / context | Graphiti 开源，Zep 托管平台商业化 | 中 | 弱 | 中，偏长期记忆 | 弱 | 最强邻近 memory 玩家 |
| Letta | Stateful agents with memory | runtime / memory | 核心框架开源，另有托管/平台化能力 | 中 | 弱 | 中，偏状态延续 | 弱 | memory-first 运行时玩家 |
| Mem0 | Universal memory layer | memory | 开源 SDK / OSS 方案 + 托管平台并存 | 弱到中 | 弱 | 中 | 弱 | 记忆层玩家 |
| Supermemory | Context engineering infrastructure | memory / RAG | 核心仓库开源，商业 API 与云服务并存 | 弱到中 | 弱 | 中 | 弱 | context infra 玩家 |
| MemLayer | Bitemporal memory graph | memory | 官方产品页偏闭源托管，未见明确成熟 OSS 主仓 | 弱 | 弱 | 中 | 弱 | 时间型 memory 玩家 |
| Ryumem | Bi-temporal graph memory | memory | 开源项目 | 弱 | 弱 | 中 | 弱 | 开源 memory 玩家 |
| Recallr | Versioned memory graph | memory | 未见明确 OSS 主仓，当前更像闭源产品/等待名单 | 弱 | 弱 | 中 | 弱 | benchmark 导向 memory 玩家 |
| Memgraph | Cognitive memory layer | memory | 项目形态不清晰，未见明确成熟 OSS 主仓 | 弱 | 弱 | 中 | 弱 | cognitive memory 玩家 |
| Mnemosyne | Cognitive memory OS | memory | 存在开源实现与 MIT 叙事，但品牌与实现分散 | 弱 | 弱 | 中 | 弱 | memory OS 玩家 |

## 4. 重点玩家逐一分析

### 4.1 ElixirData

#### 核心判断

ElixirData 是当前最值得重点跟踪的玩家，因为它已经把你们终局文档里的几条关键判断整合成完整叙事：

- `Context Graphs`
- `Decision Boundaries`
- `Decision Traces`
- `Decision Lineage`
- `Decision Graph`

它的官方首页把自己定义为 `The Missing Layer for Agentic Execution`，强调在 AI 执行前先完成 `policy, authority, and evidence` 的治理。[S1]

#### 产品结构

从公开资料看，ElixirData 不是单点工具，而是一个四层叙事：

- Context Plane：解决 AI 知道什么
- Control Plane：解决 AI 被允许做什么
- Decision Loop / Traces：解决为什么这样做
- Decision Ledger：解决如何沉淀证据

它还明确区分了：

- Knowledge Graph：组织知识存储
- Context Graph：某一决策时刻的决策相关上下文
- Decision Graph：跨时间的决策网络与组织记忆

这套概念定义已经相当成熟。[S2][S3]

#### 与我们最重合的地方

- 不把 observability 当终局
- 强调“为什么”而不是只看“发生了什么”
- 强调 precedents / organizational memory
- 强调 policy 和 authority
- 把 decision 视为产品核心对象

#### 与我们的差异

- 它更偏企业治理与受控执行
- 它从高风险企业流程出发，而不是从单 agent MVP 出发
- 它的叙事比我们现在的 MVP 更重 control plane

#### 结论

ElixirData 是终局方向上的直接竞品，但不是你们当前 MVP 的直接实现对手。你们现阶段最合理的策略不是复制它的完整“Context OS”，而是用更轻的 `decision replay + explain + precedent` 闭环切入。

### 4.2 Zep

#### 核心判断

Zep 是当前 memory / context engineering 层最重要的邻近玩家。它的核心主张是：统一聊天历史、业务数据和用户行为，构建 `temporal context graph`，为 agent 组装正确上下文。[S4][S5]

#### 优势

- temporal graph 明确
- context assembly 清晰
- 对个性化 agent、销售、支持等场景叙事比较成熟
- 产品表达更偏开发者可用性

#### 局限

- 重心仍是 `what the agent should remember`
- 不是 `why the agent made this decision`
- governance、authority、audit evidence 不是主轴
- precedent 和 decision object 不是产品中心

#### 结论

Zep 是非常重要的邻近竞品，但更准确地说，它竞争的是 `memory/context layer`，不是 `decision infrastructure layer`。

#### 开源情况判断

Zep 本体是商业化平台，但它已经把底层核心图能力 `Graphiti` 开源，且 Graphiti README 明确区分了“Zep 是 fully managed platform”“Graphiti 是 open-source graph framework”。这说明它采取的是典型 `open core / open framework + hosted platform` 路线。[S4][S5][S6]

### 4.3 Letta

#### 核心判断

Letta 的主轴是 `stateful agents that remember and learn`。它把 agent 定义成由 system prompt、memory blocks、messages、tools 组成的 stateful object，并且强调 runs / steps / conversations 这些 runtime 对象。[S6][S7]

#### 优势

- 对长期状态和可持续 agent 体验建模较清楚
- 兼顾 runtime 与 memory
- Letta Code 证明它开始进入 coding agent 本地工作场景

#### 局限

- 决策解释不是主轴
- policy / authority / approval 不是主轴
- replay 更偏运行态，而非审计态

#### 结论

Letta 更像“有长期记忆的 agent runtime”，不是决策审计平台，但它在本地 stateful coding agent 方向值得持续关注。

#### 开源情况判断

Letta 核心框架明确开源，官方文档直接提供从 source 安装与贡献方式；同时官方也提供 Letta Developer Platform / Cloud 等托管能力。这属于 `开源核心 + 托管平台` 模式。[S7][S8][S9]

### 4.4 Mem0 / Supermemory / MemLayer / Ryumem / Recallr / Memgraph / Mnemosyne

#### 共性

这一组玩家大多围绕以下关键词构建：

- persistent memory
- temporal / bitemporal knowledge graph
- memory compression
- recall
- reflection / consolidation
- long-term personalization

它们普遍证明了一个事实：`memory infra` 已经成为活跃赛道，而时间感知、版本化、知识图谱化正在成为主流方向。[S8][S9][S10][S11][S12][S13][S14][S15]

#### 局限

这些产品普遍存在同一个边界：

- 强于“记住什么”
- 弱于“为什么这样决策”
- 弱于“决策证据链”
- 弱于“policy-governed action”
- 弱于“决策审计”

#### 结论

这组玩家不是你们的正面终局竞品，但它们会持续侵蚀“Context Graph”概念空间。如果你们对外叙事不清，很容易被市场误解为“又一个 memory graph”。

#### 开源情况判断

- Mem0：明确提供 `Mem0 Open Source` 与官方 GitHub，自托管与托管平台并存。[S10][S11]
- Supermemory：主仓库公开，官方与 GitHub 均强调开源项目，但同时存在商业 API、控制台和云服务。[S12][S13]
- MemLayer：当前更像托管产品与研发品牌，未见像 Mem0 / Letta / Graphiti 这样成熟明确的核心 OSS 仓库。[S14]
- Ryumem：公开文档与社区形态更接近开源项目。[S15]
- Recallr：公开站点更像产品与等待名单页面，未见明确成熟 OSS 主仓。[S16]
- Memgraph：当前在 AI memory 语境下的项目形态不够清晰，未见成熟公开 OSS 主仓，需谨慎判断。[S17]
- Mnemosyne：存在开源实现与公开代码，但品牌、产品与实现之间仍较分散，不像 Letta / Mem0 那样形成统一平台心智。[S18]

### 4.5 LangSmith / Langfuse / Braintrust / Arize Phoenix / OpenLIT

#### 核心判断

这一组是 agent observability 主流玩家。共同点是：

- tracing 很强
- production monitoring 很强
- eval / feedback / dashboards 越来越强
- framework 接入越来越全面

LangSmith 已经明确把自己表述为 `AI Agent & LLM Observability Platform`，强调 tracing、monitoring、alerting 和 usage insights。[S16]
Langfuse 则明确把自己表述为 `open source LLM engineering platform`，并支持自托管。[S17][S18]
Braintrust 强调从 traces 到 annotate、evaluate、deploy 的闭环。[S19][S20]
Phoenix 和 OpenLIT 都依托 OpenTelemetry，强调 open-source、无锁定和快速接入。[S21][S22]

#### 优势

- 接入门槛低
- tracing 生态成熟
- 工程可用性强
- 对开发团队来说替代成本低
- 其中 Langfuse、Phoenix、OpenLIT 都具备明确开源与自托管叙事

#### 局限

- 主体对象仍然是 trace / run / log
- 即使会提到 decision points，也通常是执行层 decision points
- 很少把 precedent、policy、authority、exception override 作为核心对象

#### 结论

这是最现实的替代威胁。用户很可能先用这些工具满足“看 agent 做了什么”的需求，然后短期内不再寻找更深层产品。也就是说，你们必须证明自己不是“另一个 trace viewer”。

#### 开源情况判断

- LangSmith：不是开源产品，但支持自托管；自托管需要企业许可，不属于社区开源模式。[S23][S24]
- Langfuse：核心平台已经开源并支持自托管，当前是最重要的开源 LLMOps 玩家之一。[S17][S18]
- Braintrust：官方公开了 SDK 与部分关键组件，例如 AI Proxy，但主平台并未按 Phoenix / Langfuse 的方式完全开源。[S19][S25]
- Phoenix：明确自称 fully open-source，支持自由 self-host，采用 ELv2。[S21][S26]
- OpenLIT：Apache-2.0 开源，产品仓库和 Helm 部署都公开。[S22][S27]

#### 结论

这一层的开源竞争比决策层和治理层更激烈。对你们来说，最大的现实压力不是闭源巨头，而是开源 observability 平台已经足够成熟，能先吃掉一部分开发者与团队的“复盘”预算。

### 4.6 Microsoft Foundry / AWS AgentCore / OpenAI Agents SDK

#### 核心判断

云厂商和 runtime 原生 SDK 已经把 tracing 作为基础能力内建。

- Foundry 支持 ordered run steps、tool calls、memory management、planning spans，并与多个框架集成。[S21]
- AWS AgentCore 提供内建 metrics、spans、logs 和 CloudWatch 可视化。[S22][S23]
- OpenAI Agents SDK 默认开启 tracing，可记录 LLM generations、tool calls、handoffs、guardrails 等事件。[S24][S25]

#### 意义

这进一步证明：单纯 “agent tracing” 已经不是白区，而是基础设施标配。

#### 结论

这些不是你们的完整产品竞品，但会压缩任何纯 tracing 产品的独立空间。

#### 开源情况判断

- Microsoft Foundry：闭源平台能力。[S28]
- AWS AgentCore：闭源平台能力。[S29][S30]
- OpenAI Agents SDK：SDK 本身开源，Python 与 TypeScript 都有官方 GitHub 仓库，但 tracing 后端与平台能力不等于完整开源产品。[S31][S32][S33]

### 4.7 IBM watsonx Orchestrate

#### 核心判断

IBM 的重点是 `agent governance and observability`，强调 dashboard、policy controls、drift monitoring、pre-deployment evaluation、sensitive data protection 等。[S26]

#### 优势

- 企业信任叙事强
- 治理、风控、合规语言成熟
- 更容易进入高监管客户

#### 局限

- precedent / decision memory 不是强主轴
- 更像企业 AI 管理面板和治理层
- 与本地、开发者、agent runtime 近距离协作场景较远

#### 结论

IBM 是企业治理邻近竞品，不是最贴近你们 MVP 的玩家。

#### 开源情况判断

watsonx Orchestrate 是商业产品。IBM 整体长期参与开源生态，但该产品本身并不是一个开源治理平台。[S34][S35]

### 4.8 AI Agentree

#### 核心判断

AI Agentree 对外直接使用 `Decision Tracing & Governance for AI Agents` 这一表述，概念上与我们非常接近。[S27]

#### 现状判断

目前公开信息较少，更像早期或小规模玩家，产品深度暂时不如 ElixirData 清晰。

#### 结论

值得监控，但现阶段更像概念重叠型竞品，而不是成熟主导者。

#### 开源情况判断

公开产品页强调 SDK 和 API，但当前未见清晰官方 GitHub 开源主仓，倾向于闭源 SaaS 或商业平台。[S36]

## 5. 横向能力对比

### 5.1 核心能力矩阵

| 能力 | ElixirData | Zep | Letta | LangSmith | Langfuse | Braintrust | Phoenix | OpenLIT | OpenAI Agents SDK | IBM |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 开源程度 | 闭源 | 部分开源 | 开源核心 | 闭源 | 开源 | 部分开源 | 开源 | 开源 | 开源 SDK | 闭源 |
| 事件 / 轨迹采集 | 强 | 中 | 中 | 强 | 强 | 强 | 强 | 强 | 强 | 强 |
| 决策节点显式建模 | 强 | 弱 | 弱 | 弱到中 | 弱 | 弱到中 | 弱 | 弱 | 弱 | 中 |
| 解释与证据绑定 | 强 | 弱 | 弱 | 中 | 中 | 中 | 弱到中 | 弱 | 弱 | 中 |
| precedent / 历史先例 | 强 | 中 | 中 | 中 | 中 | 中 | 弱 | 弱 | 弱 | 弱 |
| temporal / graph context | 强 | 强 | 中 | 弱 | 弱 | 弱 | 弱 | 弱 | 弱 | 弱 |
| policy / authority / approval | 强 | 弱 | 弱 | 弱 | 弱 | 弱 | 弱 | 弱 | 弱到中 | 强 |
| 审计导向 | 强 | 弱 | 弱 | 中 | 中 | 中 | 中 | 弱 | 弱 | 强 |
| 本地单 agent 场景贴合度 | 中 | 中 | 强 | 中 | 中 | 中 | 中 | 中 | 中 | 弱 |
| 企业高风险场景贴合度 | 强 | 中 | 弱 | 中 | 中 | 中 | 中 | 中 | 中 | 强 |

### 5.2 与我们 MVP 的贴合度

| 玩家 | 与当前 MVP 贴合度 | 原因 |
| --- | --- | --- |
| OpenAI Agents SDK | 中 | 可作为事件与 tracing 基础能力，但不是完整产品替代 |
| LangSmith | 中到高 | 很容易先满足用户“看执行轨迹”的需求 |
| Langfuse | 中到高 | 开源、自托管、traces/evals/prompt workflows 完整，最容易成为团队默认基础设施 |
| Braintrust | 中 | tracing + eval 能吃掉一部分复盘价值 |
| Letta | 中 | 在本地 stateful coding agent 场景贴近，但目标不同 |
| Zep | 中 | 如果我们表达不清，会被误解为 memory graph 替代 |
| ElixirData | 中到高 | 终局方向强重合，但当前切入市场不同 |
| IBM | 低到中 | 太偏企业治理，离 MVP 较远 |

## 6. 关键结论

### 6.1 赛道并不空白，但空白存在于“组合层”

单看每一层，市场已经有大量玩家：

- tracing 不空白
- memory 不空白
- governance 不空白

真正相对稀缺的是把三者组合为一个以 `decision object` 为中心的产品层。

### 6.2 ElixirData 是最值得高度重视的直接玩家

它已经把很多你们文档中的核心判断产品化并公开叙事，说明这条路线不是凭空想象，而是真实赛道。

### 6.3 最大现实威胁不是单一直接竞品，而是“被分层替代”

用户完全可能用以下组合替代你们：

- LangSmith / Langfuse / Braintrust / Phoenix 解决 tracing
- Zep / Mem0 / Letta 解决 memory
- IBM / 内部 policy engine 解决 governance

如果你们不能把组合价值讲清楚，就容易被拆解替代。

### 6.3.1 开源格局带来的额外压力

在 observability 和 memory 层，开源已经成为非常现实的竞争变量：

- Phoenix、OpenLIT、Langfuse 都是明确的开源自托管方案
- Zep 虽然主平台商业化，但 Graphiti 已把核心 temporal graph 能力开源
- Letta、Mem0、Supermemory 也都存在开放代码或 OSS 入口

这意味着你们未来如果只提供“能自己搭出来”的 tracing 或 memory 能力，很容易被开源方案压制。你们需要占据的是更上层的 `decision object`、`evidence binding`、`precedent reuse` 和 `policy-aware replay`。

### 6.4 当前 MVP 的正确切入仍然成立

因为对你们来说，最小验证目标不是先打赢所有平台，而是先证明：

- agent 轨迹可以被结构化
- 关键决策可以被抽取
- 决策可以被回放与解释
- 历史 case 可以形成 precedent

只要这个闭环成立，后面再扩 context graph、policy boundary、enterprise governance 才有基础。

### 6.5 对外叙事必须刻意避免被归类为“又一个 memory graph”或“又一个 trace viewer”

更稳的表达方向应当是：

- decision replay
- decision evidence
- decision precedent
- decision auditability

而不是一上来强调 graph 或 memory。

## 7. 对我们的产品启发

### 7.1 短期

MVP 只做四件事：

- capture
- decision extraction
- replay / explain
- precedent retrieval

### 7.2 中期

在 MVP 成立后，再补两层：

- context graph assembly
- human override / policy boundary

### 7.3 长期

如果继续向终局走，最合理的演进路径是：

1. 决策轨迹采集
2. 决策对象建模
3. 先例库与组织记忆
4. 决策边界与审批
5. 受控 agent 执行基础设施

## 8. 建议的后续动作

1. 持续跟踪 ElixirData 的产品材料、概念框架和客户叙事变化。
2. 把你们自己的文档表达从“graph”进一步收敛到“decision replay / precedent”。
3. 在 MVP 设计里预留：
   - evidence refs
   - human override
   - policy refs
   - precedent links
4. 在后续仓库 README 和对外介绍中，避免把自己写成：
   - 通用 graph database
   - 通用 memory layer
   - 通用 observability tool

## 9. 参考来源

- [S1] ElixirData 首页
  - https://www.elixirdata.co/
- [S2] ElixirData Context Graph 概念页
  - https://www.elixirdata.co/concepts/context-graph/
- [S3] ElixirData Decision Graph 概念页
  - https://www.elixirdata.co/concepts/decision-graph/
- [S4] Zep 首页
  - https://www.getzep.com/
- [S5] Zep Agent Memory
  - https://www.getzep.com/product/agent-memory/
- [S6] Zep Graphiti GitHub
  - https://github.com/getzep/graphiti
- [S7] Letta 平台概览
  - https://docs.letta.com/overview
- [S8] Letta Stateful Agents 核心概念
  - https://docs.letta.com/guides/core-concepts/stateful-agents/
- [S9] Letta Installing from source
  - https://docs.letta.com/guides/server/source/
- [S10] Mem0 首页
  - https://mem0.ai/
- [S11] Mem0 Open Source
  - https://docs.mem0.ai/open-source
- [S12] Supermemory 首页
  - https://supermemory.ai/
- [S13] Supermemory GitHub
  - https://github.com/supermemoryai/supermemory
- [S14] MemLayer 首页
  - https://www.memlayer.dev/
- [S15] Ryumem 文档首页
  - https://docs.ryumem.io/
- [S16] Recallr 首页
  - https://recallrai.com/
- [S17] Memgraph 首页
  - https://www.memgraph.ai/
- [S18] Mnemosyne 首页
  - https://mnemosy.ai/
- [S19] AI Agentree 首页
  - https://aiagentree.com/
- [S20] LangSmith Observability
  - https://www.langchain.com/langsmith
- [S21] Langfuse GitHub
  - https://github.com/langfuse/langfuse
- [S22] Langfuse Kubernetes Self-hosting
  - https://langfuse.com/self-hosting/docker
- [S23] Braintrust 文档首页
  - https://www.braintrust.dev/docs
- [S24] Braintrust Observability Quickstart
  - https://www.braintrust.dev/docs/observability
- [S25] Arize Phoenix 首页
  - https://phoenix.arize.com/
- [S26] OpenLIT 文档首页
  - https://docs.openlit.io/
- [S27] LangSmith Self-hosted
  - https://docs.langchain.com/langsmith/self-hosted
- [S28] LangSmith Self-hosted License
  - https://support.langchain.com/articles/7011309930-how-do-i-obtain-a-self-hosted-langsmith-license-key
- [S29] Braintrust SDK
  - https://github.com/braintrustdata/braintrust-sdk
- [S30] Braintrust Proxy
  - https://github.com/braintrustdata/braintrust-proxy
- [S31] Phoenix License
  - https://arize.com/docs/phoenix/self-hosting/license
- [S32] OpenLIT GitHub
  - https://github.com/openlit/openlit
- [S33] Microsoft Foundry Tracing
  - https://learn.microsoft.com/azure/ai-services/agents/concepts/tracing
- [S34] AWS AgentCore Observability 概览
  - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html
- [S35] AWS AgentCore Observability 配置
  - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html
- [S36] OpenAI Agents SDK
  - https://openai.github.io/openai-agents-python/
- [S37] OpenAI Agents SDK Tracing
  - https://openai.github.io/openai-agents-python/tracing/
- [S38] OpenAI Agents SDK Guide
  - https://platform.openai.com/docs/guides/agents-sdk
- [S39] IBM watsonx Orchestrate Governance and Observability
  - https://www.ibm.com/products/watsonx-orchestrate/governance-and-observability
- [S40] IBM watsonx Orchestrate
  - https://www.ibm.com/products/watsonx-orchestrate
- [S41] AI Agentree
  - https://aiagentree.com/

## 10. 决策记录

- `2026-03-09`: 本轮竞品分析按“observability / memory / governance / mixed platform”四层结构进行整理。
- `2026-03-09`: ElixirData 被标记为终局方向上最接近的直接玩家。
- `2026-03-09`: Zep 被标记为最重要的 memory / context 邻近竞品，而非完整 decision infrastructure 竞品。
- `2026-03-09`: MVP 阶段仍建议以 decision replay / explain / precedent 闭环验证为优先，而不是抢先构建完整 enterprise control plane。
