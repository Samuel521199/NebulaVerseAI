import os
import json
import requests

def generate_content(api_key, model_name, prompt):
    """
    调用 Gemini API 生成文本回复
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)  # 设置超时时间
        response.raise_for_status()  # 检查 HTTP 状态码
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"API 请求失败: {e}")
        return "抱歉，我无法生成回复。"
    except KeyError as e:
        print(f"API 响应解析失败: {e}")
        return "抱歉，我无法解析回复。"