# Java + Spring Boot 规范

## 分层架构

```
controller  →  service  →  repository  →  entity / mapper
   (入参出参)    (业务编排)    (数据访问)      (持久化模型)
```

| 层 | 职责 | 禁止事项 |
|---|---|---|
| controller | 参数校验、调用 service、包装响应 | 写业务逻辑、直接访问 mapper |
| service | 业务编排、事务边界 | 处理 HTTP 语义 |
| repository | 数据访问 | 写业务判断 |

## 命名规范

- 包名全小写：`com.company.project.module`
- 类名 PascalCase：`TaskController`、`TaskService`、`TaskServiceImpl`
- 方法名 camelCase，动词开头：`createTask`、`getTaskById`
- 常量全大写下划线：`MAX_TASK_LENGTH`
- REST 路径 kebab-case 复数名词：`/api/v1/tasks`

## 统一约定

1. **统一响应体**：`{ code, message, data }`，code=0 或 200 表示成功（与 C3 保持一致）；
2. **统一异常**：`@RestControllerAdvice` 全局处理，业务异常抛 `BizException(ErrorCode)`，不裸抛；
3. **参数校验**：controller 入参用 `@Valid` + JSR-380 注解，不在 service 重复校验格式；
4. **DTO 隔离**：对外 DTO 与 entity 分离，禁止直接暴露 entity；
5. **事务**：`@Transactional` 只加在 service 层，默认 REQUIRED，读操作用 `readOnly=true`；
6. **日志**：SLF4J + 占位符 `log.info("createTask id={}", id)`，禁止字符串拼接；敏感字段脱敏；
7. **配置**：敏感配置走环境变量 / 配置中心，禁止硬编码密钥。

## OpenAPI 集成

- 引入 `springdoc-openapi`，启动时自动生成 OpenAPI 3.x 文档；
- 注解与 C3 保持一致：`@Operation` 写摘要、`@ApiResponse` 写状态码与说明；
- 导出 YAML 到 `docs/api/` 作为 C3 交付物，并跑 `scripts/validate_openapi.py` 校验。

## 测试

- 单元测试 JUnit 5 + Mockito，覆盖 service 核心分支；
- controller 层用 `@WebMvcTest`，数据库层用 `@DataJpaTest` 或 Testcontainers；
- 测试命名：`方法名_场景_预期`，如 `createTask_whenTitleBlank_throwBizException`。

## 常见反模式

- controller 里写业务；entity 直接当出参；catch 后只打日志不抛业务异常；N+1 查询不处理。
