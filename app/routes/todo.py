from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db import models, database
from app import auth
from typing import List
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from datetime import datetime
from app.schemas import schemas
from app.ws import manager
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/todos", tags=["todos"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    statement = select(models.User).where(models.User.username == username)
    user = db.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=schemas.TodoOut)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    new_todo = models.Todo(**todo.dict(), user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    asyncio.create_task(manager.broadcast(f"Todo created:{new_todo.task}"))
    return new_todo

@router.get("/", response_model=List[schemas.TodoOut])
def read_todos(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Todo).where(models.Todo.user_id == current_user.id)
    todos = db.exec(statement).all()
    return todos


@router.put("/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == todo_id, models.Todo.user_id == current_user.id)
    db_todo = db.exec(statement).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == todo_id, models.Todo.user_id == current_user.id)
    db_todo = db.exec(statement).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"}

@router.get("/grouped")
def get_grouped_todos(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Todo).where(models.Todo.user_id == current_user.id)
    todos = db.exec(statement).all()
    now = datetime.utcnow()

    completed = []
    to_be_done = []
    time_elapsed = []
    for todo in todos:
        if todo.is_completed:
            completed.append(todo)
        elif todo.done_by < now:
            time_elapsed.append(todo)
        else:
            to_be_done.append(todo)

    return {
        "completed": completed,
        "to_be_done": to_be_done,
        "time_elapsed": time_elapsed
    }