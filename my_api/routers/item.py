from fastapi import APIRouter, Depends, HTTPException

from database import database
from models import Item

from schemas import ItemRequest, ItemResponse

from utils.auth import get_api_key


router = APIRouter()





@router.get("/items")
async def list_items(api_key: str = Depends(get_api_key)):
    
    query = Item.select()
    return await database.fetch_all(query)
    





@router.post("/items")
async def create_item(item: ItemRequest, api_key: str = Depends(get_api_key)):
    
    query = Item.insert().values(**item.dict())
    last_id = await database.execute(query)
    return {**item.dict(), "id": last_id}
    








@router.get("/items/{id}")
async def get_item(id: int, api_key: str = Depends(get_api_key)):
    
    query = Item.select().where(Item.c.id == id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
    






@router.put("/items/{id}")
async def update_item(id: int, item: ItemRequest, api_key: str = Depends(get_api_key)):
    
    query = Item.select().where(Item.c.id == id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    update_query = Item.update().where(Item.c.id == id).values(**item.dict())
    await database.execute(update_query)
    return {"message": "Updated"}
    






@router.delete("/items/{id}")
async def delete_item(id: int, api_key: str = Depends(get_api_key)):
    
    query = Item.select().where(Item.c.id == id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_query = Item.delete().where(Item.c.id == id)
    await database.execute(delete_query)
    return {"message": "Deleted"}
    



