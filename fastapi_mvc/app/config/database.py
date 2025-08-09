import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # sync URL, e.g. mysql+pymysql://user:pass@host/db
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")  # async URL, e.g. mysql+asyncmy://user:pass@host/db

# Synchronous engine and session for REST API (sync code)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine and session for async code (socketio, etc)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
