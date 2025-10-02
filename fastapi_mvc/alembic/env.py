import os
import sys
import pathlib
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from dotenv import load_dotenv

load_dotenv()

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from app.config.database import Base
from app.models import user, message  # import all models

target_metadata = Base.metadata

# Get DATABASE_URL directly from .env
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL not set in .env")

# Logging config
config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline():
    context.configure(
        url=db_url,  # pass URL directly, no interpolation
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(db_url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
