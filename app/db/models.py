from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,List
from datetime import datetime

class User(SQLModel,table=True):
    __tablename__="Users"
    id:Optional[int] = Field(default=None,primary_key=True,index=True)
    username:str = Field(index=True,nullable=False,unique=True)
    email:str=Field(nullable==False)
    password:str=Field(nullable=False)

    todos:List["Todo"]=Relationship(back_populates="owner")

class Todo(SQLModel,table=True):
    __tablename__="todos"

    id:Optional[int] = Field(default=None,primary_key=True,index=True)
    title: str =Field(nullable=False)
    description: Optional[str] = None
    done_by: Optional[datetime] = None
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    owner_id: int = Field(foreign_key="users.id")
    owner: Optional[User] = Relationship(back_populates="todos")

