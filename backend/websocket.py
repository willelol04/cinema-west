from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.screening_connections: dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        screening_id = int(websocket.path_params['screening_id'])
        if screening_id not in self.screening_connections:
            self.screening_connections[screening_id] = [websocket]
        else:
            self.screening_connections[screening_id].append(websocket)


    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.screening_connections[int(websocket.path_params['screening_id'])].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_json(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    async def broadcast_screening_json(self, screening_id: int, data: dict):
        print("\n\n\n\n\n")
        print(screening_id)
        print("\n\n\n\n\n")
        if(screening_id in self.screening_connections):
            for connection in self.screening_connections[screening_id]:
                await connection.send_json(data)
