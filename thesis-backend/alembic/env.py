import os
from dotenv import load_dotenv
load_dotenv()

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from sqlmodel import SQLModel
from app.models.user import User
from app.models.department import Department
from app.models.staff import Staff

# Load .env database URL
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Set up logging
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata  # 🚀 Use SQLModel metadata

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
