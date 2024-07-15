from api_poller.api_request_session import APIRequestSession
from api_poller.models.query_options import QueryOptions
from api_poller.exceptions import NoticeListParsingException

class NoticeListFetcher:
    def __init__(self, session: APIRequestSession, url: str):
        self._session = session
        self._url = url

    def _extract_ids_from_page(self, data: dict) -> list[str]:
        try:
            notices = data['_embedded']['notices']
        except KeyError as e:
            raise NoticeListParsingException(e)
        ids = [notice['entity_id'].replace('/', '-') for notice in notices]
        return ids

    def fetch_notice_ids(self, query: QueryOptions) -> list[str]:
        params = query.get_options_dict()
        resp_dict = self._session.get_json_response(self._url, params=params)
        return self._extract_ids_from_page(resp_dict)


