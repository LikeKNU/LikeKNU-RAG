"""
수정된 프로토타입 테스트
청킹과 필터링을 분리한 구조 테스트
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import Campus, Category, is_campus_allowed, get_allowed_campuses
from src.document_processor import NoticeDocumentProcessor, create_sample_notice, create_sample_notices


def test_chunking_all_notices():
    """모든 공지사항 청킹 테스트 (사용자 무관)"""
    print("=" * 50)
    print("전체 공지사항 청킹 테스트")
    print("=" * 50)

    processor = NoticeDocumentProcessor()
    notices = create_sample_notices()
    
    print(f"📢 총 공지사항 수: {len(notices)}")
    print()
    
    all_chunks = []
    for i, notice in enumerate(notices, 1):
        chunks = processor.create_chunks(notice)  # user_campus 제거!
        all_chunks.extend(chunks)
        
        print(f"--- 공지사항 {i} ---")
        print(f"제목: {notice.title}")
        print(f"캠퍼스: {notice.campus.value}")
        print(f"생성된 청크 수: {len(chunks)}")
        print()
    
    print(f"📝 전체 청크 수: {len(all_chunks)}")
    print("✅ 모든 공지사항이 정상적으로 청킹됨!")
    print()
    
    return all_chunks


def test_search_filtering():
    """검색 시 필터링 테스트 (사용자별)"""
    print("=" * 50)
    print("검색 필터링 테스트")
    print("=" * 50)
    
    # 모든 청크 생성 (실제로는 벡터DB에 저장됨)
    processor = NoticeDocumentProcessor()
    notices = create_sample_notices()
    all_chunks = []
    
    for notice in notices:
        chunks = processor.create_chunks(notice)
        all_chunks.extend(chunks)
    
    # 사용자별 필터링 시뮬레이션
    test_users = [
        (Campus.CHEONAN, "천안 캠퍼스 사용자"),
        (Campus.SINGWAN, "신관 캠퍼스 사용자")
    ]
    
    for user_campus, user_desc in test_users:
        print(f"👤 {user_desc} ({user_campus.value})")
        print(f"허용된 캠퍼스: {[c.value for c in get_allowed_campuses(user_campus)]}")
        
        # 필터링된 결과
        filtered_chunks = []
        for chunk in all_chunks:
            chunk_campus = Campus(chunk.metadata["campus"])
            if is_campus_allowed(user_campus, chunk_campus):
                filtered_chunks.append(chunk)
        
        print(f"📝 전체 청크: {len(all_chunks)}개")
        print(f"🔍 필터링 후: {len(filtered_chunks)}개")
        
        print("표시되는 공지사항:")
        for chunk in filtered_chunks:
            print(f"  - {chunk.metadata['title']} ({chunk.metadata['campus']})")
        print()


def test_campus_filtering():
    """캠퍼스 필터링 로직 테스트"""
    print("=" * 30)
    print("캠퍼스 필터링 테스트")
    print("=" * 30)
    
    user_campus = Campus.CHEONAN
    
    print(f"사용자 캠퍼스: {user_campus.value}")
    print(f"허용된 캠퍼스: {[c.value for c in get_allowed_campuses(user_campus)]}")
    print()
    
    test_cases = [
        (Campus.ALL, "전체 공지"),
        (Campus.CHEONAN, "천안 캠퍼스"),
        (Campus.SINGWAN, "신관 캠퍼스"),
        (Campus.YESAN, "예산 캠퍼스")
    ]
    
    for campus, description in test_cases:
        allowed = is_campus_allowed(user_campus, campus)
        status = "✅ 허용" if allowed else "❌ 필터링"
        print(f"{description:10} ({campus.value:8}): {status}")
    print()


if __name__ == "__main__":
    # 캠퍼스 필터링 로직 테스트
    test_campus_filtering()
    
    # 전체 공지사항 청킹 테스트
    all_chunks = test_chunking_all_notices()
    
    # 사용자별 검색 필터링 테스트
    test_search_filtering()
    
    print("✅ 수정된 프로토타입 테스트 완료!")
    print("📋 청킹: 사용자 무관하게 모든 문서 처리")
    print("🔍 필터링: 검색 시에만 사용자별 적용")
    print("다음 단계: 임베딩 및 벡터 저장소 구현")
