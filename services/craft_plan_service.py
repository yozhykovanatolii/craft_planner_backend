from exceptions.access_denied_exception import AccessDeniedException
from exceptions.conflict_exception import RecipeLockedException
from exceptions.resource_not_found_exception import CraftPlanNotFoundException, RecipeNotFoundException
from repositories.craft_plan_repository import CraftPlanRepository
from repositories.recipe_repository import RecipeRepository
from schemas.craft_plan import CraftPlanBaseSchema, CraftPlanInfoSchema
from utils.save_file_parser import parse_player_save_file
from collections import deque


class CraftPlanService:
    def __init__(self, recipe_repository: RecipeRepository, craft_plan_repository: CraftPlanRepository):
        self.__recipe_repository = recipe_repository
        self.__craft_plan_repository = craft_plan_repository    
        
    async def create_craft_plan(self, target_name: str, target_quantity: int, file_bytes, file_path: str, user_id: int):
        player_unlocked_recipes, player_inventory = parse_player_save_file(file_bytes, file_path)
        working_inventory = player_inventory.copy()
        recipe_records = await self.__recipe_repository.get_recipe_graph_by_item_name(target_name)
        if not recipe_records:
            raise RecipeNotFoundException()
        recipe_id = recipe_records['recipe_id']
        recipe_ingredients = recipe_records['ingredients']
        if recipe_id not in player_unlocked_recipes:
            raise RecipeLockedException(recipe_id)
        calculated_ingredients = self.__get_calculated_ingredients(recipe_ingredients, target_quantity)
        calculated_ingredients = self.__check_inventory(calculated_ingredients, working_inventory)
        missing_ingredients = self.__get_missing_ingredients(calculated_ingredients)
        ingredients_existing = {
            ingredient["item_display_name"]: ingredient["inventory_quantity"]
            for ingredient in calculated_ingredients
            if ingredient['inventory_quantity'] > 0
        }
        ingredients_need_craft = {
            ingredient["item_display_name"]: ingredient["missing_quantity"]
            for ingredient in missing_ingredients
        }
        items_need_find = await self.__resolve_crafting_dependencies(missing_ingredients, target_name, working_inventory)
        await self.__craft_plan_repository.create_craft_plan(user_id, target_name, target_quantity, ingredients_existing, ingredients_need_craft, items_need_find)
        
    async def __resolve_crafting_dependencies(self, missing_ingredients, target_item_name, working_inventory):
        items_need_find = {}
        queue = deque()
        for ingredient in missing_ingredients:
            queue.append({
                "item_display_name": ingredient["item_display_name"],
                "missing_quantity": ingredient["missing_quantity"],
                "path": [
                    target_item_name,
                    ingredient["item_display_name"],
                ],
            })
        while queue:
            current = queue.popleft()
            print(current)
            item_display_name = current["item_display_name"]
            missing_quantity = current["missing_quantity"]
            path = current["path"]
            recipe_records = await self.__recipe_repository.get_recipe_graph_by_item_name(item_display_name)
            if not recipe_records:
                items_need_find[item_display_name] = items_need_find.get(item_display_name, 0) + missing_quantity
                continue
            recipe_ingredients = recipe_records['ingredients']
            missing_calculated_ingredients = self.__get_calculated_ingredients(recipe_ingredients, missing_quantity)
            missing_calculated_ingredients = self.__check_inventory(missing_calculated_ingredients, working_inventory)
            missing_sub_ingredients = self.__get_missing_ingredients(missing_calculated_ingredients)
            for ingredient in missing_sub_ingredients:
                ingredient_display_name = ingredient["item_display_name"]
                if ingredient_display_name in path:
                    continue
                new_path = path + [ingredient_display_name]
                queue.append({
                    "item_display_name": ingredient_display_name,
                    "missing_quantity": ingredient["missing_quantity"],
                    "path": new_path,
                })
        return items_need_find
        
    async def delete_craft_plan(self, plan_id: int, user_id: int):
        db_craft_plan = await self.__craft_plan_repository.get_craft_plan_by_id(plan_id)
        if db_craft_plan is None:
            raise CraftPlanNotFoundException()
        if db_craft_plan.user_id != user_id:
            raise AccessDeniedException()
        await self.__craft_plan_repository.delete_craft_plan(db_craft_plan) 
        
    async def get_user_craft_plans(self, user_id: int):
        db_craft_plans = await self.__craft_plan_repository.get_craft_plans_by_user_id(user_id)
        if db_craft_plans is None:
            raise CraftPlanNotFoundException
        return [CraftPlanBaseSchema.model_validate(db_craft_plan) for db_craft_plan in db_craft_plans]
    
    async def get_user_craft_plan(self, user_id: int, plan_id: int):
        db_craft_plan = await self.__craft_plan_repository.get_craft_plan_by_id(plan_id)
        if db_craft_plan is None:
            raise CraftPlanNotFoundException()
        if db_craft_plan.user_id != user_id:
            raise AccessDeniedException()
        return CraftPlanInfoSchema.model_validate(db_craft_plan)
    
    async def recalculate_craft_plan(self, user_id: int, plan_id: int, file_bytes, file_path: str):
        player_inventory = parse_player_save_file(file_bytes, file_path)[1]
        working_inventory = player_inventory.copy()
        db_craft_plan = await self.__craft_plan_repository.get_craft_plan_by_id(plan_id)
        if db_craft_plan is None:
            raise CraftPlanNotFoundException()
        if db_craft_plan.user_id != user_id:
            raise AccessDeniedException()
        recipe_records = await self.__recipe_repository.get_recipe_graph_by_item_name(db_craft_plan.target_item_name)
        if not recipe_records:
            raise RecipeNotFoundException()
        target_item_id = recipe_records['item_id']
        recipe_ingredients = recipe_records['ingredients']
        remaining_quantity = db_craft_plan.target_item_quantity - working_inventory.get(target_item_id, 0)
        if remaining_quantity <= 0:
            db_craft_plan.status = 'Completed'
            await self.__craft_plan_repository.update_craft_plan(db_craft_plan)
            return
        calculated_ingredients = self.__get_calculated_ingredients(recipe_ingredients, db_craft_plan.target_item_quantity)
        calculated_ingredients = self.__check_inventory(calculated_ingredients, working_inventory)
        missing_ingredients = self.__get_missing_ingredients(calculated_ingredients)
        ingredients_existing = {
            ingredient["item_display_name"]: ingredient["inventory_quantity"]
            for ingredient in calculated_ingredients
            if ingredient['inventory_quantity'] > 0
        }
        ingredients_need_craft = {
            ingredient["item_display_name"]: ingredient["missing_quantity"]
            for ingredient in missing_ingredients
        }
        items_need_find = await self.__resolve_crafting_dependencies(missing_ingredients, db_craft_plan.target_item_name, working_inventory)
        db_craft_plan.available_ingredients = ingredients_existing
        db_craft_plan.ingredients_to_craft = ingredients_need_craft
        db_craft_plan.required_components = items_need_find
        await self.__craft_plan_repository.update_craft_plan(db_craft_plan)

    def __check_inventory(self, ingredients: list[dict], player_inventory: dict[str, int]):
        for ingredient in ingredients:
            item_id = ingredient["item_id"]
            required_quantity = ingredient["required_quantity"]
            inventory_quantity = player_inventory.get(item_id, 0)
            used_quantity = min(required_quantity, inventory_quantity)
            ingredient["inventory_quantity"] = inventory_quantity
            ingredient["missing_quantity"] = required_quantity - used_quantity
            player_inventory[item_id] = inventory_quantity - used_quantity
        return ingredients
    
    def __get_calculated_ingredients(self, ingredients: list[dict], target_quantity: int):
        return [
            {
                "item_id": ingredient["item_id"],
                "item_display_name": ingredient["item_display_name"],
                "required_quantity": ingredient["quantity"] * target_quantity,
            }
            for ingredient in ingredients
        ]
        
    def __get_missing_ingredients(self, ingredients: list[dict]):
        return [
            {
                "item_id": ingredient["item_id"],
                "item_display_name": ingredient["item_display_name"],
                "missing_quantity": ingredient["missing_quantity"],
            }
            for ingredient in ingredients
            if ingredient['missing_quantity'] > 0
        ]
    
            