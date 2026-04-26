#!/usr/bin/env python3
"""读取当前目录下所有文件，统计代码行数和文件类型分布。"""

import os
from collections import defaultdict
from pathlib import Path


IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}
IGNORE_FILES = {'.DS_Store'}
EXT_LABELS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.txt': 'Text',
    '.html': 'HTML',
    '.css': 'CSS',
}


def scan_directory(root):
    total_files = 0
    total_lines = 0
    ext_stats = defaultdict(lambda: {'count': 0, 'lines': 0})
    file_details = []

    for entry in Path(root).rglob('*'):
        # 跳过忽略的目录
        if any(part in IGNORE_DIRS for part in entry.parts):
            continue
        if not entry.is_file():
            continue
        if entry.name in IGNORE_FILES:
            continue

        total_files += 1
        try:
            lines = entry.read_text(encoding='utf-8', errors='ignore').count('\n')
        except Exception:
            lines = 0

        total_lines += lines
        ext = entry.suffix.lower() if entry.suffix else '(无扩展名)'
        ext_stats[ext]['count'] += 1
        ext_stats[ext]['lines'] += lines
        file_details.append((str(entry.relative_to(root)), ext, lines))

    return total_files, total_lines, ext_stats, file_details


def print_report(root):
    print(f"{'='*60}")
    print(f"  代码统计报告")
    print(f"  目录: {os.path.abspath(root)}")
    print(f"{'='*60}")

    total_files, total_lines, ext_stats, file_details = scan_directory(root)

    # 统计汇总
    print(f"\n{'--- 统计汇总 ---':^60}")
    print(f"{'文件总数':<20} {total_files}")
    print(f"{'代码总行数':<20} {total_lines}")
    avg = total_lines / total_files if total_files else 0
    print(f"{'平均行数/文件':<20} {avg:.1f}")

    # 文件类型分布
    print(f"\n{'--- 文件类型分布 ---':<60}")
    print(f"{'类型':<18} {'数量':<8} {'行数':<10} {'占比'}")
    print(f"{'-'*60}")
    sorted_exts = sorted(ext_stats.items(), key=lambda x: -x[1]['lines'])
    for ext, stats in sorted_exts:
        label = EXT_LABELS.get(ext, ext)
        pct = stats['lines'] / total_lines * 100 if total_lines else 0
        print(f"{label:<18} {stats['count']:<8} {stats['lines']:<10} {pct:.1f}%")

    # 文件详情
    print(f"\n{'--- 文件详情 ---':<60}")
    print(f"{'文件路径':<50} {'类型':<12} {'行数'}")
    print(f"{'-'*60}")
    file_details.sort(key=lambda x: -x[2])
    for path, ext, lines in file_details:
        label = EXT_LABELS.get(ext, ext)
        print(f"{path:<50} {label:<12} {lines}")


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    print_report(root)
