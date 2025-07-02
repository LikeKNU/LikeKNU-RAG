import os
import chromadb
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma

from .embeddings import KoreanEmbeddings
from .models import Campus, filter_documents_by_campus


class NoticeVectorStore:

    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = KoreanEmbeddings()
        self.collection_name = "notice_collection"

        os.makedirs(persist_directory, exist_ok=True)

        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

    def add_documents(self, documents: List[Document]) -> List[str]:
        return self.vectorstore.add_documents(documents)

    def similarity_search(
            self,
            query: str,
            k: int = 5,
            campus_filter: Optional[Campus] = None
    ) -> List[Document]:

        if campus_filter:
            filter_dict = {
                "$or": [
                    {"campus": Campus.ALL.value},
                    {"campus": campus_filter.value}
                ]
            }
            results = self.vectorstore.similarity_search(
                query, k=k, filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search(query, k=k)

        return results

    def similarity_search_with_score(
            self,
            query: str,
            k: int = 5,
            campus_filter: Optional[Campus] = None
    ) -> List[tuple[Document, float]]:

        if campus_filter:
            filter_dict = {
                "$or": [
                    {"campus": Campus.ALL.value},
                    {"campus": campus_filter.value}
                ]
            }
            results = self.vectorstore.similarity_search_with_score(
                query, k=k, filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search_with_score(query, k=k)

        return results

    def delete_collection(self):
        try:
            client = chromadb.PersistentClient(path=self.persist_directory)
            client.delete_collection(name=self.collection_name)
        except Exception:
            pass

    def get_collection_info(self) -> Dict[str, Any]:
        try:
            client = chromadb.PersistentClient(path=self.persist_directory)
            collection = client.get_collection(name=self.collection_name)
            return {
                "name": collection.name,
                "count": collection.count(),
                "metadata": collection.metadata
            }
        except Exception:
            return {"name": self.collection_name, "count": 0, "metadata": {}}

    def update_documents(self, documents: List[Document]) -> List[str]:
        self.delete_collection()

        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        return self.add_documents(documents)


def create_vector_store_with_sample_data() -> NoticeVectorStore:
    from .document_loader import create_sample_langchain_documents

    vector_store = NoticeVectorStore()
    documents = create_sample_langchain_documents()
    vector_store.add_documents(documents)

    return vector_store
