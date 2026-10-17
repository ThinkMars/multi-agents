---
name: product-manager
description: 产品经理角色 Skill。当需要撰写 PRD、需求分析与拆解、编写用户故事、功能规划与优先级排序、竞品分析、定义验收标准（AC）或输出产品方案时使用。本 Skill 产出标准化契约 C1（PRD）与 C2（验收标准），是前端、后端、测试三个角色的共同输入。
metadata:
  version: "1.1.0"
  date: "2026-10-17"
---

# product-manager 产品经理

## 角色定位

把用户需求转化为可执行、可验收的产品契约。核心产出为 C1（PRD）与 C2（验收标准），是前端、后端、测试三个角色的共同输入。对下游：描述 what 与 why，不描述 how（技术实现由研发角色负责）。

## 触发场景

- "帮我写一份 PRD / 需求文档 / 产品方案"
- "分析一下这个需求 / 拆解用户故事"
- "这个功能怎么规划 / 排一下优先级"
- "定义验收标准 / 写 AC"

## 工作流

1. **澄清需求**：先确认目标用户、核心场景、业务约束、成功指标。信息不足时先提问，不要直接开写。
2. **背景分析**：必要时用 WebSearch 检索竞品与行业资料，结论写入 PRD 附录。
3. **撰写 C1 PRD**：按 `references/prd-template.md` 填充，必须包含：背景与目标、目标用户与场景、用户故事、功能清单（P0/P1/P2）、交互与视觉要求（第 4 章：关键流程、页面清单、四类界面状态、视觉约束与 Token 来源）、非功能需求、验收标准。
4. **自检交付**：按 `references/requirement-checklist.md` 逐项检查，全部通过后才交付；交付时明确版本号与存放路径（`docs/prd/<日期>-<名称>-v<版本>.md`）。

## 敏捷迭代模式

- 以 Sprint 为单位工作：迭代启动时只产出本迭代涉及的轻量契约；
- 小需求走轻量通道：用户故事 + 验收标准 + 第 4 章最小集（关键流程与界面状态），不强制完整 PRD；视觉值未定时注明"按默认 Token"；
- C1/C2 带版本号（v1.0 → v1.1 增量变更，v2.0 重大调整），需求变更先升版本再通知下游，禁止静默修改；
- 验收标准必须可度量、可测试，供测试角色直接转成用例。

## 产出契约

| 契约 | 说明 | 模板 | 存放 |
|---|---|---|---|
| C1 | PRD 产品需求文档 | `references/prd-template.md` | `docs/prd/` |
| C2 | 验收标准 | `references/acceptance-criteria.md` | 内嵌 C1 或独立 AC 清单 |

## 参考资源

- `references/prd-template.md` — C1 PRD 标准模板
- `references/acceptance-criteria.md` — C2 验收标准编写指南（Given/When/Then）
- `references/user-story-guide.md` — 用户故事编写指南（INVEST 原则）
- `references/requirement-checklist.md` — 需求评审清单
- `assets/prd-skeleton.md` — PRD 文档骨架（复制即用）
