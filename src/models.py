from datetime import datetime
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class Campus(Enum):
    ALL = "ALL"
    SINGWAN = "SINGWAN"
    CHEONAN = "CHEONAN"
    YESAN = "YESAN"


class Category(Enum):
    ACADEMIC = "ACADEMIC"
    STUDENT_NEWS = "STUDENT_NEWS"
    LIBRARY = "LIBRARY"
    SCHOLARSHIP = "SCHOLARSHIP"
    RECRUITMENT = "RECRUITMENT"
    GENERAL = "GENERAL"


@dataclass
class NoticeDocument:
    title: str
    content: str
    date: datetime
    campus: Campus
    url: str
    category: Category
    notice_id: Optional[str] = None

    def to_langchain_document(self) -> Document:
        page_content = f"제목: {self.title}\n\n{self.content}"

        metadata = {
            "source": "notice",
            "title": self.title,
            "date": self.date.isoformat(),
            "campus": self.campus.value,
            "category": self.category.value,
            "url": self.url,
            "notice_id": self.notice_id,
        }

        return Document(
            page_content=page_content,
            metadata=metadata
        )


class NoticeTextSplitter(RecursiveCharacterTextSplitter):
    def __init__(
            self,
            chunk_size: int = 500,
            chunk_overlap: int = 50,
            **kwargs
    ):
        separators = ["\n\n", "\n", ".", "?", "!", " ", ""]

        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            **kwargs
        )


def get_allowed_campuses(user_campus: Campus) -> List[Campus]:
    return [Campus.ALL, user_campus]


def is_campus_allowed(user_campus: Campus, notice_campus: Campus) -> bool:
    allowed_campuses = get_allowed_campuses(user_campus)
    return notice_campus in allowed_campuses


def filter_documents_by_campus(
        documents: List[Document],
        user_campus: Campus
) -> List[Document]:
    filtered_docs = []

    for doc in documents:
        doc_campus = Campus(doc.metadata["campus"])
        if is_campus_allowed(user_campus, doc_campus):
            filtered_docs.append(doc)

    return filtered_docs


def create_sample_notices() -> List[NoticeDocument]:
    return [
        NoticeDocument(
            title="2024년 1학기 수강신청 안내",
            content="""2024년 1학기 수강신청 일정을 안내드립니다.

신청 기간: 2024년 2월 15일(목) 09:00 ~ 2월 17일(토) 18:00
신청 방법: 학사정보시스템 접속 후 수강신청 메뉴 이용

주의사항:
1. 수강신청 시간을 반드시 확인하시기 바랍니다.
2. 선수과목을 이수하지 않은 경우 수강신청이 제한될 수 있습니다.
3. 수강정원 초과 시 추첨을 통해 수강자를 선정합니다.

문의처: 학사지원과 (041-850-8114)""",
            date=datetime(2024, 2, 10, 9, 0, 0),
            campus=Campus.ALL,
            url="https://www.kongju.ac.kr/notice/12345",
            category=Category.ACADEMIC,
            notice_id="12345"
        ),
        NoticeDocument(
            title="천안캠퍼스 도서관 휴관 안내",
            content="""천안캠퍼스 중앙도서관 시설 점검으로 인한 임시 휴관을 안내드립니다.

휴관 기간: 2024년 2월 20일(화) ~ 2월 22일(목)
휴관 사유: 공조시설 점검 및 서가 정리

이용 안내:
- 휴관 기간 중 도서 반납은 반납함을 이용해주세요
- 신관캠퍼스 도서관은 정상 운영됩니다
- 전자자료는 24시간 이용 가능합니다

문의처: 천안캠퍼스 도서관 (041-850-8888)""",
            date=datetime(2024, 2, 12, 14, 0, 0),
            campus=Campus.CHEONAN,
            url="https://www.kongju.ac.kr/notice/12346",
            category=Category.LIBRARY,
            notice_id="12346"
        ),
        NoticeDocument(
            title="신관캠퍼스 주차장 공사 안내",
            content="""신관캠퍼스 제2주차장 확장 공사 안내입니다.

공사 기간: 2024년 3월 1일 ~ 3월 31일
공사 구간: 제2주차장 동편 구역

주차 안내:
- 공사 기간 중 제1주차장 이용 부탁드립니다
- 임시주차장도 운영 예정입니다
- 대중교통 이용을 권장합니다

문의처: 신관캠퍼스 시설관리과 (041-850-9999)""",
            date=datetime(2024, 2, 11, 10, 0, 0),
            campus=Campus.SINGWAN,
            url="https://www.kongju.ac.kr/notice/12347",
            category=Category.GENERAL,
            notice_id="12347"
        )
    ]
