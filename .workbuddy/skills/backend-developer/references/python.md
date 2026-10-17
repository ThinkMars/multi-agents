# Python 后端规范（FastAPI 首选）

## 框架选择

- **FastAPI**（默认）：异步、Pydantic 校验、自动生成 OpenAPI 3.x；
- **Django**：重后台、需要 ORM + 管理后台时；
- **Flask**：仅限存量轻量服务，新服务不首选。

## 项目结构（FastAPI）

```
app/
├── main.py            # 应用入口、中间件、路由注册
├── api/               # 路由层（按资源分文件）
│   └── tasks.py
├── schemas/           # Pydantic 模型（请求 / 响应）
│   └── task.py
├── services/          # 业务编排
│   └── task_service.py
├── models/            # ORM 模型
│   └── task.py
├── db/                # 数据库会话与迁移
└── core/              # 配置、异常、安全
```

## 命名规范

- 模块 / 函数 / 变量 snake_case，类 PascalCase，常量 UPPER_SNAKE；
- 路由文件与资源名单数一致：`tasks.py` 对应 `/api/v1/tasks`；
- Pydantic 模型带后缀：`TaskCreate`、`TaskUpdate`、`TaskOut`。

## 统一约定

1. **类型注解**：公开函数必须带完整类型注解，FastAPI 依赖它生成 C3；
2. **分层**：路由层只做参数与响应，业务在 service，禁止路由里写 SQL；
3. **异常**：定义 `AppException` + 错误码枚举，全局 exception handler 统一转 `{code, message, data}`，与 C3 一致；
4. **数据库**：SQLAlchemy 2.x 风格（或项目既有 ORM），session 用依赖注入，禁止在路由里手动开关 session；
5. **异步**：I/O 密集操作用 `async def` + 异步驱动；CPU 密集放线程池；
6. **配置**：pydantic-settings 管理，密钥走环境变量；
7. **日志**：标准库 logging 或 loguru，禁止 print 调试残留。

## OpenAPI

- FastAPI 默认生成 OpenAPI 3.x：访问 `/openapi.json`；
- 导出 YAML 到 `docs/api/` 作为 C3，每条路由补 `summary` / `response_model` / `status_code`，保证文档可读；
- 交付前跑 `scripts/validate_openapi.py` 校验。

## 测试

- pytest + httpx AsyncClient 覆盖接口；service 层用依赖注入打桩；
- 命名：`test_<场景>_<预期>`，如 `test_create_task_when_title_blank_returns_400`。

## 常见反模式

- 路由里写业务逻辑；裸 `dict` 当出入参（丢失类型与文档）；同步阻塞调用混入异步路由；迁移脚本不入库。
