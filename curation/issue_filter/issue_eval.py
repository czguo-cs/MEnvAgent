import json
import re
from tqdm import tqdm
from multiprocessing import Pool
from utils import request_g4
import os
import argparse
# 使用issue_prompt.py中的标准提示模板
EVAL_PROMPT = """
你是一位经验丰富的软件工程师，你需要评估Issue质量，判断Issue是否包含足够信息，以便工程师能够无歧义地给出解决方案。

**Issue评分标准**
满分为10分，其中10分表示质量非常好(issue描述清晰，解决方案所需条件明确)，0分表示质量非常差(无法理解需要解决的问题是什么)
注：无法根据Issue实现解决方案的，评分不应高于5分

扣分项核查需要逐条解释是否存在扣分，如果发现issue存在问题或者违反了评分标准请及时指出，并在后续的评估中进行扣分。
以下是重要扣分项（违反一项扣5分）：
1. 关键信息缺失
    缺少预期结果：未说明代码修复后系统应有的正确行为或输出；涉及数据处理时，未提供输入示例及期望/错误输出
    缺乏重现步骤：未提供重现问题的操作流程或可运行的代码示例
    遗漏版本信息：未提供使用的库、框架、操作系统及相关软件的具体版本号；跨平台问题未明确环境细节
    错误日志不完整：仅提供错误信息片段，缺少关键的上下文或堆栈跟踪
2、非Issue类型提交
    误用 PR 描述：将 Pull Request (PR) 的说明性文字直接作为 Issue
    已解决问题：Issue 所描述的问题已被修复或关闭
    非问题咨询：内容涉及代码版本发布计划、未来功能咨询等，而非实际的缺陷报告或功能描述

以下是常见扣分项（根据严重程度酌情扣分）：
1、Issue表述不清
    问题混杂：单个 Issue 包含多个无关问题，或问题描述本身存在逻辑矛盾
    术语未定义：使用了未加解释的项目专有名词或缩写
    要求未量化：使用模糊描述（如"合理的默认值"、"用户友好"、"速度更快"、"更高效"），缺乏可衡量的验收标准，或未清晰界定问题的具体范围或边界
    测试用例低质(如果有)：提供的测试用例不充分、过于宽泛、缺失或要求不足（通过测试用例并不能够表明issue得到解决）
2、过度依赖外部资源
    核心信息依赖外部链接：关键问题描述、日志或重现步骤存放在可能失效或无法访问的外部链接中
    依赖私有仓库：问题重现依赖于非公开的代码库，导致他人无法验证


**内容如下**
Issue
{issue}


请提供你的专业评估分析并直接输出一个数字(严格按照以下格式输出)：
reason for evaluation:xxx
issue score:0-10
"""

MODEL_ID = "deepseek-v3.1"
# MODEL_ID = "kimi-k2-instruct"
MAX_RETRIES = 3

def parse_eval_response(response: str) -> tuple:
    """解析评估响应，提取评分和分析"""
    try:
        analysis = re.search(r"reason for evaluation:(.*?)issue score:", response, re.DOTALL)
        score = re.search(r"issue score:(\d+)", response)
        
        if not analysis or not score:
            raise ValueError("Invalid response format")
            
        return analysis.group(1).strip(), int(score.group(1))
    except Exception as e:
        raise ValueError(f"Failed to parse response: {str(e)}")

def get_eval_response(line: dict) -> dict:
    """获取单条issue的评估结果"""
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
    """保存评估结果到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

def save_filtered_results(results: list, output_file: str):
    """保存过滤后的结果(score>5)"""
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
        required=True, # 标记为必填参数
        help="要处理的原始 .jsonl 文件路径。"
    )
    parser.add_argument(
        '--output_dir', 
        '-o',
        type=str,
        required=True, # 标记为必填参数
        help="输出目录"
    )
    
    args = parser.parse_args()
    basename = os.path.basename(args.input_file)
    suffix = os.path.basename(args.input_file).split('.',1)[1]
    output_file = f"{args.output_dir}/{basename}.evaluation_result"
    filtered_output_file = f"{args.output_dir}/{basename}.issue_filter"
    # 读取输入数据
    with open(args.input_file, 'r', encoding='utf-8') as f:
        test_data = [json.loads(line) for line in f]
    
    # 并行处理评估
    with Pool(processes=32) as pool:
        results = list(tqdm(
            pool.imap(get_eval_response, test_data),
            total=len(test_data),
            desc="Evaluating issues"
        ))
    
    # 保存全部结果
    save_results(results, output_file)
    total_count = len(results)
    print(f"Evaluation completed. Total issues: {total_count}. Results saved to {output_file}")
    
    # 保存过滤后的结果
    filtered_count = save_filtered_results(results, filtered_output_file)
    print(f"Filtered results: {filtered_count}/{total_count} issues with score >5, saved to {filtered_output_file}")
    print(f"Filter ratio: {filtered_count/total_count:.1%}")
