#!/usr/bin/env python3
"""C6 测试报告生成脚本：从用例执行结果 CSV 汇总统计，生成测试报告骨架。

用法：
    python3 gen_test_report.py <results.csv> [-o 输出.md]

CSV 格式（首行为表头，UTF-8）：
    用例编号,AC追溯,标题,结果,缺陷编号,备注
    结果取值：通过 / 失败 / 阻塞 / 跳过
    缺陷编号：失败或阻塞时填写，如 BUG-001，可为空

示例：
    用例编号,AC追溯,标题,结果,缺陷编号,备注
    TC-001,AC-01,正常创建任务,通过,,
    TC-002,AC-03,空标题创建,失败,BUG-001,与 AC-03 不符

退出码：0 成功；1 运行错误；2 用法错误。
"""
import argparse
import csv
import sys
from collections import Counter

VALID_RESULTS = {"通过", "失败", "阻塞", "跳过"}


def load_rows(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"用例编号", "AC追溯", "标题", "结果"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV 缺少必需列: {', '.join(sorted(missing))}")
        rows = []
        for i, row in enumerate(reader, start=2):
            result = (row.get("结果") or "").strip()
            if result not in VALID_RESULTS:
                raise ValueError(f"第 {i} 行结果值非法: {result!r}（应为 {'/'.join(VALID_RESULTS)}）")
            rows.append(row)
        return rows


def render(rows):
    total = len(rows)
    counter = Counter(r["结果"].strip() for r in rows)
    executed = total - counter.get("跳过", 0)
    pass_rate = (counter.get("通过", 0) / executed * 100) if executed else 0.0

    bugs = [r for r in rows if r["结果"] in ("失败", "阻塞") and (r.get("缺陷编号") or "").strip()]
    no_bug = [r for r in rows if r["结果"] in ("失败", "阻塞") and not (r.get("缺陷编号") or "").strip()]

    acs = sorted({(r.get("AC追溯") or "").strip() for r in rows if (r.get("AC追溯") or "").strip() and r["AC追溯"].strip() != "-"})

    lines = []
    lines.append("# 测试报告（自动生成骨架）\n")
    lines.append("> 由 gen_test_report.py 生成，请补充环境、范围、风险与验收结论后交付。\n")
    lines.append("## 1. 概述\n")
    lines.append("| 项 | 内容 |")
    lines.append("|---|---|")
    lines.append("| 测试对象 | <需求 / 版本> |")
    lines.append("| 依据契约 | C1 v___ / C3 v___ / C4 v___ |")
    lines.append("| 测试周期 | ___ ~ ___ |\n")
    lines.append("## 2. 测试范围与环境\n")
    lines.append("- 范围：<补充分削>")
    lines.append("- 环境：<补充>\n")
    lines.append("## 3. 用例执行统计\n")
    lines.append("| 指标 | 数值 |")
    lines.append("|---|---|")
    lines.append(f"| 用例总数 | {total} |")
    lines.append(f"| 通过 | {counter.get('通过', 0)} |")
    lines.append(f"| 失败 | {counter.get('失败', 0)} |")
    lines.append(f"| 阻塞 | {counter.get('阻塞', 0)} |")
    lines.append(f"| 跳过 | {counter.get('跳过', 0)} |")
    lines.append(f"| 通过率 | {pass_rate:.1f}% |\n")
    lines.append("## 4. 缺陷清单\n")
    if bugs:
        lines.append("| 缺陷编号 | 关联用例 | 标题 |")
        lines.append("|---|---|---|")
        for r in bugs:
            lines.append(f"| {(r.get('缺陷编号') or '').strip()} | {r['用例编号']} | {r['标题']} |")
    else:
        lines.append("无失败 / 阻塞用例关联缺陷。")
    if no_bug:
        lines.append("\n> 警告：以下失败 / 阻塞用例未填缺陷编号，请补录 C5 缺陷单：")
        for r in no_bug:
            lines.append(f"> - {r['用例编号']} {r['标题']}")
    lines.append("\n## 5. 契约覆盖情况\n")
    if acs:
        lines.append(f"AC 覆盖 {len(acs)} 条：{', '.join(acs)}")
        lines.append("\n| AC 编号 | 关联用例数 |")
        lines.append("|---|---|")
        for ac in acs:
            n = sum(1 for r in rows if (r.get("AC追溯") or "").strip() == ac)
            lines.append(f"| {ac} | {n} |")
    else:
        lines.append("未检测到 AC 追溯信息，请检查 CSV 是否填写 AC追溯 列。")
    lines.append("\n## 6. 风险与遗留问题\n")
    lines.append("- <补充>\n")
    lines.append("## 7. 验收结论\n")
    lines.append("- [ ] 通过 / 有条件通过 / 不通过（删除不适用项，说明理由）\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="从用例结果 CSV 生成 C6 测试报告骨架")
    parser.add_argument("csv", help="用例执行结果 CSV 文件")
    parser.add_argument("-o", "--output", help="输出 Markdown 路径（默认打印到终端）")
    args = parser.parse_args()
    try:
        rows = load_rows(args.csv)
    except (OSError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    if not rows:
        print("错误: CSV 无数据行", file=sys.stderr)
        return 1
    report = render(rows)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print(f"已生成: {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
