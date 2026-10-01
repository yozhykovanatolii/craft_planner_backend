from pydantic import BaseModel


class ResourceUsageItem(BaseModel):
    item_id: str
    display_name: str


class ResourceUsageResponse(BaseModel):
    resource_name: str
    used_in: list[ResourceUsageItem]