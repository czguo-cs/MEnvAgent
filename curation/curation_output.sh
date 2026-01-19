# Configure proxy settings (replace with your own proxy if needed)
# export https_proxy="http://username:password@proxy-host:proxy-port"
# export http_proxy="http://username:password@proxy-host:proxy-port"
export no_proxy="localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,172.16.0.0/12"
export NO_PROXY="$no_proxy"

# 设置语言 Python Java JavaScript TypeScript Rust C C++ Go PHP Ruby
language=PHP
phase=phase13-25

echo "处理语言: $language"

# # 创建输出目录
# mkdir -p "output/${language}"

# # 步骤1: 爬取仓库
# echo "步骤1: 爬取仓库..."
# python crawl_repo.py \
#     --language "${language}" \
#     --min_stars 500 \
#     --tokens_file tokens1.txt \
#     --output_file "output/${language}/raw_repos.jsonl"

# echo "步骤2: 过滤仓库..."  
# python filter_repo.py \
#     --input_file "output/${language}/raw_repos.jsonl" \
#     --output_file "output/${language}/filtered_repos.jsonl" \
#     --tokens_file tokens1.txt \
#     --min_pr 0 \
#     --min_issues 0 \
#     --min_forks 0 \
#     --language "${language}" \
#     --max_workers 40

# echo "处理语言: $language"
# mkdir -p output/${language}/${phase}
# ./swe_task_crawling/run_get_tasks_pipeline.sh \
#         --repos-jsonl output/${language}/filtered_repos.jsonl \
#         --token-file tokens1.txt \
#         --path-prs output/${language}/${phase}/results/prs/\
#         --path-tasks output/${language}/${phase}/results/tasks/ \
#         --output-dir output/${language}/${phase}/results/split_jobs/ \
#         --cutoff-date 20130101 

# echo "output/${language}/${phase}/results/tasks"
python swe_task_crawling/merge_tasks.py \
        --input output/${language}/${phase}/results/tasks \
        --output output/${language}/${phase}/tasks.jsonl




# # 步骤2: 分割文件
# echo "步骤2: 分割仓库文件..."
# mkdir -p "output/${language}/raw_repos"
# split -l 100 -d -a 3 "output/${language}/raw_repos.jsonl" "output/${language}/raw_repos/raw_repos_"

# # 步骤3: 处理每个分割文件
# echo "步骤3: 过滤仓库..."
# mkdir -p "output/${language}/filtered_repos"
# for file in output/${language}/raw_repos/raw_repos_*; do
#     # 提取文件编号
#     number=$(echo "$file" | grep -o '[0-9][0-9][0-9]$' || echo "000")
    
#     echo "处理文件: $file (编号: $number)"
    
#     python filter_repo.py \
#         --input_file "$file" \
#         --output_file "output/${language}/filtered_repos/filtered_repos_${number}" \
#         --tokens_file tokens.txt \
#         --min_pr 200 \
#         --min_issues 200 \
#         --min_forks 200 \
#         --language "${language}" \
#         --max_workers 30
# done

# # 步骤4: 获取每个批次的issue2pr数据
# echo "步骤4: 获取每个批次的issue2pr数据..."
# mkdir -p "output/${language}/results"
# for file in output/${language}/filtered_repos/filtered_repos_*; do
#     # 提取文件编号
#     number=$(echo "$file" | grep -o '[0-9][0-9][0-9]$' || echo "000")
    
#     echo "处理文件: $file (编号: $number)"

#     ./swe_task_crawling/run_get_tasks_pipeline.sh \
#         --repos-jsonl ${file} \
#         --token-file tokens2.txt \
#         --cutoff-date 20230101 \
#         --path-prs output/${language}/results/prs/${number} \
#         --path-tasks output/${language}/results/tasks/${number} \
#         --output-dir output/${language}/results/split_jobs/${number}
# done

# # 步骤5: 合并数据
# echo "步骤5: 合并任务..."
# mkdir -p "output/${language}/tasks/"
# for number in {000..999}; do
#     task_dir="output/${language}/results/tasks/${number}"
#     if [ -d "$task_dir" ]; then
#         echo "合并任务目录: $task_dir"
#         python swe_task_crawling/merge_tasks.py \
#             --input "$task_dir" \
#             --output "output/${language}/tasks/raw_tasks_${number}.jsonl"
#     fi
# done

# echo "语言 $language 处理完成!"