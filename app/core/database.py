from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.sql import func
from app.core.config import get_settings
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column
from typing import Generator

settings = get_settings()
ECHO_SQL = settings.debug

engine = create_engine(settings.DATABASE_URL,
                        echo = ECHO_SQL,
                        pool_size = 5,
                        max_overflow = 8,
                        pool_recycle=3600,
                        pool_pre_ping= True)

SessionLocal = sessionmaker(bind = engine,
                            autoflush=False,
                            autocommit = False)
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
