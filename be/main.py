from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import threading
import time
from app.routers import detect_face
from app.routers import face_recognize
from app.routers import camera
from app.routers import auth
from pymongo import MongoClient
# from config.database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect_face.router)
app.include_router(face_recognize.router)
app.include_router(camera.router)
app.include_router(auth.router)
