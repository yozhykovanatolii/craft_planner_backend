from exceptions.app_exception import AppException

class ConflictException(AppException):
    pass

class EmailAlreadyUsedException(ConflictException):
    def __init__(self):
        super().__init__(
            message="User is already created by this email",
            error_code="email_already_use",
        )
        
class RecipeLockedException(ConflictException):
    def __init__(self, recipe_id: str):
        super().__init__(
            message=f"Recipe '{recipe_id}' is not unlocked",
            error_code="recipe_locked",
        )