from exceptions.app_exception import AppException


class ResourceNotFoundException(AppException):
    pass


class RecipeNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(
            message="Recipe was not found",
            error_code="recipe_not_found",
        )
        
class CraftPlanNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(
            message="Craft plan was not found",
            error_code="craft_plan_not_found",
        )
        
class ItemNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(
            message="Item was not found",
            error_code="item_not_found",
        )