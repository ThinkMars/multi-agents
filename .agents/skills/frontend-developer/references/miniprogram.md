# 微信小程序规范

## 目录结构

```
├── app.js / app.json / app.wxss      # 应用级配置与全局样式
├── pages/                            # 页面（一个页面一个目录）
│   └── task-list/
│       ├── task-list.js / .json / .wxml / .wxss
├── components/                       # 自定义组件
├── services/                         # 请求层（对应 C3）
├── utils/
└── project.config.json
```

## 页面规范

1. **页面四件套命名一致**（js/json/wxml/wxss 同名）；
2. **路由只走 navigator API /  navigator 组件**，禁止手动拼 URL 跳未注册页面；
3. **数据流单向**：逻辑层 data → 视图层，视图事件回传修改；
4. **事件命名**：业务组件用 `bind:` 冒泡或 `catch:` 拦截要有明确意图，注释说明。

## setData 性能（小程序头号优化点）

1. **只 set 变化的字段**，禁止 `this.setData({ list: wholeHugeArray })` 全量刷新；
2. **数据扁平化**：避免深层嵌套对象导致 diff 成本高；
3. **列表分页加载**：一屏数据 + 触底加载，禁止一次拉全量；
4. **setData 与用户操作分离**：高频输入用表单值缓存，失焦或防抖后提交；
5. **避免在 setData 里传未使用字段**。

## 请求层

- `wx.request` 统一封装：baseURL 对应 C3、token 注入、错误码映射、loading 管理；
- 接口类型以 C3 为基准；mock 数据同样以 C3 为基准；
- HTTPS + 合法域名配置；开发期走"不校验合法域名"仅限开发工具。

## 组件化

- 跨页面复用块抽自定义组件，properties 定义入参、triggerEvent 抛出事件；
- 组件间通信：父传子 properties，子传父 triggerEvent，跨层级用事件总线或 store（mobx-miniprogram 按项目选型）。

## 分包与体积

- 主包控制在 2M 内，非首页页面 / 资源按 tab 或场景分包；
- 图片走 CDN + 适当压缩，禁止大图塞包内；
- 引入第三方库前评估增量体积。

## 审核与发布

- 用户协议 / 隐私指引按平台要求配置；
- 涉及虚拟支付、直播等特殊能力提前确认资质；
- 发布前按 `ui-review-checklist.md` 小程序专项检查。

## 常见反模式

- setData 传巨型对象；页面间用全局 getApp().globalData 传复杂状态；未处理网络失败的空态。
