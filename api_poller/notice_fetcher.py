import requests
import json
import time

from config import Config

class BaseFetcher:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._red_list_url =  f"{self._config.BASE_URL}"
        self._red_list_url += f"/{self._config.RED_LIST_PATH}"
        self._headers = {}
        self._load_headers_from_file(self._config.HEADERS_FILE_PATH)

    def _load_headers_from_file(self, file_path: str) -> None:
        with open(file_path) as f:
            data = json.load(f)
        self._set_headers(data)

    def _set_headers(self, headers: dict) -> None:
        self._headers = headers

    def fetch(self):
        pass

    def _send_request_with_custom_headers(
        self,
        url: str, 
        params: dict={},
        headers: dict={}
    ) -> dict:
        r = requests.get(url, headers=headers, params=params)
        time.sleep(self._config.API_RATE_LIMIT_DELAY_MS // 1000)
        return r.json()

    def _send_request(self, url, params={}) -> dict:
        return self._send_request_with_custom_headers(
            url,
            params,
            self._headers
        )

class NoticeListFetcher(BaseFetcher):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._notice_list = set()

    def _extract_ids_from_page(self, data: dict) -> list[str]:
        notices = data['_embedded']['notices']
        ids = [
                notice['entity_id'].replace('/', '-')
                    for notice in notices
            ]
        return ids

    def _fetch_ids_from_page(self, page_no: int) -> list[str]:
        params = {
                    'page': page_no,
                    'resultPerPage': self._config.RESULT_PER_PAGE
                }
        data = self._send_request(self._red_list_url, params)
        ids = self._extract_ids_from_page(data)
        return ids

    def fetch(self) -> list[str]:
        for page_num in range(1, self._config.MAX_PAGES + 1):
            fetched_ids = self._fetch_ids_from_page(page_num)
            self._notice_list.update(fetched_ids)
        return list(self._notice_list)


class NoticeDetailFetcher(BaseFetcher):
    def __init__(self, config):
        super().__init__(config)

    def fetch(self, notice_id: str) -> dict:
        url = f"{self._red_list_url}/{notice_id}"
        data = self._send_request(url)
        return data
