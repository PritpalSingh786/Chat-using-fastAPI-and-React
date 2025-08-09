from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import CommonModel
from app.models.user import CustomUser  # Your User model (SQLAlchemy version)

class Message(CommonModel):
    __tablename__ = "messages"

    sender_id = Column(CHAR(36), ForeignKey("users.id"), nullable=True)
    receiver_id = Column(CHAR(36), ForeignKey("users.id"), nullable=True)
    message = Column(Text, nullable=True)

    sender = relationship(CustomUser, foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship(CustomUser, foreign_keys=[receiver_id], backref="received_messages")
