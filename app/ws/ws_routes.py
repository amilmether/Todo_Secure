# app/ws/ws_routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
from app.db import database, models
from sqlmodel import Session, select
import os
from dotenv import load_dotenv
from app.ws.manager import manager

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()

@router.websocket("/ws/todos")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if token is None:
        await websocket.close(code=1008)
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    with Session(database.engine) as db:
        user = db.exec(select(models.User).where(models.User.username == username)).first()
        if not user:
            await websocket.close(code=1008)
            return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
