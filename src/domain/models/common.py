from enum import Enum


class NoticeCategory(Enum):
    ACADEMIC = "ACADEMIC"
    STUDENT_NEWS = "STUDENT_NEWS"
    LIBRARY = "LIBRARY"
    SCHOLARSHIP = "SCHOLARSHIP"
    RECRUITMENT = "RECRUITMENT"
    GENERAL = "GENERAL"


# Alias for backwards compatibility
Category = NoticeCategory