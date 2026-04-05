from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import cv2
import threading
import time

router = APIRouter()

cap = None
camera_active = False
lock = threading.Lock()

def generate_frames():
    global cap, camera_active
    while camera_active:
        with lock:
            if cap is None or not cap.isOpened():
                break

            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@router.get("/video_feed")
async def video_feed():
    global cap, camera_active
    with lock:
        if cap:
            cap.release()
            cap = None
        cap = cv2.VideoCapture(0)
        camera_active = True
        time.sleep(1)
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/stop_camera")
async def stop_camera():
    global cap, camera_active
    with lock:
        camera_active = False
        if cap:
            cap.release()
            cap = None
    return {"message": "Camera stopped"}
