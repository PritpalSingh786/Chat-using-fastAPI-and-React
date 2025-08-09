from sqlalchemy import Column, String, Boolean
from app.models.base import CommonModel

class CustomUser(CommonModel):
    __tablename__ = "users"

    userId = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    isLogin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User {self.userId}>"
    

