from fastapi import FastAPI
from app.db.database import engine, create_tables
from app.db import models
from app.routes import user, todo
from app.ws import manager, websocket_endpoint  # ✅ import here

app = FastAPI()

# Create all tables
models.SQLModel.metadata.create_all(bind=engine)
create_tables()

# Include routers
app.include_router(user.router)
app.include_router(todo.router)

# Add WebSocket route manually (important!)
app.add_api_websocket_route("/ws/todos", websocket_endpoint)

# Test endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Todo App"}