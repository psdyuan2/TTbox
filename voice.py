import requests
import json
from config import *
import pygame
import time
import os

group_id = GROUP_ID
api_key = MINIMAX_API_KEY

url = "https://api.minimaxi.com/v1/t2a_v2"


def play_audio(file_path):
    """使用 pygame 播放一个音频文件"""

    # 检查文件是否存在，避免程序因找不到文件而崩溃
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{file_path}'")
        return

    # 初始化 pygame 的音频模块
    pygame.mixer.init()

    try:
        # 加载音乐文件
        pygame.mixer.music.load(file_path)

        # 播放音乐
        print(f"正在播放: {os.path.basename(file_path)}")  # 只显示文件名，更整洁
        pygame.mixer.music.play()

        # 使用一个循环来等待音乐播放结束
        # 这样程序就不会在音乐开始播放后立刻退出
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)  # 短暂休眠，降低CPU占用

    except pygame.error as e:
        print(f"播放时发生错误: {e}")
    finally:
        # 停止播放并卸载模块（好习惯）
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("播放结束。")


def get_audio(text):
    payload = {
        "model": "speech-02-hd",
        "text": text,
        "stream": False,
        "language_boost": "auto",
        "output_format": "hex",
        "voice_setting": {
            "voice_id": "male-qn-qingse",
            "speed": 1,
            "vol": 1,
            "pitch": 0,
            "emotion": "happy"
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        }
    }
    payload = json.dumps(payload)
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, stream=True, headers=headers, data=payload)
    parsed_json = json.loads(response.text)

    # 获取audio字段的值
    audio_value = bytes.fromhex(parsed_json['data']['audio'])
    with open('./data/output.mp3', 'wb') as f:
        f.write(audio_value)
    # 播放音频
    play_audio('./data/output.mp3')
