from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from exceptions.access_denied_exception import AccessDeniedException
from exceptions.authentication_exception import AuthenticationException
from exceptions.conflict_exception import ConflictException
from exceptions.media_type_exception import MediaTypeException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from exceptions.save_file_parse_exception import SaveFileParseException

def register_error_handlers(app: FastAPI):
    @app.exception_handler(SaveFileParseException)
    def save_file_parse_exception_handler(_: Request, exception: SaveFileParseException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
    
    @app.exception_handler(AuthenticationException)
    def authentication_exception_handler(_: Request, exception: AuthenticationException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(ConflictException)
    def conflict_exception_handler(_: Request, exception: ConflictException):
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
        
    @app.exception_handler(AccessDeniedException)
    def media_type_exception_handler(_: Request, exception: AccessDeniedException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(ResourceNotFoundException)
    def recipe_not_exception_handler(_: Request, exception: ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
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