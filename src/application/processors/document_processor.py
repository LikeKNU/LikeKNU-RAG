from typing import List
from langchain.schema import Document

from ...domain.models import NoticeDocument, Notice
from .text_splitter import NoticeTextSplitter


class DocumentProcessor:
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = NoticeTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def process_notice(self, notice: Notice) -> List[Document]:
        """Notice 객체를 Document 청크들로 변환합니다."""
        page_content = f"제목: {notice.title}\n\n{notice.content}"
        
        metadata = {
            "source": "notice",
            "title": notice.title,
            "notice_id": notice.id,
            "url": notice.url,
            "campus": notice.campus.value,
            "category": notice.category.value,
            "published_date": notice.published_date.isoformat(),
            "author": notice.author,
            "department": notice.department
        }
        
        document = Document(page_content=page_content, metadata=metadata)
        chunks = self.text_splitter.split_documents([document])
        
        # 모든 청크에 동일한 메타데이터 적용
        for chunk in chunks:
            chunk.metadata.update(metadata)
        
        return chunks


class NoticeDocumentLoader:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = NoticeTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_notices(self, notices: List[NoticeDocument]) -> List[Document]:
        documents = []
        for notice in notices:
            doc = notice.to_langchain_document()
            documents.append(doc)
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        return self.text_splitter.split_documents(documents)

    def load_and_split(self, notices: List[NoticeDocument]) -> List[Document]:
        documents = self.load_notices(notices)
        chunks = self.split_documents(documents)
        return chunks


def create_sample_langchain_documents() -> List[Document]:
    from ...domain.models import create_sample_notices
    notices = create_sample_notices()
    loader = NoticeDocumentLoader()
    return loader.load_and_split(notices)
