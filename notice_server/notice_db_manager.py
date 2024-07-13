from datetime import datetime
from enum import Enum, auto

import mongoengine
from mongoengine import DoesNotExist

from models.notice import Notice

from config import Config

class NoticeUpdateType(Enum):
    CREATED = auto()
    REFETCHED = auto()
    MODIFIED = auto()

class NoticeDBManager:
    def __init__(self, config: Config) -> None:
        self._config = config
        mongoengine.connect(
            db=self._config.DB_NAME,
            host=self._config.DB_HOST,
            port=self._config.DB_PORT
            )
    
    def get_notice_by_id(self, notice_id: str, default=None) -> Notice:
        try:
            return Notice.objects.get(notice_id=notice_id)
        except DoesNotExist as e:
            return default
    
    def update_notice_from_doc(self, new_notice: Notice) -> NoticeUpdateType:
        old_notice = self.get_notice_by_id(new_notice.notice_id)

        # Notice exists with exact details
        if old_notice and old_notice == new_notice:
            old_notice.last_fetched_date = new_notice.last_fetched_date
            old_notice.save()
            new_notice.reload()
            return NoticeUpdateType.REFETCHED

        # Notice modified
        elif old_notice:
            new_notice.first_fetched_date = old_notice.first_fetched_date
            new_notice.save()
            return NoticeUpdateType.MODIFIED

        # New notice
        else:
            new_notice.save()
            return NoticeUpdateType.CREATED
    
    def close(self):
        mongoengine.disconnect()
