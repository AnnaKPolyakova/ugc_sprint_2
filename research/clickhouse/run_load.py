import logging
import subprocess
from time import sleep

from clickhouse_driver import Client

from research.clickhouse.data_lists_generators import (
    get_bookmark_list,
    get_movie_ratings_list,
)
from research.settings_for_testing import NUMBER_OF_OBJECTS_TO_LOAD_BY_INSERTION
from research.utils import dictConfig  # noqa: F401


class ClickhouseLoad:
    def __init__(self):
        self.client = Client(host="localhost")

    def _init_test_db(self):
        subprocess.call(["sh", "entrypoint.sh"])

    def _insert(self):
        number = 0
        while True:
            sleep(0.1)
            bookmark_objs = get_bookmark_list(
                number=NUMBER_OF_OBJECTS_TO_LOAD_BY_INSERTION
            )
            movie_rating_objs = get_movie_ratings_list(
                number=NUMBER_OF_OBJECTS_TO_LOAD_BY_INSERTION
            )
            try:
                self.client.execute(
                    "INSERT INTO default.bookmark_test ("
                    "id, create_at, user_id, movie_id"
                    ") VALUES",
                    bookmark_objs,
                )
                self.client.execute(
                    "INSERT INTO default.movie_rating_test ("
                    "id, create_at, user_id, movie_id, rating"
                    ") VALUES",
                    movie_rating_objs,
                )
                number += 1
                logging.info(number)
            except Exception as error:
                logging.error(error)

    def run(self):
        with open("result.txt", "a") as result_file:
            result_file.write("Нагрузка\n")
        self._init_test_db()
        self._insert()


if __name__ == "__main__":
    load = ClickhouseLoad()
    load.run()
