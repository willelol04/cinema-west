from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_json(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_seats_json(self, screening_id, data: dict):
        print("\n\n\n\n\n")
        print(screening_id)
        print("\n\n\n\n\n")
        for connection in self.active_connections:
            if(connection.path_params["screening_id"] == str(screening_id)):
                print("\n\n\n\n\n", dir(connection), "\n\n\n\n\n")
                print(connection.path_params["screening_id"])
                await connection.send_json(data)
        