from pydantic import BaseModel


class ItemRequest(BaseModel):
    
    name: string
    
    price: float
    

class ItemResponse(BaseModel):
    
    id: integer
    
    name: string
    
    price: float
    

class UserRequest(BaseModel):
    
    username: string
    
    email: string
    

class UserResponse(BaseModel):
    
    id: integer
    
    username: string
    
    email: string
    
