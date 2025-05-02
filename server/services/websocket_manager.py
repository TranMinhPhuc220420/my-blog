from fastapi import WebSocket

class Client:
    def __init__(self, websocket: WebSocket, username: str):
        self.websocket = websocket
        self.username = username
        
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[Client] = []

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(Client(websocket, username))

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [
            client for client in self.active_connections if client.websocket != websocket
        ]

    async def broadcast(self, message: str, sender: str):
        for client in self.active_connections:
            await client.websocket.send_text(f"{sender}: {message}")