from enum import Enum, auto
import datetime
from werkzeug.http import http_date

from flask_socketio import SocketIO


class NoticeUpdateType(Enum):
    CREATED = auto()
    REFETCHED = auto()
    MODIFIED = auto()


class NoticeUpdateNotifier:
    def __init__(self, socketio: SocketIO) -> None:
        """
        Initializes the NoticeUpdateNotifier.

        :param socketio: A SocketIO instance representing the clients connected to receive notice updates
        """
        self._socketio = socketio

    def _prepare_notice_data_for_transmission(self, data: dict) -> None:
        """Preprocess and updates the data to make sure dates are encodable"""
        for key, value in data.items():
            if (
                isinstance(value, datetime.datetime)
                or isinstance(value, datetime.date)
            ):
                data[key] = http_date(value)

    def notify(
            self,
            notice_id: str,
            update_type: NoticeUpdateType,
            changed_data: dict
    ) -> None:
        """
        Sends a notice update to all clients connected via the SocketIO instance.

        :param notice_id: The id of the notice being updated.
        :param update_type: The type of update being performed (created, refetched, modified).
        :param changed_data: A dictionary containing the changed data for the notice.
        """
        changed_data = changed_data.copy()
        self._prepare_notice_data_for_transmission(changed_data)
        self._socketio.emit(
            'notice_update',
            {
                'notice_id': notice_id,
                'update_type': update_type.name.lower(),
                'changed_data': changed_data
            }
        )
