import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.websocket_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/socket")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()

  init_data = await websocket.receive_text()
  init_payload = json.loads(init_data)
  username = init_payload.get("username", "Anonymous")

  await manager.connect(websocket, username)

  try:
    while True:
      data = await websocket.receive_text()
      await manager.broadcast(data, sender=username)
  except WebSocketDisconnect:
    manager.disconnect(websocket)
