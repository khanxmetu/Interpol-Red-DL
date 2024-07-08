import time

import requests
import pika

class Config:
    BASE_URL = "https://ws-public.interpol.int"
    RED_LIST_URL = f"{BASE_URL}/notices/v1/red"
    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    RESULT_PER_PAGE = 160
    MAX_PAGES = 1
    API_RATE_LIMIT_DELAY_MS = 0

class BaseFetcher:
    def __init__(self, config):
        self._config = config

    def fetch(self):
        pass

    def _send_request(self, url, params={}):
        r = requests.get(url, headers=Config.HEADERS, params=params)
        time.sleep(self._config.API_RATE_LIMIT_DELAY_MS // 1000)
        print(r.text)
        return r.json()

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
        data = self._send_request(self._config.RED_LIST_URL, params)
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
        url = f"{self._config.RED_LIST_URL}/{notice_id}"
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
    config = Config()
    worker = FetchWorker(config)
    worker.run()
    print("Ran successfully")


if __name__ == "__main__":
    main()