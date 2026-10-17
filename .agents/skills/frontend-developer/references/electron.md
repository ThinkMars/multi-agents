# Electron 规范

## 进程模型

```
主进程 main          ← 窗口管理、系统能力、本地存储
  ↕ IPC（contextBridge 白名单）
预加载 preload       ← 只暴露最小 API 表面
渲染进程 renderer    ← 界面（Web 技术）
```

## 硬性规则

1. **渲染进程禁用 nodeIntegration**，必须 `contextIsolation: true`；
2. **preload 只通过 contextBridge 暴露白名单 API**，禁止把 ipcRenderer 整个透传；
3. **IPC 通道集中定义**（常量或枚举），禁止字符串散落；
4. **敏感操作（文件、网络、数据库）只在主进程**，渲染进程通过 IPC 申请；
5. **CSP 配置**：禁止 `unsafe-inline` 脚本（开发期可用，生产必须收紧）。

## 项目结构

```
electron/
├── main/                 # 主进程
│   ├── index.ts
│   └── ipc/              # IPC 处理器
├── preload/
│   └── index.ts          # contextBridge 暴露面
└── renderer/             # 渲染进程（React/Vue，遵循对应规范）
```

## 窗口与体验

- 窗口尺寸 / 位置持久化（electron-store）；
- 启动白屏处理：ready-to-show 后再显示窗口；
- 崩溃自愈：`process.on('uncaughtException')` 记录 + 重启渲染进程（主进程不退出）。

## 打包与更新

- electron-builder 打包，签名按平台要求配置；
- 自动更新 electron-updater，更新源与版本号集中管理；
- 版本号三处同步：package.json、更新清单、C1 非功能需求（如声明了更新要求）。

## 与 C3 的关系

- 渲染进程请求后端 API 时遵守 C3（baseURL、token、错误码）；
- 本地缓存数据与 C4 字段保持一致，禁止自造字段名。

## 常见反模式

- 渲染进程直接 require('fs')；IPC 无校验直接执行主进程命令；生产包开着 remote 调试端口。
