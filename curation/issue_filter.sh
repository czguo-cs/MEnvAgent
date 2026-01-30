# Configure proxy settings (replace with your own proxy if needed)
export https_proxy="http://username:password@proxy-host:proxy-port"
export http_proxy="http://username:password@proxy-host:proxy-port"


# Set language: Python Java JavaScript TypeScript Rust C C++ Go PHP Ruby
language=PHP
suffix=medium
phase=phase18-25
echo "Processing language: $language"


#issue filter
echo "issue filter"
echo "processing ../output/${language}/${phase}/tasks.jsonl.${suffix}"
mkdir -p "../output/${language}/${phase}/issue_filter_tasks"
python issue_filter/issue_eval.py \
    --input_file ../output/${language}/${phase}/tasks.jsonl.${suffix} \
    --output_dir ../output/${language}/${phase}/issue_filter_tasks

