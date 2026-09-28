from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import CraftPlan

class CraftPlanRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def create_craft_plan(self, user_id, target_item_name, target_item_quantity, available_ingredients, ingredients_to_craft, required_components):
        db_craft_plan = CraftPlan(user_id = user_id, target_item_name = target_item_name, target_item_quantity = target_item_quantity, available_ingredients = available_ingredients, ingredients_to_craft = ingredients_to_craft, required_components = required_components)
        self.__db.add(db_craft_plan)
        await self.__db.commit()
        await self.__db.refresh(db_craft_plan)
        return db_craft_plan
    
    async def get_craft_plan_by_id(self, craft_plan_id: int):
        return await self.__db.get(CraftPlan, craft_plan_id)
    
    async def delete_craft_plan(self, db_craft_plan: CraftPlan):
        await self.__db.delete(db_craft_plan)
        await self.__db.commit()
        
    async def get_craft_plans_by_user_id(self, user_id: int):
        query = select(CraftPlan).where(CraftPlan.user_id == user_id)
        result = await self.__db.execute(query)
        return result.scalars().all()
    
    async def update_craft_plan(self, db_craft_plan_new: CraftPlan):
        await self.__db.commit()
        await self.__db.refresh(db_craft_plan_new)