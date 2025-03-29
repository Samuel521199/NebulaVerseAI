import os
import chromadb
from langchain_chroma import Chroma
import numpy as np  # 导入 numpy

class ChromaManager:
    def __init__(self, embedding_dimension=128, persist_directory="db"):  # 请替换为您实际的 Embedding 维度
        self.embedding_dimension = embedding_dimension
        self.persist_directory = persist_directory
        self.db = self._initialize_chroma()

    def _initialize_chroma(self):
        class EmbeddingFunction:
            def __init__(self, embedding_dimension):
                self.embedding_dimension = embedding_dimension

            def embed_documents(self, texts):
                embeddings = []
                for text in texts:
                    # 使用本地随机向量，不需要api key
                    embedding = np.random.rand(self.embedding_dimension).tolist() #添加了np向量
                    embeddings.append(embedding)
                return embeddings

        embedding_fn = EmbeddingFunction(self.embedding_dimension)
        chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        db = Chroma(client=chroma_client, embedding_function=embedding_fn)
        return db

    def load_conversation_history(self, session_id):
        results = self.db.get(where={"session_id": session_id})
        if results and results['documents']:
            return results['documents']
        else:
            return []

    def store_conversation(self, user_input, ai_response, session_id):
        self.db.add_texts(
            texts=[f"User: {user_input}\nAI: {ai_response}"],
            metadatas=[{"session_id": session_id}]
        )

    def delete_data(self, ids=None, where=None):
        if ids:
            self.db.delete(ids=ids)
        elif where:
            self.db.delete(where=where)
        else:
            print("请提供要删除的ids或者where条件")