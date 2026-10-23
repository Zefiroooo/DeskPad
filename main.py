from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from drivers.evdev_driver import EvdevDriver


app = FastAPI()
driver = EvdevDriver()

@app.get("/")
async def home():
    return FileResponse("static/index.html")



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data: dict = await websocket.receive_json()
            if data.get("type") == "move":
                driver.move(data.get("dx", 0), data.get("dy", 0))
    except WebSocketDisconnect:
        print("Layanan websocket dihentikan")


