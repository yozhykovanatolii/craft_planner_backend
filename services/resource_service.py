from exceptions.resource_not_found_exception import ItemsNotFoundException, ResourceUsagePathNotFoundException
from repositories.item_repository import ItemRepository
from schemas.resource import ResourceUsageItemSchema, ResourceUsagePathSchema, ResourceUsageSchema


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
        items_path = await self.__item_repository.get_shortest_path_between_items(start_item_id, target_item_id)
        if items_path is None:
            raise ResourceUsagePathNotFoundException(resource_name, target_name)
        return ResourceUsagePathSchema(
            resource_name=resource_name,
            target_name=target_name,
            path=items_path,
        )