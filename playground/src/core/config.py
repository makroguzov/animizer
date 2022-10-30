from __future__ import annotations

import os
import pathlib

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker, Session  # type: ignore

from src.adapters.database import orm

DATA_PATH = pathlib.Path(__file__).parent.parent.parent.resolve()
DATA_PATH = DATA_PATH / 'movies'

DATABASE_URL = 'sqlite:///%s' % os.environ['DATABASE_PATH']

engine = create_engine(
    DATABASE_URL, echo=True, future=True
)

session_builder = sessionmaker(
    engine,
    class_=Session, expire_on_commit=False
)


def create_database():
    orm.BaseModel.metadata.drop_all(engine)  # type: ignore
    orm.BaseModel.metadata.create_all(engine)  # type: ignore
