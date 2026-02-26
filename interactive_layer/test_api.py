import requests
import json

url = "http://127.0.0.1:8001/chat"
payload = {"user_input": "总结一下最近国际利率相关的新闻"}

try:
    print(f"发送测试请求到: {url}")
    print(f"测试问题: {payload['user_input']}")
    response = requests.post(url, json=payload, timeout=30)
    print("\nAPI 返回状态码:", response.status_code)
    if response.status_code == 200:
        print("\n智能体回答:")
        print(response.json().get("answer"))
    else:
        print("错误信息:", response.text)
except Exception as e:
    print(f"请求失败: {e}")
