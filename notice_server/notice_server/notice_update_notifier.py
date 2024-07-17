from flask_socketio import SocketIO

from notice_db_manager import NoticeUpdateType
from config import Config

class NoticeUpdateNotifier:
    def __init__(self, config: Config, socketio: SocketIO) -> None:
        self._config = config
        self._socketio = socketio

    def notify(
            self,
            notice_id: str,
            update_type: NoticeUpdateType,
            changed_data: dict
            ) -> None:
        self._socketio.emit(
            'notice_update',
            {
                'notice_id': notice_id,
                'update_type': update_type.name.lower(),
                'changed_data': changed_data
            }
        )