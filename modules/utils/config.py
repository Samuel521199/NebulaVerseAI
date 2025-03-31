"""
配置管理模块
管理应用程序的配置信息
"""

import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 数据库配置
        self.db_directory = os.getenv("DB_DIRECTORY", "db")
        
        # 日志配置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # AI配置
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.ai_model = os.getenv("AI_MODEL", "gemini-2.0-flash")
        
        # 模型配置
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "embedding-001")
        self.embedding_dimension = int(os.getenv("EMBEDDING_DIMENSION", "128"))
        
        # 语音模块配置
        self.enable_tts = os.getenv("ENABLE_TTS", "false").lower() == "true"
        self.tts_voice = os.getenv("TTS_VOICE", "zh-CN-XiaoxiaoNeural")
        self.tts_output_dir = os.getenv("TTS_OUTPUT_DIR", "audio")
        self.save_audio = os.getenv("SAVE_AUDIO", "true").lower() == "true"

    def get(self, key, default=None):
        """获取配置值"""
        return getattr(self, key, default)

    def get_api_key(self):
        """获取API密钥"""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            api_key = input("请输入你的 Gemini API 密钥: ")
        return api_key

    def get_model_name(self):
        """获取模型名称"""
        return self.model_name

    def get_embedding_model(self):
        """获取嵌入模型"""
        return self.embedding_model

    def get_embedding_dimension(self):
        """获取嵌入维度"""
        return self.embedding_dimension

    def get_db_directory(self):
        """获取数据库目录"""
        return self.db_directory

    def get_log_level(self):
        """获取日志级别"""
        return self.log_level

    def get_log_format(self):
        """获取日志格式"""
        return self.log_format

    def get_enable_tts(self):
        """获取是否启用语音合成"""
        return self.enable_tts

    def get_tts_voice(self):
        """获取语音合成声音"""
        return self.tts_voice

    def get_tts_output_dir(self):
        """获取语音合成输出目录"""
        return self.tts_output_dir

    def get_save_audio(self):
        """获取是否保存音频文件"""
        return self.save_audio 