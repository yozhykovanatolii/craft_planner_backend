import json
from database.neo4j import driver


async def import_recipes(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        recipes_data = json.load(file)
    recipes = [
        {
            "id": recipe["Id"],
            "creates_item_id": recipe["CreatesItemId"],
            "produces_count": recipe["Count"],
            "ingredients": [
                {
                    "item_id": ingredient["ItemId"],
                    "count": ingredient["Count"],
                }
                for ingredient in recipe.get("Ingredients", [])
            ],
        }
        for recipe in recipes_data['Recipes']
    ]
    items = [
        {
            "id": item["Id"],
            "display_name": item["DisplayName"],
        }
        for item in recipes_data["Items"]
    ]
    async with driver.session() as session:
        await session.run(
            """
            UNWIND $items AS item
            MERGE (i:Item {id: item.id})

            SET i.display_name = item.display_name
            """,
            items=items,
        )
        await session.run(
            """
            UNWIND $recipes AS recipe

            MERGE (r:Recipe {id: recipe.id})
            MERGE (item:Item {id: recipe.creates_item_id})

            MERGE (r)-[p:PRODUCES]->(item)
            SET p.count = recipe.produces_count
            """,
            recipes=recipes,
        )
        await session.run(
            """
            UNWIND $recipes AS recipe
            UNWIND recipe.ingredients AS ingredient

            MERGE (r:Recipe {id: recipe.id})
            MERGE (item:Item {id: ingredient.item_id})

            MERGE (r)-[req:REQUIRES]->(item)
            SET req.count = ingredient.count
            """,
            recipes=recipes,
        )