from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Genre:
    id: int
    name: str
    russian: str
    kind: str


@dataclasses.dataclass(frozen=True)
class Movie:
    id: str
    name: str
    russian: str
    score: float
    description: str
    genres: list[Genre]


@dataclasses.dataclass(frozen=True)
class Review:
    movie_id: int
    score: float


@dataclasses.dataclass(frozen=True)
class User:
    name: str
    reviews: list[Review]
