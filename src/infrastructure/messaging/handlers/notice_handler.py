import logging
from datetime import datetime
from typing import Dict, Any

from ....application.processors.document_processor import DocumentProcessor
from ..events import BaseEvent, NoticeEvent, EventType
from ....domain.models import Notice
from ...vector_store.chroma_store import NoticeVectorStore

logger = logging.getLogger(__name__)


class RAGEventHandler:

    def __init__(self, vector_store: NoticeVectorStore):
        self.vector_store = vector_store
        self.document_processor = DocumentProcessor()

    async def handle_notice_event(self, event: NoticeEvent):
        logger.info(f"공지사항 이벤트 처리 시작: {event.event_type} - {event.title}")
        print(f"🔄 이벤트 핸들러에서 처리 중: {event.event_type} - {event.title}")

        try:
            if event.event_type == EventType.NOTICE_CREATED:
                await self._create_notice(event)

            print(f"✅ 이벤트 처리 완료: {event.event_type}")

        except Exception as e:
            logger.error(f"공지사항 이벤트 처리 실패: {e}")
            print(f"❌ 이벤트 처리 실패: {e}")
            raise

    async def _create_notice(self, event: NoticeEvent):
        print(f"📝 새 공지사항 생성 처리: {event.title}")

        notice = Notice(
            id=event.notice_id,
            title=event.title,
            content=event.content,
            url=event.url,
            campus=event.campus,
            category=event.category,
            published_date=event.published_date,
            author=event.author,
            department=event.department,
            attachments=event.attachments
        )

        documents = self.document_processor.process_notice(notice)
        print(f"📄 생성된 문서 청크 수: {len(documents)}")

        existing_docs = self.vector_store.get_documents_by_id(event.notice_id)
        if existing_docs:
            logger.warning(f"이미 존재하는 공지사항: {event.notice_id}, 건너뜀")
            print(f"⚠️ 이미 존재하는 공지사항, 건너뜀")
            return

        self.vector_store.add_documents(documents)
        print(f"✅ 새 공지사항 추가 완료: {event.title} ({len(documents)}개 문서)")
        logger.info(f"새 공지사항 추가 완료: {event.title} ({len(documents)}개 문서)")


class DataSyncManager:

    def __init__(self, vector_store: NoticeVectorStore, message_broker):
        self.vector_store = vector_store
        self.message_broker = message_broker
        self.event_handler = RAGEventHandler(vector_store)
        self.running = False

    async def start(self):
        await self.message_broker.start()

        await self.message_broker.subscribe("university.notices", self._handle_notice_events)

        self.running = True
        logger.info("데이터 동기화 관리자 시작")

    async def stop(self):
        self.running = False
        await self.message_broker.stop()
        logger.info("데이터 동기화 관리자 종료")

    async def _handle_notice_events(self, event: BaseEvent):
        if isinstance(event, NoticeEvent):
            await self.event_handler.handle_notice_event(event)

    def get_sync_status(self) -> Dict[str, Any]:
        return {
            "running": self.running,
            "vector_store_count": self.vector_store.get_collection_info()["count"],
            "last_sync": datetime.now().isoformat()
        }
