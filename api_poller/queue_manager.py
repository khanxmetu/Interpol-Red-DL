import pika
import json

from config import Config
import time # TODO
class QueueManager:
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
        params = pika.ConnectionParameters(host=host, port=port)
        return pika.BlockingConnection(parameters=params)

    def push(self, data: dict) -> None:
        data_str = json.dumps(data)
        self._channel.basic_publish(
            exchange='', routing_key=self._queue_name, body=data_str
        )

    def __del__(self):
        self._connection.close()