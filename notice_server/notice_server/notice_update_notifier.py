from enum import Enum, auto

from flask_socketio import SocketIO

class NoticeUpdateType(Enum):
    CREATED = auto()
    REFETCHED = auto()
    MODIFIED = auto()

class NoticeUpdateNotifier:
    def __init__(self, socketio: SocketIO) -> None:
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