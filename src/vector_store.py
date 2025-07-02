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
    
    def add_documents_with_dedup(self, documents: List[Document]) -> List[str]:
        """notice_id 기반으로 중복을 방지하며 문서를 추가합니다."""
        # 기존 notice_id 목록 가져오기
        existing_notice_ids = self.get_existing_notice_ids()
        
        # 중복되지 않은 문서만 필터링
        new_documents = []
        for doc in documents:
            notice_id = doc.metadata.get('notice_id')
            if notice_id and notice_id not in existing_notice_ids:
                new_documents.append(doc)
                print(f"📄 새 문서 추가: {doc.metadata.get('title', 'Unknown')} (ID: {notice_id})")
            elif notice_id:
                print(f"⚠️  중복 건너뜀: {doc.metadata.get('title', 'Unknown')} (ID: {notice_id})")
        
        if new_documents:
            print(f"✅ {len(new_documents)}개 새 문서를 벡터 저장소에 추가")
            return self.vectorstore.add_documents(new_documents)
        else:
            print("📚 추가할 새 문서가 없습니다")
            return []
    
    def get_existing_notice_ids(self) -> set:
        """기존에 저장된 notice_id 목록을 가져옵니다."""
        try:
            client = chromadb.PersistentClient(path=self.persist_directory)
            collection = client.get_collection(name=self.collection_name)
            results = collection.get(include=['metadatas'])
            
            notice_ids = set()
            for metadata in results['metadatas']:
                if metadata and 'notice_id' in metadata:
                    notice_ids.add(metadata['notice_id'])
            
            return notice_ids
        except Exception:
            # 컬렉션이 없거나 오류 시 빈 세트 반환
            return set()

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
    
    # notice_id 기반 중복 방지로 샘플 데이터 추가
    print("📝 샘플 데이터를 중복 검사하며 추가 중...")
    documents = create_sample_langchain_documents()
    vector_store.add_documents_with_dedup(documents)
    
    # 최종 상태 확인
    final_info = vector_store.get_collection_info()
    print(f"📊 현재 총 문서 수: {final_info['count']}개")

    return vector_store
