import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from PIL import Image
from io import BytesIO
from datetime import datetime
import face_recognition
import os
import math
import cv2

router = APIRouter()

# ----------------------Nhận diện khuôn mặt----------------------
known_faces_cache = {}

class FaceRecognition:
    def __init__(self, face_id: str):
        self.face_id = face_id
        self.known_encodings, self.known_names = self.load_known_faces()

    def load_known_faces(self):
        known_encodings = []
        known_names = []

        folder_path = f"dataset/detect_face/{self.face_id}"
        if not os.path.exists(folder_path):
            print(f"⚠️ Folder {folder_path} không tồn tại.")
            return known_encodings, known_names

        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            print(f"📥 Loading image: {image_path}")
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(filename)

        return known_encodings, known_names

    # def recognize_faces(self, frame):
    #     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #     rgb_small_frame = small_frame[:, :, ::-1]
    #     face_locations = face_recognition.face_locations(rgb_small_frame)
    #     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    #     face_names = []

    #     for face_encoding in face_encodings:
    #         matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
    #         face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)

    #         name = "Unknown"
    #         confidence = "Unknown"

    #         if len(face_distances) > 0:
    #             best_match_index = np.argmin(face_distances)
    #             if matches[best_match_index]:
    #                 name = self.known_names[best_match_index]
    #                 confidence = face_confidence(face_distances[best_match_index])

    #         face_names.append(f"{name} ({confidence})")

    #     return face_names
    def recognize_faces(self, frame):
        rgb_small_frame = frame[:, :, ::-1]
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame, dtype=np.uint8)
        height, width, _ = rgb_small_frame.shape

        face_locations = face_recognition.face_locations(rgb_small_frame)
        print("face_locations:", face_locations)
        print("rgb_small_frame shape:", rgb_small_frame.shape, "dtype:", rgb_small_frame.dtype)

        if not face_locations:
            return []

        # Lọc các face_locations nằm ngoài biên ảnh
        valid_face_locations = []
        for (top, right, bottom, left) in face_locations:
            if 0 <= top < bottom <= height and 0 <= left < right <= width:
                valid_face_locations.append((top, right, bottom, left))
            else:
                print(f"Bỏ qua face_location ngoài biên: {(top, right, bottom, left)}")

        if not valid_face_locations:
            return []

        face_encodings = face_recognition.face_encodings(rgb_small_frame, valid_face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)

            name = "Unknown"
            confidence = "Unknown"

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

            face_names.append(f"{name} ({confidence})")

        return face_names

# WebSocket endpoint 1: Nhận diện khuôn mặt
@router.websocket("/ws/face_recognition/{face_id}")
async def ws_face_recognition(websocket: WebSocket, face_id: str):
    await websocket.accept()

    if face_id not in known_faces_cache:
        print(f"🆔 Nhận kết nối với face_id: {face_id}")  # Thêm dòng này để kiểm tra
        face_recognition_instance = FaceRecognition(face_id)
        known_faces_cache[face_id] = face_recognition_instance
    else:
        face_recognition_instance = known_faces_cache[face_id]

    try:
        while True:
            data = await websocket.receive_bytes()

            img = Image.open(BytesIO(data))
            # img_rgb = img.convert("RGB")
            # img_rgb.save("/Users/macbook/Desktop/PBL5/PBL5/be/debug/debug_after_rgb.jpg")
            # img.save("/Users/macbook/Desktop/PBL5/PBL5/be/debug/debug2.jpg")

            frame = np.array(img.convert("RGB"))

            # frame.save("/Users/macbook/Desktop/PBL5/PBL5/be/debug/debug3.jpg")

            face_names = face_recognition_instance.recognize_faces(frame)

            await websocket.send_text(", ".join(face_names) or "Không nhận diện được khuôn mặt.")

    except WebSocketDisconnect:
        print("❌ WebSocket client (recognition) disconnected.")

# WebSocket endpoint 2: Quét và lưu khuôn mặt
@router.websocket("/ws/get_face/{face_id}") 
async def ws_get_face(websocket: WebSocket, face_id: str):
    await websocket.accept()
    print("🔌 Client connected to face scanning.")

    # ----------------------Quét khuôn mặt----------------------
    base_dir = os.path.dirname(__file__)
    cascade_path = os.path.join(base_dir, "haarcascade_frontalface_default.xml")
    face_detector = cv2.CascadeClassifier(cascade_path)

    save_dir = f"dataset/detect_face/{face_id}"
    os.makedirs(save_dir, exist_ok=True)

    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                print("⚠️ Không thể giải mã ảnh.")
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                filename = f"{save_dir}/{face_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
                with open(filename, "wb") as f: 
                    f.write(data)
                print(f"📸 Khuôn mặt được lưu: {filename}")
    except WebSocketDisconnect:
        print("❌ WebSocket client (get face) disconnected.")
