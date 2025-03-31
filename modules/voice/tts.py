"""
文字转语音模块
使用 edge-tts 实现文字转语音功能
"""

import edge_tts
import asyncio
import os
import pygame
from datetime import datetime
from modules.utils.logger import logger
from modules.utils.config import Config
from modules.utils.cleanText import clean_text

class TextToSpeech:
    def __init__(self):
        self.config = Config()
        self.voice = self.config.get_tts_voice()
        self.output_dir = self.config.get_tts_output_dir()
        self.save_audio = self.config.get_save_audio()
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        # 初始化 pygame 音频
        pygame.mixer.init()

    async def text_to_speech(self, text, filename=None):
        """将文本转换为语音并保存为文件
        
        Args:
            text: 要转换的文本
            filename: 输出文件名（可选）
            
        Returns:
            生成的音频文件路径
        """
        try:
            # 清理文本
            text = clean_text(text)
            if not filename:
                # 使用时间戳生成文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tts_{timestamp}.mp3"
            
            output_path = os.path.join(self.output_dir, filename)
            
            # 使用 edge-tts 生成语音
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice
            )
            await communicate.save(output_path)
            
            if self.save_audio:
                logger.info(f"语音文件已生成: {output_path}")
            else:
                # 如果不保存音频，删除文件
                os.remove(output_path)
                logger.info("语音已播放，文件已删除")
            
            return output_path
            
        except Exception as e:
            logger.error(f"生成语音文件时出错: {str(e)}")
            return None

    def speak(self, text):
        """将文本转换为语音并立即播放
        
        Args:
            text: 要转换的文本
            
        Returns:
            生成的音频文件路径
        """
        try:
            # 生成语音文件
            audio_path = asyncio.run(self.text_to_speech(text))
            if audio_path:
                # 播放音频
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                # 等待播放完成
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                # 停止播放
                pygame.mixer.music.stop()
                
                # 如果不保存音频，删除文件
                if not self.save_audio:
                    os.remove(audio_path)
                    return None
                    
                return audio_path
            return None
            
        except Exception as e:
            logger.error(f"播放语音时出错: {str(e)}")
            return None

def get_tts():
    """获取TTS实例"""
    return TextToSpeech() 