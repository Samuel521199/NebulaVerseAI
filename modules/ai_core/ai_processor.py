from modules.ai_core.gemini_api import generate_content

class AIProcessor:
    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model

    def process_input(self, prompt):
        # 处理输入并返回 Gemini API 的结果
        ai_response = generate_content(self.api_key, self.model, prompt)
        return ai_response
