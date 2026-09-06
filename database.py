from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    import models
    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)
    
async def get_db():
    async with async_session_maker() as session:
        yield session