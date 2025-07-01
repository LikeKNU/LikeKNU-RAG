import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import Campus, filter_documents_by_campus
from src.document_loader import NoticeDocumentLoader, create_sample_notices


def test_langchain_filtering():
    print("=" * 40)
    print("LangChain 기반 캠퍼스 필터링 테스트")
    print("=" * 40)

    notices = create_sample_notices()
    loader = NoticeDocumentLoader()
    all_chunks = loader.load_and_split(notices)

    print(f"📢 전체 청크 수: {len(all_chunks)}")

    test_users = [
        (Campus.CHEONAN, "천안 캠퍼스 사용자"),
        (Campus.SINGWAN, "신관 캠퍼스 사용자")
    ]

    for user_campus, user_desc in test_users:
        print(f"\n👤 {user_desc} ({user_campus.value})")

        filtered_chunks = filter_documents_by_campus(all_chunks, user_campus)

        print(f"🔍 필터링 후: {len(filtered_chunks)}개")
        print("표시되는 공지사항:")
        for chunk in filtered_chunks:
            print(f"  - {chunk.metadata['title']} ({chunk.metadata['campus']})")


def test_langchain_structure():
    print("\n" + "=" * 40)
    print("LangChain Document 구조 테스트")
    print("=" * 40)

    notices = create_sample_notices()
    loader = NoticeDocumentLoader()
    chunks = loader.load_and_split(notices)

    sample_chunk = chunks[0]
    print(f"📝 Document 타입: {type(sample_chunk)}")
    print(f"📄 page_content 길이: {len(sample_chunk.page_content)}자")
    print(f"🏷️ metadata 키: {list(sample_chunk.metadata.keys())}")
    print(f"📋 내용 미리보기:")
    print(f"   {sample_chunk.page_content[:100]}...")


if __name__ == "__main__":
    test_langchain_structure()
    test_langchain_filtering()

    print("\n✅ LangChain 리팩토링 테스트 완료!")
    print("다음 단계: 임베딩 및 벡터 저장소 구현")
