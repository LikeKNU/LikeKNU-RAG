from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from ...domain.models import Campus, NoticeCategory


class EventType(Enum):
    NOTICE_CREATED = "notice_created"


class BaseEvent(BaseModel):
    event_id: str
    event_type: EventType
    timestamp: datetime
    source_service: str
    
    class Config:
        use_enum_values = True


class NoticeEvent(BaseEvent):
    notice_id: str
    title: str
    content: str
    url: str
    campus: Campus
    category: NoticeCategory
    published_date: datetime
    author: Optional[str] = None
    department: Optional[str] = None
    attachments: List[str] = []
    
    class Config:
        use_enum_values = True
