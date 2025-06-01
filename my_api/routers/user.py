from fastapi import APIRouter, Depends, HTTPException

from database import database
from models import User

from schemas import UserRequest, UserResponse

from utils.auth import get_api_key


router = APIRouter()





@router.get("/users")
async def list_users(api_key: str = Depends(get_api_key)):
    
    query = User.select()
    return await database.fetch_all(query)
    





@router.post("/users")
async def create_user(user: UserRequest, api_key: str = Depends(get_api_key)):
    
    query = User.insert().values(**user.dict())
    last_id = await database.execute(query)
    return {**user.dict(), "id": last_id}
    








@router.get("/users/{id}")
async def get_user(id: int, api_key: str = Depends(get_api_key)):
    
    query = User.select().where(User.c.id == id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
    






@router.put("/users/{id}")
async def update_user(id: int, user: UserRequest, api_key: str = Depends(get_api_key)):
    
    query = User.select().where(User.c.id == id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    update_query = User.update().where(User.c.id == id).values(**user.dict())
    await database.execute(update_query)
    return {"message": "Updated"}
    






@router.delete("/users/{id}")
async def delete_user(id: int, api_key: str = Depends(get_api_key)):
    
    query = User.select().where(User.c.id == id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_query = User.delete().where(User.c.id == id)
    await database.execute(delete_query)
    return {"message": "Deleted"}
    



