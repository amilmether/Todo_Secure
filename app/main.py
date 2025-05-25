from fastapi import FastAPI
from app.db.database import engine, create_tables
from app.db import models
from app.routes import user, todo
from app.ws import ws_routes
app = FastAPI()

# Create all tables
models.SQLModel.metadata.create_all(bind=engine)
create_tables()

# Include routers
app.include_router(user.router)
app.include_router(todo.router)
app.include_router(ws_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Todo App"}