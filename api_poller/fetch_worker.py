from config import Config
from notice_fetcher import NoticeListFetcher, NoticeDetailFetcher
from queue_manager import NoticePublisher

class FetchWorker:
    """Orchestrates data fetching and queueing."""
    def __init__(self, config: Config) -> None:
        self._config = config
        self._list_fetcher = NoticeListFetcher(config)
        self._detail_fetcher = NoticeDetailFetcher(config)
        self._queue_manager = NoticePublisher(config)

    def run(self) -> None:
        notice_list = self._list_fetcher.fetch()
        for notice_id in notice_list:
            data = self._detail_fetcher.fetch(notice_id)
            self._queue_manager.publish_notice(data)

def run_fetch_worker() -> None:
    config = Config.load_from_env()
    worker = FetchWorker(config)
    worker.run()

if __name__ == "__main__":
    run_fetch_worker()