from typing import List
from langchain.schema import Document

from .models import (NoticeDocument, NoticeTextSplitter, create_sample_notices)


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
    notices = create_sample_notices()
    loader = NoticeDocumentLoader()
    return loader.load_and_split(notices)


if __name__ == "__main__":
    print("LangChain 기반 문서 로더 테스트")
    print("=" * 40)

    notices = create_sample_notices()
    print(f"📢 원본 공지사항 수: {len(notices)}")

    loader = NoticeDocumentLoader(chunk_size=300, chunk_overlap=50)
    chunks = loader.load_and_split(notices)
    print(f"📝 생성된 청크 수: {len(chunks)}")
    print()

    for i, chunk in enumerate(chunks[:3], 1):
        print(f"--- 청크 {i} ---")
        print(f"내용 길이: {len(chunk.page_content)}자")
        print(f"제목: {chunk.metadata['title']}")
        print(f"캠퍼스: {chunk.metadata['campus']}")
        print(f"미리보기: {chunk.page_content[:100]}...")
        print()

    print("✅ LangChain 기반 문서 처리 완료!")
