from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import cv2
import threading
import time

router = APIRouter()

cap = None
camera_active = False
lock = threading.Lock()
branch_1 = None

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


