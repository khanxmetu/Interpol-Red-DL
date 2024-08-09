import pytest
from unittest.mock import MagicMock, patch
from api_poller.rabbitmq_client import RabbitMQClient, RabbitMQSender


@pytest.fixture
def mock_pika():
    with patch('pika.BlockingConnection') as mock_conn:
        yield mock_conn


def test_rabbitmqclient_init():
    client = RabbitMQClient(
        username='user', password='pass', host='host', port=1234)
    assert client._username == 'user'
    assert client._password == 'pass'
    assert client._host == 'host'
    assert client._port == 1234
    assert client._connection is None
    assert client._channel is None


def test_connect(mock_pika):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_pika.return_value = mock_connection
    mock_connection.channel.return_value = mock_channel

    client = RabbitMQClient()
    client.connect()

    mock_pika.assert_called_once()
    mock_connection.channel.assert_called_once()
    assert client._connection == mock_connection
    assert client._channel == mock_channel


def test_ensure_connection(mock_pika):
    client = RabbitMQClient()
    client.connect = MagicMock()
    client._ensure_connection()
    client.connect.assert_called_once()

    # Simulate existing connection
    client.connect.reset_mock()
    client._connection = MagicMock()
    client._connection.is_closed = False
    client._ensure_connection()
    client.connect.assert_not_called()


def test_close(mock_pika):
    client = RabbitMQClient()
    client._channel = MagicMock()
    client._connection = MagicMock()

    client.close()

    client._channel.close.assert_called_once()
    client._connection.close.assert_called_once()


def test_declare_queue(mock_pika):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_pika.return_value = mock_connection
    mock_connection.channel.return_value = mock_channel

    client = RabbitMQClient()
    client.declare_queue('test_queue', exclusive=True)

    mock_channel.queue_declare.assert_called_once_with(
        queue='test_queue', exclusive=True)


def test_rabbitmqsender_send_message(mock_pika):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_pika.return_value = mock_connection
    mock_connection.channel.return_value = mock_channel

    sender = RabbitMQSender()
    sender.send_message('test_exchange', 'test_key', 'test_body')

    mock_channel.basic_publish.assert_called_once_with(
        exchange='test_exchange',
        routing_key='test_key',
        body='test_body'
    )
