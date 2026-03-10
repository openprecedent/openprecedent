---
type: task
epic: real-history-quality
slug: add-chinese-mvp-architecture
title: Add Chinese MVP architecture document matching the English version
status: in_progress
labels: feature,docs
issue: 56
---

## Context

仓库已经有一份英文版 MVP v1 架构文档，但还没有一份内容等价的中文版，导致中文读者需要在英文文档与旧设计稿之间来回切换。
需要补一份与当前英文架构文档对齐的中文版本，明确说明已交付的 MVP v1 能力边界。

## Deliverable

新增一份中文版 MVP v1 架构文档，覆盖与英文版相同的系统结构、能力边界、接口、对象模型和图示。

## Scope

- 在 `docs/zh/architecture/` 下新增中文版 MVP v1 架构文档
- 保持与英文版 `docs/architecture/mvp-design.md` 的能力边界一致
- 包含 PlantUML 图和其他有助于理解的图
- 不引入与英文版相冲突的未来态描述

## Acceptance Criteria

- 中文读者无需阅读英文文档即可理解当前已交付的 MVP v1 架构
- 中文文档与英文文档在能力边界和图示上保持一致
- 文档准确对应当前 `upstream/main` 的实现状态

## Validation

- 对照英文版架构文档、CLI、service 层和 roadmap 复核中文内容
- 确认没有新增未交付能力的描述

## Implementation Notes

优先保证与英文版的结构和信息密度一致，再追求术语润色。
