import json
import time
import os

from api_poller.exceptions import APIPollerException
from api_poller.api_request_session import APIRequestSession
from api_poller.models.query_options import QueryOptions
from api_poller.models.notice import Notice
from api_poller.notice_list_fetcher import NoticeListFetcher
from api_poller.notice_detail_fetcher import NoticeDetailFetcher, NoticeImageIDsFetcher
from api_poller.notice_publisher import NoticePublisher
from api_poller.query_strategy import SimpleDefaultSearch
from api_poller.rabbitmq_client import RabbitMQSender


class APIPoller:
    def __init__(
        self,
        query_options_list: list[QueryOptions],
        notice_list_fetcher: NoticeListFetcher,
        notice_detail_fetcher: NoticeDetailFetcher,
        notice_publisher: NoticePublisher,
        api_rate_limit_delay: int,
        poll_interval: int
    ):
        self._query_options_list = query_options_list
        self._notice_list_fetcher = notice_list_fetcher
        self._notice_publisher = notice_publisher
        self._notice_detail_fetcher = notice_detail_fetcher
        self._api_rate_limit_delay = api_rate_limit_delay
        self._poll_interval = poll_interval

    def _read_and_publish_notice(self, notice_id: str) -> bool:
        """Returns whether notice published successfully"""
        try:
            notice: Notice = self._notice_detail_fetcher.fetch_notice_detail(
                notice_id)
        except APIPollerException as e:
            print(f"[-] Failed to fetch notice: {notice_id}. Reason: {e}")
            return False
        try:
            self._notice_publisher.publish_notice(notice)
        except APIPollerException as e:
            print(
                f"[-] Failed to publish notice: {notice_id}. Reason: {e}")
            return False
        print(f"[+] Notice: {notice_id} published successfully")
        return True

    def _read_and_publish_notices(self) -> int:
        """Returns number of notices published successfully"""
        count = 0
        for query_options in self._query_options_list:
            try:
                notice_ids = self._notice_list_fetcher.fetch_notice_ids(
                    query_options)
            except APIPollerException as e:
                print(
                    f"[-] Failed to fetch notice list"
                    f" with query options: {query_options}. Reason: {e}"
                )
                continue
            print(
                f"[+] {len(notice_ids)} notices"
                f" found with query: {query_options}"
            )
            for notice_id in notice_ids:
                count += self._read_and_publish_notice(notice_id)
                print(
                    f"[+] Waiting {self._api_rate_limit_delay}s for next read...")
                time.sleep(self._api_rate_limit_delay)
        return count

    def run(self):
        while True:
            count = self._read_and_publish_notices()
            print(f"[+] {count} notices published successfully")
            print(
                f"[+] Waiting {self._poll_interval}s for next poll run...")


def main():
    red_list_url = os.environ["RED_LIST_URL"]
    api_rate_limit_delay = int(os.environ["API_RATE_LIMIT_DELAY"])
    poll_interval = int(os.environ["POLL_INTERVAL"])
    session_headers = json.loads(open('config_data/headers.json').read())
    rabbitmq_host = os.environ["RABBITMQ_HOST"]
    rabbitmq_port = int(os.environ["RABBITMQ_PORT"])
    rabbitmq_user = os.environ["RABBITMQ_DEFAULT_USER"]
    rabbitmq_pass = os.environ["RABBITMQ_DEFAULT_PASS"]
    queue_name = os.environ["QUEUE_NAME"]

    session = APIRequestSession(headers=session_headers)

    query_options_list: list[QueryOptions] = SimpleDefaultSearch(
    ).get_query_options_list()

    notice_list_fetcher = NoticeListFetcher(
        session,
        red_list_url
    )
    notice_img_ids_fetcher = NoticeImageIDsFetcher(
        session,
        red_list_url
    )
    notice_detail_fetcher = NoticeDetailFetcher(
        session,
        red_list_url,
        notice_img_ids_fetcher
    )

    rmq_client = RabbitMQSender(
        host=rabbitmq_host,
        port=rabbitmq_port,
        username=rabbitmq_user,
        password=rabbitmq_pass
    )
    notice_publisher = NoticePublisher(rmq_client, queue_name=queue_name)
    APIPoller(
        query_options_list,
        notice_list_fetcher,
        notice_detail_fetcher,
        notice_publisher,
        api_rate_limit_delay,
        poll_interval
    ).run()


if __name__ == "__main__":
    main()
