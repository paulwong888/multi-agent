import requests


resp = requests.post(
    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
    headers={"Authorization": "Bearer sk-a6856b0574784d5aae1d358cad4e7fe5", "Content-Type": "application/json"},
    json = {
    # "model": "qwen3-235b-a22b",
    "model": "qwen-max-latest",
    'stream': False,
    "enable_thinking": False,
    "enable_search": True,
    "search_options": {
        "forced_search": True,
        "search_strategy": "pro"
    },
    # 'stream_options': {"include_usage": False},
    "messages": [
        {
            "role": "user",
            "content": "现在哪吒2的票房是多少"
        }
    ]}
)
import json
print(json.loads(resp.content)['choices'][0]['message'])
print('----------------')