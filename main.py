from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from api.router import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
    
    
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
