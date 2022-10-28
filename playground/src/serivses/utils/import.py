from __future__ import annotations

import json
import pathlib

import pandas

from src.domain import models

DATA = pathlib.Path(__file__) \
           .parent.parent.parent.parent.resolve() / 'movies'

MOVIES_DATA = DATA / 'movies.json'
USERS_DATA = DATA / 'users'


def import_movies(movies_data=MOVIES_DATA) -> list[models.Movie]:
    movies: list[models.Movie] = []
    for movie in json.load(movies_data.open()).values():
        movies.append(
            models.Movie(
                id=movie['id'],
                name=movie['name'],
                russian=movie['russian'],
                score=movie['score'],
                description=movie['description'],
                genres=movie['genres']
            )
        )
    return movies


def import_users(users_data=USERS_DATA) -> list[models.User]:
    users: list[models.User] = []
    for user_f in users_data.iterdir():
        user_d = pandas.read_csv(user_f)
        users.append(
            models.User(
                name=user_f.name,
                reviews=[
                    models.Review(
                        movie_id=review['anime_id'],
                        score=review['score'],
                    ) for review in user_d[['anime_id', 'score']].T.to_dict().values()
                ]
            )
        )
        break
    return users


if __name__ == '__main__':
    print(import_users()[:3])
