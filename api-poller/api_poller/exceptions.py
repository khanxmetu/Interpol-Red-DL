class APIPollerException(Exception):
    """Base class for all api_poller-related errors."""

class APIRequestException(APIPollerException):
    """Class for HTTP requests related errors"""

class NoticeListParsingException(APIPollerException):
    """"""

class NoticeDetailParsingException(APIPollerException):
    """"""

class RabbitMQException(APIPollerException):
    """Class for all RabbitMQ related errors"""