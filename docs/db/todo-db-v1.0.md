# 待办事项应用 数据契约

> 契约编号：C4 · 版本：v1.0 · 生产者：后端角色 · 消费者：前端、测试
> 联调试跑产物，按 db-conventions.md 规范产出。变更须升版本并通知前端与测试。

## 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|---|---|---|---|
| v1.0 | 2026-10-17 | 首版（联调试跑） | 后端角色 |

## ER 说明

关系：tasks.user_id → users.id（多对一）。无物理外键（按团队约定用逻辑外键 + 索引）。

### users 用户表

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | BIGINT | PK, 自增 | 用户 ID |
| username | VARCHAR(50) | NOT NULL, UK | 用户名，唯一 |
| password_hash | VARCHAR(100) | NOT NULL | BCrypt 哈希 |
| created_at | TIMESTAMP | NOT NULL, 默认当前时间 | |
| updated_at | TIMESTAMP | NOT NULL, 默认当前时间 | |
| is_deleted | TINYINT | NOT NULL, 默认 0 | 软删除 |

### tasks 任务表

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | BIGINT | PK, 自增 | 任务 ID |
| user_id | BIGINT | NOT NULL, idx | 所属用户 |
| title | VARCHAR(200) | NOT NULL | 任务标题 |
| status | TINYINT | NOT NULL, 默认 0 | 0 未完成 1 已完成 |
| due_at | TIMESTAMP | 可空 | 截止时间 |
| created_at | TIMESTAMP | NOT NULL, 默认当前时间 | |
| updated_at | TIMESTAMP | NOT NULL, 默认当前时间 | |
| is_deleted | TINYINT | NOT NULL, 默认 0 | 软删除 |

索引：`idx_tasks_user_id (user_id)`；`idx_tasks_user_status (user_id, status)`（列表按状态筛选）。

## DDL

```sql
CREATE TABLE users (
  id            BIGINT       PRIMARY KEY AUTO_INCREMENT COMMENT '用户 ID',
  username      VARCHAR(50)  NOT NULL COMMENT '用户名',
  password_hash VARCHAR(100) NOT NULL COMMENT 'BCrypt 密码哈希',
  created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_deleted    TINYINT      NOT NULL DEFAULT 0,
  UNIQUE KEY uk_users_username (username)
) COMMENT '用户表';

CREATE TABLE tasks (
  id         BIGINT       PRIMARY KEY AUTO_INCREMENT COMMENT '任务 ID',
  user_id    BIGINT       NOT NULL COMMENT '所属用户',
  title      VARCHAR(200) NOT NULL COMMENT '任务标题',
  status     TINYINT      NOT NULL DEFAULT 0 COMMENT '0 未完成 1 已完成',
  due_at     TIMESTAMP    NULL COMMENT '截止时间',
  created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_deleted TINYINT      NOT NULL DEFAULT 0,
  KEY idx_tasks_user_id (user_id),
  KEY idx_tasks_user_status (user_id, status)
) COMMENT '任务表';
```

## 迁移脚本

`v1.0__init_users_tasks.sql`（内容同上 DDL，联调环境已执行）。
