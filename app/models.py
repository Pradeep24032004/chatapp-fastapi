from pydantic import BaseModel, EmailStr
#from typing import Optional
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class MessageCreate(BaseModel):
   
    content: str
"""
class MessageOut(BaseModel):
    id: str
    content: str
    timestamp: datetime
    user_id: str
    username: str
   """ 
   # Your existing models...

class MessageOut(BaseModel):
    id: str
    content: str
    username: str
    user_id: str
    timestamp: datetime
    email: Optional[str] = None  # Add this field

    class Config:
        from_attributes = True 
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: str | None = None