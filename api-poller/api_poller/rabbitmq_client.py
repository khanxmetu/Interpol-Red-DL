import time
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
        port: int = 5672,
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
            host=self._host, port=self._port, credentials=credentials
        )
        self._connection = pika.BlockingConnection(parameters=params)
        self._channel = self._connection.channel()

    def _ensure_connection(self, max_retries=3, delay=60) -> None:
        if not self._connection or self._connection.is_closed:
            last_exception = None
            for _ in range(max_retries):
                try:
                    self.connect()
                    return
                except pika.exceptions.AMQPError as e:
                    last_exception = e
                time.sleep(delay)
            raise last_exception

    def close(self) -> None:
        self._channel.close()
        self._connection.close()

    def declare_queue(self, queue_name: str, exclusive: bool = False) -> None:
        self._ensure_connection()
        self._channel.queue_declare(queue=queue_name, exclusive=exclusive)


class RabbitMQSender(RabbitMQClient):
    def send_message(
        self,
        exchange_name: str,
        routing_key: str,
        body: str,
    ):
        self._ensure_connection()
        try:
            self._channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=body,
            )
        except pika.exceptions.AMQPError as e:
            print(f"[-] RabbitMQError: {e}. Reconnecting...")
            self._ensure_connection()
            self.send_message(exchange_name, routing_key, body)
