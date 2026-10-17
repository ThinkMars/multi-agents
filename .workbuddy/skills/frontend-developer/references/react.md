# React 规范

## 技术基线

- React 18+，函数组件 + Hooks，禁止新写 class 组件；
- 构建用 Vite；TypeScript 为默认（`.tsx`）；
- 包管理用项目既有锁文件，禁止混用 npm/yarn/pnpm。

## 目录结构

```
src/
├── components/        # 通用组件（按域分目录）
│   └── TaskList/
│       ├── TaskList.tsx
│       ├── TaskList.module.css
│       └── index.ts
├── pages/             # 页面级组件（对应路由）
├── hooks/             # 自定义 hooks
├── services/          # 请求层（对应 C3）
├── stores/            # 状态管理
├── types/             # TypeScript 类型定义
└── utils/
```

## 组件规范

1. **一个文件一个组件**，文件名 PascalCase 与组件名一致；
2. **props 类型用 interface 显式定义**，禁止隐式 any；可选属性标注 `?`；
3. **组件保持纯粹**：副作用（请求、订阅、定时器）放 `useEffect`，且必须写清理函数；
4. **状态提升**：共享状态提升到最近公共父级，局部状态不进全局 store；
5. **列表 key 用稳定 ID**，禁止用数组索引当 key（动态列表）；
6. **条件渲染**：`&&` 注意 `0`/`""` 渲染问题，用三元或显式布尔。

## 状态管理

- 组件内：`useState` / `useReducer`；
- 跨组件：Zustand 或 Redux Toolkit（按项目既有选型，不混用）；
- 服务端数据：TanStack Query 类库（或项目既有请求封装），禁止把接口数据手动同步进全局 store。

## 请求层

- 统一 axios/fetch 实例，集中处理 baseURL（对应 C3 servers）、token 注入、错误码映射；
- 类型以 C3 的 schema 为准生成/手写 `types/`，禁止在组件里直接 any 响应；
- mock 数据以 C3 为基准（含分页结构、错误码），不自行编造字段。

## 性能要点

- 路由级代码分割 `React.lazy`；
- 大列表虚拟化（>100 条）；
- `useMemo` / `useCallback` 只用于有实测收益处，禁止全组件滥用；
- 避免在渲染函数中创建新对象作为 props。

## 测试

- 组件测试 React Testing Library（按用户行为查询元素）；
- 关键流程 E2E（Playwright，可配合 ego-browser）。
