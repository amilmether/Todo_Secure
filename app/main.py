from fastapi import FastAPI
from app.db.database import engine,create_tables
from app.db import models
from app.routes import user,todo

app = FastAPI()
models.SQLModel.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(todo.router)
create_tables()
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Todo App"}