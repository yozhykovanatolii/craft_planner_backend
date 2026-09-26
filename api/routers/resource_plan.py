from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from api.dependencies import get_current_user, get_resource_service
from schemas.user import UserInfoSchema
from services.resource_service import ResourceService


resource_plan_router = APIRouter(prefix='/resource-plans')
ResourceServiceDependency = Annotated[ResourceService, Depends(get_resource_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@resource_plan_router.post('', status_code = status.HTTP_201_CREATED)
async def create_resource_plan(target_name: Annotated[str, Form(min_length=2, strip_whitespace=True)], target_quantity: Annotated[int, Form(ge=1, le=10)], player_file: Annotated[UploadFile, File()], resource_service: ResourceServiceDependency, current_user: CurrentUser):
    file_bytes = await player_file.read()
    await resource_service.create_resource_plan(target_name, target_quantity, file_bytes, player_file.filename, current_user.id)
    
@resource_plan_router.delete('/{plan_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_resource_plan(plan_id: int, resource_service: ResourceServiceDependency, current_user: CurrentUser):
    await resource_service.delete_resource_plan(plan_id, current_user.id)