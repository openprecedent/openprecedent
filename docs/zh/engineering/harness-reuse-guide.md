# Harness 复用指南

## 目标

总结 OpenPrecedent 当前已经具备的 harness 能力，并说明如何把这套 harness 迁移到另一个已有仓库，或者一个全新的仓库里。

这份文档关注的是工程 harness 能力和复用方式。
它不是产品架构文档。

## 当前 Harness 能力总览

OpenPrecedent 当前的 harness 可以分成六层。

### 1. 工作流与 PM 层

这一层负责把 agent 的开发工作约束到 issue 作用域内。

主要组成：

- [AGENTS.md](/workspace/02-projects/incubation/openprecedent/AGENTS.md)
- [.codex/skills/ccpm-codex/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/ccpm-codex/SKILL.md)
- [codex_pm.py](/workspace/02-projects/incubation/openprecedent/src/openprecedent/codex_pm.py)
- `.codex/pm/tasks/`
- `.codex/pm/issue-state/`

关键能力：

- 一 issue 一分支
- 一 issue 一 PR
- 本地 task twin
- issue-scoped development state
- `implementation`、`docs`、`research`、`umbrella` 等 task type
- PR 与 task 状态闭环校验

### 2. 本地护栏层

这一层负责在 push 前拦住高频流程错误。

主要组成：

- [.githooks/pre-push](/workspace/02-projects/incubation/openprecedent/.githooks/pre-push)
- [install-hooks.sh](/workspace/02-projects/incubation/openprecedent/scripts/install-hooks.sh)
- [run-codex-review-checkpoint.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-codex-review-checkpoint.sh)
- [check_branch_freshness.py](/workspace/02-projects/incubation/openprecedent/scripts/check_branch_freshness.py)

关键能力：

- 强制 `.codex-review`
- 阻止向已合并 PR 的旧分支继续 push
- 阻止落后于 `upstream/main` 的 stale branch
- 为原生 Codex `/review` 提供固定触发点

### 3. Preflight 与 CI 支撑层

这一层负责在本地和 PR 阶段提前发现常见问题。

主要组成：

- [run-agent-preflight.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-agent-preflight.sh)
- [triage_pr_checks.py](/workspace/02-projects/incubation/openprecedent/scripts/triage_pr_checks.py)
- [pr-review-gate.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/pr-review-gate.yml)
- [python-ci.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/python-ci.yml)
- [markdownlint.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/markdownlint.yml)

关键能力：

- 一个统一的本地 preflight 入口
- 可选 Markdown lint 和 E2E
- 本地 branch freshness 与 issue-state 检查
- 本地 PR closure sync 检查
- CI 失败快速分类

### 4. 仓库内验证层

这一层负责不依赖真实运行时宿主机的标准验证。

主要组成：

- [run-e2e.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-e2e.sh)
- [merge-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/merge-validation.md)
- [openclaw-full-user-journey-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-full-user-journey-validation.md)

关键能力：

- 标准端到端验证命令
- 基于 fixture 的 OpenClaw 旅程回放
- 可重复的合并前验证基线

### 5. Live Runtime 验证层

这一层负责真实 OpenClaw 集成路径。

主要组成：

- [run-openclaw-live-validation.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-openclaw-live-validation.sh)
- [.codex/skills/openclaw-live-validation/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/openclaw-live-validation/SKILL.md)
- [openclaw-live-validation-harness.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-live-validation-harness.md)

关键能力：

- 准备 live validation 用的 shared runtime home
- 可选 seed prior history
- 自动同步目标 profile workspace 里的 installed skill bundle
- 生成 prompt、launcher 和结构化 artifact
- 告诉 agent 什么时候应该主动跑真实 smoke validation

### 6. 研究工作流层

这一层负责 post-MVP 的 hypothesis-driven work。

主要组成：

- [.codex/skills/research-harness/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/research-harness/SKILL.md)
- `.codex/skills/research-harness/templates/` 下的模板
- [mvp-status.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-status.md)
- umbrella issue `#100`

关键能力：

- 显式表达 hypothesis、method、artifact、interpretation
- 轻量实验模板
- 与现有 issue-task-PR 流程兼容

## 哪些是 OpenPrecedent 专属的

下面这些内容通常不适合原样复制到别的仓库：

- OpenClaw 专属 live validation 文档
- decision-lineage skill 内容
- OpenPrecedent CLI 假设
- 当前产品专属的 issue epic 和 task 名称
- precedent / decision 领域术语

迁移时应把这些内容视为样例，而不是通用基础设施。

## 哪些能力是通用可复用的

下面这些能力更适合作为通用 harness 复用：

- issue-task-PR 本地 twin 工作流
- task type 与 closure sync 校验
- issue-scoped development state
- `.codex-review` checkpoint 模式
- stale branch / merged branch 护栏
- unified local preflight
- CI failure triage helper
- research-harness 模板
- live-validation skill 这种“何时验证”的 workflow pattern

即便目标仓库不是 OpenPrecedent，这些模式通常也仍然有价值。

## 迁移策略

有两种更现实的迁移路径。

### 1. 迁移到已有仓库

适用于目标仓库已经有自己的 CI、文档和协作模式。

推荐顺序：

1. 先迁 workflow 核心
2. 再迁本地护栏
3. 再适配 preflight 和 CI
4. 然后补 issue-state
5. 最后再决定是否需要 live validation 或 research workflow

最小可复用集合：

- 针对目标仓库改写后的 `AGENTS.md`
- `.codex/skills/ccpm-codex/` 或等价本地 PM skill
- `codex_pm.py` 风格的本地 PM 工具
- `.githooks/pre-push`
- `scripts/install-hooks.sh`
- `scripts/run-agent-preflight.sh`
- `.codex/pm/` 目录结构

需要适配的点：

- 产品专属路径
- 默认基线分支是否仍然是 `upstream/main`
- triage 里引用的 CI workflow 名称
- preflight 中的测试命令

### 2. 迁移到新仓库

适用于新建一个 agent 产品仓库。

推荐顺序：

1. 先加 `AGENTS.md`
2. 再加本地 PM workspace 和 `codex_pm` 风格工具
3. 再加 hook 安装和 pre-push 护栏
4. 再加 unified preflight
5. 再加一个标准 E2E 或 smoke validation 入口
6. 最后按需要补 runtime-specific skill 或 research skill

对于新仓库，通常不应该一开始就把所有复杂层全部搬过去。

## 推荐的复用配置

### Profile A：纯交付型 Harness

适合主要做实现交付的仓库。

包含：

- workflow 与 PM 层
- 本地护栏层
- preflight 与 CI 支撑层

初期可以不包含：

- live runtime 验证层
- 研究工作流层

### Profile B：Agent 产品 Harness

适合存在真实 runtime integration 路径的仓库。

包含：

- workflow 与 PM 层
- 本地护栏层
- preflight 与 CI 支撑层
- 仓库内验证层
- live runtime 验证层

### Profile C：研究验证型 Harness

适合已经过了 MVP plumbing，需要持续做 hypothesis loop 的仓库。

包含：

- workflow 与 PM 层
- issue-state 支撑
- 研究工作流层
- 与产品相匹配的验证层

## 实际迁移检查清单

迁移到别的仓库时，至少确认：

- 分支命名与默认 base ref 是否正确
- triage 里引用的 CI workflow 名称是否匹配
- hook 提示语是否符合新仓库术语
- preflight 里的测试命令是否匹配目标仓库
- task twin metadata 是否适配目标流程
- runtime smoke validation 是否真的指向新产品的真实运行路径

## 推荐的打包方式

不要试图一次性复制全部能力。

更合理的顺序是：

1. 先迁 workflow、hook、preflight 核心
2. 在目标仓库里用几轮真实任务跑起来
3. 再按需要补 live validation 或 research workflow

这样能避免把 OpenPrecedent 特有复杂度一并带过去。

## 相关文档

- [Harness capability analysis](/workspace/02-projects/incubation/openprecedent/docs/engineering/harness-capability-analysis.md)
- [Harness reuse guide](/workspace/02-projects/incubation/openprecedent/docs/engineering/harness-reuse-guide.md)
- [Tooling setup](/workspace/02-projects/incubation/openprecedent/docs/engineering/tooling-setup.md)
