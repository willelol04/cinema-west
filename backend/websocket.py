from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.screening_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, screening_id: int):
        await websocket.accept()

        if screening_id not in self.screening_connections:
            self.screening_connections[screening_id] = [websocket]
        else:
            self.screening_connections[screening_id].append(websocket)


    def disconnect(self, websocket: WebSocket, screening_id: int):
        self.screening_connections[screening_id].remove(websocket)

    async def send_personal_json(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast_screening_json(self, screening_id: int, booked_seat_ids):
        print("\n\n\n\n\n")
        print(screening_id)
        print("\n\n\n\n\n")

        if screening_id in self.screening_connections:
            disconnected_connections = []
            for connection in self.screening_connections[screening_id]:
                try:
                    await connection.send_json({"type":"update", "screening_id": screening_id, "booked_seat_ids": booked_seat_ids})
                except Exception:
                    disconnected_connections.append(connection)

            for conn in disconnected_connections:
                self.disconnect(conn, screening_id)
