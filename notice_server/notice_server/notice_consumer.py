import json
import pika
import pika.adapters.blocking_connection
import pika.spec

from notice_server.notice_db_manager import NoticeDBManager, NoticeUpdateType
from notice_server.notice_update_notifier import NoticeUpdateNotifier
from notice_server.models.notice import Notice
from notice_server.rabbitmq_client import RabbitMQConsumer


class NoticeConsumer:
    def __init__(
            self,
            queue_name: str,
            rmq_consumer: RabbitMQConsumer,
            db_manager: NoticeDBManager,
            update_notifier: NoticeUpdateNotifier
    ) -> None:
        self._queue_name = queue_name
        self._rmq_consumer = rmq_consumer
        self._db_manager = db_manager
        self._update_notifier = update_notifier
        self._rmq_consumer.declare_queue(self._queue_name)

    def _consume_callback(
        self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ) -> None:
        notice = Notice.from_json(body.decode())
        notice.validate()
        update_type = self._db_manager.update_notice_from_doc(notice)
        if update_type in [NoticeUpdateType.CREATED, NoticeUpdateType.MODIFIED]:
            changed_data = notice.to_dict()
        else:
            changed_data = {
                "last_fetched_date": notice.last_fetched_date
            }
        self._update_notifier.notify(
            notice.notice_id, update_type, changed_data
        )

    def run(self):
        self._rmq_consumer.consume_messages(
            queue=self._queue_name, callback=self._consume_callback
        )
