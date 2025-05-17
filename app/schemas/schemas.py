from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional,List
class UserCreate(BaseModel):
    username: str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TodoBase(BaseModel):
    title:str
    description:Optional[str] = None
    done_by:datetime
class TodoCreate(TodoBase):
    pass
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description:Optional[str] = None
    done_by:Optional[datetime] = None
    is_completed:bool = False

class TodoOut(TodoBase):
    id:int
    is_completed:bool
    created_at:datetime

    class Config:
        orm_mode = True