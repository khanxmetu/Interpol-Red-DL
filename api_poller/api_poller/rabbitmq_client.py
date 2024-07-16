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
        params = pika.ConnectionParameters(host=self._host, port=self._port)
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


class RabbitMQSender(RabbitMQClient):
    def send_message(
        self,
        exchange_name: str,
        routing_key: str,
        body: str,
    ):
        self._ensure_connection()
        self._channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body,
        )

