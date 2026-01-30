# MEnvData Curation Tutorial

This guide walks you through the data curation pipeline for collecting and filtering high-quality GitHub repositories and Issue-PR pairs.

## Step 1: Preparation

### 1.1 GitHub Tokens

Create a `tokens.txt` file in the `curation/` directory with your GitHub Personal Access Tokens (one per line):

```
ghp_your_token_1
ghp_your_token_2
ghp_your_token_3
```

Multiple tokens help avoid GitHub API rate limits.

### 1.2 Environment Variables

Set up your LLM API credentials:

```bash
export OPENAI_API_BASE_URL="https://your-api-endpoint.com/v1"
export OPENAI_KEY="your-api-key"
```

## Step 2: Data Collection and Filtering

Run the main curation script:

```bash
cd curation
bash curation.sh
```

This script performs the following steps:
1. **Crawl repositories** from GitHub based on language and star criteria
2. **Filter repositories** by quality thresholds (PRs, issues, forks, language ratio)
3. **Extract Issue-PR pairs** from filtered repositories
4. **Merge task files** into a single dataset

### Configuration

Edit `curation.sh` to customize:

```bash
# Target language: Python Java JavaScript TypeScript Rust C C++ Go PHP Ruby
language=Python

# Phase identifier for output organization
phase=phase18-25

# Quality thresholds
# min_stars=1000
# min_pr=200
# min_issues=200
# min_forks=200
```

### Output

Results will be saved to:
```
output/{language}/{phase}/tasks.jsonl
```

## Step 3: Issue Quality Assessment

Run LLM-based issue quality evaluation:

```bash
cd issue_filter
bash issue_filter.sh
```

This script:
1. Evaluates each issue using an LLM-based scoring system (0-10 points)
2. Filters out low-quality issues (score < 5)
3. Outputs filtered dataset

### Configuration

Edit `issue_filter.sh` to set:

```bash
# Target language
language=Python

# Phase identifier (must match Step 2)
phase=phase18-25

# Input file suffix (default: medium)
suffix=medium
```

### Output

Filtered results will be saved to:
```
output/{language}/{phase}/issue_filter_tasks/tasks.jsonl.issue_filter
```

## Pipeline Summary

```
Step 1: Preparation
  ├─ tokens.txt (GitHub tokens)
  └─ Environment variables (OPENAI_API_BASE_URL, OPENAI_KEY)

Step 2: Data Collection (curation.sh)
  ├─ crawl_repo.py          → output/{lang}/raw_repos.jsonl
  ├─ filter_repo.py         → output/{lang}/filtered_repos.jsonl
  ├─ run_get_tasks_pipeline → output/{lang}/{phase}/results/tasks/
  └─ merge_tasks.py         → output/{lang}/{phase}/tasks.jsonl

Step 3: Quality Assessment (issue_filter.sh)
  └─ issue_eval.py          → output/{lang}/{phase}/issue_filter_tasks/
                              tasks.jsonl.issue_filter
```

## Notes

- The pipeline is designed for large-scale data collection (thousands of repositories)
- Execution time varies depending on the number of repositories and API rate limits
- Intermediate results are cached; the pipeline can be resumed if interrupted
- Always respect GitHub's API rate limits and terms of service
