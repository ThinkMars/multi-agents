# 跨端 Design Token 规范（D1 视觉契约）

无专职设计师时的默认设计系统；有专职设计师时，Token 文件由其维护，前端按 Token 还原，不自行发挥视觉值。

## 1. 什么是 Design Token

设计决策与代码实现解耦后的命名实体（W3C Design Tokens 社区标准）：颜色、间距、字号等"设计决策"以 Token 形式唯一命名，代码只引用 Token 名，不出现具体值。

**铁律：前端代码禁止硬编码视觉值**（`#185FA5`、`16px` 之类），一律引用 Token。

## 2. 三层结构

| 层 | 内容 | 示例 |
|---|---|---|
| 全局 Token | 原始值，不带用途 | `blue-600: #185FA5` |
| 语义 Token | 按用途引用全局值 | `color-primary: {blue-600}` |
| 组件 Token | 按组件引用语义值 | `button-bg: {color-primary}` |

规则：**组件只许引用语义 Token，不许直接引用全局 Token**——保证换主题 / 改品牌色只动语义层。

## 3. 命名规范

`<类别>-<用途>-<变体>-<状态>`，全小写中划线：`text-secondary`、`bg-surface`、`border-danger`、`space-md`。

## 4. 默认 Token 值（无设计师时的默认设计系统）

### 4.1 色彩

语义色（全局色阶略，组件只用语义层）：

| 语义 Token | 默认值 | 用途 |
|---|---|---|
| `color-primary` | `#185FA5` | 主操作、品牌强调 |
| `color-primary-hover` | `#0C447C` | 主操作悬停 |
| `color-primary-bg` | `#E6F1FB` | 主色浅底（选中态、提示条） |
| `color-success` | `#3B6D11` | 成功状态 |
| `color-warning` | `#854F0B` | 警告状态 |
| `color-danger` | `#A32D2D` | 错误、删除、必填 |
| `text-primary` | `#1F2937` | 正文主色 |
| `text-secondary` | `#6B7280` | 辅助说明 |
| `text-disabled` | `#9CA3AF` | 禁用文字 |
| `text-inverse` | `#FFFFFF` | 主色底上的反白文字 |
| `bg-page` | `#F9FAFB` | 页面底 |
| `bg-surface` | `#FFFFFF` | 卡片 / 面板 |
| `bg-hover` | `#F3F4F6` | 悬停浅灰 |
| `border-default` | `#E5E7EB` | 常规边框 |
| `border-focus` | `#185FA5` | 聚焦描边 |

### 4.2 字体

| Token | 默认值 | 用途 |
|---|---|---|
| `font-family` | `-apple-system, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif` | 正文 |
| `font-mono` | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` | 代码 / 编号 |
| `font-caption` | `12px / 1.5` | 辅助说明 |
| `font-body` | `14px / 1.6` | 正文 |
| `font-title` | `16px / 1.4` | 模块标题 |
| `font-heading` | `20px / 1.3` | 页面标题 |
| `font-display` | `28px / 1.2` | 大数字 / 空状态主视觉 |
| `weight-regular` / `weight-medium` | `400` / `500` | 常规 / 强调 |

### 4.3 间距（4px 基准）

| Token | 值 | 典型用途 |
|---|---|---|
| `space-1` | `4px` | 图标与文字间距 |
| `space-2` | `8px` | 组件内紧凑间距 |
| `space-3` | `12px` | 表单项间距 |
| `space-4` | `16px` | 卡片内边距 |
| `space-6` | `24px` | 模块间距 |
| `space-8` | `32px` | 大模块间距 |
| `space-12` | `48px` | 页面级留白 |

### 4.4 圆角与阴影

| Token | 值 | 用途 |
|---|---|---|
| `radius-sm` | `4px` | 标签、小元素 |
| `radius-md` | `8px` | 按钮、输入框、卡片 |
| `radius-lg` | `12px` | 弹窗、大面板 |
| `radius-full` | `999px` | 胶囊、头像 |
| `shadow-1` | `0 1px 2px rgba(0,0,0,.05)` | 卡片 |
| `shadow-2` | `0 4px 12px rgba(0,0,0,.10)` | 下拉、浮层 |
| `shadow-3` | `0 8px 24px rgba(0,0,0,.12)` | 模态框 |

### 4.5 动效

| Token | 值 | 用途 |
|---|---|---|
| `duration-fast` | `150ms` | hover、点击反馈 |
| `duration-normal` | `240ms` | 展开、切换 |
| `duration-slow` | `360ms` | 页面转场 |
| `easing-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | 通用曲线 |

### 4.6 断点与层级

| Token | 值 | 用途 |
|---|---|---|
| `breakpoint-sm / md / lg / xl` | `640 / 768 / 1024 / 1280px` | 响应式断点，移动优先 |
| `z-dropdown / sticky / modal / toast / tooltip` | `1000 / 1020 / 1030 / 1040 / 1050` | 浮层层级，按序递增 |

## 5. 五端落地映射

| 栈 | 落地方式 |
|---|---|
| React / Vue / Electron | CSS 自定义属性挂 `:root`（`--color-primary: #185FA5`）；用 Tailwind 等项目时映射到 theme 配置 |
| Flutter | `ThemeData` + `ThemeExtension`，`ColorScheme` / `TextTheme` 与语义 Token 一一对应 |
| 小程序 | WXSS CSS 变量；尺寸用 rpx（750rpx = 100vw），断点概念弱化，重点保证安全区适配 |

**单一来源原则**：Token 定义只存一份——项目级 `docs/design/design-tokens-v<版本>.md`（或代码中的 tokens 源文件），各端从同一份同步，禁止各端各写一套。

## 6. 与组件规范的衔接

- 组件四类状态（加载 / 空 / 错误 / 边界）的样式引用语义 Token，如空态用 `text-secondary` + `bg-surface`；
- 通用组件禁止包含硬编码视觉值（见 `component-standards.md` 反模式）；
- 新组件先查现有 Token 是否够用；不够先提 Token 变更，不在组件内造新值。

## 7. Token 变更管理

Token 变更是视觉契约变更，遵守契约纪律：

1. 升版本（`design-tokens-v1.0` → `v1.1`），更新变更记录；
2. 通知所有端负责人（前端各栈、如有设计师）；
3. 同步更新受影响组件，旧版本值不得残留。

## 8. 项目启用方式

1. 复制第 4 节默认值到项目 `docs/design/design-tokens-v1.0.md`，按品牌调整语义层（不动全局值）；
2. 在代码中落地对应端的 Token 源（CSS 变量 / ThemeData / WXSS 变量）；
3. PRD 第 4 章「设计 Token」栏指向该文件，前端按文件还原。
