# C3 接口文档模板（OpenAPI 3.x）

> 契约编号：C3 · 生产者：后端 · 消费者：前端、测试
> 存放：`docs/api/<名称>-v<版本>.yaml` · 设计规范见 `api-design-guide.md`

```yaml
openapi: 3.0.3
info:
  title: <服务名> API
  version: v1.0.0
  description: |
    <服务概述>
    变更记录：v1.0.0 <日期> 首版
servers:
  - url: http://localhost:8080/api/v1
    description: 本地开发
tags:
  - name: tasks
    description: 任务管理
paths:
  /tasks:
    get:
      tags: [tasks]
      summary: 获取任务列表
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: pageSize
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
        - name: status
          in: query
          schema: { type: integer, enum: [0, 1] }
          description: 0 未完成 1 已完成，不传查全部
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskPage'
        '401':
          $ref: '#/components/responses/Unauthorized'
    post:
      tags: [tasks]
      summary: 创建任务
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskOut'
        '400':
          $ref: '#/components/responses/BadRequest'
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  responses:
    BadRequest:
      description: 参数错误
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example: { code: 40001, message: "任务标题不能为空", data: null }
    Unauthorized:
      description: 未认证
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
  schemas:
    Error:
      type: object
      required: [code, message]
      properties:
        code: { type: integer }
        message: { type: string }
        data: { type: object, nullable: true }
    TaskCreate:
      type: object
      required: [title]
      properties:
        title: { type: string, maxLength: 200 }
        dueAt: { type: string, format: date-time, nullable: true }
    TaskOut:
      type: object
      properties:
        id: { type: integer, format: int64 }
        title: { type: string }
        status: { type: integer, enum: [0, 1] }
        createdAt: { type: string, format: date-time }
    TaskPage:
      type: object
      properties:
        items:
          type: array
          items: { $ref: '#/components/schemas/TaskOut' }
        total: { type: integer }
        page: { type: integer }
        pageSize: { type: integer }
```

## 填写要求

1. 每个操作必须有 summary、至少一个 2xx、相关错误响应；
2. 错误响应统一引用 `components/responses`，禁止每个接口重复定义；
3. 所有 schema 必须有 type；可空字段显式 `nullable: true`；
4. 业务错误码表附在 description 或独立 `components/schemas/ErrorCode`；
5. 交付前执行 `scripts/validate_openapi.py <文件>` 校验。
