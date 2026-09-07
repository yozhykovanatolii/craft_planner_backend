from exceptions.app_exception import AppException


class MediaTypeException(AppException):
    def __init__(self):
        super().__init__(
            message="Unsupported image type",
            error_code="unsupported_media_type",
        )