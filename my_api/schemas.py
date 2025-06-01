from pydantic import BaseModel


class ItemRequest(BaseModel):
    
    name: str
    
    price: float
    

class ItemResponse(BaseModel):
    
    id: int
    
    name: str
    
    price: float
    

class UserRequest(BaseModel):
    
    username: str
    
    email: str
    

class UserResponse(BaseModel):
    
    id: int
    
    username: str
    
    email: str
    
