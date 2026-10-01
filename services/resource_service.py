from exceptions.resource_not_found_exception import ItemNotFoundException
from repositories.recipe_repository import RecipeRepository
from schemas.resource import ResourceUsageItem, ResourceUsagePathResponse, ResourceUsageResponse


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
        
    async def get_resource_usage_path(self, resource_name: str, target_name: str):
        item_ids = await self.__recipe_repository.get_item_ids_by_names(resource_name, target_name)
        if item_ids is None:
            raise ItemNotFoundException()
        start_id = item_ids['start_id']
        target_id = item_ids['target_id']
        if start_id == target_id:
            return ResourceUsagePathResponse(
                resource_name=resource_name,
                target_name=target_name,
                path=[ResourceUsageItem(item_id=start_id, display_name=resource_name)]
            )
        return []