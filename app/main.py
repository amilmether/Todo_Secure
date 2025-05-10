from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import user
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router)
# app.include_router(todo.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Todo App"}