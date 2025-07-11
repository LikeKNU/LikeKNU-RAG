#!/usr/bin/env python3

import asyncio
import sys
import os
from datetime import datetime
from uuid import uuid4

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from src.messaging.message_broker import create_message_broker
from src.messaging.events import NoticeEvent, EventType
from src.data_sync.event_handlers import DataSyncManager
from src.vector_store import NoticeVectorStore
from src.models import Campus, NoticeCategory


async def test_messaging_system():
    print("🚀 메시징 시스템 테스트 시작")
    print("=" * 50)
    
    # 깨끗한 벡터 저장소로 시작
    vector_store = NoticeVectorStore()
    vector_store.delete_collection()
    vector_store = NoticeVectorStore()
    
    message_broker = create_message_broker()
    sync_manager = DataSyncManager(vector_store, message_broker)
    
    try:
        await sync_manager.start()
        
        # 초기 상태 확인
        initial_count = vector_store.get_collection_info()["count"]
        print(f"📊 초기 문서 수: {initial_count}")
        
        # 새 공지사항 생성 이벤트 테스트
        print("\n📝 새 공지사항 이벤트 발행...")
        
        new_notice = NoticeEvent(
            event_id=str(uuid4()),
            event_type=EventType.NOTICE_CREATED,
            timestamp=datetime.now(),
            source_service="data_collector",
            notice_id="test_notice_001",
            title="테스트 공지사항 - 메시징 시스템",
            content="""이것은 메시징 시스템을 통해 전달된 테스트 공지사항입니다.
            
주요 내용:
1. 메시징 시스템 연동 테스트
2. 실시간 데이터 동기화 확인
3. RAG 시스템 업데이트 검증

문의사항이 있으시면 시스템 관리자에게 연락해 주세요.
연락처: admin@kongju.ac.kr
담당부서: 전산관리과""",
            url="https://www.kongju.ac.kr/notice/test001",
            campus=Campus.CHEONAN,
            category=NoticeCategory.ACADEMIC,
            published_date=datetime.now(),
            author="시스템 관리자",
            department="전산관리과"
        )
        
        await message_broker.publish("university.notices", new_notice)
        
        # 잠시 대기 (비동기 처리 완료 대기)
        await asyncio.sleep(1)
        
        # 업데이트된 상태 확인
        updated_count = vector_store.get_collection_info()["count"]
        print(f"📊 업데이트 후 문서 수: {updated_count}")
        print(f"📈 추가된 문서 수: {updated_count - initial_count}")
        
        # 검색 테스트
        print("\n🔍 추가된 문서 검색 테스트...")
        search_results = vector_store.similarity_search("메시징 시스템", k=3)
        
        for i, doc in enumerate(search_results, 1):
            print(f"  {i}. {doc.metadata.get('title', 'N/A')}")
            print(f"     캠퍼스: {doc.metadata.get('campus', 'N/A')}")
            print(f"     카테고리: {doc.metadata.get('category', 'N/A')}")
        
        # 중복 공지사항 테스트
        print("\n📝 중복 공지사항 이벤트 발행...")
        
        duplicate_notice = NoticeEvent(
            event_id=str(uuid4()),
            event_type=EventType.NOTICE_CREATED,
            timestamp=datetime.now(),
            source_service="data_collector",
            notice_id="test_notice_001",  # 동일한 ID
            title="중복 테스트 공지사항",
            content="이것은 중복 테스트입니다.",
            url="https://www.kongju.ac.kr/notice/test001",
            campus=Campus.CHEONAN,
            category=NoticeCategory.ACADEMIC,
            published_date=datetime.now(),
            author="시스템 관리자",
            department="전산관리과"
        )
        
        await message_broker.publish("university.notices", duplicate_notice)
        await asyncio.sleep(1)
        
        # 중복 처리 후 상태 확인
        final_count = vector_store.get_collection_info()["count"]
        print(f"📊 중복 처리 후 문서 수: {final_count}")
        
        # 동기화 상태 확인
        sync_status = sync_manager.get_sync_status()
        print(f"\n📈 동기화 상태:")
        print(f"  - 실행 중: {sync_status['running']}")
        print(f"  - 벡터 저장소 문서 수: {sync_status['vector_store_count']}")
        print(f"  - 마지막 동기화: {sync_status['last_sync']}")
        
    finally:
        await sync_manager.stop()
    
    print("\n✅ 메시징 시스템 테스트 완료!")


if __name__ == "__main__":
    asyncio.run(test_messaging_system())
