from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from drivers.evdev_driver import EvdevDriver
import socket
import qrcode
import uvicorn
import time

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
app.mount("/static", StaticFiles(directory="static"), name="static")
driver = EvdevDriver()

def process_voice_command(text: str) -> dict:
    t = text.lower().strip()
    print(f"[VOICE] Diterima perintah suara: '{text}'")

    # 1. Double Click
    if any(k in t for k in ["dobel klik", "double click", "klik dua kali"]):
        driver.click("left", "click")
        time.sleep(0.1)
        driver.click("left", "click")
        return {"action": "double_click", "message": "Double Click"}

    # 2. Klik Kanan
    if any(k in t for k in ["klik kanan", "right click"]):
        driver.click("right", "click")
        return {"action": "right_click", "message": "Klik Kanan"}

    # 3. Klik Kiri
    if any(k in t for k in ["klik kiri", "left click", "klik", "click"]):
        driver.click("left", "click")
        return {"action": "left_click", "message": "Klik Kiri"}

    # 4. Scroll
    if any(k in t for k in ["scroll atas", "scroll ke atas", "scroll up", "gulir atas", "geser atas", "ke atas", "naik"]):
        driver.scroll(5)
        return {"action": "scroll_up", "message": "Scroll ke Atas"}

    if any(k in t for k in ["scroll bawah", "scroll ke bawah", "scroll down", "gulir bawah", "geser bawah", "ke bawah", "turun"]):
        driver.scroll(-5)
        return {"action": "scroll_down", "message": "Scroll ke Bawah"}

    # 5. Kontrol Presentasi
    if any(k in t for k in ["mulai canva", "start canva", "canva"]):
        driver.key_press("start_canva")
        return {"action": "start_canva", "message": "Mulai Presentasi (Canva)"}

    if any(k in t for k in ["mulai ppt", "start ppt", "powerpoint", "ppt", "f5"]):
        driver.key_press("start_ppt")
        return {"action": "start_ppt", "message": "Mulai Presentasi (PPT)"}

    if any(k in t for k in ["mulai", "start", "tayang", "tampilkan", "play"]):
        driver.key_press("start_canva")
        return {"action": "start", "message": "Mulai Presentasi"}

    if any(k in t for k in ["keluar", "berhenti", "stop", "tutup", "selesai", "exit", "escape", "esc"]):
        driver.key_press("exit")
        return {"action": "exit", "message": "Stop / Keluar (Esc)"}

    if any(k in t for k in ["hitam", "blank", "gelap", "black", "layar hitam"]):
        driver.key_press("black")
        return {"action": "black", "message": "Layar Hitam (B)"}

    # 6. Navigasi Slide
    if any(k in t for k in ["lanjut", "selanjutnya", "next", "maju", "berikutnya", "kanan", "depan"]):
        driver.key_press("next")
        return {"action": "next", "message": "Slide Selanjutnya (Next)"}

    if any(k in t for k in ["sebelumnya", "kembali", "mundur", "prev", "previous", "balik", "kiri", "belakang"]):
        driver.key_press("prev")
        return {"action": "prev", "message": "Slide Sebelumnya (Prev)"}

    return {"action": "unknown", "message": f"Perintah '{text}' tidak dikenali"}

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data: dict = await websocket.receive_json()
            msg_type = data.get("type")
            if msg_type == "move":
                driver.move(data.get("dx", 0), data.get("dy", 0))
            elif msg_type == "scroll":
                driver.scroll(data.get("dy", 0))
            elif msg_type == "click":
                driver.click(data.get("button"), data.get("action", "click"))
            elif msg_type == "key":
                driver.key_press(data.get("key_name"))
            elif msg_type == "voice":
                text = data.get("text", "")
                result = process_voice_command(text)
                await websocket.send_json({
                    "type": "voice_ack",
                    "text": text,
                    "action": result.get("action"),
                    "message": result.get("message")
                })

    except WebSocketDisconnect:
        print("Layanan websocket dihentikan")


