#!/usr/bin/env python3
"""统计指定文件的行数。"""

import sys


def count_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        total = len(lines)
        non_empty = sum(1 for line in lines if line.strip())
        print(f"{'文件':<12} {file_path}")
        print(f"{'总行数':<12} {total}")
        print(f"{'非空行':<12} {non_empty}")
        print(f"{'空行':<12} {total - non_empty}")
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python count_lines.py <文件路径>")
        sys.exit(1)
    count_lines(sys.argv[1])
