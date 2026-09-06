from exceptions.app_exception import AppException


class EmailAlreadyUsedException(AppException):
    def __init__(self):
        super().__init__(
            message="User is already created by this email",
            error_code="email_already_use",
        )