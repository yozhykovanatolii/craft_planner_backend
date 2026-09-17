from exceptions.app_exception import AppException

class RecipeNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="Recipe was not found",
            error_code="recipe_not_found",
        )