from neo4j import AsyncSession

class ItemRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def get_items_by_resource_name(self, resource_name: str):
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
        
    async def get_items_by_required_item_id(self, item_id: str):
        result = await self.__db.run(
            """
            MATCH (r:Recipe)-[:REQUIRES]->
                (resource:Item {id: $item_id})
            MATCH (r)-[:PRODUCES]->(item:Item)
            RETURN DISTINCT
                    item.id AS item_id,
                    item.display_name AS item_display_name
            """,
            item_id=item_id
        )
        records = [record async for record in result]
        return [
                {
                    "item_id": record["item_id"],
                    "display_name": record["item_display_name"],
                }
                for record in records
        ]