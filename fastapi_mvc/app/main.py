from fastapi import FastAPI
from app.routers import user_router
from app.config.database import Base, engine
from app.models import user  # ensure the model is imported for table creation

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router.router)
