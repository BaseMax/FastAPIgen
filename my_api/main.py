from fastapi import FastAPI

from utils.auth import get_api_key


from database import database

from routers import user, item
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


# Include routers

app.include_router(user.router)

app.include_router(item.router)
