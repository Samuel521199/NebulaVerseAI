"""
NebulaVerseAI - 基于Google Gemini API的智能对话系统
主要功能：
1. 支持自定义AI角色设定
2. 使用ChromaDB存储对话历史
3. 实现多轮对话上下文管理
4. 通过Gemini API生成智能回复
"""

import os
import json
import requests
from vector_db.chroma_db import ChromaManager  # 导入向量数据库管理类

# 1. 加载 AI 角色设定
def load_ai_persona(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        persona = json.load(f)
    return persona

# 5. 构建 Prompt (包含角色和对话历史)
def build_prompt(persona, conversation_history, user_input):
    prompt = f"""你是一个名为 {persona['name']} 的 AI 助手。{persona['description']} 你的语气是：{persona['tone']}
    这是之前的对话历史: {conversation_history}
    用户输入：{user_input} 请根据以上信息，生成一个符合你角色的回复。"""
    return prompt

# 6. 调用 Gemini API (使用 requests)
def generate_content(api_key, model_name, prompt):
    import requests
    import json
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

def main():
    import os
    # 替换为你的 Gemini API 密钥
    api_key = os.environ.get("GEMINI_API_KEY")  # 从环境变量中读取 API 密钥
    if not api_key:
        api_key = input("请输入你的 Gemini API 密钥: ")

    session_id = "user123"  # 每个用户的会话ID

    # 1. 加载 AI 角色
    persona = load_ai_persona("ai_persona.json")

    # 2. 初始化 ChromaDB
    db = ChromaManager(api_key) #将API 密钥传入chroma

    # 循环对话
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # 3. 加载对话历史
        conversation_history = db.load_conversation_history(session_id)

        # 4. 构建 Prompt
        prompt = build_prompt(persona, conversation_history, user_input)

        # 5. 调用 Gemini API (使用 requests)
        ai_response = generate_content(api_key, "gemini-2.0-flash", prompt)  # 使用 requests

        print(f"{persona['name']}: {ai_response}")

        # 6. 存储对话到向量数据库
        db.store_conversation(user_input, ai_response, session_id)

if __name__ == "__main__":
    main()