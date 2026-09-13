import asyncio

from database.recipe_importer import import_recipes

async def main():
    await import_recipes("recipes.json")


if __name__ == "__main__":
    asyncio.run(main())