from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from drivers.evdev_driver import EvdevDriver
import socket
import qrcode
import uvicorn

def get_device_ip():
    s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def show_qr(url: str):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.print_ascii(invert=True)

    print(f"\nAtau bisa klik :{url}\n")

if __name__ == "__main__":
    ip = get_device_ip()
    url = f"http://{ip}:8000"

    show_qr(url)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    
        


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


