from fastapi import FastAPI

from utils.auth import get_api_key


from database import database

from routers import user, item

app = FastAPI()

# Include routers

app.include_router(user.router)

app.include_router(item.router)


# Startup and shutdown events

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
