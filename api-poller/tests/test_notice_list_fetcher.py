import pytest
from unittest import mock

from api_poller.notice_list_fetcher import NoticeListFetcher, NoticeListParsingException
from api_poller.api_request_session import APIRequestSession
from api_poller.models.query_options import QueryOptions


@pytest.fixture
def mock_session():
    return mock.MagicMock(spec=APIRequestSession)

@pytest.fixture
def fetcher(mock_session):
    return NoticeListFetcher(mock_session, "https://example.com")

@pytest.fixture
def mock_query():
    query = mock.MagicMock(spec=QueryOptions)
    query.get_options_dict.return_value = {'param1': 'value1'}
    return query

def test_fetch_notice_ids_calls_get_json_response_with_correct_params(fetcher, mock_session, mock_query):
    mock_session.get_json_response.return_value = {
        '_embedded': {
            'notices': [
                {'entity_id': '123/2024'},
                {'entity_id': '654/2023'}
            ]
        }
    }

    result = fetcher.fetch_notice_ids(mock_query)

    mock_query.get_options_dict.assert_called_once()
    mock_session.get_json_response.assert_called_once_with("https://example.com", params={'param1': 'value1'})
    assert result == ['123-2024', '654-2023']

def test_extract_ids_from_page_raises_exception_on_key_error(fetcher):
    with pytest.raises(NoticeListParsingException):
        fetcher._extract_ids_from_page({})

def test_extract_ids_from_page_returns_correct_ids(fetcher):
    data = {
        '_embedded': {
            'notices': [
                {'entity_id': '123/2024'},
                {'entity_id': '654/2023'}
            ]
        }
    }
    result = fetcher._extract_ids_from_page(data)
    assert result == ['123-2024', '654-2023']
