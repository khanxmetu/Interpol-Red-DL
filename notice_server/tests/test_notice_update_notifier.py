import pytest
from unittest.mock import MagicMock
from flask_socketio import SocketIO

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
