from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String,unique=True, index=True,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    description = Column(String)
    done_by = Column(DateTime)
    is_completed = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    owner_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User",back_populates="todos")
