# Context Graph MVP 设计文档 v1

## 文档信息

- 文档类型：MVP 设计文档
- 主题：以本机 OpenClaw 为锚点的 case 轨迹、决策与回放设计
- 版本：v1
- 日期：2026-03-09
- 状态：Historical draft（已被当前 OpenPrecedent MVP 架构文档取代）
- 关联需求：[2026-03-context-graph-mvp-prd-v1.md](/workspace/01-product/04-requirements/2026-03-context-graph-mvp-prd-v1.md)
- 关联战略：[2026-03-context-graph-product-strategy.md](/workspace/01-product/01-strategy/2026-03-context-graph-product-strategy.md)

## 当前状态说明

这份文档保留的是 `2026-03-09` 的早期中文设计草案，记录的是从 Context Graph 概念向当前 OpenPrecedent MVP 收敛前的方案。

当前已交付系统边界请改看：

- [MVP 状态说明](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-status.md)
- [MVP 路线图](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-roadmap.md)
- [当前 MVP 架构文档](/workspace/02-projects/incubation/openprecedent/docs/zh/architecture/mvp-design.md)

## 1. 设计目标

本设计文档只服务 MVP 验证，不提前承担终局平台职责。

设计目标只有四个：

- 可靠采集单个 case 的完整轨迹
- 从轨迹中提炼高价值决策节点
- 支持 case 回放与节点解释
- 支持最小可用的相似 case 检索

## 2. 设计原则

- 事件流优先：先保证事实可追溯，再做图谱化抽象
- 双层对象：原始事件与结构化决策分层存储
- 证据绑定：所有解释必须能回指原始事件
- 规则优先：决策抽取先用规则，不把核心闭环全交给模型
- 轻存储起步：MVP 使用关系型存储与派生索引，不引入图数据库

## 3. 核心概念

### 3.1 Case

一次明确任务的完整生命周期。

关键字段：

- `case_id`
- `title`
- `status`
- `user_id`
- `agent_id`
- `started_at`
- `ended_at`
- `final_summary`

### 3.2 Event

case 中按时间发生的原子事实。

关键字段：

- `event_id`
- `case_id`
- `event_type`
- `actor`
- `timestamp`
- `sequence_no`
- `payload`
- `parent_event_id`

### 3.3 Decision

从事件流中提炼出的关键判断节点。

关键字段：

- `decision_id`
- `case_id`
- `decision_type`
- `title`
- `question`
- `chosen_action`
- `alternatives`
- `evidence_event_ids`
- `constraint_summary`
- `requires_human_confirmation`
- `outcome`
- `sequence_no`

### 3.4 Artifact

case 中的重要产物或引用对象。

关键字段：

- `artifact_id`
- `case_id`
- `artifact_type`
- `uri_or_path`
- `summary`

### 3.5 Case Fingerprint

用于检索相似 case 的最小结构表示。

关键字段：

- `case_id`
- `task_summary`
- `task_type`
- `tool_pattern`
- `decision_pattern`
- `file_scope`
- `has_write`
- `has_retry`
- `has_human_override`
- `embedding`

## 4. 事件模型

### 4.1 事件类型

MVP 第一版统一支持以下事件：

- `case.started`
- `message.user`
- `message.agent`
- `model.invoked`
- `model.completed`
- `tool.called`
- `tool.completed`
- `command.started`
- `command.completed`
- `file.read`
- `file.write`
- `decision.inferred`
- `user.confirmed`
- `case.completed`
- `case.failed`

### 4.2 最小事件结构

```json
{
  "event_id": "evt_0001",
  "case_id": "case_20260309_001",
  "event_type": "tool.called",
  "actor": "agent",
  "timestamp": "2026-03-09T10:00:00Z",
  "sequence_no": 12,
  "parent_event_id": "evt_0000",
  "payload": {
    "tool_name": "exec_command",
    "args": {
      "cmd": "rg --files /workspace"
    }
  }
}
```

### 4.3 payload 设计要求

- payload 保留原始信息，但允许敏感字段遮罩
- 对 command、tool、file 事件，必须保留可供回放的最小必要参数
- 对 message 与 model 事件，必须保留可供解释引用的文本片段或摘要

## 5. 决策抽取设计

### 5.1 决策抽取原则

不是每个事件都是决策。MVP 只抽取“对任务推进有显著影响的判断”。

### 5.2 第一版决策类型

- `clarify`
- `plan`
- `select_tool`
- `apply_change`
- `retry_or_recover`
- `finalize`

### 5.3 抽取触发规则

满足以下任一条件，可生成决策候选：

- agent 明确提出或调整计划
- agent 在两个以上工具或路径中做出选择
- agent 执行文件修改
- agent 遇到失败后采取恢复策略
- agent 请求用户确认或接收到人工覆盖
- agent 结束任务并给出最终交付

### 5.4 抽取流程

1. 事件写入后按顺序进入 extractor
2. extractor 基于规则产生决策候选
3. 对候选做窗口聚合，避免将连续微动作拆成大量噪音节点
4. 调用模型生成结构化解释草稿
5. 将解释草稿与证据事件绑定，生成最终 decision record

### 5.5 决策对象示例

```json
{
  "decision_id": "dec_014",
  "case_id": "case_20260309_001",
  "decision_type": "select_tool",
  "title": "定位主文档",
  "question": "应先从哪类文件确认 Context Graph 的主文档",
  "chosen_action": "优先检索 strategy 文档，再参考 archive 材料",
  "alternatives": [
    "直接阅读 archive 中的 summary",
    "先浏览所有相关 docx"
  ],
  "evidence_event_ids": ["evt_012", "evt_013"],
  "constraint_summary": "需要找到唯一持续维护文档，避免使用归档稿作为主来源",
  "requires_human_confirmation": false,
  "outcome": "锁定当前战略主文档"
}
```

## 6. 数据存储设计

### 6.1 存储策略

MVP 使用 PostgreSQL 或同类关系型数据库即可，核心是稳定、简单、便于检索。

### 6.2 逻辑表

#### `cases`

- `case_id`
- `title`
- `status`
- `user_id`
- `agent_id`
- `started_at`
- `ended_at`
- `final_summary`
- `task_type`

#### `events`

- `event_id`
- `case_id`
- `event_type`
- `actor`
- `timestamp`
- `sequence_no`
- `parent_event_id`
- `payload_json`

#### `decisions`

- `decision_id`
- `case_id`
- `decision_type`
- `title`
- `question`
- `chosen_action`
- `alternatives_json`
- `evidence_event_ids_json`
- `constraint_summary`
- `requires_human_confirmation`
- `outcome`
- `sequence_no`

#### `artifacts`

- `artifact_id`
- `case_id`
- `artifact_type`
- `uri_or_path`
- `summary`

#### `case_fingerprints`

- `case_id`
- `task_summary`
- `task_type`
- `tool_pattern_json`
- `decision_pattern_json`
- `file_scope_json`
- `has_write`
- `has_retry`
- `has_human_override`
- `embedding`

### 6.3 为什么不先上图数据库

- MVP 主要查询是按 case 回放，不是复杂图遍历
- 决策节点与证据关系完全可以先用关系表表达
- 先把 schema 和产品价值跑通，再决定是否需要图存储

## 7. 回放设计

### 7.1 回放目标

回放不是简单日志浏览，而是让用户同时理解：

- 实际发生了什么
- 为什么会这样发生

### 7.2 MVP 页面结构

建议采用三栏结构：

- 左栏：原始时间线
- 中栏：关键决策链
- 右栏：节点解释与证据面板

### 7.3 左栏：原始时间线

按顺序展示：

- 用户消息
- agent 回复
- 工具调用
- 命令执行
- 文件读写
- 错误和重试
- case 完成状态

### 7.4 中栏：决策链

只显示关键决策节点，每个节点展示：

- 标题
- 决策类型
- 简短结果
- 是否涉及人工确认

### 7.5 右栏：解释面板

点击决策节点后展示：

- 决策目标
- 关键证据
- 约束条件
- 选择原因
- 结果
- 关联原始事件

## 8. 解释生成设计

### 8.1 解释模板

每个决策节点统一用以下模板输出：

1. 当时在解决什么问题
2. 关键证据是什么
3. 受哪些约束影响
4. 为什么采取当前动作
5. 结果是什么

### 8.2 解释生成方式

- 规则层负责收集候选事件窗口
- 模型层负责把候选窗口整理为结构化说明
- 系统层负责校验是否绑定了足够证据

### 8.3 最低质量门槛

解释若缺少以下任一项，则不视为有效解释：

- 明确的问题陈述
- 至少一个证据引用
- 明确的 chosen action
- 明确的结果

## 9. 先例检索设计

### 9.1 检索目标

让用户知道“历史上有没有类似 case，以及当时怎么处理”。

### 9.2 检索输入

可基于以下对象发起检索：

- 当前 case
- 当前 case 的某个决策节点
- 新输入任务的摘要

### 9.3 检索方法

MVP 采用混合召回：

- 结构召回：基于 task type、tool pattern、decision pattern、file scope
- 语义召回：基于 case summary 或 decision summary 的 embedding

### 9.4 检索返回内容

每条结果至少展示：

- 历史 case 标题
- 相似点
- 差异点
- 历史结果
- 可点击进入完整回放

## 10. 接口草案

### 10.1 写入接口

- `POST /api/cases`
- `POST /api/events`
- `POST /api/cases/{case_id}/complete`

### 10.2 查询接口

- `GET /api/cases`
- `GET /api/cases/{case_id}`
- `GET /api/cases/{case_id}/events`
- `GET /api/cases/{case_id}/decisions`
- `GET /api/cases/{case_id}/replay`
- `GET /api/cases/{case_id}/similar`

### 10.3 回放接口返回建议

```json
{
  "case": {},
  "timeline": [],
  "decisions": [],
  "artifacts": [],
  "similar_cases": []
}
```

## 11. 实施顺序建议

### 阶段一：轨迹采集

- 定义统一事件 schema
- 接入 OpenClaw 外层 hook
- 打通 case 与 event 落库

### 阶段二：决策抽取

- 建立规则抽取器
- 定义 6 类决策
- 完成 evidence 绑定

### 阶段三：回放与解释

- 实现 case replay API
- 实现三栏回放界面
- 实现节点解释面板

### 阶段四：先例检索

- 生成 case 指纹
- 建立混合召回
- 在回放页面嵌入相似 case

## 12. 主要取舍

### 12.1 为什么先做 case 而不是先做 graph

因为用户首先需要复盘一件完整任务，而不是先操作一张抽象图。

### 12.2 为什么先规则抽取而不是全模型抽取

因为决策节点是产品核心对象，完全依赖模型会导致稳定性和审计性不足。

### 12.3 为什么先做单机 OpenClaw

因为这是最低成本、最高反馈密度、最容易建立真实数据闭环的场景。

## 13. 风险与缓解

- OpenClaw 运行时缺少足够 hook 点
  - 缓解：先从对话、命令、文件、工具四类高价值事件接入
- 决策节点噪音过多
  - 缓解：增加事件窗口聚合与最小阈值
- 解释可信度不足
  - 缓解：解释必须强制 evidence refs
- 检索效果不稳定
  - 缓解：优先结构特征，再叠加语义 embedding

## 14. 当前结论

MVP 的合理实现方式不是“先建 Context Graph 平台”，而是：

1. 先把 OpenClaw 的单 case 过程沉淀为事件流
2. 再把高价值判断沉淀为 decision records
3. 再提供 replay、explain、precedent 三个面向用户的能力

只要这三层成立，后续扩展到更复杂场景时，底层对象模型和交互方式才有继续扩展的价值。
