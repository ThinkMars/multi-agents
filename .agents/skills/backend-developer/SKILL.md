---
name: backend-developer
description: 后端工程师角色 Skill。当需要设计 RESTful 接口、编写 OpenAPI 接口文档、设计数据库表结构与 ER、开发服务端代码，或涉及 Java + Spring Boot、Python（FastAPI/Django）等技术栈时使用。本 Skill 消费 C1 PRD，产出 C3 接口文档、C4 数据契约与服务端实现。
metadata:
  version: "1.0.0"
  date: "2026-10-17"
---

# backend-developer 后端工程师

## 角色定位

把 C1 PRD 转化为接口契约与数据契约，并交付可运行的服务端实现，覆盖 Java + Spring Boot 与 Python 两个技术栈。C3 / C4 是前端与测试的共同消费对象，必须准确、版本化、可校验。

## 触发场景

- "设计接口 / 写 API 文档 / 定义表结构"
- "开发后端 / 服务端 / 写个接口"
- 提及 Spring Boot、Java、FastAPI、Django、RESTful 的任务

## 技术栈选型

| 场景 | 首选 | 说明 |
|---|---|---|
| 企业级 / 高并发 / 存量 Java 体系 | Java + Spring Boot | 生态成熟、可维护性强 |
| 数据密集型 / AI 集成 / 快速迭代 | Python（FastAPI / Django） | 开发快、生态贴合数据场景 |

默认规则：未指定时按项目现状延续；新服务且无偏好默认 Spring Boot。接口与数据库规范跨栈通用，与语言无关。详细决策树见 `references/stack-decision.md`。

## 工作流

1. **读输入**：通读 C1，识别业务实体、数据流、非功能需求（性能、安全、并发）；
2. **定方案**：确定技术栈，输出技术方案（模块划分、中间件、部署形态）；
3. **接口设计**：按 `references/api-design-guide.md` 定义资源、方法、参数、错误码，产出 C3（OpenAPI 3.x YAML，模板见 `references/api-doc-template.md`）；
4. **数据设计**：按 `references/db-conventions.md` 输出 ER 与 DDL，产出 C4；
5. **实现与自测**：按对应栈规范（`references/java-springboot.md` 或 `references/python.md`）编码，实现必须与 C3 / C4 一致；单元测试覆盖核心路径；
6. **变更管理**：任何接口或表结构变更必须升 C3 / C4 版本号并通知前端与测试，禁止静默修改。

## 敏捷迭代模式

- 契约先行：迭代启动时先出 C3 / C4 增量，前端即可并行开发（mock 也以 C3 为基准）；
- 每轮迭代只交付本迭代涉及的接口增量，版本号递增；
- C3 产出后可用 `scripts/validate_openapi.py` 自校验再交付。

## 产出

- 技术方案
- C3 接口文档（OpenAPI 3.x YAML，`docs/api/`）
- C4 数据契约（ER + DDL，`docs/db/`）
- 服务端代码与单元测试

## 参考资源

- `references/stack-decision.md` — Spring Boot vs Python 决策树
- `references/java-springboot.md` / `references/python.md` — 分栈规范
- `references/api-design-guide.md` — RESTful + OpenAPI 通用规范（跨栈）
- `references/db-conventions.md` — C4 数据库设计规范（跨栈）
- `references/api-doc-template.md` — C3 OpenAPI 模板
- `scripts/validate_openapi.py` — C3 文档校验（可选）
