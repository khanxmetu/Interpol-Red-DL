from unittest import mock
import pytest
from requests import Response
import json

from api_poller.api_request_session import APIRequestSession
from api_poller.exceptions import APIRequestException


def test_default_headers_empty():
    session = APIRequestSession()
    assert session._session.headers == {}

def test_headers_set():
    headers = {"User-Agent": "Dummy"}
    session = APIRequestSession(headers)
    assert session._session.headers == headers

def test_get_json_response_success():
    session = APIRequestSession()
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    with mock.patch.object(session._session, 'get', return_value=mock_response):
        result = session.get_json_response('http://example.com')
        assert result == {"key": "value"}

def test_get_json_response_decode_failure():
    session = APIRequestSession()
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
    with mock.patch.object(session._session, 'get', return_value=mock_response):
        with pytest.raises(APIRequestException):
            result = session.get_json_response('http://example.com')

def test_get_json_response_status_failure():
    session = APIRequestSession()
    mock_response = mock.Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"key": "value"}
    mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
    with mock.patch.object(session._session, 'get', return_value=mock_response):
        with pytest.raises(APIRequestException):
            result = session.get_json_response('http://example.com')