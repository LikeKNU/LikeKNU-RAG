from typing import List
from langchain.schema import Document

from .models import NoticeDocument, NoticeTextSplitter


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
    from .models import create_sample_notices
    notices = create_sample_notices()
    loader = NoticeDocumentLoader()
    return loader.load_and_split(notices)
