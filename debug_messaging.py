#!/usr/bin/env python3

import asyncio
import sys
import os
from datetime import datetime
from uuid import uuid4

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from src.messaging.events import NoticeEvent, EventType
from src.data_sync.event_handlers import RAGEventHandler
from src.vector_store import NoticeVectorStore
from src.models import Campus, NoticeCategory


async def debug_event_handler():
    print("🐛 이벤트 핸들러 디버깅 시작")
    print("=" * 50)
    
    # 깨끗한 벡터 저장소로 시작
    vector_store = NoticeVectorStore()
    vector_store.delete_collection()
    vector_store = NoticeVectorStore()
    
    print(f"📊 초기 문서 수: {vector_store.get_collection_info()['count']}")
    
    # 이벤트 핸들러 직접 테스트
    event_handler = RAGEventHandler(vector_store)
    
    # 테스트 이벤트 생성
    test_event = NoticeEvent(
        event_id=str(uuid4()),
        event_type=EventType.NOTICE_CREATED,
        timestamp=datetime.now(),
        source_service="debug_test",
        notice_id="debug_notice_001",
        title="디버그 테스트 공지사항",
        content="이것은 디버그 테스트용 공지사항입니다. 메시징 시스템이 제대로 작동하는지 확인합니다.",
        url="https://test.com/debug001",
        campus=Campus.CHEONAN,
        category=NoticeCategory.ACADEMIC,
        published_date=datetime.now(),
        author="디버그 테스터",
        department="개발팀"
    )
    
    print(f"\n📝 이벤트 직접 처리 테스트...")
    await event_handler.handle_notice_event(test_event)
    
    print(f"📊 처리 후 문서 수: {vector_store.get_collection_info()['count']}")
    
    # 검색 테스트
    search_results = vector_store.similarity_search("디버그", k=5)
    print(f"🔍 검색 결과 수: {len(search_results)}")
    
    for i, doc in enumerate(search_results, 1):
        print(f"  {i}. {doc.metadata.get('title', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(debug_event_handler())
