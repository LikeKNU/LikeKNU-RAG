"""
문서 처리 및 청킹 로직 (수정된 버전)
"""
from datetime import datetime
from typing import List

from .models import NoticeDocument, DocumentChunk, Campus, Category


class NoticeDocumentProcessor:
    """공지사항 문서 처리기"""

    def create_chunks(self, notice: NoticeDocument) -> List[DocumentChunk]:
        """
        공지사항을 검색 가능한 청크로 변환
        
        Args:
            notice: 공지사항 문서
            
        Returns:
            문서 청크 리스트 (항상 1개)
        """
        # 메타데이터 생성 (사용자 무관)
        metadata = {
            "source": "notice",
            "title": notice.title,
            "date": notice.date.isoformat(),
            "campus": notice.campus.value,
            "category": notice.category.value,
            "url": notice.url,
            "notice_id": notice.notice_id,
        }

        # 제목과 내용을 하나의 텍스트로 결합
        full_text = f"제목: {notice.title}\n\n{notice.content}"

        chunk = DocumentChunk(
            text=full_text,
            chunk_type="full_document",
            metadata=metadata
        )

        return [chunk]


def create_sample_notice() -> NoticeDocument:
    """테스트용 샘플 공지사항 생성"""
    return NoticeDocument(
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
    )


def create_sample_notices() -> List[NoticeDocument]:
    """테스트용 여러 캠퍼스 공지사항 생성"""
    return [
        # 전체 공지
        NoticeDocument(
            title="2024년 1학기 수강신청 안내",
            content="2024년 1학기 수강신청 일정을 안내드립니다...",
            date=datetime(2024, 2, 10, 9, 0, 0),
            campus=Campus.ALL,
            url="https://www.kongju.ac.kr/notice/12345",
            category=Category.ACADEMIC,
            notice_id="12345"
        ),
        # 천안 캠퍼스 공지
        NoticeDocument(
            title="천안캠퍼스 도서관 휴관 안내",
            content="천안캠퍼스 도서관이 시설 점검으로 임시 휴관합니다...",
            date=datetime(2024, 2, 12, 14, 0, 0),
            campus=Campus.CHEONAN,
            url="https://www.kongju.ac.kr/notice/12346",
            category=Category.LIBRARY,
            notice_id="12346"
        ),
        # 신관 캠퍼스 공지
        NoticeDocument(
            title="신관캠퍼스 전용 공지사항",
            content="신관캠퍼스 학생들을 위한 전용 공지사항입니다...",
            date=datetime(2024, 2, 11, 10, 0, 0),
            campus=Campus.SINGWAN,
            url="https://www.kongju.ac.kr/notice/12347",
            category=Category.GENERAL,
            notice_id="12347"
        )
    ]
