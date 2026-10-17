#!/usr/bin/env python3
"""C3 接口文档校验脚本：校验 OpenAPI 3.x YAML 的完整性。

用法：
    python3 validate_openapi.py <path/to/api.yaml> [more.yaml ...]

依赖：PyYAML（pip install pyyaml）。无第三方依赖时自动降级为基础结构检查。
退出码：0 全部通过；1 存在错误；2 用法或依赖错误。
"""
import sys
import re

REQUIRED_TOP = ["openapi", "info", "paths"]


def load_yaml(path):
    try:
        import yaml
    except ImportError:
        return None, "no-yaml"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f), None
    except Exception as e:
        return None, f"YAML 解析失败: {e}"


def basic_check(path):
    """无 PyYAML 时的降级检查：关键字段存在性。"""
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        return [f"无法读取文件: {e}"]
    if not re.search(r"^openapi:\s*[\"']?3\.", text, re.M):
        errors.append("缺少 openapi: 3.x 声明")
    if not re.search(r"^info:", text, re.M):
        errors.append("缺少 info 段")
    if not re.search(r"^paths:", text, re.M):
        errors.append("缺少 paths 段")
    return errors


def check(doc, path):
    errors = []
    if not isinstance(doc, dict):
        return [f"{path}: 文档根节点必须是对象"]
    for key in REQUIRED_TOP:
        if key not in doc:
            errors.append(f"{path}: 缺少必需字段 {key}")
    if "info" in doc and isinstance(doc["info"], dict):
        for key in ("title", "version"):
            if not doc["info"].get(key):
                errors.append(f"{path}: info.{key} 缺失")
    if not doc.get("openapi", "").startswith("3"):
        errors.append(f"{path}: 仅支持 OpenAPI 3.x")
    paths = doc.get("paths")
    if isinstance(paths, dict):
        if not paths:
            errors.append(f"{path}: paths 为空")
        methods = {"get", "post", "put", "patch", "delete", "head", "options"}
        for p, item in paths.items():
            if not isinstance(item, dict):
                errors.append(f"{path}: {p} 定义不是对象")
                continue
            ops = [m for m in item if m.lower() in methods]
            if not ops:
                errors.append(f"{path}: {p} 没有任何 HTTP 操作")
            for m in ops:
                op = item[m]
                if not isinstance(op, dict):
                    errors.append(f"{path}: {m.upper()} {p} 定义不是对象")
                    continue
                if not op.get("summary"):
                    errors.append(f"{path}: {m.upper()} {p} 缺少 summary")
                responses = op.get("responses")
                if not isinstance(responses, dict) or not responses:
                    errors.append(f"{path}: {m.upper()} {p} 缺少 responses")
                    continue
                codes = [str(c) for c in responses]
                if not any(c.startswith("2") for c in codes):
                    errors.append(f"{path}: {m.upper()} {p} 没有 2xx 响应")
    schemas = doc.get("components", {}).get("schemas", {}) if isinstance(doc.get("components"), dict) else {}
    refs = re.findall(r"#/components/schemas/(\w+)", str(doc))
    for r in set(refs):
        if r not in schemas:
            errors.append(f"{path}: 引用了不存在的 schema: {r}")
    return errors


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    all_errors = []
    for path in sys.argv[1:]:
        doc, err = load_yaml(path)
        if err == "no-yaml":
            print(f"[warn] 未安装 PyYAML，{path} 使用基础检查（pip install pyyaml 可获完整校验）")
            errs = basic_check(path)
        elif err:
            errs = [f"{path}: {err}"]
        else:
            errs = check(doc, path)
        if errs:
            all_errors.extend(errs)
        else:
            print(f"[pass] {path}")
    if all_errors:
        print("\n校验失败：")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print("\n全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
