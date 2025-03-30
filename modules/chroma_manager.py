import os
import chromadb
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from enum import Enum
import numpy as np

class EmbeddingModelType(Enum):
    MINILM = "all-MiniLM-L6-v2"
    # 可以在这里添加更多 Embedding 模型

class ChromaManager:
    def __init__(self, api_key=None, embedding_model_type=EmbeddingModelType.MINILM, embedding_dimension=384, persist_directory="db"):
        self.api_key = api_key
        self.embedding_model_type = embedding_model_type
        self.embedding_dimension = embedding_dimension
        self.persist_directory = persist_directory
        self.db = self._initialize_chroma()

    def _initialize_chroma(self):
        class EmbeddingFunction:
            def __init__(self, embedding_model_type, embedding_dimension):
                self.embedding_model_type = embedding_model_type
                self.embedding_dimension = embedding_dimension
                self.model = SentenceTransformer(self.embedding_model_type.value)

            def embed_documents(self, texts):
                embeddings = self.model.encode(texts).tolist()
                return embeddings

            def embed_query(self, query):  # 添加 embed_query 方法
                embedding = self.model.encode(query).tolist()
                return embedding

        embedding_fn = EmbeddingFunction(self.embedding_model_type, self.embedding_dimension)
        chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        db = Chroma(client=chroma_client, embedding_function=embedding_fn)
        return db

    def load_conversation_history(self, session_id):
        results = self.db.get(where={"session_id": session_id})
        if results and results['documents']:
            return results['documents']
        else:
            return []

    def store_conversation(self, user_input, ai_response, session_id, metadata=None):
        if metadata is None:
           metadata = {"session_id": session_id}
        else:
           metadata["session_id"] = session_id
        self.db.add_texts(
            texts=[f"User: {user_input}\nAI: {ai_response}"],
            metadatas=[metadata] #应用新的metadata
        )

    def search(self, query, n_results=5, where=None):
        """根据查询返回结果"""
        results = self.db.similarity_search(query, k=n_results, filter=where)
        return results

    def delete_data(self, ids=None, where=None):
        if ids:
            self.db.delete(ids=ids)
        elif where:
            self.db.delete(where=where)
        else:
            print("请提供要删除的ids或者where条件")