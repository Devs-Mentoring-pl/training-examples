from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="WebSocket Chat")


class ConnectionManager:
    """Zarządza aktywnymi połączeniami WebSocket."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Akceptuje nowe połączenie i dodaje do listy."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Usuwa połączenie z listy."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Wysyła wiadomość do wszystkich podłączonych klientów."""
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """Prosty echo – odsyła to, co otrzyma."""
    await ws.accept()

    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"Echo: {data}")
    except Exception:
        print("Klient się rozłączył")


@app.websocket("/ws/chat/{username}")
async def chat_endpoint(websocket: WebSocket, username: str):
    """Endpoint czatu – obsługuje jednego klienta."""
    await manager.connect(websocket)
    await manager.broadcast(f"📢 {username} dołączył do czatu!")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"📢 {username} opuścił czat")
