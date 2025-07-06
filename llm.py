import requests
import readline
from config import *
from voice import get_audio
group_id = GROUP_ID
api_key = MINIMAX_API_KEY

url = f"https://api.minimaxi.com/v1/text/chatcompletion_v2"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

with open("prompt_template.txt", "r") as f:
    prompt = f.read()
# tokens_to_generate/bot_setting/reply_constraints可自行修改
request_body = payload = {
    "model": "MiniMax-Text-01",
    "messages": [
        {
            "role": "system",
            "name": "小听宝",
            "content": prompt
        },
        {
            "role": "user",
            "name": "原笑笑",  # 选填字段
            "content": "你好"
        }
    ]
}
# 添加循环完成多轮交互

while True:
    # 下面的输入获取是基于python终端环境，请根据您的场景替换成对应的用户输入获取代码
    line = input("发言:")
    # 将当次输入内容作为用户的一轮对话添加到messages
    request_body["messages"].append(
        {
            "role": "user",
            "name": "原笑笑",  # 选填字段
            "content": line
        }
    )
    response = requests.post(url, headers=headers, json=request_body)
    reply = response.json()
    message = reply["choices"][0]["message"]
    # print(f"reply: {reply}")
    print(message["content"])
    get_audio(message["content"])
    #  将当次的ai回复内容加入messages
    request_body["messages"].append(
        {
            "role": message["role"],
            "name": message["name"],  # 选填字段
            "content": message["content"]
        }
    )
