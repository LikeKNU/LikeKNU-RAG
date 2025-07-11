from typing import List
from langchain.schema import Document

from ...domain.models import Campus


def filter_documents_by_campus(
        documents: List[Document],
        user_campus: Campus
) -> List[Document]:
    allowed_campuses = [Campus.ALL, user_campus]
    filtered_docs = []

    for doc in documents:
        doc_campus = Campus(doc.metadata["campus"])
        if doc_campus in allowed_campuses:
            filtered_docs.append(doc)

    return filtered_docs