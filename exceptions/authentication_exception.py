from exceptions.app_exception import AppException

class AuthenticationException(AppException):
    pass
        
class PasswordNotVerifiedException(AuthenticationException):
    def __init__(self):
        super().__init__(
            message="Password was not verified",
            error_code="password_not_verified",
        )
        
class UserNotFoundException(AuthenticationException):
    def __init__(self):
        super().__init__(
            message="User was not found",
            error_code="user_not_found",
        )