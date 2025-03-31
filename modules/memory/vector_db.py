"""
向量数据库管理模块
使用ChromaDB管理对话历史和向量存储
"""

import chromadb
from chromadb.config import Settings
from modules.utils.logger import logger
from modules.utils.config import Config
from modules.utils.embeddings import get_embeddings
import uuid
import numpy as np
import os

class VectorDB:
    def __init__(self):
        self.logger = logger
        self.config = Config()
        self.dimension = 384  # sentence-transformer 的维度
        self.embedding_function = get_embeddings()
        
        # 确保db目录存在
        db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db')
        self.logger.info(f"数据库目录路径: {db_dir}")
        
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            self.logger.info(f"创建数据库目录: {db_dir}")
        
        # 初始化ChromaDB客户端
        self.client = chromadb.PersistentClient(path=db_dir)
        self.logger.info(f"ChromaDB客户端初始化完成，持久化目录: {db_dir}")
        
        # 创建或获取集合
        try:
            # 先尝试删除已存在的集合
            try:
                self.client.delete_collection("conversation_history")
                self.logger.info("删除已存在的conversation_history集合")
            except Exception as e:
                self.logger.info(f"没有找到已存在的conversation_history集合: {str(e)}")
                
            # 创建新集合
            self.collection = self.client.create_collection(
                name="conversation_history",
                metadata={"hnsw:space": "cosine"},
                embedding_function=self.embedding_function
            )
            self.logger.info("创建新的conversation_history集合")
            
            # 添加一个初始化文档
            init_text = "初始化文档"
            init_embedding = self.embedding_function(init_text)[0]
            self.collection.add(
                documents=[init_text],
                embeddings=[init_embedding],
                metadatas=[{"role": "system", "timestamp": self._get_timestamp()}],
                ids=["init"]
            )
            self.logger.info("添加初始化文档到集合")
            
            # 验证数据库文件是否创建
            db_files = os.listdir(db_dir)
            self.logger.info(f"数据库目录中的文件: {db_files}")
            
            self.logger.info("成功初始化向量数据库")
        except Exception as e:
            self.logger.error(f"初始化向量数据库失败: {str(e)}")
            raise

    def store_conversation(self, user_input, ai_response):
        """存储对话记录"""
        try:
            # 生成唯一的ID
            user_id = str(uuid.uuid4())
            assistant_id = str(uuid.uuid4())
            
            # 确保输入是字符串类型
            user_input = str(user_input)
            ai_response = str(ai_response)
            
            # 分别存储用户输入和AI响应
            try:
                # 生成用户输入的向量
                user_embedding = self.embedding_function(user_input)[0]
                
                # 存储用户输入
                self.collection.add(
                    documents=[user_input],
                    embeddings=[user_embedding],
                    metadatas=[{"role": "user", "timestamp": self._get_timestamp()}],
                    ids=[user_id]
                )
                self.logger.info(f"存储用户输入: {user_input}")
                
                # 生成AI响应的向量
                ai_embedding = self.embedding_function(ai_response)[0]
                
                # 存储AI响应
                self.collection.add(
                    documents=[ai_response],
                    embeddings=[ai_embedding],
                    metadatas=[{"role": "assistant", "timestamp": self._get_timestamp()}],
                    ids=[assistant_id]
                )
                self.logger.info(f"存储AI响应: {ai_response}")
                
                # 验证存储
                results = self.collection.get()
                self.logger.info(f"当前集合中的文档数量: {len(results['ids'])}")
                
                # 验证数据库文件
                db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db')
                db_files = os.listdir(db_dir)
                self.logger.info(f"数据库目录中的文件: {db_files}")
                
                self.logger.info("对话记录已存储")
            except Exception as e:
                self.logger.error(f"存储对话记录时出错: {str(e)}")
                # 如果存储失败，尝试重新初始化集合
                try:
                    # 删除现有集合
                    self.client.delete_collection("conversation_history")
                    self.logger.info("删除失败的集合")
                    
                    # 创建新集合
                    self.collection = self.client.create_collection(
                        name="conversation_history",
                        metadata={"hnsw:space": "cosine"},
                        embedding_function=self.embedding_function
                    )
                    self.logger.info("创建新的集合")
                    
                    # 添加初始化文档
                    init_text = "初始化文档"
                    init_embedding = self.embedding_function(init_text)[0]
                    self.collection.add(
                        documents=[init_text],
                        embeddings=[init_embedding],
                        metadatas=[{"role": "system", "timestamp": self._get_timestamp()}],
                        ids=["init"]
                    )
                    self.logger.info("添加初始化文档")
                    
                    # 重新尝试存储
                    user_embedding = self.embedding_function(user_input)[0]
                    self.collection.add(
                        documents=[user_input],
                        embeddings=[user_embedding],
                        metadatas=[{"role": "user", "timestamp": self._get_timestamp()}],
                        ids=[user_id]
                    )
                    self.logger.info("重新存储用户输入")
                    
                    ai_embedding = self.embedding_function(ai_response)[0]
                    self.collection.add(
                        documents=[ai_response],
                        embeddings=[ai_embedding],
                        metadatas=[{"role": "assistant", "timestamp": self._get_timestamp()}],
                        ids=[assistant_id]
                    )
                    self.logger.info("重新存储AI响应")
                    
                    # 验证数据库文件
                    db_files = os.listdir(db_dir)
                    self.logger.info(f"数据库目录中的文件: {db_files}")
                    
                    self.logger.info("对话记录已重新存储")
                except Exception as e2:
                    self.logger.error(f"重新存储对话记录时出错: {str(e2)}")
            
        except Exception as e:
            self.logger.error(f"存储对话记录时出错: {str(e)}")

    def get_recent_history(self, limit=5):
        """获取最近的对话历史"""
        try:
            # 获取所有记录
            results = self.collection.get()
            
            # 如果没有记录，返回空结果
            if not results['ids']:
                self.logger.info("没有找到历史记录")
                return None
                
            # 按时间戳排序
            sorted_indices = sorted(
                range(len(results['metadatas'])),
                key=lambda i: results['metadatas'][i]['timestamp'],
                reverse=True
            )[:limit]
            
            # 重新组织结果
            history = {
                'documents': [results['documents'][i] for i in sorted_indices],
                'metadatas': [results['metadatas'][i] for i in sorted_indices],
                'ids': [results['ids'][i] for i in sorted_indices]
            }
            self.logger.info(f"获取到 {len(history['documents'])} 条历史记录")
            return history
            
        except Exception as e:
            self.logger.error(f"获取对话历史时出错: {str(e)}")
            return None

    def search_similar(self, query, limit=3):
        """搜索相似对话"""
        try:
            # 确保查询是字符串类型
            if not isinstance(query, str):
                query = str(query)
            
            # 执行查询
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            # 验证结果
            if not results or not results.get('documents'):
                self.logger.info("没有找到相似的对话")
                return None
                
            self.logger.info(f"找到 {len(results['documents'][0])} 条相似对话")
            return results
            
        except Exception as e:
            self.logger.error(f"搜索相似对话时出错: {str(e)}")
            return None

    def _get_timestamp(self):
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat() 