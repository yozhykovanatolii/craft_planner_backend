from neo4j import AsyncGraphDatabase
from config import settings

URI = settings.neo4j_uri
AUTH = (settings.neo4j_username, settings.neo4j_password)

driver = AsyncGraphDatabase.driver(URI, auth=AUTH)

async def connect_neo4j():
    await driver.verify_connectivity()
    
async def close_neo4j():
    await driver.close()
    
async def create_constraints_neo4j():
    async with driver.session() as session:
        await session.run("""
            CREATE CONSTRAINT recipe_id_unique IF NOT EXISTS
            FOR (r:Recipe)
            REQUIRE r.id IS UNIQUE
        """)
        await session.run("""
            CREATE CONSTRAINT item_id_unique IF NOT EXISTS
            FOR (i:Item)
            REQUIRE i.id IS UNIQUE
        """)
        
async def get_neo4j_session():
    async with driver.session() as session:
        yield session