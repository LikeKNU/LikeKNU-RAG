import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models import Campus, filter_documents_by_campus, create_sample_notices
from src.document_loader import NoticeDocumentLoader
from src.embeddings import KoreanEmbeddings


def test_document_processing():
    notices = create_sample_notices()
    loader = NoticeDocumentLoader()
    all_chunks = loader.load_and_split(notices)

    assert len(all_chunks) > 0, "문서 청크 생성 실패"
    assert all_chunks[0].metadata['title'], "메타데이터 누락"
    print("✅ 문서 처리 테스트 통과")


def test_campus_filtering():
    notices = create_sample_notices()
    loader = NoticeDocumentLoader()
    all_chunks = loader.load_and_split(notices)

    filtered_chunks = filter_documents_by_campus(all_chunks, Campus.CHEONAN)

    assert len(filtered_chunks) > 0, "필터링된 문서가 없음"
    print("✅ 캠퍼스 필터링 테스트 통과")


def test_embeddings():
    embeddings_model = KoreanEmbeddings()

    texts = ["테스트 문서입니다.", "임베딩이 잘 작동하는지 확인합니다."]
    embeddings = embeddings_model.embed_documents(texts)

    assert len(embeddings) == 2, "임베딩 개수 불일치"
    assert len(embeddings[0]) > 0, "임베딩 벡터 생성 실패"
    print("✅ 임베딩 테스트 통과")


if __name__ == "__main__":
    test_document_processing()
    test_campus_filtering()
    test_embeddings()
    print("\n✅ 모든 기본 테스트 통과!")
