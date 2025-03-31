from modules.utils.logger import logger
import chromadb  # 确保你已安装这个库
from modules.utils.embeddings import get_embeddings  # 假设你有这个函数来获取文本的嵌入

class ChromaManager:
    def __init__(self, api_key):
        self.client = chromadb.Client()  # 初始化 Chroma 客户端
        self.collection = self.client.get_or_create_collection("conversation_history")
        self.api_key = api_key

    def load_conversation_history(self, session_id):
        # 假设你能从数据库加载历史记录
        logger.info(f"加载会话 {session_id} 的历史记录")
        results = self.collection.query(where={"session_id": session_id}, n_results=5)
        return results.get("documents", [])

    def search(self, query, n_results=3, where=None):
        logger.info(f"正在搜索查询: {query}")
        # 使用嵌入搜索查询相关记录
        embedding = get_embeddings(query)
        return self.collection.query(embedding=embedding, n_results=n_results, where=where)

    def store_conversation(self, user_input, ai_response, session_id, metadata):
        logger.info(f"存储对话记录: {session_id}")
        # 假设你将对话记录存储到数据库
        document = {
            "session_id": session_id,
            "user_input": user_input,
            "ai_response": ai_response,
            "metadata": metadata
        }
        self.collection.add(documents=[document])
