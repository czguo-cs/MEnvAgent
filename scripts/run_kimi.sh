#!/bin/bash
set -euo pipefail

# =========================
# 可配置参数（放在最前面，方便修改）
# =========================
# Supported languages: Python, JavaScript, cpp, C, Rust, TypeScript, Go, Java
# Note: JavaScript can also be specified as "js", C++ as "cpp" or "c++"
export REPO_LANGUAGE="cpp"
language="cpp"
dataset_name="benchmark_v6.0_${language}"
version="irv3.1"
FILTERED_ISSUE_FILE="./data/${dataset_name}_new.jsonl"
# FILTERED_ISSUE_FILE="./data/raw_tasks_003_095_head_3000.jsonl.medium.issue_filter"

# MODEL="gemini/gemini-3-flash-preview"
MODEL="kimi-k2-instruct"
ROUND=5
NUM_PROCS=4
# NUM_PROCS=50
export K8S_NAME_PREFIX=sweimages-debug-gcz
TEMP=0.0
SETUP_DIR="testbed_test"

# 数据目录及任务路径
DATA_NAME="${dataset_name}_test_${version}"
BASE_TASK_DIR="data_collection/collect/${DATA_NAME}"
TASKS_MAP="${BASE_TASK_DIR}/raw_tasks_003_095_head_3000.jsonl"

# =========================
# 基础路径和工作目录
# =========================

WORK_DIR=$(pwd)

cd "$WORK_DIR"
echo "Current working directory: $(pwd)"
echo "Repository language: $REPO_LANGUAGE"

# 数据目录
DATA_DIR="$WORK_DIR/data_collection/collect/$DATA_NAME"
mkdir -p "$DATA_DIR"
echo "Created directory: $DATA_DIR"

# =========================
# 准备数据文件
# =========================
MERGED_FILE="$DATA_DIR/raw_tasks_003_095_head_3000.jsonl"
cp "$FILTERED_ISSUE_FILE" "$MERGED_FILE"
echo "Copied $FILTERED_ISSUE_FILE -> $MERGED_FILE"

INSTANCE_IDX_FILE="$DATA_DIR/instance_idx.txt"
python3 "$WORK_DIR/data_collection/collect/instance_id_extra.py" \
    --input "$MERGED_FILE" \
    --output "$INSTANCE_IDX_FILE"
echo "Generated instance index: $INSTANCE_IDX_FILE"

# =========================
# 环境变量
# =========================
export PYTHONPATH="${WORK_DIR}:${WORK_DIR}/app:${PYTHONPATH:-}"

# Configure proxy if needed (commented out by default)
# export http_proxy="http://username:password@proxy-host:proxy-port"
# export https_proxy="http://username:password@proxy-host:proxy-port"
# export HTTP_PROXY="$http_proxy"
# export HTTPS_PROXY="$https_proxy"

export no_proxy="localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,172.16.0.0/12"
export NO_PROXY="$no_proxy"

# Configure your LLM API settings
export OPENAI_API_BASE_URL="${OPENAI_API_BASE_URL:-https://api.openai.com/v1}"
export OPENAI_KEY="${OPENAI_KEY:-your-api-key-here}"
export GEMINI_API_KEY="${GEMINI_API_KEY:-your-api-key-here}"
export GEMINI_API_BASE="${GEMINI_API_BASE:-https://generativelanguage.googleapis.com/v1}"
echo "Python path: $PYTHONPATH"

# =========================
# 检查必要文件
# =========================
if [ ! -f "$TASKS_MAP" ]; then
    echo "❌ Missing file: $TASKS_MAP"
    exit 1
fi

# 输出目录
OUT_DIR="playground/${DATA_NAME}/${MODEL}/round_${ROUND}"
# find "$OUT_DIR" -name "cosllected_information.txt" -type f -delete
RESULT_DIR="playground/${DATA_NAME}/${MODEL}/results"
mkdir -p "$OUT_DIR" "$RESULT_DIR"

# =========================
# 执行任务
# =========================
echo "▶️ Running swe-bench on ${TASKS_MAP}"
python -m app.main swe-bench \
    --model "$MODEL" \
    --tasks-map "$TASKS_MAP" \
    --task-list-file "$INSTANCE_IDX_FILE" \
    --num-processes "$NUM_PROCS" \
    --model-temperature "$TEMP" \
    --conv-round-limit "$ROUND" \
    --output-dir "$OUT_DIR" \
    --setup-dir "$SETUP_DIR" \
    --results-path "$RESULT_DIR" \
    # --disable-image-reuse #禁用镜像复用机制

echo "✅ All tasks completed. Results saved in $RESULT_DIR"

# kubectl delete pods -n default $(kubectl get pods -n default | grep "sweimages-debug-wjj" | grep "Error" | awk '{print $1}') > log.log 2>&1 &



