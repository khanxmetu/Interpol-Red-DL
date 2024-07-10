class APIPollerException(Exception):
    """Base class for all api_poller-related errors."""

class APIRequestException(APIPollerException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoticeListParsingException(APIPollerException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoticeDetailParsingException(APIPollerException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)