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
        
class RefreshTokenExpiredException(AuthenticationException):
    def __init__(self):
        super().__init__(
            message="Refresh token has expired",
            error_code="refresh_token_expired",
        )


class InvalidRefreshTokenException(AuthenticationException):
    def __init__(self):
        super().__init__(
            message="Invalid refresh token",
            error_code="invalid_refresh_token",
        )
        
class TokenTypeException(AuthenticationException):
    def __init__(self):
        super().__init__(
            message="Invalid token type",
            error_code="invalid_token_type",
        )
        
class AccessTokenExpiredException(AuthenticationException):
    def __init__(self):
        super().__init__(
            message="Access token has expired",
            error_code="access_token_expired",
        )


class InvalidAccessTokenException(AuthenticationException):
    def __init__(self):
        super().__init__(
            message="Invalid access token",
            error_code="invalid_access_token",
        )