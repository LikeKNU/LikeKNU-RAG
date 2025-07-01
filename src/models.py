"""
데이터 모델 정의
"""
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class Campus(Enum):
    """캠퍼스 구분"""
    ALL = "ALL"
    SINGWAN = "SINGWAN"
    CHEONAN = "CHEONAN"
    YESAN = "YESAN"


class Category(Enum):
    """공지사항 카테고리"""
    ACADEMIC = "ACADEMIC"  # 학사
    STUDENT_NEWS = "STUDENT_NEWS"  # 학생소식
    LIBRARY = "LIBRARY"  # 도서관
    SCHOLARSHIP = "SCHOLARSHIP"  # 장학금
    RECRUITMENT = "RECRUITMENT"  # 채용정보
    GENERAL = "GENERAL"  # 일반공지


@dataclass
class NoticeDocument:
    """공지사항 문서 구조"""
    title: str
    content: str
    date: datetime
    campus: Campus
    url: str
    category: Category
    notice_id: Optional[str] = None

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "title": self.title,
            "content": self.content,
            "date": self.date.isoformat(),
            "campus": self.campus.value,
            "url": self.url,
            "category": self.category.value,
            "notice_id": self.notice_id
        }


@dataclass
class DocumentChunk:
    """임베딩을 위한 문서 청크"""
    text: str
    chunk_type: str  # "title_summary" or "full_content"
    metadata: dict

    def __post_init__(self):
        """청크 생성 후 메타데이터 검증"""
        required_fields = ["source", "title", "campus", "category"]
        for field in required_fields:
            if field not in self.metadata:
                raise ValueError(f"Missing required metadata field: {field}")


def get_allowed_campuses(user_campus: Campus) -> list[Campus]:
    """
    사용자가 볼 수 있는 캠퍼스 목록 반환
    
    Args:
        user_campus: 사용자 캠퍼스
        
    Returns:
        허용된 캠퍼스 리스트 [ALL, 사용자캠퍼스]
    """
    return [Campus.ALL, user_campus]


def is_campus_allowed(user_campus: Campus, notice_campus: Campus) -> bool:
    """
    해당 공지사항이 사용자에게 표시되어야 하는지 확인
    
    Args:
        user_campus: 사용자 캠퍼스
        notice_campus: 공지사항 캠퍼스
        
    Returns:
        True if 표시 가능, False if 필터링 대상
    """
    allowed_campuses = get_allowed_campuses(user_campus)
    return notice_campus in allowed_campuses
