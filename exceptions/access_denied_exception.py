from exceptions.app_exception import AppException


class AccessDeniedException(AppException):
    def __init__(self):
        super().__init__(
            message="Access was denied",
            error_code="access_denied",
        )