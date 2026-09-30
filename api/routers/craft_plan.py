from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from api.dependencies import get_current_user, get_craft_plan_service
from schemas.user import UserInfoSchema
from services.craft_plan_service import CraftPlanService

craft_plan_router = APIRouter(prefix='/craft-plans')
CraftPlanServiceDependency = Annotated[CraftPlanService, Depends(get_craft_plan_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@craft_plan_router.post('', status_code = status.HTTP_201_CREATED)
async def create_craft_plan(target_name: Annotated[str, Form(min_length=2, strip_whitespace=True)], target_quantity: Annotated[int, Form(ge=1, le=10)], player_file: Annotated[UploadFile, File()], craft_plan_service: CraftPlanServiceDependency, current_user: CurrentUser):
    file_bytes = await player_file.read()
    await craft_plan_service.create_craft_plan(target_name, target_quantity, file_bytes, player_file.filename, current_user.id)
    
@craft_plan_router.delete('/{plan_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_craft_plan(plan_id: int, craft_plan_service: CraftPlanServiceDependency, current_user: CurrentUser):
    await craft_plan_service.delete_craft_plan(plan_id, current_user.id)
    
@craft_plan_router.get('', status_code = status.HTTP_200_OK)
async def get_craft_plans(craft_plan_service: CraftPlanServiceDependency, current_user: CurrentUser):
    return await craft_plan_service.get_user_craft_plans(current_user.id)

@craft_plan_router.get('/{plan_id}', status_code = status.HTTP_200_OK)
async def get_craft_plan(plan_id: int, craft_plan_service: CraftPlanServiceDependency, current_user: CurrentUser):
    return await craft_plan_service.get_user_craft_plan(current_user.id, plan_id)

@craft_plan_router.patch('/{plan_id}/recalculate', status_code = status.HTTP_200_OK)
async def recalculate_craft_plan(plan_id: int, player_file: Annotated[UploadFile, File()], craft_plan_service: CraftPlanServiceDependency, current_user: CurrentUser):
    file_bytes = await player_file.read()
    await craft_plan_service.recalculate_craft_plan(current_user.id, plan_id, file_bytes, player_file.filename)