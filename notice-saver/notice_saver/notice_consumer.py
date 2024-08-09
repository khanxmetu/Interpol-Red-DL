import json
import pika
import pika.adapters.blocking_connection
import pika.spec
import pika.exceptions

from notice_saver.rabbitmq_client import RabbitMQConsumer
from typing import Callable

class NoticeConsumer:
    def __init__(
            self,
            queue_name: str,
            rmq_consumer: RabbitMQConsumer,
            consume_callback_function: Callable
    ) -> None:
        self._queue_name = queue_name
        self._rmq_consumer = rmq_consumer
        self._rmq_consumer.declare_queue(self._queue_name)
        self._consume_callback_function = consume_callback_function

    def _consume_callback(
        self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ) -> None:
        notice_data = json.loads(body)
        self._consume_callback_function(notice_data)
        ch.basic_ack(method.delivery_tag)

    def run(self):
        self._rmq_consumer.consume_messages(
            queue=self._queue_name, callback=self._consume_callback, auto_ack=False
        )

