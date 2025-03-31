"""
配置管理模块
处理应用程序的配置信息
"""

import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 默认配置
        self.default_config = {
            "GEMINI_API_KEY": None,
            "MODEL_NAME": "gemini-1.5-flash",
            "EMBEDDING_MODEL": "embedding-001",
            "EMBEDDING_DIMENSION": 128,
            "DB_DIRECTORY": "db"
        }

    def get_api_key(self):
        """获取API密钥"""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            api_key = input("请输入你的 Gemini API 密钥: ")
        return api_key

    def get(self, key, default=None):
        """获取配置值"""
        return os.environ.get(key, self.default_config.get(key, default)) 