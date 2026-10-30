import asyncio
from typing import Annotated
from api.dependencies import get_craft_plan_repository, get_recipe_repository, get_user_repository
from clients.firebase_client import send_push_notification
from config import settings
from taskiq_redis import RedisStreamBroker
from taskiq import TaskiqDepends
from repositories.craft_plan_repository import CraftPlanRepository
from repositories.recipe_repository import RecipeRepository
from repositories.user_repository import UserRepository
from services.craft_plan_service import CraftPlanService

broker = RedisStreamBroker(
    url=settings.redis_url,
)

def get_taskiq_craft_plan_service(recipe_repository: Annotated[RecipeRepository, TaskiqDepends(get_recipe_repository)], craft_plan_repository: Annotated[CraftPlanRepository, TaskiqDepends(get_craft_plan_repository)]):
    return CraftPlanService(recipe_repository, craft_plan_repository)

@broker.task(retry_on_error=True)
async def generate_craft_plan(target_name: str, target_quantity: int, user_id: int, player_inventory, recipe_ingredients, target_item_id, craft_plan_service: Annotated[CraftPlanService, TaskiqDepends(get_taskiq_craft_plan_service)]):
    await craft_plan_service.calculate_craft_plan(target_name, target_quantity, user_id, player_inventory, recipe_ingredients, target_item_id)
    await send_notification_to_user.kiq(
        user_id=user_id,
        message_title="Craft plan created",
        message_body="Your craft plan was created. Check results.",
    )
    
@broker.task
async def recalculate_plan(plan_id, user_id, player_inventory, recipe_ingredients, target_item_id, craft_plan_service: Annotated[CraftPlanService, TaskiqDepends(get_taskiq_craft_plan_service)]):
    await craft_plan_service.recalculate_craft_plan(plan_id, player_inventory, recipe_ingredients, target_item_id)
    await send_notification_to_user.kiq(
        user_id=user_id,
        message_title="Craft plan recalculated",
        message_body="Your craft plan was recalculated. Check new results.",
    )
      
@broker.task()
async def send_notification_to_user(user_id: int, message_title: str, message_body: str, user_repository: Annotated[UserRepository, TaskiqDepends(get_user_repository)]):
    user_fcm_token = await user_repository.get_user_fcm_token(user_id)
    if user_fcm_token is None:
        return
    await asyncio.to_thread(send_push_notification, fcm_token=user_fcm_token, title=message_title, body=message_body)