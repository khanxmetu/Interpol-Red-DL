import pika
import pika.channel
import pika.connection


class RabbitMQClient:
    """Base RabbitMQClient class that encapsulates connection logic"""

    def __init__(
        self,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672
    ):
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._connection: pika.connection.Connection | None = None
        self._channel: pika.channel.Channel | None = None

    def connect(self) -> None:
        credentials = pika.PlainCredentials(self._username, self._password)
        params = pika.ConnectionParameters(
            host=self._host, port=self._port, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters=params)
        self._channel = self._connection.channel()

    def _ensure_connection(self) -> None:
        if not self._connection or self._connection.is_closed:
            self.connect()

    def close(self) -> None:
        self._channel.close()
        self._connection.close()

    def declare_queue(self, queue_name: str, exclusive: bool = False) -> None:
        self._ensure_connection()
        self._channel.queue_declare(
            queue=queue_name,
            exclusive=exclusive
        )


class RabbitMQConsumer(RabbitMQClient):
    def __init__(
        self,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672
    ):
        super().__init__(username, password, host, port)
        self._channel_tag = None

    def consume_messages(self, queue, callback):
        self._ensure_connection()
        self._channel_tag = self._channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )
        self._channel.start_consuming()

    def cancel_consumer(self):
        if self._channel_tag is not None:
            self._channel.basic_cancel(self.channel_tag)
            self._channel_tag = None
