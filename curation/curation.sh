# Configure proxy settings (replace with your own proxy if needed)
export https_proxy="http://username:password@proxy-host:proxy-port"
export http_proxy="http://username:password@proxy-host:proxy-port"

# Set language: Python Java JavaScript TypeScript Rust C C++ Go PHP Ruby
language=PHP
phase=phase18-25

echo "Processing language: $language"

# Create output directory
mkdir -p "output/${language}/${phase}"

# Step 1: Crawl repositories
# echo "Step 1: Crawling repositories..."
python crawl_repo.py \
    --language "${language}" \
    --min_stars 1000 \
    --tokens_file tokens.txt \
    --output_file "output/${language}/raw_repos.jsonl"

# Step 2: Filter repositories
# echo "Step 2: Filtering repositories..."  
python filter_repo.py \
    --input_file "output/${language}/raw_repos.jsonl" \
    --output_file "output/${language}/filtered_repos.jsonl" \
    --tokens_file tokens.txt \
    --min_pr 200 \
    --min_issues 200 \
    --min_forks 200 \
    --language "${language}" \
    --max_workers 40

# Step 3: Extract task instances from Issue-PR pairs
# echo "Processing language: $language"
# mkdir -p output/${language}/${phase}
./swe_task_crawling/run_get_tasks_pipeline.sh \
        --repos-jsonl output/${language}/filtered_repos.jsonl \
        --token-file tokens.txt \
        --path-prs output/${language}/${phase}/results/prs/\
        --path-tasks output/${language}/${phase}/results/tasks/ \
        --output-dir output/${language}/${phase}/results/split_jobs/ \
        --cutoff-date 20180101 

# Step 4: Merge task files
# echo "Merging tasks from: output/${language}/${phase}/results/tasks"
python swe_task_crawling/merge_tasks.py \
        --input output/${language}/${phase}/results/tasks \
        --output output/${language}/${phase}/tasks.jsonl
