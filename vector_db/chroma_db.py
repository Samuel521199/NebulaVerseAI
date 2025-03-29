import os
import chromadb
from langchain_chroma import Chroma
import google.generativeai as genai

class ChromaManager:
    def __init__(self, api_key, embedding_model="embedding-001", embedding_dimension=1536, persist_directory="db"): # 1536是embedding向量的维度,要替换为你使用的模型对应的维度
        self.api_key = api_key
        self.embedding_model = embedding_model
        self.embedding_dimension = embedding_dimension
        self.persist_directory = persist_directory
        self.db = self._initialize_chroma()

    def _initialize_chroma(self):
        class EmbeddingFunction:
            def __init__(self, api_key, embedding_model, embedding_dimension):
                self.api_key = api_key
                self.embedding_model = embedding_model
                self.embedding_dimension = embedding_dimension

            def embed_documents(self, texts):
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(self.embedding_model)  # 使用api_key配置
                embeddings = []
                for text in texts:
                    try:
                        response = model.embed_content(content={"text": text}, task_type="RETRIEVAL_QUERY")
                        if response and response.embedding and response.embedding.value:
                             embeddings.append(response.embedding.value)
                        else:
                            print(f"Embedding 失败 for text: {text}")
                            embeddings.append([0.0] * self.embedding_dimension)

                    except Exception as e:
                        print(f"Embedding 错误 for text: {text}: {e}")
                        embeddings.append([0.0] * self.embedding_dimension)

                return embeddings

        embedding_fn = EmbeddingFunction(self.api_key, self.embedding_model, self.embedding_dimension)
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