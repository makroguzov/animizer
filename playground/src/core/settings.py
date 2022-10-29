from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session  # type: ignore

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

session_builder = sessionmaker(
    engine,
    class_=Session, expire_on_commit=False
)
