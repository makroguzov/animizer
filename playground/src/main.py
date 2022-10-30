from __future__ import annotations

import fire  # type: ignore

from src.core import config
from src.serivces import services


class Playground:
    @staticmethod
    def init():
        try:
            config.create_database()
        except Exception as e:
            print('Database creation error: %s' % e)
        try:
            services.import_data(config.session_builder)
        except Exception as e:
            print('Import data error: %s' % e)


if __name__ == '__main__':
    fire.Fire(Playground, name='playground')
