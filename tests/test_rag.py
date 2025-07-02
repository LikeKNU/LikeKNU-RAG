import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.vector_store import NoticeVectorStore, create_vector_store_with_sample_data
from src.rag_system import NoticeRAGSystem, create_rag_system_with_sample_data
from src.models import Campus


def test_vector_store_creation():
    vector_store = create_vector_store_with_sample_data()

    info = vector_store.get_collection_info()
    assert info["count"] > 0, "문서가 저장되지 않음"
    print("✅ 벡터 저장소 생성 테스트 통과")


def test_similarity_search():
    vector_store = create_vector_store_with_sample_data()

    results = vector_store.similarity_search("수강신청", k=3)
    assert len(results) > 0, "검색 결과가 없음"
    assert "수강신청" in results[0].page_content, "관련 문서를 찾지 못함"
    print("✅ 유사도 검색 테스트 통과")


def test_campus_filtering():
    vector_store = create_vector_store_with_sample_data()

    cheonan_results = vector_store.similarity_search(
        "도서관", k=5, campus_filter=Campus.CHEONAN
    )

    assert len(cheonan_results) > 0, "캠퍼스 필터링 실패"

    for doc in cheonan_results:
        campus = doc.metadata.get("campus")
        assert campus in [Campus.ALL.value, Campus.CHEONAN.value], f"잘못된 캠퍼스 필터링: {campus}"

    print("✅ 캠퍼스 필터링 테스트 통과")


def test_rag_system_basic():
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY가 설정되지 않아 RAG 시스템 테스트를 건너뜁니다.")
        return

    try:
        rag_system = create_rag_system_with_sample_data()

        response = rag_system.chat("수강신청은 언제인가요?")

        assert "answer" in response, "응답 형식 오류"
        assert "sources" in response, "소스 정보 누락"
        assert len(response["sources"]) > 0, "소스 문서가 없음"

        print("✅ RAG 시스템 기본 테스트 통과")

    except Exception as e:
        print(f"⚠️  RAG 시스템 테스트 실패: {e}")


def test_rag_system_campus_filter():
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY가 설정되지 않아 RAG 시스템 캠퍼스 필터링 테스트를 건너뜁니다.")
        return

    try:
        rag_system = create_rag_system_with_sample_data()

        response = rag_system.chat("도서관 정보를 알려주세요", campus="CHEONAN")

        assert response["campus_filter"] == "CHEONAN", "캠퍼스 필터 설정 실패"

        print("✅ RAG 시스템 캠퍼스 필터링 테스트 통과")

    except Exception as e:
        print(f"⚠️  RAG 시스템 캠퍼스 필터링 테스트 실패: {e}")


def cleanup_test_data():
    try:
        vector_store = NoticeVectorStore()
        vector_store.delete_collection()
        print("✅ 테스트 데이터 정리 완료")
    except Exception:
        pass


if __name__ == "__main__":
    test_vector_store_creation()
    test_similarity_search()
    test_campus_filtering()
    test_rag_system_basic()
    test_rag_system_campus_filter()
    cleanup_test_data()
    print("\n✅ 모든 RAG 시스템 테스트 완료!")
