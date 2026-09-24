from exceptions.conflict_exception import RecipeLockedException
from exceptions.recipe_not_found_exception import RecipeNotFoundException
from repositories.recipe_repository import RecipeRepository
from utils.save_file_parser import parse_player_save_file
from collections import deque


class ResourceService:
    def __init__(self, recipe_repository: RecipeRepository):
        self.__recipe_repository = recipe_repository
        
    async def create_resource_plan(self, target_name: str, target_quantity: int, file_bytes, file_path: str):
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
        items_need_find = {}
        queue = deque()
        for ingredient in missing_ingredients:
            queue.append({
                "item_display_name": ingredient["item_display_name"],
                "missing_quantity": ingredient["missing_quantity"],
                "path": [
                    target_name,
                    ingredient["item_display_name"],
                ],
            })
        print(queue)
        while queue:
            current = queue.popleft()
            print(current)
            item_display_name = current["item_display_name"]
            missing_quantity = current["missing_quantity"]
            path = current["path"]
            print("\nCURRENT:", item_display_name, missing_quantity)
            print("PATH:", path)
            recipe_records = await self.__recipe_repository.get_recipe_graph_by_item_name(item_display_name)
            print("RECIPE:", recipe_records)
            if not recipe_records:
                print(f"SKIP / NO RECIPE: {item_display_name}")
                print(
                    "ADD TO TOTALS:",
                    item_display_name,
                    missing_quantity,
                    "PATH:",
                    path,
                )
                items_need_find[item_display_name] = items_need_find.get(item_display_name, 0) + missing_quantity
                print("TOTALS:", items_need_find)
                continue
            recipe_ingredients = recipe_records['ingredients']
            missing_calculated_ingredients = self.__get_calculated_ingredients(recipe_ingredients, missing_quantity)
            missing_calculated_ingredients = self.__check_inventory(missing_calculated_ingredients, working_inventory)
            missing_sub_ingredients = self.__get_missing_ingredients(missing_calculated_ingredients)
            print("NEW MISSING:", missing_sub_ingredients)
            for ingredient in missing_sub_ingredients:
                ingredient_display_name = ingredient["item_display_name"]
                if ingredient_display_name in path:
                    print("CYCLE:", path + [ingredient_display_name])
                    continue
                new_path = path + [ingredient_display_name]
                queue.append({
                    "item_display_name": ingredient_display_name,
                    "missing_quantity": ingredient["missing_quantity"],
                    "path": new_path,
                })
                print(
                    "ADDED:",
                    ingredient_display_name,
                    "PATH:",
                    new_path,
                )
            print("QUEUE:", list(queue))
            
        return ingredients_need_craft 
    
    
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
    
            