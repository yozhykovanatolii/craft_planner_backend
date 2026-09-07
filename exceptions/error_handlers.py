from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from exceptions.authentication_exception import AuthenticationException
from exceptions.email_already_used_exception import EmailAlreadyUsedException
from exceptions.media_type_exception import MediaTypeException

def register_error_handlers(app: FastAPI):
    @app.exception_handler(AuthenticationException)
    def authentication_exception_handler(_: Request, exception: AuthenticationException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(EmailAlreadyUsedException)
    def email_already_use_exception_handler(_: Request, exception: EmailAlreadyUsedException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(MediaTypeException)
    def media_type_exception_handler(_: Request, exception: MediaTypeException):
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
            
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(_: Request, exception: RequestValidationError):
        messages = [error["msg"] for error in exception.errors()]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                'error_code': 'validation_error',
                'message': '; '.join(messages),
            }
        )