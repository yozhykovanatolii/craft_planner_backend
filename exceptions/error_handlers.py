from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

def register_error_handlers(app: FastAPI):    
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