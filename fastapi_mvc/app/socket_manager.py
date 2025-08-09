# socket_manager.py
import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.models.user import CustomUser
from app.config.database import async_session

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")

# Track user_id to socket_id mappings
user_socket_map = {}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    # You might want to authenticate here using environ or query params
    # For now, we'll assume user_id is sent in the query

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    # Remove user from mapping if found
    for user_id, socket_id in list(user_socket_map.items()):
        if socket_id == sid:
            del user_socket_map[user_id]
            break

@sio.event
async def register_user(sid, user_id):
    """Register which socket belongs to which user"""
    user_socket_map[user_id] = sid
    print(f"User {user_id} registered with socket {sid}")

@sio.event
async def send_message(sid, data):
    print(f"Received message from {sid}: {data}")

    # Save to database
    async with async_session() as session:
        new_message = Message(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            message=data['message']
        )
        session.add(new_message)
        await session.commit()

    # Emit to sender
    await sio.emit('receive_message', data, room=sid)
    
    # Emit to receiver if they're connected
    receiver_sid = user_socket_map.get(data['receiver_id'])
    if receiver_sid:
        await sio.emit('receive_message', data, room=receiver_sid)