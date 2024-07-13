import time
import pika
import pika.adapters.blocking_connection
import pika.spec

from config import Config
from exceptions import RabbitMQConnectionError, RabbitMQConsumeError
from notice_db_manager import NoticeDBManager, NoticeUpdateType
from notice_update_notifier import NoticeUpdateNotifier

class NoticeConsumer:
    def __init__(
            self, config: Config,
            db_manager: NoticeDBManager,
            update_notifier: NoticeUpdateNotifier
            ) -> None:
        self._config = config
        self._db_manager = db_manager
        self._update_notifier = update_notifier
        self._connection = self._initialize_connection(
            self._config.BROKER_HOST, self._config.BROKER_PORT
        )
        self._channel = self._connection.channel()
        self._queue_name = self._config.QUEUE_NAME
        self._init_queue(self._queue_name)

    def _init_queue(self, name: str) -> None:
        self._channel.queue_declare(name)

    def _initialize_connection(
        self,
        host: str, port: int
    ) -> pika.BlockingConnection:
        try:
            params = pika.ConnectionParameters(host=host, port=port)
            return pika.BlockingConnection(parameters=params)
        except pika.exceptions.AMQPConnectionError as e:
            raise RabbitMQConnectionError(f"Failed to connect to RabbitMQ at {host}:{port}")
    
    def consume_callback(
        self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver, 
        properties: pika.spec.BasicProperties,
        body: bytes
    ) -> None:
        print(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def run(self):
        self._channel.basic_consume(
            self._queue_name, self.consume_callback, auto_ack=False
        )
        self._channel.start_consuming()