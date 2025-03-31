"""
日志管理模块
配置和管理应用程序的日志记录
"""

import logging
import os
from datetime import datetime

def setup_logger():
    """设置日志记录器"""
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 配置日志记录器
    logger = logging.getLogger('ai_chatbot')
    logger.setLevel(logging.INFO)

    # 创建文件处理器
    log_file = f'logs/chatbot_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# 创建一个全局的logger实例
logger = setup_logger()
