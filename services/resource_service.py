from exceptions.resource_not_found_exception import ItemNotFoundException, ItemsNotFoundException, ResourceUsagePathNotFoundException
from repositories.item_repository import ItemRepository
from schemas.resource import ResourceUsageItemSchema, ResourceUsagePathSchema, ResourceUsageSchema
from collections import deque


class ResourceService:
    def __init__(self, item_repository: ItemRepository):
        self.__item_repository = item_repository
        
    async def get_resource_usage(self, resource_name: str):
        items = await self.__item_repository.get_items_by_resource_name(resource_name)
        if items is None:
            raise ItemsNotFoundException(f"Items were not found by {resource_name}")
        return ResourceUsageSchema(
            resource_name=resource_name,
            used_in=items,
        )
        
    async def get_resource_usage_path(self, resource_name: str, target_name: str):
        item_ids = await self.__item_repository.get_item_ids_by_names(resource_name, target_name)
        if item_ids is None:
            raise ItemsNotFoundException(f"Items were not found by {resource_name} and {target_name}")
        start_item_id = item_ids['start_id']
        target_item_id = item_ids['target_id']
        if start_item_id == target_item_id:
            return ResourceUsagePathSchema(
                resource_name=resource_name,
                target_name=target_name,
                path=[ResourceUsageItemSchema(item_id=start_item_id, display_name=resource_name)]
            )
        visited_items, parent, items_by_id = await self.__find_item_path(start_item_id, target_item_id, resource_name)
        if target_item_id not in visited_items:
            raise ResourceUsagePathNotFoundException(resource_name, target_name)
        path = self.__reconstruct_path(parent, items_by_id, start_item_id, target_item_id)
        return ResourceUsagePathSchema(
            resource_name=resource_name,
            target_name=target_name,
            path=path,
        )
        
    async def __find_item_path(self, start_id, target_id, resource_name):
        queue = deque([start_id])
        visited_items = {start_id}
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
            items = await self.__item_repository.get_items_by_required_item_id(current_item_id)
            for item in items:
                neighbor_item_id = item["item_id"]
                if neighbor_item_id in visited_items:
                    continue
                items_by_id[neighbor_item_id] = {
                    "item_id": neighbor_item_id,
                    "display_name": item["display_name"],
                }
                visited_items.add(neighbor_item_id)
                parent[neighbor_item_id] = current_item_id
                queue.append(neighbor_item_id)
        return visited_items, parent, items_by_id
        
    def __reconstruct_path(self, parent, items_by_id, start, end):
        path = [items_by_id[end]]
        current_id = end
        while current_id != start:
            current_id = parent[current_id]
            path.append(items_by_id[current_id])
        path.reverse()
        return path