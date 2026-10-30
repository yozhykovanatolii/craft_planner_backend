from contextlib import asynccontextmanager
from fastapi import FastAPI
from clients.firebase_client import init_firebase_sdk
from database.postgresql import init_postgresql_db
from database import neo4j
from api.router import api_router
from exceptions.error_handlers import register_error_handlers
from taskiq_app import broker


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_firebase_sdk()
    await broker.startup()
    await init_postgresql_db()
    await neo4j.connect_neo4j()
    await neo4j.create_constraints_neo4j()
    yield
    await neo4j.close_neo4j()
    await broker.shutdown()
    
    
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
register_error_handlers(app)