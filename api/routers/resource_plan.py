from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from api.dependencies import get_resource_service
from services.resource_service import ResourceService


resource_plan_router = APIRouter(prefix='/resource-plans')
ResourceServiceDependency = Annotated[ResourceService, Depends(get_resource_service)]

@resource_plan_router.post('', status_code = status.HTTP_201_CREATED)
async def create_resource_plan(target_name: Annotated[str, Form(min_length=2, strip_whitespace=True)], target_quantity: Annotated[int, Form(gt=0)], player_file: Annotated[UploadFile, File()], resource_service: ResourceServiceDependency):
    file_bytes = await player_file.read()
    return await resource_service.create_resource_plan(target_name, target_quantity, file_bytes, player_file.filename)