import pika
import json

from config import Config
from exceptions import RabbitMQConnectionError, RabbitMQPublishError
from exceptions import NoticeDetailParsingException

class NoticePublisher:
    def __init__(self, config: Config):
        self._config = config
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

    def publish_notice(self, data: dict) -> None:
        try:
            data_str = json.dumps(data)
        except TypeError as e:
            NoticeDetailParsingException(f"Failed to serialize notice: {data}")
        try:
            self._channel.basic_publish(
                exchange='', routing_key=self._queue_name, body=data_str
            )
        except pika.exceptions.AMQPError as e:
            raise RabbitMQPublishError(f"Failed to publish message: {e}")

    def __del__(self):
        self._connection.close()