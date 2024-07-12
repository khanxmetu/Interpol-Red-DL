import time

from config import Config
from notice_db_manager import NoticeDBManager
from notice_update_notifier import NoticeUpdateNotifier, NoticeUpdateType

class NoticeConsumer:
    def __init__(
            self, config: Config,
            db_manager: NoticeDBManager,
            update_notifier: NoticeUpdateNotifier
            ) -> None:
        self._config = config
        self._db_manager = db_manager
        self._update_notifier = update_notifier

    def run(self):
        while True:
            self._update_notifier.notify('2222-2024', NoticeUpdateType.CREATED, {"asd": "asdsd"})
            time.sleep(1)