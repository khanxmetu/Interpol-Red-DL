import pytest
from unittest.mock import Mock, patch
from pika.exceptions import AMQPError
from api_poller.models.notice import Notice
from api_poller.rabbitmq_client import RabbitMQSender
from api_poller.exceptions import RabbitMQException
from api_poller.notice_publisher import NoticePublisher

# Sample Notice class with a model_dump_json method
class MockNotice:
    def model_dump_json(self):
        return '{"mock": "notice"}'

@pytest.fixture
def rmq_sender_mock():
    return Mock(spec=RabbitMQSender)

@pytest.fixture
def notice_mock():
    return MockNotice()

@pytest.fixture
def notice_publisher(rmq_sender_mock):
    return NoticePublisher(rmq_sender_mock, 'test_queue')

def test_publish_notice_success(notice_publisher, notice_mock, rmq_sender_mock):
    # Act
    notice_publisher.publish_notice(notice_mock)

    # Assert
    rmq_sender_mock.send_message.assert_called_once_with(
        exchange_name="",
        routing_key='test_queue',
        body='{"mock": "notice"}'
    )

def test_publish_notice_amqp_error(notice_publisher, notice_mock, rmq_sender_mock):
    # Arrange
    rmq_sender_mock.send_message.side_effect = AMQPError("Test AMQP Error")

    # Act & Assert
    with pytest.raises(RabbitMQException) as exc_info:
        notice_publisher.publish_notice(notice_mock)

    assert str(exc_info.value) == 'Test AMQP Error'
    rmq_sender_mock.send_message.assert_called_once_with(
        exchange_name="",
        routing_key='test_queue',
        body='{"mock": "notice"}'
    )
