from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from api.router import api_router
from exceptions.error_handlers import register_error_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
    
    
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
register_error_handlers(app)