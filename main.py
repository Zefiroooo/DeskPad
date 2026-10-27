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
            if data.get("type") == "move" :
                driver.move(data.get("dx", 0), data.get("dy", 0))
            elif data.get("type") == "scroll":
                driver.scroll(data.get("dy", 0))
            elif data.get("type") == "click":
                driver.click(data.get("button"), data.get("action"))
            elif data.get("type") == "key":
                driver.key_press(data.get("key_name"))


    except WebSocketDisconnect:
        print("Layanan websocket dihentikan")


