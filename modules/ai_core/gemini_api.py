"""
Gemini API模块
处理与Google Gemini API的所有交互
"""

import requests
import json
from modules.utils.logger import logger
from modules.utils.config import Config
import time

class GeminiAPI:
    def __init__(self):
        self.logger = logger
        self.config = Config()
        self.api_key = self.config.get("GEMINI_API_KEY")
        self.model_name = self.config.get("GEMINI_MODEL", "gemini-1.5-flash")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.max_retries = 3
        self.retry_delay = 2  # 重试延迟（秒）

    def generate_content(self, prompt):
        """生成AI响应"""
        try:
            # 构建请求URL
            url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
            
            # 构建请求体
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            # 发送请求（带重试机制）
            for attempt in range(self.max_retries):
                try:
                    response = requests.post(
                        url,
                        json=payload,
                        timeout=30  # 设置超时时间
                    )
                    response.raise_for_status()  # 检查HTTP错误
                    
                    # 解析响应
                    result = response.json()
                    
                    # 检查API错误
                    if "error" in result:
                        error_msg = result["error"].get("message", "未知错误")
                        self.logger.error(f"API返回错误: {error_msg}")
                        return f"抱歉，API返回错误: {error_msg}"
                    
                    # 提取生成的文本
                    if "candidates" in result and result["candidates"]:
                        return result["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        return "抱歉，无法生成有效的响应。"
                        
                except requests.exceptions.RequestException as e:
                    if attempt < self.max_retries - 1:
                        self.logger.warning(f"API请求失败（尝试 {attempt + 1}/{self.max_retries}）: {str(e)}")
                        time.sleep(self.retry_delay)  # 等待后重试
                        continue
                    else:
                        self.logger.error(f"API请求失败: {str(e)}")
                        return "抱歉，我现在无法连接到API服务。请稍后再试。"
                        
        except Exception as e:
            self.logger.error(f"生成内容时出错: {str(e)}")
            return "抱歉，处理请求时出现错误。"
