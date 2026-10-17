# Flutter 规范

## 技术基线

- Flutter 3.x 稳定版，Dart 3；
- 状态管理默认 Riverpod（存量 Provider 项目延续，禁止混用多套）；
- 路由 go_router 或项目既有方案。

## 目录结构

```
lib/
├── main.dart
├── app.dart                # MaterialApp 根
├── pages/                  # 页面（一个页面一个目录）
│   └── task_list/
├── widgets/                # 跨页面复用组件
├── models/                 # 数据模型（fromJson/toToast）
├── services/               # 网络层（对应 C3）
├── providers/              # Riverpod providers
└── utils/
```

## Widget 规范

1. **优先组合而非继承**：小 Widget 拆分，一个 build 方法不超过约 80 行；
2. **const 构造优先**：能 const 就 const，减少重建；
3. **build 保持纯粹**：请求、订阅放 initState / provider 生命周期，build 内不做 IO；
4. **列表用 builder**：`ListView.builder`，禁止无界列表一次性构建；
5. **主题统一**：颜色 / 字体 / 圆角走 ThemeData，禁止散落硬编码；
6. **文本与本地化**：用户可见文案集中管理，禁止拼死在 Widget 里。

## 模型与网络

- 模型与 C3 schema 一一对应，字段名保持与 C3 一致（或集中做一次映射）；
- 网络层 dio，集中处理 baseURL（对应 C3）、token、错误码；
- JSON 序列化优先 json_serializable 或手写 fromJson，禁止动态 map 满天飞。

## 平台适配

- 双端差异用 `Platform.isIOS/isAndroid` 或 Theme 分支处理，集中在适配层；
- 权限、相机、通知等能力封装成 service，禁止页面直接调插件。

## 测试

- Widget 测试覆盖关键交互；单测覆盖 model 与 provider；
- 集成测试 integration_test 覆盖主流程。

## 常见反模式

- setState 滥用导致整页重建；build 里发请求；忽略键盘弹出遮挡；图片无限大不裁剪。
