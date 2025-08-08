import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.dialects.mysql import CHAR
from app.config.database import Base

class CommonModel(Base):
    __abstract__ = True

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isDeleted = Column(Boolean, default=False)
