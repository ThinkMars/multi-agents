# C4 数据库设计规范（跨栈）

> 契约编号：C4 · 生产者：后端 · 消费者：前端、测试
> 组成：ER 说明 + DDL 脚本。任何表结构变更必须升版本并通知前端与测试。

## 命名规范

- 数据库 / 表 / 字段用 snake_case，表名用复数：`tasks`、`task_tags`；
- 关联表名：`<主表>_<关联表>`，如 `user_roles`；
- 索引命名：`idx_<表>_<字段>`；唯一索引：`uk_<表>_<字段>`；
- 禁止数据库保留字做标识符；注释用 COMMENT 标注表与关键字段。

## 必备字段（每张业务表）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT 自增 或 UUID | 主键 |
| created_at | TIMESTAMP | 创建时间，默认当前时间 |
| updated_at | TIMESTAMP | 更新时间，随更新自动维护 |
| is_deleted | TINYINT/BOOLEAN | 软删除标记，默认 0/false |

## 类型选型

- 主键：单表自增用 BIGINT；分布式 / 对外暴露用 UUID；
- 字符串：短枚举 VARCHAR(n) 并设长度；长文本 TEXT；禁止无长度 VARCHAR；
- 金额：整数存最小单位（分），禁止 FLOAT/DOUBLE；
- 时间：TIMESTAMP（带时区按数据库能力），统一 UTC 存储、展示层转换；
- 状态 / 枚举：TINYINT + 代码注释，或 VARCHAR 枚举值，全库统一一种方式。

## 索引与约束

- 高频查询字段建索引；组合索引遵循最左前缀；
- 外键关系在文档中说明（是否建物理外键按团队约定，高并发场景用逻辑外键）；
- 唯一约束用 uk 索引落实（如用户名唯一）；
- 禁止对低基数字段（性别、状态）单独建索引。

## ER 说明格式

```markdown
### users 用户表
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | BIGINT | PK, 自增 | 用户 ID |
| username | VARCHAR(50) | NOT NULL, UK | 用户名 |

关系：tasks.user_id → users.id（多对一）
```

## DDL 模板

```sql
CREATE TABLE tasks (
  id          BIGINT       PRIMARY KEY AUTO_INCREMENT COMMENT '任务 ID',
  user_id     BIGINT       NOT NULL COMMENT '所属用户',
  title       VARCHAR(200) NOT NULL COMMENT '任务标题',
  status      TINYINT      NOT NULL DEFAULT 0 COMMENT '0 未完成 1 已完成',
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_deleted  TINYINT      NOT NULL DEFAULT 0,
  KEY idx_tasks_user_id (user_id)
) COMMENT '任务表';
```

## 变更规则

1. 变更必须升 C4 版本（v1.0 → v1.1），并在文档头部变更记录登记；
2. 破坏性变更（删字段、改类型）需同步评估前端影响，提前一个迭代通知；
3. 新增字段必须有默认值或可空，保证向后兼容；
4. 迁移脚本随 C4 一起交付，命名 `<版本>__<描述>.sql`。
