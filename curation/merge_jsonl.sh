#!/bin/bash

# 设置语言 Python Java JavaScript TypeScript Rust C C++ Go
language=JavaScript
suffix=medium

# Use relative paths from project root
SOURCE_DIR="./output/${language}/tasks"
OUTPUT_FILE="./output/${language}/tasks.jsonl.${suffix}"
# mkdir -p ./data/github_commit_pr_issue/02/QAdata_final
# SOURCE_DIR="$1"
# OUTPUT_FILE="${SOURCE_DIR}.jsonl.medium"
mkdir -p $(dirname "$OUTPUT_FILE")

# 检查源目录是否存在
if [ ! -d "$SOURCE_DIR" ]; then
    echo "错误: 源目录 '$SOURCE_DIR' 不存在"
    exit 1
fi

# 如果输出文件已存在，询问是否覆盖
if [ -f "$OUTPUT_FILE" ]; then
    read -p "输出文件 '$OUTPUT_FILE' 已存在，是否覆盖? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "操作已取消"
        exit 0
    fi
    # 先删除已有文件，避免追加
    rm -f "$OUTPUT_FILE"
fi

# 查找所有jsonl文件并合并
echo "正在查找 '$SOURCE_DIR' 下的所有jsonl文件..."
jsonl_files=$(find "$SOURCE_DIR" -type f -name "*.jsonl.${suffix}")

# 检查是否找到任何jsonl文件
if [ -z "$jsonl_files" ]; then
    echo "警告: 在 '$SOURCE_DIR' 及其子目录中未找到任何jsonl文件"
    exit 0
fi

# 统计找到的文件数量
file_count=$(echo "$jsonl_files" | wc -l | tr -d ' ')
echo "找到 $file_count 个jsonl文件，开始合并..."

# 合并文件
echo "$jsonl_files" | while read -r file; do
    # 输出当前处理的文件，便于跟踪进度
    echo "处理: $file"
    # 将文件内容追加到输出文件
    cat "$file" >> "$OUTPUT_FILE"
done

# 验证输出文件
if [ -f "$OUTPUT_FILE" ]; then
    line_count=$(wc -l < "$OUTPUT_FILE")
    echo "合并完成! 输出文件: $OUTPUT_FILE"
    echo "总记录数: $line_count"
else
    echo "错误: 合并过程失败，未生成输出文件"
    exit 1
fi

exit 0
