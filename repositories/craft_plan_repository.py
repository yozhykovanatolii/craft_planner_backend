from sqlalchemy.ext.asyncio import AsyncSession
from models import CraftPlan

class CraftPlanRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def create_craft_plan(self, user_id, target_item_name, available_ingredients, ingredients_to_craft, required_components):
        db_craft_plan = CraftPlan(user_id = user_id, target_item_name = target_item_name, available_ingredients = available_ingredients, ingredients_to_craft = ingredients_to_craft, required_components = required_components)
        self.__db.add(db_craft_plan)
        await self.__db.commit()
        await self.__db.refresh(db_craft_plan)
        return db_craft_plan