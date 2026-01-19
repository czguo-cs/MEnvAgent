# Configure proxy settings (replace with your own proxy if needed)
# export https_proxy="http://username:password@proxy-host:proxy-port"
# export http_proxy="http://username:password@proxy-host:proxy-port"
export no_proxy="localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,172.16.0.0/12"
export NO_PROXY="$no_proxy"
export no_proxy="localhost,127.0.0.1,10.0.0.0/8"

# 设置语言 Python Java JavaScript TypeScript Rust C C++ Go Ruby PHP
language=PHP
suffix=medium
phase=phase13-25
output="output"
echo "处理语言: $language"


# issue 过滤
echo "issue 过滤"
echo "正处理../curation/${output}/${language}/${phase}/tasks.jsonl.${suffix}"
mkdir -p "../curation/${output}/${language}/${phase}/issue_filter_tasks"
python issue_eval.py \
    --input_file ../curation/${output}/${language}/${phase}/tasks.jsonl.${suffix} \
    --output_dir ../curation/${output}/${language}/${phase}/issue_filter_tasks

# Optional: Copy to your custom output location
# mkdir -p <your_output_path>/${output}/${language}/${phase}/
# cp ../curation/${output}/${language}/${phase}/issue_filter_tasks/tasks.jsonl.${suffix}.issue_filter <your_output_path>/${output}/${language}/${phase}/

