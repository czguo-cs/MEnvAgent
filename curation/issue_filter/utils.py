from collections import Counter
import requests
import random
import json
import time
import uuid
import os


def convert_context_to_messages(context, system_message=""):
    assert len(context) % 2 == 1
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    for idx, utt in enumerate(context):
        if idx % 2 == 0:
            messages.append({"role": "user", "content": utt})
        else:
            messages.append({"role": "assistant", "content": utt})
    # print(json.dumps(messages, ensure_ascii=False, indent=2))
    return messages


def request_g4(context, model_id, system_message=""):
    # Configure your API endpoint and key
    url = os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1") + "/chat/completions"
    api_key = os.environ.get("OPENAI_KEY", "your-api-key-here")

    payload = {
        "model": model_id,
        "messages": convert_context_to_messages(context, system_message)
    }
    if model_id == "gemini-2.5-pro":
        payload["extra_body"] = {
            "generationConfig":{
                "thinkingConfig": {
                    "includeThoughts": True,
                    "thinkingBudget": -1
                }
            }
        }
        
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try_num = 3
    res = {"choices": None}
    while try_num > 0 and res["choices"] == None:
        try:
            try_num -= 1
            res = requests.request("POST", url, json=payload, timeout=1000, headers=headers).json()
            # print(json.dumps(res, indent=2, ensure_ascii=False))
            response, reasoning, _, _ = parse_g4_result(res)
        except Exception as e:
            print(f"{try_num}, {e}")
            res = {"choices": None}
            time.sleep(1)

    if res["choices"] == None:
        return "ERROR", "ERROR"
    else:
        return reasoning, response

def parse_g4_result(result):
    response = result["choices"][0]["message"]["content"]
    if "reasoning_content" in result["choices"][0]["message"]:
        reasoning = result["choices"][0]["message"]["reasoning_content"]
    else:
        reasoning = ""
    prompt_token = result["usage"]["prompt_tokens"]
    completion_token = result["usage"]["completion_tokens"]
    return response, reasoning, prompt_token, completion_token

