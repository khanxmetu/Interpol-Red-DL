class NoticeServerException(Exception):
    """Base class for all notice_server-related errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RabbitMQConnectionError(NoticeServerException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RabbitMQConsumeError(NoticeServerException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)