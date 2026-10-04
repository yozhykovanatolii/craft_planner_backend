from pydantic import BaseModel

class ResourceUsageItemSchema(BaseModel):
    item_id: str
    display_name: str


class ResourceUsageSchema(BaseModel):
    resource_name: str
    used_in: list[ResourceUsageItemSchema]
    
class ResourceUsagePathSchema(BaseModel):
    resource_name: str
    target_name: str
    path: list[ResourceUsageItemSchema]