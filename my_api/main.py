from fastapi import FastAPI

from utils.auth import get_api_key


from database import database

from routers import item, user

app = FastAPI()

# Include routers

app.include_router(item.router)

app.include_router(user.router)


# Startup and shutdown events

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
