from typing import Annotated
from api.dependencies import get_craft_plan_repository, get_recipe_repository
from config import settings
from taskiq_redis import RedisStreamBroker
from taskiq import TaskiqDepends
from repositories.recipe_repository import RecipeRepository
from services.craft_plan_service import CraftPlanService

broker = RedisStreamBroker(
    url=settings.redis_url,
)

def get_taskiq_craft_plan_service(recipe_repository: Annotated[RecipeRepository, TaskiqDepends(get_recipe_repository)], craft_plan_repository: Annotated[RecipeRepository, TaskiqDepends(get_craft_plan_repository)]):
    return CraftPlanService(recipe_repository, craft_plan_repository)

@broker.task
async def generate_craft_plan(craft_plan_service: Annotated[RecipeRepository, TaskiqDepends(get_taskiq_craft_plan_service)]):
    pass