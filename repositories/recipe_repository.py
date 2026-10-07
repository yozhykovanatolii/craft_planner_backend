from neo4j import AsyncSession

class RecipeRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def get_recipe_ingredients_by_item_name(self, item_display_name: str):
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
        
    async def get_dependency_edges_by_item_ids(self, items_ids: list[str]):
        result = await self.__db.run(
            """
            MATCH (start:Item)
            WHERE start.id IN $items_ids
            MATCH p =
                (start)
                ((parent:Item)<-[:PRODUCES]-(recipe:Recipe)-[req:REQUIRES]->(ingredient:Item))+
            UNWIND range(0, size(req) - 1) AS index
            RETURN
                parent[index].id AS parent_item_id,
                parent[index].display_name AS parent_display_name,
                ingredient[index].id AS ingredient_id,
                ingredient[index].display_name AS ingredient_display_name,
                req[index].count AS quantity
            """,
            items_ids=items_ids
        )
        records = [record async for record in result]
        return records
            
        