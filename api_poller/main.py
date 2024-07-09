import os
import time
import json

import requests
import pika

class Config:
    def __init__(self, base_url=None, red_list_path=None, result_per_page=None, max_pages=None, api_rate_limit_delay_ms=None, headers_file_path="headers.json"):
        self.BASE_URL = base_url or "https://ws-public.interpol.int"
        self.RED_LIST_PATH = red_list_path or "/notices/v1/red"
        self.RESULT_PER_PAGE = result_per_page or 160
        self.MAX_PAGES = max_pages or 1
        self.API_RATE_LIMIT_DELAY_MS = api_rate_limit_delay_ms or 0
        self.HEADERS_FILE_PATH = headers_file_path

    @classmethod
    def load_from_env(cls):
        return cls(
            base_url=os.getenv("BASE_URL"),
            red_list_path=os.getenv("RED_LIST_PATH"),
            result_per_page=int(os.getenv("RESULT_PER_PAGE")),
            max_pages=int(os.getenv("MAX_PAGES")),
            api_rate_limit_delay_ms=int(os.getenv("API_RATE_LIMIT_DELAY_MS"))
        )

class BaseFetcher:
    def __init__(self, config):
        self._config = config
        self._red_list_url =  f"{self._config.BASE_URL}"
        self._red_list_url += f"/{self._config.RED_LIST_PATH}"
        self._headers = {}
        self._load_headers_from_file(self._config.HEADERS_FILE_PATH)

    def _load_headers_from_file(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        self._set_headers(data)

    def _set_headers(self, headers):
        self._headers = headers

    def fetch(self):
        pass

    def _send_request_with_custom_headers(self, url, params={}, headers={}):
        r = requests.get(url, headers=headers, params=params)
        time.sleep(self._config.API_RATE_LIMIT_DELAY_MS // 1000)
        return r.json()

    def _send_request(self, url, params={}):
        return self._send_request_with_custom_headers(url, params,
                                                      self._headers)

class NoticeListFetcher(BaseFetcher):
    def __init__(self, config):
        super().__init__(config)
        self._notice_list = set()

    def _extract_ids_from_page(self, data):
        notices = data['_embedded']['notices']
        ids = [
                notice['entity_id'].replace('/', '-')
                    for notice in notices
            ]
        return ids

    def _fetch_ids_from_page(self, page_no):
        params = {
                    'page': page_no,
                    'resultPerPage': self._config.RESULT_PER_PAGE
                }
        data = self._send_request(self._red_list_url, params)
        ids = self._extract_ids_from_page(data)
        return ids

    def fetch(self):
        for page_num in range(1, self._config.MAX_PAGES + 1):
            fetched_ids = self._fetch_ids_from_page(page_num)
            self._notice_list.update(fetched_ids)
        return list(self._notice_list)


class NoticeDetailFetcher(BaseFetcher):
    def __init__(self, config):
        super().__init__(config)

    def fetch(self, notice_id):
        url = f"{self._red_list_url}/{notice_id}"
        data = self._send_request(url)
        return data

class FetchWorker:
    """Orchestrates data fetching and queueing."""
    def __init__(self, config):
        self._config = config
        self._list_fetcher = NoticeListFetcher(config)
        self._detail_fetcher = NoticeDetailFetcher(config)

    def run(self):
        notice_list = self._list_fetcher.fetch()
        for notice_id in notice_list:
            data = self._detail_fetcher.fetch(notice_id)
            print(data)

def main():
    config = Config.load_from_env()
    worker = FetchWorker(config)
    worker.run()
    print("Ran successfully")


if __name__ == "__main__":
    main()