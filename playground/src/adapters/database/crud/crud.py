from __future__ import annotations

import functools
import typing

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.adapters.database import orm
from src.domain import models


@typing.overload
def dump(movie: models.Movie, session: Session): ...


@typing.overload
def dump(genre: models.Genre, session: Session): ...


@typing.overload
def dump(user: models.User, session: Session): ...


def dump(obj: typing.Any, session: Session):
    """

    :param obj:
    :param session:
    :return:
    """
    return _dump_function_dispatcher(obj, session)


@functools.singledispatch
def _dump_function_dispatcher(_: typing.Any, __):
    raise NotImplementedError()


@_dump_function_dispatcher.register
def _(movie: models.Movie, session: Session):
    session.add(
        orm.Movie(id_=movie.id,
                  name=movie.name,
                  russian=movie.russian,
                  description=movie.description,
                  score=movie.score,
                  genres=[
                      orm.Genre(
                          id_=genre.id,
                          name=genre.name,
                          russian=genre.russian,
                          kind=genre.kind
                      ) for genre in movie.genres
                  ])
    )
    session.commit()


@_dump_function_dispatcher.register
def _(genre: models.Genre, session: Session):
    session.add(
        orm.Genre(
            id_=genre.id,
            name=genre.name,
            russian=genre.russian,
            kind=genre.kind
        )
    )
    session.commit()


@_dump_function_dispatcher.register
def _(user: models.User, session: Session):
    session.add(
        orm.User(
            name=user.name,
            reviews=[
                orm.Review(
                    movie_id=review.movie_id,
                    score=review.score
                ) for review in user.reviews
            ]
        )
    )
    session.commit()


def load_movies(
        id_: typing.Optional[int],
        session: Session
) -> typing.Generator[models.Movie, ..., ...]:
    """

    :param id_:
    :param session:
    :return:
    """
    query = select(orm.Movie)
    if id_:
        query = query.where(orm.Movie == id_)
    for movie in session.scalars(query):
        yield models.Movie(
            id=movie.id,
            name=movie.name,
            russian=movie.russian,
            description=movie.description,
            score=movie.score,
            genres=[
                models.Genre(
                    id=genre.id,
                    name=genre.name,
                    russian=genre.russian,
                    kind=genre.kind
                ) for genre in movie.genres
            ]
        )
