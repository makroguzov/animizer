from __future__ import annotations

from sqlalchemy import (  # type: ignore
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore


@as_declarative()
class BaseModel(object):
    """"""

    __name__: str

    id: int = Column(Integer,
                     primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    """
    """

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        """Генерация __tablename__ автоматически по названия класса модели."""
        return cls.__name__


genres_association_table = Table(
    "genres_association_table",
    BaseModel.metadata,  # type: ignore
    Column("genre_id", ForeignKey("Genre.id"), primary_key=True),
    Column("movie_id", ForeignKey("Movie.id"), primary_key=True),
)


class Genre(BaseModel):
    name: str = Column(String(255), nullable=False, unique=True)
    russian: str = Column(String(255), nullable=False)
    kind: str = Column(String(255), nullable=False)

    def __init__(self, id_: int, name: str, russian: str, kind: str):
        self.id = id_
        self.name = name
        self.russian = russian
        self.kind = kind

    def __repr__(self):
        return f'<Genre({self.id=}, {self.name=}, {self.russian=}, {self.kind=})>'


class Movie(BaseModel):
    name: str = Column(String(255), nullable=False, unique=True)
    russian: str = Column(String(255), nullable=False)
    score: float = Column(Float, nullable=False)
    description: str = Column(String(511), nullable=False)
    genres: list[Genre] = relationship('Genre',
                                       secondary=genres_association_table)

    def __init__(self, id_: int, name: str, russian: str,
                 score: float, description: str, genres: list[Genre]):
        self.id = id_
        self.name = name
        self.russian = russian
        self.score = score
        self.description = description
        self.genres = genres

    def __repr__(self):
        return f'<Movie({self.id=}, {self.name=}, ' \
               f'{self.russian=}, {self.score=}, {self.description=}, {self.genres=})>'


class Review(BaseModel):
    score: float
    movie_id: int = Column(Integer,
                           ForeignKey(
                               'Movie.id', onupdate='CASCADE', ondelete='CASCADE'),
                           nullable=False)

    user_id: int = Column(Integer,
                          ForeignKey(
                              'User.id', onupdate='CASCADE', ondelete='CASCADE'),
                          nullable=False)

    def __init__(self, score: float, movie_id: int):
        self.score = score
        self.movie_id = movie_id

    def __repr__(self):
        return f'<Review({self.id=}, {self.score=}, {self.movie_id=}, {self.user_id=})>'


class User(BaseModel):
    name: str = Column(String(255), nullable=False, unique=True)
    reviews: list[Review] = relationship('Review',
                                         cascade='all, delete-orphan')

    def __init__(self, name: str, reviews: list[Review]):
        self.name = name
        self.reviews = reviews

    def __repr__(self):
        return f'<User({self.id=}, {self.name=}, {self.reviews=})>'
