from pika.exceptions import AMQPError
from api_poller.models.notice import Notice
from api_poller.rabbitmq_client import RabbitMQSender
from api_poller.exceptions import RabbitMQException

class NoticePublisher:
    def __init__(self, rmq_sender: RabbitMQSender, queue_name: str):
        self._rmq_sender = rmq_sender
        self._queue_name = queue_name
    
    def publish_notice(self, notice: Notice):
        notice_json: str = notice.model_dump_json()
        try:
            self._rmq_sender.send_message(
                exchange_name="",
                routing_key=self._queue_name,
                body=notice_json
            )
        except AMQPError as e:
            raise RabbitMQException(e)