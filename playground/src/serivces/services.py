from __future__ import annotations

from src.serivces.utils import import_utils


def import_data(session_builder):
    with session_builder() as session:
        import_utils.dump_users(session)
        import_utils.dump_movies(session)
