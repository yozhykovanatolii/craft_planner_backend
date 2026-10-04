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
        
class ItemsNotFoundException(ResourceNotFoundException):
    def __init__(self, error_text):
        super().__init__(
            message=error_text,
            error_code="items_not_found",
        )
        
class ResourceUsagePathNotFoundException(ResourceNotFoundException):
    def __init__(self, resource_name: str, target_name: str):
        super().__init__(
            message=f"No usage path found from '{resource_name}' to '{target_name}'",
            error_code="resource_usage_path_not_found",
        )