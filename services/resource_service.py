from exceptions.conflict_exception import RecipeLockedException
from exceptions.recipe_not_found_exception import RecipeNotFoundException
from repositories.recipe_repository import RecipeRepository
from utils.save_file_parser import parse_player_save_file


class ResourceService:
    def __init__(self, recipe_repository: RecipeRepository):
        self.__recipe_repository = recipe_repository
        
    async def create_resource_plan(self, target_name: str, target_quantity: int, file_bytes, file_path: str):
        player_unlocked_recipes, player_inventory = parse_player_save_file(file_bytes, file_path)
        recipe_records = await self.__recipe_repository.get_recipe_graph_by_item_name(target_name)
        if not recipe_records:
            raise RecipeNotFoundException()
        recipe_id = recipe_records['recipe_id']
        recipe_ingredients = recipe_records['ingredients']
        if recipe_id not in player_unlocked_recipes:
            raise RecipeLockedException(recipe_id)
        calculated_ingredients = [
            {
                "item_id": ingredient["item_id"],
                "quantity": ingredient["quantity"] * target_quantity,
            }
            for ingredient in recipe_ingredients
        ]
        return recipe_records