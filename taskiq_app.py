from typing import Annotated
from api.dependencies import get_craft_plan_repository, get_recipe_repository
from config import settings
from taskiq_redis import RedisStreamBroker
from taskiq import TaskiqDepends
from repositories.craft_plan_repository import CraftPlanRepository
from repositories.recipe_repository import RecipeRepository
from services.craft_plan_service import CraftPlanService

broker = RedisStreamBroker(
    url=settings.redis_url,
)

def get_taskiq_craft_plan_service(recipe_repository: Annotated[RecipeRepository, TaskiqDepends(get_recipe_repository)], craft_plan_repository: Annotated[CraftPlanRepository, TaskiqDepends(get_craft_plan_repository)]):
    return CraftPlanService(recipe_repository, craft_plan_repository)

@broker.task
async def generate_craft_plan(target_name: str, target_quantity: int, user_id: int, player_inventory, recipe_ingredients, target_item_id, craft_plan_service: Annotated[CraftPlanService, TaskiqDepends(get_taskiq_craft_plan_service)]):
    await craft_plan_service.calculate_craft_plan(target_name, target_quantity, user_id, player_inventory, recipe_ingredients, target_item_id)
    
@broker.task
async def recalculate_plan(plan_id, player_inventory, recipe_ingredients, target_item_id, craft_plan_service: Annotated[CraftPlanService, TaskiqDepends(get_taskiq_craft_plan_service)]):
    await craft_plan_service.recalculate_craft_plan(plan_id, player_inventory, recipe_ingredients, target_item_id)