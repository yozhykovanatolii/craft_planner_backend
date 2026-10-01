from exceptions.resource_not_found_exception import ItemNotFoundException
from repositories.recipe_repository import RecipeRepository
from schemas.resource import ResourceUsageResponse


class ResourceService:
    def __init__(self, recipe_repository: RecipeRepository):
        self.__recipe_repository = recipe_repository
        
    async def get_resource_usage(self, resource_name: str):
        items = await self.__recipe_repository.get_items_using_resource(resource_name)
        if items is None:
            raise ItemNotFoundException()
        return ResourceUsageResponse(
            resource_name=resource_name,
            used_in=items,
        )