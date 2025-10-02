from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import CommonModel  # Your base model with metadata and common fields

class CustomUser(CommonModel):
    __tablename__ = "users"

    userId = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    isLogin = Column(Boolean, default=False)
    phoneNumber = Column(String(20), unique=True, nullable=True)

    # Removed the many-to-many relationships since we're using JSON lists now

    def __repr__(self):
        return f"<User {self.userId}>"


class Post(CommonModel):
    __tablename__ = "posts"

    postTitle = Column(String(255), nullable=False)
    invited_user_ids = Column(JSON, default=list)  # Stores list of user IDs

    # If you still need to access user objects, you can create a property
    @property
    def invited_users(self):
        # This would require a query to get users by their IDs
        # Implementation depends on your application context
        pass

    def __repr__(self):
        return f"<Post {self.postTitle}>"


class Notification(CommonModel):
    __tablename__ = "notifications"

    notifyTextMessage = Column(String(255), nullable=False)
    invited_user_ids = Column(JSON, default=list)  # Stores list of user IDs

    # If you still need to access user objects, you can create a property
    @property
    def invited_users(self):
        # This would require a query to get users by their IDs
        # Implementation depends on your application context
        pass

    def __repr__(self):
        return f"<Notification {self.notifyTextMessage}>"