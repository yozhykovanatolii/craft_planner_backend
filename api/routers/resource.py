from typing import Annotated
from fastapi import APIRouter, Depends
from api.dependencies import get_resource_service
from schemas.resource import ResourceUsageSchema
from services.resource_service import ResourceService

resource_router = APIRouter(prefix='/resources')
ResourceServiceDependency = Annotated[ResourceService, Depends(get_resource_service)]

@resource_router.get("/{resource_name}/usage", response_model=ResourceUsageSchema)
async def get_resource_usage(resource_name: str, resource_service: ResourceServiceDependency):
    return await resource_service.get_resource_usage(resource_name)

@resource_router.get("/{resource_name}/usage/{target_name}/path")
async def get_resource_usage_path(resource_name: str, target_name: str, resource_service: ResourceServiceDependency):
    return await resource_service.get_resource_usage_path(resource_name, target_name)