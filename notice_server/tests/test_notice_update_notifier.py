import pytest
from unittest.mock import MagicMock
from flask_socketio import SocketIO
import datetime
from werkzeug.http import http_date

from notice_server.notice_update_notifier import NoticeUpdateNotifier, NoticeUpdateType

class MockNoticeUpdateType:
    def __init__(self, name):
        self.name = name

@pytest.fixture
def mock_socketio():
    return MagicMock(spec=SocketIO)

@pytest.fixture
def notice_update_notifier(mock_socketio):
    return NoticeUpdateNotifier(socketio=mock_socketio)

def test_notify(notice_update_notifier, mock_socketio):
    notice_id = "1234-2020"
    update_type = MockNoticeUpdateType("CREATED")
    changed_data = {"field1": "value1", "field2": "value2"}

    notice_update_notifier.notify(notice_id, update_type, changed_data)

    mock_socketio.emit.assert_called_once_with(
        'notice_update',
        {
            'notice_id': "1234-2020",
            'update_type': "created",
            'changed_data': {"field1": "value1", "field2": "value2"}
        }
    )


def test_notify_with_notice_having_date_fields(notice_update_notifier, mock_socketio):
    notice_id = "1234-2020"
    update_type = MockNoticeUpdateType("CREATED")
    cur_date = datetime.datetime(
        2024, 7, 17, 20, 29, 49, 537770, tzinfo=datetime.timezone.utc)
    dob = datetime.date(2020, 4, 20)
    changed_data = {
        "field1": "value1",
        "date_of_birth": dob,
        "last_fetched_date": cur_date,
        "first_fetched_date": cur_date,
        "last_modified_date": cur_date
    }

    notice_update_notifier.notify(notice_id, update_type, changed_data)

    mock_socketio.emit.assert_called_once_with(
        'notice_update',
        {
            'notice_id': "1234-2020",
            'update_type': "created",
            'changed_data': {
                "field1": "value1",
                "date_of_birth": "Mon, 20 Apr 2020 00:00:00 GMT",
                "last_fetched_date": 'Wed, 17 Jul 2024 20:29:49 GMT',
                "first_fetched_date": 'Wed, 17 Jul 2024 20:29:49 GMT',
                "last_modified_date": 'Wed, 17 Jul 2024 20:29:49 GMT'
            }

        }
    )
