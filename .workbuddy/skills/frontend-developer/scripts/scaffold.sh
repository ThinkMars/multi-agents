#!/usr/bin/env bash
# 生成 React 页面 / 组件骨架
# 用法：./scaffold.sh <component|page> <Name> [输出目录]
# 示例：./scaffold.sh component TaskItem src/components
set -euo pipefail

TYPE="${1:-}"
NAME="${2:-}"
OUT="${3:-}"

if [[ "$TYPE" != "component" && "$TYPE" != "page" ]]; then
  echo "用法: $0 <component|page> <Name> [输出目录]" >&2
  exit 2
fi
if [[ -z "$NAME" ]]; then
  echo "错误: 必须提供名称（PascalCase）" >&2
  exit 2
fi
if [[ ! "$NAME" =~ ^[A-Z][A-Za-z0-9]+$ ]]; then
  echo "错误: 名称必须为 PascalCase，如 TaskItem" >&2
  exit 2
fi

if [[ -z "$OUT" ]]; then
  if [[ "$TYPE" == "page" ]]; then OUT="src/pages"; else OUT="src/components"; fi
fi

DIR="$OUT/$NAME"
mkdir -p "$DIR"

if [[ "$TYPE" == "component" ]]; then
  cat > "$DIR/$NAME.tsx" <<EOF
import { useState } from 'react';
import './$NAME.module.css';

export interface ${NAME}Props {
  // TODO: 定义入参（显式类型，禁止 any）
}

export function $NAME(props: ${NAME}Props) {
  // TODO: 实现组件，注意处理加载态 / 空态 / 错误态
  return <div className="$NAME">$NAME</div>;
}

export default $NAME;
EOF
  cat > "$DIR/$NAME.module.css" <<EOF
.$NAME {
  /* TODO: 样式走 CSS 变量，禁止硬编码主题色 */
}
EOF
else
  cat > "$DIR/$NAME.tsx" <<EOF
import { useEffect } from 'react';

export default function $NAMEPage() {
  useEffect(() => {
    // TODO: 数据请求放 services/ 请求层，类型以 C3 为基准
    // useEffect 必须返回清理函数（有订阅 / 定时器时）
  }, []);

  return (
    <div>
      <h1>$NAME</h1>
      {/* TODO: 页面内容，注意加载态 / 空态 / 错误态 */}
    </div>
  );
}
EOF
fi

cat > "$DIR/index.ts" <<EOF
export { default as $NAME } from './$NAME';
EOF

echo "已生成: $DIR"
