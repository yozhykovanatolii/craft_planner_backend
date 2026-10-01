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
        
    async def get_items_using_resource(self, resource_name: str):
        result = await self.__db.run(
            """
            MATCH (r:Recipe)-[:REQUIRES]->
                (resource:Item {display_name: $display_name})
            MATCH (r)-[:PRODUCES]->(item:Item)
            RETURN DISTINCT
                    item.id AS item_id,
                    item.display_name AS item_display_name
            """,
            display_name=resource_name
        )
        records = [record async for record in result]
        if not records:
            return None
        return [
                {
                    "item_id": record["item_id"],
                    "display_name": record["item_display_name"],
                }
                for record in records
        ]
        
    async def get_item_ids_by_names(self, resource_name: str, target_name: str):
        result = await self.__db.run(
            """
            MATCH (start:Item {display_name: $resource_name})
            MATCH (target:Item {display_name: $target_name}) 
            RETURN start.id as start_id, target.id as target_id
            """,
            resource_name=resource_name,
            target_name=target_name
        )
        record = await result.single()
        if record is None:
            return None
        return {
            "start_id": record["start_id"],
            "target_id": record["target_id"]
        }
            
        