from typing import List, Optional, Dict, Any
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from ...infrastructure.vector_store.chroma_store import NoticeVectorStore
from ...domain.models import Campus


class NoticeRAGSystem:

    def __init__(self, vector_store: NoticeVectorStore, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """당신은 공주대학교 학생들을 위한 AI 어시스턴트입니다.
주어진 문서들을 바탕으로 학생들의 질문에 정확하고 친절하게 답변해주세요.

답변 가이드라인:
1. 주어진 문서 내용만을 근거로 답변하세요
2. 문서에 없는 내용은 "관련 정보를 찾을 수 없습니다"라고 말하세요
3. 가능한 구체적인 날짜, 장소, 연락처 등을 포함하여 답변하세요
4. 학생들이 이해하기 쉽게 친근한 톤으로 답변하세요
5. 추가 문의가 필요한 경우 관련 부서 연락처를 안내하세요

관련 문서들:
{context}"""),
            ("human", "{question}")
        ])

    def search_documents(
            self,
            query: str,
            k: int = 5,
            campus_filter: Optional[Campus] = None
    ) -> List[Document]:
        return self.vector_store.similarity_search(
            query, k=k, campus_filter=campus_filter
        )

    def generate_answer(
            self,
            query: str,
            campus_filter: Optional[Campus] = None,
            k: int = 5
    ) -> Dict[str, Any]:

        relevant_docs = self.search_documents(query, k=k, campus_filter=campus_filter)

        if not relevant_docs:
            return {
                "answer": "죄송합니다. 관련된 정보를 찾을 수 없습니다.",
                "sources": [],
                "campus_filter": campus_filter.value if campus_filter else "ALL"
            }

        context = "\n\n".join([
            f"문서 {i + 1}:\n제목: {doc.metadata.get('title', 'N/A')}\n내용: {doc.page_content}"
            for i, doc in enumerate(relevant_docs)
        ])

        chain = (
                {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
                | self.prompt_template
                | self.llm
                | StrOutputParser()
        )

        answer = chain.invoke({"context": context, "question": query})

        sources = [
            {
                "title": doc.metadata.get("title", "N/A"),
                "url": doc.metadata.get("url", "N/A"),
                "campus": doc.metadata.get("campus", "N/A"),
                "category": doc.metadata.get("category", "N/A"),
                "date": doc.metadata.get("date", "N/A")
            }
            for doc in relevant_docs
        ]

        return {
            "answer": answer,
            "sources": sources,
            "campus_filter": campus_filter.value if campus_filter else "ALL"
        }

    def chat(self, query: str, campus: Optional[str] = None) -> Dict[str, Any]:
        campus_filter = None
        if campus:
            try:
                campus_filter = Campus(campus.upper())
            except ValueError:
                pass

        return self.generate_answer(query, campus_filter=campus_filter)


def create_rag_system_with_sample_data() -> NoticeRAGSystem:
    from ...infrastructure.vector_store.chroma_store import create_vector_store_with_sample_data

    vector_store = create_vector_store_with_sample_data()
    return NoticeRAGSystem(vector_store)
