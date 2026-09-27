from neo4j import AsyncSession

class RecipeRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def get_recipe_graph_by_item_name(self, item_display_name: str):
        result = await self.__db.run(
            """
            MATCH (r:Recipe)-[:PRODUCES]->
                (i:Item {display_name: $display_name})
            MATCH (r)-[req:REQUIRES]->(ingredient:Item)
            RETURN r.id AS recipe_id,
                i.id AS item_id,
                ingredient.id AS ingredient_id,
                ingredient.display_name AS ingredient_display_name,
                req.count AS quantity
            """,
            display_name=item_display_name
        )
        records = [record async for record in result]
        if not records:
            return None
        return {
            "recipe_id": records[0]["recipe_id"],
            "item_id": records[0]["item_id"],
            "ingredients": [
                {
                    "item_id": record["ingredient_id"],
                    "item_display_name": record["ingredient_display_name"],
                    "quantity": record["quantity"],
                }
                for record in records
            ]
        }
            
        