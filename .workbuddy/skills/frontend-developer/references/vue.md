# Vue 规范

## 技术基线

- Vue 3 + `<script setup>` + 组合式 API，禁止新写选项式 API 组件；
- 构建 Vite；TypeScript 默认；
- 状态管理 Pinia（Vuex 仅限存量）。

## 目录结构

```
src/
├── components/        # 通用组件 PascalCase 目录
├── pages/ 或 views/   # 路由页面
├── composables/       # 组合式函数（use 开头）
├── services/          # 请求层（对应 C3）
├── stores/            # Pinia store
├── types/
└── utils/
```

## 组件规范

1. **单文件组件三段式**：`<script setup>` → `<template>` → `<style scoped>`；
2. **props 用 `defineProps<{...}>()` 泛型定义**，emits 用 `defineEmits`；
3. **组件名 PascalCase**，使用时可用 kebab-case；
4. **模板中禁止复杂表达式**：超过两步计算放 computed；
5. **v-for 必须写 key**，用稳定 ID；v-if 与 v-for 不同作用于同一元素；
6. **样式 scoped 优先**，主题变量走 CSS 自定义属性，禁止硬编码主题色散落各处。

## 组合式函数

- 命名 `useXxx`，存放 `composables/`；
- 响应式状态用 `ref`（基本类型）/ `reactive`（对象），禁止混用导致解包混乱；
- 副作用统一 `watch` / `watchEffect`，及时清理（`onUnmounted`）。

## 请求层

- 统一请求实例处理 baseURL（对应 C3）、token、错误码映射；
- 接口类型以 C3 schema 为准；mock 以 C3 为基准；
- 页面内数据请求放组件 setup，禁止在 store 里散落请求逻辑。

## 性能要点

- 路由懒加载；大组件异步组件；
- 长列表用虚拟滚动；
- `v-once` / `v-memo` 用于静态或低频变化块；
- 避免深度 watch 大对象，能精确监听就精确监听。

## 测试

- 组件测试 Vitest + Vue Test Utils；
- E2E Playwright。
