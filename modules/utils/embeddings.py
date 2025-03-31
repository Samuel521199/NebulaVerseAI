"""
文本嵌入工具模块
使用sentence-transformers生成文本向量表示
"""

from sentence_transformers import SentenceTransformer
from modules.utils.logger import logger
from modules.utils.config import Config
import numpy as np

class EmbeddingFunction:
    def __init__(self):
        self.logger = logger
        self.config = Config()
        self.dimension = 384  # sentence-transformer 的维度
        
        # 初始化sentence-transformer模型
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.logger.info("成功加载sentence-transformer模型")
        except Exception as e:
            self.logger.error(f"加载sentence-transformer模型失败: {str(e)}")
            raise

    def __call__(self, input):
        """生成文本的向量表示
        
        Args:
            input: 输入文本列表或单个文本
            
        Returns:
            向量列表
        """
        try:
            # 确保输入是列表
            if isinstance(input, str):
                input = [input]
            elif not isinstance(input, list):
                input = [str(input)]
            
            # 使用sentence-transformer生成向量
            embeddings = self.model.encode(input, convert_to_list=True)
            return embeddings
            
        except Exception as e:
            self.logger.error(f"生成文本嵌入时出错: {str(e)}")
            # 生成一个默认向量而不是返回None
            default_vector = np.zeros(self.dimension)
            default_vector[0] = 1  # 设置一个非零值
            return [default_vector.tolist()] * len(input)

def get_embeddings():
    """获取嵌入函数实例"""
    return EmbeddingFunction() 