from exceptions.resource_not_found_exception import ItemNotFoundException, ResourceUsagePathNotFoundException
from repositories.recipe_repository import RecipeRepository
from schemas.resource import ResourceUsageItem, ResourceUsagePathResponse, ResourceUsageResponse
from collections import deque


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
        queue = deque([start_id])
        visited = {start_id}
        parent = {}
        items_by_id = {}
        items_by_id[start_id] = {
            "item_id": start_id,
            "display_name": resource_name,
        }
        while queue:
            current_item_id = queue.popleft()
            if current_item_id == target_id:
                break
            items = await self.__recipe_repository.get_next_items(current_item_id)
            for item in items:
                neighbor_item_id = item["item_id"]
                if neighbor_item_id in visited:
                    continue
                items_by_id[neighbor_item_id] = {
                    "item_id": neighbor_item_id,
                    "display_name": item["display_name"],
                }
                visited.add(neighbor_item_id)
                parent[neighbor_item_id] = current_item_id
                queue.append(neighbor_item_id)
        if target_id not in visited:
            raise ResourceUsagePathNotFoundException(resource_name, target_name)
        path = self.__backtrace(parent, items_by_id, start_id, target_id)
        return ResourceUsagePathResponse(
            resource_name=resource_name,
            target_name=target_name,
            path=path,
        )
        
    def __backtrace(self, parent, items_by_id, start, end):
        path = [items_by_id[end]]
        current_id = end
        while current_id != start:
            current_id = parent[current_id]
            path.append(items_by_id[current_id])
        path.reverse()
        return path