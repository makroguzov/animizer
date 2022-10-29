from __future__ import annotations

import json
import pathlib
import typing

import pandas

from src.adapters.database import crud
from src.domain import models

DATA = pathlib.Path(__file__) \
           .parent.parent.parent.parent.resolve() / 'movies'

MOVIES_DATA = DATA / 'movies.json'
USERS_DATA = DATA / 'users'


def import_movies(movies_data) -> typing.Generator[models.Movie]:
    for movie in json.load(movies_data.open()).values():
        yield models.Movie(
            id=movie['id'],
            name=movie['name'],
            russian=movie['russian'],
            score=movie['score'],
            description=movie['description'],
            genres=movie['genres']
        )


def import_users(users_data) -> typing.Generator[models.User]:
    for user_f in users_data.iterdir():
        user_d = pandas.read_csv(user_f)
        yield models.User(
            name=user_f.name,
            reviews=[
                models.Review(
                    movie_id=review['anime_id'],
                    score=review['score'],
                ) for review in user_d[['anime_id', 'score']].T.to_dict().values()
            ]
        )


def dump_users(session, users_dir):
    for user in import_users(users_dir):
        crud.dump(user, session)


def dump_movies(session, movies_path):
    for movie in import_movies(movies_path):
        crud.dump(movie, session)
