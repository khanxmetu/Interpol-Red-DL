class NoticeSaverException(Exception):
    pass


class ImageDownloadException(NoticeSaverException):
    pass


class OffenseClassificationException(NoticeSaverException):
    pass


class NotAnImageException(NoticeSaverException):
    pass


class InterpolServerRequestException(NoticeSaverException):
    pass
