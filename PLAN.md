# 多角色 Skill 开发计划

> 场景：开发 Skill（scene#57） · v2 优化版
> v2 变更：① 明确前端（React / Vue / Flutter / Electron / 小程序）与后端（Java+Spring Boot / Python）技术栈定位；② 新增「角色消费 / 产出 / 契约」清单（C1–C6）；③ 契约模板先行，再建各角色 Skill。

## 1. 目标

1. **角色专业化**：每个 Skill 聚焦一个角色的工作流、规范与产出物模板，Agent 加载后即获得该角色的完整职能上下文；
2. **多智能体协作**：不同 Agent 实例加载不同角色 Skill，按标准化契约接力完成研发全流程；
3. **契约化研发**：角色间通过 C1–C6 六个标准契约交接，替换任一角色（人或 Agent）不影响流程，全部产出可评审、可追溯。

## 2. 技术栈定位

### 2.1 前端（frontend-developer 覆盖）

| 技术栈 | 适用场景 | 规范文档 |
|---|---|---|
| React | 中大型 Web 应用、组件化 SPA | `references/react.md` |
| Vue | 中小型 Web 应用、快速交付 | `references/vue.md` |
| Flutter | 跨端 App（iOS / Android） | `references/flutter.md` |
| Electron | 桌面端应用 | `references/electron.md` |
| 小程序 | 微信生态轻应用 | `references/miniprogram.md` |

- SKILL.md 内置**选型决策树**（目标平台 × 项目规模 × 团队熟悉度）：Web 优先 React；快速交付 / 小团队选 Vue；移动端跨端选 Flutter；桌面端选 Electron；微信生态选小程序；
- 默认规则：项目未指定栈时，Web 场景默认 React；项目已有栈时延续现有栈；
- 组件设计原则、UI 走查清单跨栈通用，按栈细节放各 references 文件按需加载。

### 2.2 后端（backend-developer 覆盖）

| 技术栈 | 适用场景 | 规范文档 |
|---|---|---|
| Java + Spring Boot | 企业级服务、复杂业务、高并发、既有 Java 体系 | `references/java-springboot.md` |
| Python（FastAPI / Django / Flask） | 快速原型、数据 / AI 服务、脚本化后端 | `references/python.md` |

- SKILL.md 内置**选型决策树**：企业级 / 高并发 / 存量 Java 体系 → Spring Boot；数据密集型 / AI 集成 / 快速迭代 → Python；
- 默认规则：未指定时按项目现状延续；新服务且无偏好时默认 Spring Boot（生态与可维护性）；
- RESTful 接口规范与数据库规范**跨栈通用，与语言无关**。

### 2.3 跨栈通用契约

- 接口文档统一 **OpenAPI 3.x（YAML）** 描述；
- 数据契约统一 **SQL DDL + ER 说明**；
- 两者语言无关，是前端与测试的共同消费对象。

## 3. 角色消费 / 产出 / 契约

### 3.1 总表

| 角色 | 消费（输入） | 产出（输出） | 契约职责 |
|---|---|---|---|
| 产品经理 | 用户需求描述、业务背景、竞品资料 | PRD、验收标准、优先级与里程碑 | **生产** C1、C2 |
| 前端工程师 | C1 PRD、C3 接口文档、C4 数据契约 | 页面 / 组件代码、前端自测记录、联调问题清单 | 消费 C1 / C3 / C4 |
| 后端工程师 | C1 PRD | 技术方案、服务端代码、单元测试 | **生产** C3、C4 |
| 测试工程师 | C1 PRD、C2 验收标准、C3 接口文档、C4 数据契约、前后端实现 | 测试计划、测试用例、缺陷单、测试报告 | **生产** C5、C6 |

### 3.2 契约清单

| 编号 | 契约 | 生产者 | 消费者 | 格式与存放 |
|---|---|---|---|---|
| C1 | PRD 产品需求文档 | 产品 | 前端、后端、测试 | Markdown，`docs/prd/<日期>-<名称>.md` |
| C2 | 验收标准 | 产品 | 测试（全员评审参考） | 内嵌 PRD，或独立 AC 清单 |
| C3 | 接口文档 | 后端 | 前端、测试 | OpenAPI 3.x YAML，`docs/api/` |
| C4 | 数据契约（ER + DDL） | 后端 | 前端、测试 | Markdown + SQL，`docs/db/` |
| C5 | 缺陷单 | 测试 | 前端、后端 | Markdown，`issues/BUG-<编号>.md` |
| C6 | 测试报告 | 测试 | 产品、全员 | Markdown，`docs/test/` |

设计规范不占契约编号：以根目录 `DESIGN.md` 为唯一源，业务项目使用其项目根目录 DESIGN.md。

### 3.3 契约纪律

1. **契约先行**：契约未就绪，下游不开始（接口文档未出时，前端 mock 也须以 C3 为基准）；
2. **变更受控**：契约变更必须升版本号并通知所有消费者，禁止静默修改；
3. **模板统一**：每个契约有唯一模板，存放于对应生产者 Skill 的 `references/`，四角色共用同一套定义。

## 4. 各 Skill 详细设计

### 4.1 product-manager（产品经理）

- **定位**：需求澄清与拆解、PRD 撰写、用户故事编写、优先级排序、验收标准定义。
- **触发词**：写PRD、需求分析、用户故事、产品方案、功能规划、竞品分析、产品文档、PRD review。
- **消费**：用户需求描述、业务背景、竞品资料（WebSearch 检索）。
- **产出**：C1 PRD（背景 / 目标 / 用户故事 / 功能清单 P0-P2 / 交互说明 / 非功能需求）、C2 验收标准、优先级与里程碑。
- **SKILL.md 工作流**：
  1. 澄清需求：先确认目标用户、核心场景、约束条件，不明确时先问再写；
  2. 背景分析：必要时检索竞品与资料；
  3. 撰写 C1：按模板填充，验收标准逐条可度量、可测试；
  4. 自检：按需求评审清单逐项检查后才交付。

```
product-manager/
├── SKILL.md
├── references/
│   ├── prd-template.md          # C1 模板
│   ├── acceptance-criteria.md   # C2 验收标准编写指南
│   ├── user-story-guide.md      # 用户故事（INVEST 原则）
│   └── requirement-checklist.md # 需求评审清单
└── assets/
    └── prd-skeleton.md          # PRD 文档骨架（复制即用）
```

### 4.2 frontend-developer（前端工程师）

- **定位**：页面与组件开发、UI 还原、交互实现、响应式适配、前端自测与走查；覆盖 React / Vue / Flutter / Electron / 小程序五栈。
- **触发词**：写页面、前端组件、实现UI、页面开发、交互开发、前端适配、UI走查、React、Vue、Flutter、Electron、小程序。
- **消费**：C1 PRD（功能与交互）、C3 接口文档（数据结构）、C4 数据契约（字段与类型）。
- **产出**：页面 / 组件代码、前端自测记录、UI 走查记录、联调问题清单（供后端与测试消费）。
- **SKILL.md 工作流**：
  1. 读输入：C1 + C3 + C4，识别缺口先向后端提问，不臆造字段；
  2. 定方案：按选型决策树确定技术栈（未指定则按默认规则）；
  3. 开发：按对应栈的规范实现，组件与命名遵循跨栈通用原则；
  4. 自测：对照 UI 走查清单逐项检查（兼容性、响应式、空态、错误态、加载态）；
  5. 联调：基于 C3 对接，问题记入联调问题清单并反馈后端。

```
frontend-developer/
├── SKILL.md                     # 含五栈选型决策树
├── references/
│   ├── stack-decision.md        # React/Vue/Flutter/Electron/小程序选型决策树
│   ├── react.md                 # React 编码与工程规范
│   ├── vue.md                   # Vue 编码与工程规范
│   ├── flutter.md               # Flutter 规范
│   ├── electron.md              # Electron 规范
│   ├── miniprogram.md           # 微信小程序规范
│   ├── component-standards.md   # 跨栈组件设计原则
│   └── ui-review-checklist.md   # UI 走查清单（按栈分节）
├── assets/
│   └── starters/                # 各栈最小脚手架（先做 React，其余渐进补充）
└── scripts/
    └── scaffold.sh              # 生成页面/组件脚手架（可选）
```

### 4.3 backend-developer（后端工程师）

- **定位**：接口设计、数据库设计、服务端逻辑实现、接口文档编写；覆盖 Java+Spring Boot 与 Python 两栈。
- **触发词**：接口设计、API开发、数据库设计、表结构设计、服务端开发、后端接口、RESTful、Spring Boot、FastAPI。
- **消费**：C1 PRD（功能清单、数据流、非功能需求）。
- **产出**：技术方案（选型与模块划分）、C3 接口文档（OpenAPI 3.x）、C4 数据契约（ER + DDL）、服务端代码、单元测试。
- **SKILL.md 工作流**：
  1. 读输入：C1，识别业务实体与数据流；
  2. 定方案：按选型决策树确定技术栈，输出技术方案；
  3. 接口设计：按 RESTful + OpenAPI 规范定义资源、方法、参数、错误码，产出 C3；
  4. 数据设计：ER 模型 → 表结构 DDL → 索引，产出 C4；
  5. 实现与自测：编码 + 单元测试，保证实现与 C3 / C4 一致，变更时升版本通知消费者。

```
backend-developer/
├── SKILL.md                     # 含 Java/Python 选型决策树
├── references/
│   ├── stack-decision.md        # Spring Boot vs Python 选型决策树
│   ├── java-springboot.md       # Java / Spring Boot 规范
│   ├── python.md                # Python（FastAPI/Django）规范
│   ├── api-design-guide.md      # RESTful + OpenAPI 通用规范（跨栈）
│   ├── db-conventions.md        # 数据库设计通用规范（跨栈）
│   └── api-doc-template.md      # C3 接口文档模板（OpenAPI 骨架）
└── scripts/
    └── validate_openapi.py      # C3 文档完整性校验（可选）
```

### 4.4 qa-tester（测试工程师）

- **定位**：测试计划、测试用例设计、缺陷管理、验收与回归测试。
- **触发词**：写测试用例、测试计划、bug分析、缺陷报告、验收测试、回归测试、测试报告、QA。
- **消费**：C1 PRD、C2 验收标准、C3 接口文档、C4 数据契约、前后端实现代码。
- **产出**：测试计划、测试用例（功能 / 边界 / 异常 / 兼容 / 性能 / 安全）、C5 缺陷单、C6 测试报告与验收结论。
- **SKILL.md 工作流**：
  1. 读输入：C1 + C2 + C3 + C4，逐条把验收标准转成可执行用例，保证可追溯；
  2. 定计划：范围、策略、环境、通过标准；
  3. 设计用例：按模板覆盖功能 / 边界 / 异常 / 兼容 / 性能 / 安全六类；
  4. 执行与报告：记录结果，缺陷按 C5 模板提交，汇总输出 C6 与验收结论（通过 / 不通过 + 理由）；
  5. 回归：缺陷修复后按影响面回归，更新 C6。

```
qa-tester/
├── SKILL.md
├── references/
│   ├── test-plan-template.md    # 测试计划模板
│   ├── test-case-template.md    # 测试用例模板（含 AC 追溯列）
│   ├── qa-checklists.md         # 功能/兼容/性能/安全测试清单
│   ├── bug-report-template.md   # C5 缺陷单模板
│   └── test-report-template.md  # C6 测试报告模板
└── scripts/
    └── gen_test_report.py       # 用例结果汇总为 C6（可选）
```

## 5. 项目目录结构

```
multi-agents/
├── PLAN.md                        # 本文档
├── docs/                          # 契约产物存放区（联调时使用）
│   ├── prd/                       # C1
│   ├── api/                       # C3
│   ├── db/                        # C4
│   └── test/                      # C6
├── issues/                        # C5 缺陷单
└── .workbuddy/
    └── skills/                    # 项目级 Skill，团队共享
        ├── product-manager/
        ├── frontend-developer/
        ├── backend-developer/
        └── qa-tester/
```

## 6. 实施步骤

| 阶段 | 内容 | 产出 |
|---|---|---|
| P0 准备 | 建目录；`init_skill.py` 初始化 4 个 Skill 骨架 | 4 个 Skill 目录 |
| P1 契约先行 | 定义 C1 / C2 / C3 / C4 / C5 / C6 六套模板（四个 Skill 共用） | references 模板 |
| P2 产品 | 完善 product-manager | 可用的产品 Skill |
| P3 后端 | 完善 backend-developer（双栈规范 + 决策树） | 可用的后端 Skill |
| P4 前端 | 完善 frontend-developer（五栈规范，先 React 其余渐进） | 可用的前端 Skill |
| P5 测试 | 完善 qa-tester | 可用的测试 Skill |
| P6 联调 | 用"待办事项应用"需求四角色串联试跑 | 全流程契约产物 + 优化清单 |
| P7 固化 | 按试跑反馈迭代；`package_skill.py` 校验打包；纳入 git | 交付的 Skill 包 |

预计总工作量约 6-8 个工作日（多栈规范是主要增量）。

## 7. 验收标准

1. 每个 Skill 通过 `package_skill.py` 校验（frontmatter、命名、目录结构）；
2. 触发准确："帮我写一份 PRD" / "用 React 实现这个页面" / "设计登录接口（Spring Boot）" / "写登录功能的测试用例"各自命中对应 Skill，不互相误触发；
3. 契约有效：C3 能被前端直接对接；C2 能被测试直接转用例；C1 能被测试逐条追溯；
4. 多栈覆盖：后端能按决策树在 Spring Boot / Python 间选型并产出合规 C3 / C4；前端能按决策树在五栈间选型；
5. 闭环试跑：待办应用从 C1 → C3 / C4 → 前后端实现 → C6 测试报告全流程跑通。

## 8. 风险与注意事项

- **多栈规范膨胀**：SKILL.md 只放选型决策树与通用流程，按栈细节放 references 按需加载，控制上下文；
- **契约模板是公共依赖**：C1–C6 模板被四个 Skill 引用，变更时四份同步，文档头标注版本号；
- **契约与实现漂移**：后端改接口必须升 C3 版本；测试以 C3 / C4 为基准发现问题，避免"以代码为准"；
- **误触发**：description 用具体场景词，联调阶段实测触发准确率；
- **脚手架成本**：五栈 starters 不必一次做全，优先 React + Spring Boot 主路径，其余按需补充。
