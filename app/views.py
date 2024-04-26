from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from sqlalchemy.orm import Session
import aioredis
from typing import List, Dict

from settings.database import get_db, User, Group

router = APIRouter(tags=["WebSocket"])

redis = aioredis.from_url("redis://redis:6379", decode_responses=True)

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, group_id: int):
        await websocket.accept()
        if group_id not in self.connections:
            self.connections[group_id] = []
        self.connections[group_id].append(websocket)

    def disconnect(self, websocket: WebSocket, group_id: int):
        self.connections[group_id].remove(websocket)
        if not self.connections[group_id]:
            del self.connections[group_id]

    async def send_message(self, message: str, group_id: int):
        for connection in self.connections.get(group_id, []):
            await connection.send_text(message)

class EnhancedConnectionManager(ConnectionManager):
    async def send_message(self, message: str, group_id: int):
        if self.connections.get(group_id):
            await super().send_message(message, group_id)
        else:
            # Store the message in Redis if no users are connected
            await redis.rpush(f"group:{group_id}:messages", message)

    async def retrieve_messages(self, group_id: int):
        return await redis.lrange(f"group:{group_id}:messages", 0, -1)

    async def clear_messages(self, group_id: int):
        await redis.delete(f"group:{group_id}:messages")

manager = EnhancedConnectionManager()

@router.websocket("/messaging/{group_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, group_id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    group = db.query(Group).filter(Group.id == group_id).first()
    if not user or not group or user not in group.users:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, group_id)
    try:
        offline_messages = await manager.retrieve_messages(group_id)
        for message in offline_messages:
            await websocket.send_text(message)
        await manager.clear_messages(group_id)

        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"User {user_id} in group {group_id} says: {data}", group_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, group_id)
