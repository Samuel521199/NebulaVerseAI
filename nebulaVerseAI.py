import os
import json
from modules.gemini_api import generate_content  # 导入 Gemini API 模块
from modules.chroma_manager import ChromaManager  # 导入 ChromaDB 模块

# 1. 加载 AI 角色设定
def load_ai_persona(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        persona = json.load(f)
    return persona

# 5. 构建 Prompt (包含角色和对话历史)
def build_prompt(persona, conversation_history, user_input,relevant_context=None):
    prompt = f"""你是一个名为 {persona['name']} 的 AI 助手。{persona['description']} 你的语气是：{persona['tone']}
    这是之前的对话历史: {conversation_history}

    用户输入：{user_input} 

    相关历史信息：{relevant_context}

    请根据以上信息，生成一个符合你角色的回复。"""
    return prompt

def main():
    # 替换为你的 Gemini API 密钥
    api_key = os.environ.get("GEMINI_API_KEY")  # 从环境变量中读取 API 密钥
    if not api_key:
        api_key = input("请输入你的 Gemini API 密钥: ")

    session_id = "user123"  # 每个用户的会话ID

    # 1. 加载 AI 角色
    persona = load_ai_persona("ai_persona.json")

    # 2. 初始化 ChromaDB
    db = ChromaManager(api_key)  #传递key

    # 循环对话
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:  # 添加退出指令
            print("感谢使用！再见！")
            break

        # 3. 加载对话历史
        conversation_history = db.load_conversation_history(session_id)

         # 4. 构建 Prompt
        # 添加元数据搜索
        search_filter = {"session_id": session_id}  # 仅搜索当前会话的记录
        relevant_context = db.search(user_input, n_results=3, where=search_filter)
        prompt = build_prompt(persona, conversation_history, user_input, relevant_context=relevant_context)


        # 5. 调用 Gemini API (使用 requests)
        ai_response = generate_content(api_key, "gemini-2.0-flash", prompt)  # 使用 Gemini API 模块

        print(f"{persona['name']}: {ai_response}")

        # 6. 存储对话到向量数据库
        # 添加用户情感和意图信息
        user_sentiment = "positive"  # 替换为情感分析结果
        ai_intent = "provide_information"  # 替换为意图识别结果

        metadata = {"user_sentiment": user_sentiment, "ai_intent": ai_intent}
        db.store_conversation(user_input, ai_response, session_id, metadata=metadata)
if __name__ == "__main__":
    main()