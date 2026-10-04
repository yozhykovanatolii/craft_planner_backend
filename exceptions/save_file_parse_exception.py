from exceptions.app_exception import AppException

class SaveFileParseException(AppException):
    pass


class InvalidFileExtensionException(SaveFileParseException):
    def __init__(self):
        super().__init__(
            message="Invalid save file extension",
            error_code="invalid_file_extension",
        )


class InvalidJsonException(SaveFileParseException):
    def __init__(self):
        super().__init__(
            message="Invalid JSON file",
            error_code="invalid_json",
        )


class InvalidSaveStructureException(SaveFileParseException):
    def __init__(self, message: str, error_code: str):
        super().__init__(
            message=message,
            error_code=error_code,
        )