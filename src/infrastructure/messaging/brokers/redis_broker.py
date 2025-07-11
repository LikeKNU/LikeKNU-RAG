import asyncio
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Dict

from .events import BaseEvent, EventType

logger = logging.getLogger(__name__)


class MessageBroker(ABC):

    @abstractmethod
    async def publish(self, topic: str, event: BaseEvent) -> None:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, handler: Callable[[BaseEvent], None]) -> None:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass


def _create_event_from_data(event_type: EventType, data: dict) -> BaseEvent:
    from .events import NoticeEvent

    event_classes = {
        EventType.NOTICE_CREATED: NoticeEvent,
    }

    event_class = event_classes.get(event_type, BaseEvent)
    return event_class(**data)


class RedisMessageBroker(MessageBroker):

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.subscribers: Dict[str, Callable] = {}
        self.publisher_client = None
        self.subscriber_client = None
        self.pubsub = None
        self.running = False
        self.listener_task = None

    async def start(self):
        try:
            import redis.asyncio as redis
            self.publisher_client = redis.from_url(self.redis_url)
            self.subscriber_client = redis.from_url(self.redis_url)
            self.pubsub = self.subscriber_client.pubsub()
            self.running = True
            logger.info(f"Redis 메시지 브로커 시작: {self.redis_url}")
        except ImportError:
            logger.error("redis 패키지가 설치되지 않았습니다: pip install redis")
            raise

    async def stop(self):
        self.running = False
        if self.listener_task:
            self.listener_task.cancel()
        if self.pubsub:
            await self.pubsub.close()
        if self.subscriber_client:
            await self.subscriber_client.close()
        if self.publisher_client:
            await self.publisher_client.close()
        logger.info("Redis 메시지 브로커 종료")

    async def publish(self, topic: str, event: BaseEvent):
        if not self.publisher_client:
            raise RuntimeError("Redis 발행 클라이언트가 초기화되지 않았습니다")

        message = {
            "event_data": event.model_dump(mode='json'),
            "published_at": datetime.now().isoformat()
        }

        await self.publisher_client.publish(topic, json.dumps(message))
        logger.info(f"메시지 발행: {topic} - {event.event_type}")

    async def subscribe(self, topic: str, handler: Callable[[BaseEvent], None]):
        if not self.pubsub:
            raise RuntimeError("PubSub이 초기화되지 않았습니다")

        await self.pubsub.subscribe(topic)
        self.subscribers[topic] = handler
        logger.info(f"토픽 구독: {topic}")

        if not self.listener_task:
            self.listener_task = asyncio.create_task(self._listen_messages())

    async def _listen_messages(self):
        if not self.pubsub:
            return

        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        topic = message["channel"].decode()
                        data = json.loads(message["data"].decode())

                        if topic in self.subscribers:
                            event_data = data["event_data"]
                            event_type = EventType(event_data["event_type"])

                            event = _create_event_from_data(event_type, event_data)

                            handler = self.subscribers[topic]
                            if asyncio.iscoroutinefunction(handler):
                                await handler(event)
                            else:
                                handler(event)

                    except Exception as e:
                        logger.error(f"메시지 처리 중 오류: {e}")
        except asyncio.CancelledError:
            logger.info("메시지 리스닝 태스크 취소됨")
        except Exception as e:
            logger.error(f"메시지 리스닝 중 오류: {e}")


def create_message_broker(redis_url: str = "redis://localhost:6379") -> MessageBroker:
    return RedisMessageBroker(redis_url)
