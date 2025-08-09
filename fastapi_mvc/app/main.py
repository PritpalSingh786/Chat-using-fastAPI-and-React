# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_router
from app.config.database import Base, engine
from app.models import user, message  # ensure models are imported

import socketio
from app.socket_manager import sio  # your socket.io server instance

# Create your FastAPI app as usual
app = FastAPI()

# CORS for React frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (or do this separately with Alembic)
Base.metadata.create_all(bind=engine)

# Include your REST routers
app.include_router(user_router.router)

# Wrap your FastAPI app with Socket.IO ASGI app
# This mounts socket.io alongside your REST routes
socket_app = socketio.ASGIApp(sio, app)

# Override the app with the socket.io ASGI app for deployment
app = socket_app
