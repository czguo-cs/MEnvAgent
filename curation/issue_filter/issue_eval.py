import json
import re
from tqdm import tqdm
from multiprocessing import Pool
from utils import request_g4
import os
import argparse

# Standard evaluation prompt template for Issue quality assessment
EVAL_PROMPT = """
**Role Definition**
You are an experienced software engineer. You need to evaluate the quality of an Issue to determine if it contains sufficient information for an engineer to unambiguously provide a solution.

**Issue Scoring Standards**
The full score is 10 points (Excellent quality: clear description, explicit requirements for the solution), and 0 points indicates very poor quality (impossible to understand the problem).
Note: If a solution cannot be implemented based on the Issue, the score should not exceed 5.

**Deduction Rules**
Check for deduction items item by item. If the issue has problems or violates the standards, point it out and deduct points in the subsequent evaluation.

**1. Major Deductions (Violating any item results in a 5-point deduction):**
- Key Information Missing:
  (1) Lack of expected results: No description of correct behavior/output; for data processing, missing input examples and expected/error outputs.
  (2) Lack of reproduction steps: No operation flow or runnable code to reproduce the issue.
  (3) Missing version info: Unspecified libraries, frameworks, OS, or environment details.
  (4) Incomplete error logs: Snippets provided without context or stack traces.
- Non-Issue Type Submission:
  (1) Misuse of PR description: Using Pull Request description text directly as an Issue.
  (2) Solved problem: The problem described is already fixed or closed.
  (3) Non-problem inquiry: Content involves release plans, future feature questions, etc., rather than actual defects.

**2. Common Deductions (Deduct points based on severity):**
- Unclear Description:
  (1) Mixed problems: Single Issue contains multiple unrelated problems or logical contradictions.
  (2) Undefined terminology: Uses unexplained jargon or abbreviations.
  (3) Unquantified requirements: Uses vague descriptions (e.g., "reasonable defaults", "user-friendly", "faster") without measurable acceptance criteria.
  (4) Low-quality test cases: Insufficient, overly broad, or missing test cases (passing the test does not prove the issue is resolved).
- Excessive Reliance on External Resources:
  (1) Core info relies on external links: Key descriptions/logs/steps are in links that may fail or be inaccessible.
  (2) Reliance on private repos: Reproduction depends on non-public codebases.

**Input Content**
Issue
{issue}

**Output Format**
Please provide your professional analysis and strictly output a number in the following format:
reason for evaluation: xxx
issue score: 0-10
"""

MODEL_ID = "deepseek-v3.2"
MAX_RETRIES = 3

def parse_eval_response(response: str) -> tuple:
    """Parse evaluation response to extract score and analysis"""
    try:
        analysis = re.search(r"reason for evaluation:(.*?)issue score:", response, re.DOTALL)
        score = re.search(r"issue score:(\d+)", response)
        
        if not analysis or not score:
            raise ValueError("Invalid response format")
            
        return analysis.group(1).strip(), int(score.group(1))
    except Exception as e:
        raise ValueError(f"Failed to parse response: {str(e)}")

def get_eval_response(line: dict) -> dict:
    """Get evaluation result for a single issue"""
    issue_text = f"{line['problem_statement']}"
    input_prompt = EVAL_PROMPT.format(issue=issue_text)
    
    for attempt in range(MAX_RETRIES):
        try:
            reasoning, response = request_g4([input_prompt], model_id=MODEL_ID)
            # print(response)
            analysis, score = parse_eval_response(response)
            
            return {
                **line,
                "issue_filter_result": response,
                "issue_filter_reason": reasoning,
                "issue_filter_score": score,
                "issue_filter_analysis": analysis
            }
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for issue {line.get('id', 'unknown')}: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                return {
                    **line,
                    "issue_filter_result": "Evaluation failed",
                    "issue_filter_reason": str(e),
                    "issue_filter_score": -1,
                    "issue_filter_analysis": ""
                }
def save_results(results: list, output_file: str):
    """Save evaluation results to file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

def save_filtered_results(results: list, output_file: str):
    """Save filtered results (score >= 5)"""
    filtered = [r for r in results if r.get("issue_filter_score", -1) >= 5]
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in filtered:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    return len(filtered)

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_file',
        '-i',
        type=str,
        required=True,
        help="Path to the input .jsonl file to process."
    )
    parser.add_argument(
        '--output_dir',
        '-o',
        type=str,
        required=True,
        help="Output directory for evaluation results."
    )

    args = parser.parse_args()
    basename = os.path.basename(args.input_file)
    suffix = os.path.basename(args.input_file).split('.',1)[1]
    output_file = f"{args.output_dir}/{basename}.evaluation_result"
    filtered_output_file = f"{args.output_dir}/{basename}.issue_filter"

    # Read input data
    with open(args.input_file, 'r', encoding='utf-8') as f:
        test_data = [json.loads(line) for line in f]

    # Parallel evaluation processing
    with Pool(processes=32) as pool:
        results = list(tqdm(
            pool.imap(get_eval_response, test_data),
            total=len(test_data),
            desc="Evaluating issues"
        ))

    # Save all results
    save_results(results, output_file)
    total_count = len(results)
    print(f"Evaluation completed. Total issues: {total_count}. Results saved to {output_file}")

    # Save filtered results
    filtered_count = save_filtered_results(results, filtered_output_file)
    print(f"Filtered results: {filtered_count}/{total_count} issues with score >=5, saved to {filtered_output_file}")
    print(f"Filter ratio: {filtered_count/total_count:.1%}")
